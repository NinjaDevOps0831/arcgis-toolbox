import unittest

from . import vendors


class VendorsTestCase(unittest.TestCase):
    def test_build_vendor_preferences(self):
        MOCK_VENDOR_1 = "VENDOR_1"
        MOCK_VENDOR_2 = "VENDOR_2"
        MOCK_VENDOR_3 = "VENDOR_3"

        self.assertEqual(
            vendors.build_vendor_preferences(
                [MOCK_VENDOR_1, MOCK_VENDOR_2, MOCK_VENDOR_3]
            ),
            {
                MOCK_VENDOR_1: "preferred",
                MOCK_VENDOR_2: "preferred",
                MOCK_VENDOR_3: "preferred",
            },
        )
