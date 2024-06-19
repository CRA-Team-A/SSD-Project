from unittest import TestCase
from unittest.mock import patch

from SHELL.TestShellApplication import TestShellApplication


class TestTestShellApplicationWithSSD(TestCase):
    def setUp(self):
        super().setUp()
        self.shell = TestShellApplication(None)

    @patch('subprocess')
    def test_simple_subprocess_call(self, mock_subprocess):
        self.shell.run("read 0")
        mock_subprocess.assert_called()
