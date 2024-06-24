from unittest import TestCase

from SSD.ssd_interface import SSDInterface


class TestLogger(TestCase):
    def test_log(self):
        app = SSDInterface()
        with self.assertRaises(SystemExit):
            app.main(["W", "-1", "INVALID"])