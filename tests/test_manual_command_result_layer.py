import unittest

from app.commands import (
    CommandResult,
    CommandStatus,
    OperatorMessage,
    RefusalReason,
    RiskLevel,
    RunSummary,
)


class ManualCommandResultLayerTest(unittest.TestCase):
    def test_command_result_carries_ui_ready_refusal_fields(self) -> None:
        result = CommandResult(
            status=CommandStatus.REFUSED,
            command="Auto3 Multi-Car Unlock Test",
            reason="Requested car count is outside the current validated boundary.",
            refusal_reason=RefusalReason.INVALID_COUNT,
            operator_message=OperatorMessage(
                message="cars must be 4 or fewer.",
                required_action="Choose 1-4 cars.",
                suggested_next_step="Use the validated A-start traversal boundary.",
                risk_level=RiskLevel.MEDIUM,
            ),
            details=[
                ("Current validated limit", "4 cars"),
                ("Validated traversal", "A1 -> B1 -> C1 -> A2"),
            ],
        )

        self.assertEqual(CommandStatus.REFUSED, result.status)
        self.assertEqual(RefusalReason.INVALID_COUNT, result.refusal_reason)
        self.assertEqual(RiskLevel.MEDIUM, result.operator_message.risk_level)
        self.assertIn(("Validated traversal", "A1 -> B1 -> C1 -> A2"), result.details)

    def test_run_summary_carries_operator_message(self) -> None:
        summary = RunSummary(
            status=CommandStatus.STOPPED,
            command="Auto1 Official Manual Run",
            fields=[("Final status", "stopped")],
            operator_message=OperatorMessage(
                message="Operator control returned.",
                suggested_next_step="Verify FH6 baseline before rerunning.",
                risk_level=RiskLevel.MEDIUM,
            ),
        )

        self.assertEqual(CommandStatus.STOPPED, summary.status)
        self.assertEqual("Operator control returned.", summary.operator_message.message)
        self.assertEqual(RiskLevel.MEDIUM, summary.operator_message.risk_level)


if __name__ == "__main__":
    unittest.main()
