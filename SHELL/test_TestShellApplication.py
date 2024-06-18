from unittest import TestCase
from unittest.mock import Mock

from SHELL.TestShellApplication import TestShellApplication


class TestTestShellApplication(TestCase):
    def setUp(self):
        super().setUp()
        self.mk_ssd = Mock()

    def test_call_ssd_write_when_shell_write(self):
        self.mk_ssd.write.return_value = '1'
        shell = TestShellApplication(self.mk_ssd)
        shell.write(3, '0xAAAABBBB')

        self.assertEqual(1, self.mk_ssd.write.call_count)

    def test_call_ssd_write_100_when_shell_fullwrite(self):
        self.mk_ssd.write.return_value = '1'
        shell = TestShellApplication(self.mk_ssd)
        shell.fullwrite('0xAAAABBBB')

        self.assertEqual(100, self.mk_ssd.write.call_count)

