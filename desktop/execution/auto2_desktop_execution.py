"""Desktop adapter for guarded Auto2 execution."""

import threading

from desktop.execution.execution_messages import (
    completion_state_id_for_status,
    summarize_ui_execution_error,
)

AUTO2_PURCHASE_COUNT_MIN = 1
AUTO2_PURCHASE_COUNT_MAX = 25


def start_auto2_ui_execution(
    companion_state: dict[str, str],
    parent,
    timer_type,
    on_result,
) -> None:
    execution_state = {
        "done": False,
        "state_id": "refused",
        "message": "Auto2 execution did not start.",
    }
    poll_timer = timer_type(parent)
    poll_timer.setInterval(250)

    def worker() -> None:
        from app_logging.log_manager import configure_logging

        logger = configure_logging()
        mode = companion_state.get("auto2_mode", "test")
        logger.warning(
            "UI-triggered Auto2 execution attempt starting. mode=%s profile=%s",
            mode,
            companion_state.get("profile_id", "default"),
            category="sequence",
        )
        try:
            purchase_count = parse_auto2_purchase_count(
                companion_state.get("auto2_purchase_count")
            )
            if mode == "purchase":
                from automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test import (
                    load_purchase_test_profile,
                    run_auto2_one_car_purchase_test,
                )

                profile_data = load_purchase_test_profile(None)
                result = run_auto2_one_car_purchase_test(
                    cycle_count=purchase_count,
                    profile_data=profile_data,
                    logger=logger,
                )
            else:
                from automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test import (
                    load_test_mode_profile,
                    run_auto2_test_mode_real_input,
                )

                profile_data = load_test_mode_profile(False, None)
                result = run_auto2_test_mode_real_input(
                    cycle_count=1,
                    profile_data=profile_data,
                    logger=logger,
                )

            execution_state["state_id"] = completion_state_id_for_status(result.status)
            execution_state["message"] = (
                f"{result.message} Completed cycles: "
                f"{result.completed_cycles}/{result.requested_cycles}."
            )
            logger.warning(
                "UI-triggered Auto2 execution returned status=%s completed_cycles=%s/%s.",
                result.status,
                result.completed_cycles,
                result.requested_cycles,
                category="sequence",
            )
        except Exception as error:
            execution_state["state_id"] = "refused"
            execution_state["message"] = summarize_ui_execution_error("Auto2", error)
            logger.error(
                "UI-triggered Auto2 execution failed closed: %s",
                execution_state["message"],
                category="error",
            )
        finally:
            execution_state["done"] = True

    def poll_for_result() -> None:
        if not execution_state["done"]:
            return

        poll_timer.stop()
        on_result(
            execution_state["state_id"],
            companion_state,
            execution_state["message"],
        )

    poll_timer.timeout.connect(poll_for_result)
    threading.Thread(target=worker, daemon=True).start()
    poll_timer.start()


def parse_auto2_purchase_count(raw_value: str | None) -> int:
    try:
        purchase_count = int(raw_value or str(AUTO2_PURCHASE_COUNT_MIN))
    except (TypeError, ValueError) as error:
        raise ValueError("Auto2 purchase count must be an integer.") from error

    if not AUTO2_PURCHASE_COUNT_MIN <= purchase_count <= AUTO2_PURCHASE_COUNT_MAX:
        raise ValueError(
            f"Auto2 purchase count must be between {AUTO2_PURCHASE_COUNT_MIN} and {AUTO2_PURCHASE_COUNT_MAX}."
        )

    return purchase_count

