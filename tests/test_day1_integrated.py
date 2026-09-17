import unittest

from device_test_guard.models import DeviceTestRecord
from device_test_guard.service import analyse_batch
from device_test_guard.validation import validate_record


def record(
    device_id: str = "TRAIN-101",
    temperature_c: float = 25.0,
    test_results: dict[str, bool] | None = None,
) -> DeviceTestRecord:
    return DeviceTestRecord(
        device_id,
        temperature_c,
        1.0,
        {"logic": True} if test_results is None else test_results,
    )


class Day1IntegratedTests(unittest.TestCase):
    def test_temperature_just_outside_range_is_rejected(self):
        low_problems = validate_record(record(temperature_c=9.99))
        high_problems = validate_record(record(temperature_c=85.01))

        self.assertIn("temperature is outside the training range", low_problems)
        self.assertIn("temperature is outside the training range", high_problems)

    def test_blank_device_identifier_is_rejected(self):
        problems = validate_record(record(device_id="   "))

        self.assertIn("device_id is required", problems)

    def test_empty_test_results_are_rejected(self):
        problems = validate_record(record(test_results={}))

        self.assertIn("at least one test result is required", problems)

    def test_empty_batch_summary_is_zero_and_held(self):
        summary = analyse_batch("TRAIN-BATCH-101", [])

        self.assertEqual(summary.record_count, 0)
        self.assertEqual(summary.yield_percent, 0.0)
        self.assertEqual(summary.disposition, "HOLD")


if __name__ == "__main__":
    unittest.main()
