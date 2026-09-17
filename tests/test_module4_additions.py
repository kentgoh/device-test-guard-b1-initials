import unittest

from device_test_guard.disposition import decide_disposition
from device_test_guard.models import DeviceTestRecord
from device_test_guard.validation import validate_record


def record(device_id: str, passed: bool = True, voltage: float = 1.0, retest_count: int = 0):
    return DeviceTestRecord(
        device_id,
        25.0,
        voltage,
        {"logic": passed},
        retest_count,
    )


class Module4AdditionalTests(unittest.TestCase):
    def test_voltage_boundaries_are_inclusive(self):
        self.assertEqual(validate_record(record("UNIT-A", voltage=0.8)), ())
        self.assertEqual(validate_record(record("UNIT-B", voltage=1.2)), ())

    def test_exhausted_retest_is_held(self):
        disposition, _ = decide_disposition(
            [record("UNIT-C", passed=False, retest_count=1)], 90.0
        )
        self.assertEqual(disposition, "HOLD")

    def test_invalid_record_is_held(self):
        disposition, _ = decide_disposition([record("UNIT-D", voltage=1.5)], 90.0)
        self.assertEqual(disposition, "HOLD")


if __name__ == "__main__":
    unittest.main()
