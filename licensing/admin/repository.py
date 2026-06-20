"""SQLite persistence for manual Licensing Authority records."""

from dataclasses import dataclass
from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator


class LicenseRepositoryError(RuntimeError):
    """Raised when license administration records cannot be persisted safely."""


@dataclass(frozen=True)
class CustomerRecord:
    discord_user_id: str
    first_seen_at: str
    current_license_id: str | None


@dataclass(frozen=True)
class AdminLicenseRecord:
    license_id: str
    discord_user_id: str
    edition: str
    payload_json: str
    signature: str
    signing_key_id: str
    status: str
    issued_at: str
    expires_at: str | None
    replaces_license_id: str | None


@dataclass(frozen=True)
class LicenseEventRecord:
    event_id: int
    license_id: str
    discord_user_id: str
    event_type: str
    timestamp: str
    notes: str | None


class LicenseAdminRepository:
    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)

    def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self._connect() as connection:
                connection.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS customers (
                        discord_user_id TEXT PRIMARY KEY,
                        first_seen_at TEXT NOT NULL,
                        current_license_id TEXT
                    );

                    CREATE TABLE IF NOT EXISTS licenses (
                        license_id TEXT PRIMARY KEY,
                        discord_user_id TEXT NOT NULL,
                        edition TEXT NOT NULL,
                        payload_json TEXT NOT NULL,
                        signature TEXT NOT NULL,
                        signing_key_id TEXT NOT NULL,
                        status TEXT NOT NULL CHECK (status IN ('active', 'superseded')),
                        issued_at TEXT NOT NULL,
                        expires_at TEXT,
                        replaces_license_id TEXT,
                        FOREIGN KEY (discord_user_id)
                            REFERENCES customers(discord_user_id),
                        FOREIGN KEY (replaces_license_id)
                            REFERENCES licenses(license_id)
                    );

                    CREATE TABLE IF NOT EXISTS license_events (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        license_id TEXT NOT NULL,
                        discord_user_id TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        notes TEXT,
                        FOREIGN KEY (license_id) REFERENCES licenses(license_id),
                        FOREIGN KEY (discord_user_id)
                            REFERENCES customers(discord_user_id)
                    );

                    CREATE INDEX IF NOT EXISTS idx_licenses_discord_user
                        ON licenses(discord_user_id);
                    CREATE INDEX IF NOT EXISTS idx_events_license
                        ON license_events(license_id);
                    """
                )
        except (OSError, sqlite3.Error) as error:
            raise LicenseRepositoryError(
                f"License database could not be initialized: {self.database_path}"
            ) from error

    def get_customer(self, discord_user_id: str) -> CustomerRecord | None:
        row = self._fetch_one(
            "SELECT * FROM customers WHERE discord_user_id = ?",
            (discord_user_id,),
        )
        return _customer_from_row(row) if row is not None else None

    def get_license(self, license_id: str) -> AdminLicenseRecord | None:
        row = self._fetch_one(
            "SELECT * FROM licenses WHERE license_id = ?",
            (license_id,),
        )
        return _license_from_row(row) if row is not None else None

    def get_active_license(self, discord_user_id: str) -> AdminLicenseRecord | None:
        row = self._fetch_one(
            """
            SELECT licenses.*
            FROM customers
            JOIN licenses ON licenses.license_id = customers.current_license_id
            WHERE customers.discord_user_id = ? AND licenses.status = 'active'
            """,
            (discord_user_id,),
        )
        return _license_from_row(row) if row is not None else None

    def list_licenses(self, discord_user_id: str) -> tuple[AdminLicenseRecord, ...]:
        rows = self._fetch_all(
            """
            SELECT * FROM licenses
            WHERE discord_user_id = ?
            ORDER BY issued_at ASC, license_id ASC
            """,
            (discord_user_id,),
        )
        return tuple(_license_from_row(row) for row in rows)

    def list_events(self, discord_user_id: str) -> tuple[LicenseEventRecord, ...]:
        rows = self._fetch_all(
            """
            SELECT * FROM license_events
            WHERE discord_user_id = ?
            ORDER BY event_id ASC
            """,
            (discord_user_id,),
        )
        return tuple(_event_from_row(row) for row in rows)

    def record_issue(
        self,
        license_record: AdminLicenseRecord,
        event_timestamp: str,
    ) -> None:
        try:
            with self._connect() as connection:
                existing = connection.execute(
                    "SELECT current_license_id FROM customers WHERE discord_user_id = ?",
                    (license_record.discord_user_id,),
                ).fetchone()
                if existing is not None and existing["current_license_id"] is not None:
                    raise LicenseRepositoryError(
                        "Customer already has an active license. Use replace instead."
                    )
                connection.execute(
                    """
                    INSERT OR IGNORE INTO customers (
                        discord_user_id, first_seen_at, current_license_id
                    ) VALUES (?, ?, NULL)
                    """,
                    (license_record.discord_user_id, event_timestamp),
                )
                self._insert_license(connection, license_record)
                connection.execute(
                    "UPDATE customers SET current_license_id = ? WHERE discord_user_id = ?",
                    (license_record.license_id, license_record.discord_user_id),
                )
                self._insert_event(
                    connection,
                    license_record.license_id,
                    license_record.discord_user_id,
                    "issued",
                    event_timestamp,
                    f"Issued {license_record.edition} license.",
                )
        except sqlite3.Error as error:
            raise LicenseRepositoryError("License issue record could not be stored.") from error

    def record_replacement(
        self,
        old_license_id: str,
        new_license: AdminLicenseRecord,
        event_timestamp: str,
    ) -> None:
        try:
            with self._connect() as connection:
                current = connection.execute(
                    "SELECT current_license_id FROM customers WHERE discord_user_id = ?",
                    (new_license.discord_user_id,),
                ).fetchone()
                if current is None or current["current_license_id"] != old_license_id:
                    raise LicenseRepositoryError(
                        "Active license changed before replacement could be recorded."
                    )
                connection.execute(
                    "UPDATE licenses SET status = 'superseded' WHERE license_id = ?",
                    (old_license_id,),
                )
                self._insert_license(connection, new_license)
                connection.execute(
                    "UPDATE customers SET current_license_id = ? WHERE discord_user_id = ?",
                    (new_license.license_id, new_license.discord_user_id),
                )
                self._insert_event(
                    connection,
                    old_license_id,
                    new_license.discord_user_id,
                    "superseded",
                    event_timestamp,
                    f"Replaced by {new_license.license_id}.",
                )
                self._insert_event(
                    connection,
                    new_license.license_id,
                    new_license.discord_user_id,
                    "replaced",
                    event_timestamp,
                    f"Replaced {old_license_id} with {new_license.edition} license.",
                )
        except sqlite3.Error as error:
            raise LicenseRepositoryError("License replacement could not be stored.") from error

    def record_export(
        self,
        license_id: str,
        discord_user_id: str,
        event_timestamp: str,
        output_path: str,
    ) -> None:
        try:
            with self._connect() as connection:
                self._insert_event(
                    connection,
                    license_id,
                    discord_user_id,
                    "exported",
                    event_timestamp,
                    f"Exported active license to {output_path}.",
                )
        except sqlite3.Error as error:
            raise LicenseRepositoryError("License export event could not be stored.") from error

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _fetch_one(self, query: str, parameters: tuple[object, ...]):
        try:
            with self._connect() as connection:
                return connection.execute(query, parameters).fetchone()
        except sqlite3.Error as error:
            raise LicenseRepositoryError("License database lookup failed.") from error

    def _fetch_all(self, query: str, parameters: tuple[object, ...]):
        try:
            with self._connect() as connection:
                return connection.execute(query, parameters).fetchall()
        except sqlite3.Error as error:
            raise LicenseRepositoryError("License database lookup failed.") from error

    @staticmethod
    def _insert_license(
        connection: sqlite3.Connection,
        record: AdminLicenseRecord,
    ) -> None:
        connection.execute(
            """
            INSERT INTO licenses (
                license_id, discord_user_id, edition, payload_json, signature,
                signing_key_id, status, issued_at, expires_at,
                replaces_license_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.license_id,
                record.discord_user_id,
                record.edition,
                record.payload_json,
                record.signature,
                record.signing_key_id,
                record.status,
                record.issued_at,
                record.expires_at,
                record.replaces_license_id,
            ),
        )

    @staticmethod
    def _insert_event(
        connection: sqlite3.Connection,
        license_id: str,
        discord_user_id: str,
        event_type: str,
        timestamp: str,
        notes: str | None,
    ) -> None:
        connection.execute(
            """
            INSERT INTO license_events (
                license_id, discord_user_id, event_type, timestamp, notes
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (license_id, discord_user_id, event_type, timestamp, notes),
        )


def _customer_from_row(row: sqlite3.Row) -> CustomerRecord:
    return CustomerRecord(
        discord_user_id=row["discord_user_id"],
        first_seen_at=row["first_seen_at"],
        current_license_id=row["current_license_id"],
    )


def _license_from_row(row: sqlite3.Row) -> AdminLicenseRecord:
    return AdminLicenseRecord(
        license_id=row["license_id"],
        discord_user_id=row["discord_user_id"],
        edition=row["edition"],
        payload_json=row["payload_json"],
        signature=row["signature"],
        signing_key_id=row["signing_key_id"],
        status=row["status"],
        issued_at=row["issued_at"],
        expires_at=row["expires_at"],
        replaces_license_id=row["replaces_license_id"],
    )


def _event_from_row(row: sqlite3.Row) -> LicenseEventRecord:
    return LicenseEventRecord(
        event_id=row["event_id"],
        license_id=row["license_id"],
        discord_user_id=row["discord_user_id"],
        event_type=row["event_type"],
        timestamp=row["timestamp"],
        notes=row["notes"],
    )
