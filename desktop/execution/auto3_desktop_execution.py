"""Desktop adapter for guarded Auto3 execution."""

import threading

from desktop.execution.execution_messages import (
    completion_state_id_for_status,
    summarize_ui_execution_error,
)

AUTO3_CAR_COUNT_MIN = 1
AUTO3_CAR_COUNT_MAX = 4


def start_auto3_ui_execution(
    companion_state: dict[str, str],
    parent,
    timer_type,
    on_result,
) -> None:
    execution_state = {
        "done": False,
        "state_id": "refused",
        "message": "Auto3 execution did not start.",
    }
    poll_timer = timer_type(parent)
    poll_timer.setInterval(250)

    def worker() -> None:
        from app_logging.log_manager import configure_logging

        logger = configure_logging()
        mode = companion_state.get("auto3_mode", "test")
        try:
            car_count = parse_auto3_car_count(companion_state.get("auto3_cars"))
            logger.warning(
                "UI-triggered Auto3 execution attempt starting. mode=%s cars=%s profile=%s",
                mode,
                car_count,
                companion_state.get("profile_id", "default"),
                category="sequence",
            )
            if mode == "unlock":
                from automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test import (
                    load_unlock_test_profile,
                    run_auto3_multi_car_unlock_test,
                )

                profile_data = load_unlock_test_profile(False, None)
                result = run_auto3_multi_car_unlock_test(
                    car_count=car_count,
                    profile_data=profile_data,
                    logger=logger,
                )
            else:
                from automation.auto3_skill_tree.dangerous_auto3_multi_car_test_mode_real_input_test import (
                    load_multi_car_test_mode_profile,
                    run_auto3_multi_car_test_mode_real_input,
                )

                profile_data = load_multi_car_test_mode_profile(False, None)
                result = run_auto3_multi_car_test_mode_real_input(
                    car_count=car_count,
                    profile_data=profile_data,
                    logger=logger,
                )

            execution_state["state_id"] = completion_state_id_for_status(result.status)
            execution_state["message"] = result.message
            logger.warning(
                "UI-triggered Auto3 execution returned status=%s cars=%s.",
                result.status,
                car_count,
                category="sequence",
            )
        except Exception as error:
            execution_state["state_id"] = "refused"
            execution_state["message"] = summarize_ui_execution_error("Auto3", error)
            logger.error(
                "UI-triggered Auto3 execution failed closed: %s",
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


def parse_auto3_car_count(raw_value: str | None) -> int:
    try:
        car_count = int(raw_value or str(AUTO3_CAR_COUNT_MIN))
    except (TypeError, ValueError) as error:
        raise ValueError("Auto3 car count must be an integer.") from error

    if not AUTO3_CAR_COUNT_MIN <= car_count <= AUTO3_CAR_COUNT_MAX:
        raise ValueError(
            f"Auto3 car count must be between {AUTO3_CAR_COUNT_MIN} and {AUTO3_CAR_COUNT_MAX}."
        )

    return car_count
