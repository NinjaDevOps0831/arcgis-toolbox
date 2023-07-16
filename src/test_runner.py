import unittest


def build_test_suite():
    return unittest.TestLoader().discover(
        start_dir=".",
        pattern="*_test.py",
    )


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    suite = build_test_suite()
    runner.run(suite)
