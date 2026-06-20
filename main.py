from app_logging.log_manager import configure_logging
from settings.config_loader import ConfigurationError, load_default_settings


def main() -> int:
    logger = configure_logging()
    logger.info("Forza Automation Assist startup started.", category="startup")

    try:
        settings = load_default_settings()
    except ConfigurationError as error:
        logger.error("Configuration loading failed: %s", error, category="config")
        return 1

    logging_settings = settings.get("logging", {})
    if isinstance(logging_settings, dict):
        logger = configure_logging(str(logging_settings.get("level", "INFO")))

    logger.info("Configuration loaded successfully.", category="config")
    logger.info("Forza Automation Assist startup completed.", category="startup")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
