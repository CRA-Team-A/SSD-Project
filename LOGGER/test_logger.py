from unittest import TestCase

from SSD.ssd_interface import SSDInterface


class TestLogger(TestCase):
    def test_log(self):
        app = SSDInterface()
        app.main(["W", "-1", "INVALID"])