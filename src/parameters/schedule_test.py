import unittest
import datetime

from . import schedule


class ScheduleTestCase(unittest.TestCase):
    def test_build_schedule(self):
        MOCK_START = datetime.datetime(1, 1, 1)
        MOCK_END = datetime.datetime(1, 1, 2)
        self.assertEqual(
            schedule.build_schedule(MOCK_START, MOCK_END),
            [
                {
                    "type": "range",
                    "range": {
                        "min": MOCK_START.isoformat(),
                        "max": MOCK_END.isoformat(),
                    },
                }
            ],
        )
