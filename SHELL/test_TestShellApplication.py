from unittest import TestCase, skip

from unittest.mock import Mock, patch

from SHELL.TestShellApplication import TestShellApplication


class TestTestShellApplication(TestCase):
    def setUp(self):
        super().setUp()
        self.mk_ssd = Mock()
        self.shell = TestShellApplication(self.mk_ssd)

    def test_verify_write_incorrect_address(self):
        self.assertEqual(False, self.shell.run("write 100 OxAAAABBBB"))
        self.assertEqual(False, self.shell.run("write -1 OxAAAABBBB"))
        self.assertEqual(False, self.shell.run("write 0x11 OxAAAABBBB"))

    def test_verify_write_incorrect_data(self):
        self.assertEqual(False, self.shell.run("write 3 OxAAAABBBB"))
        self.assertEqual(False, self.shell.run("write 3 0xAABBBB"))
        self.assertEqual(False, self.shell.run("write 3 0xAAAABBBBCC"))

    def test_verify_correct_write_command(self):
        self.assertEqual(False, self.shell.run("write 3 0xAAAABBBB"))

    def test_call_ssd_read_when_shell_read(self):
        self.mk_ssd.read.return_value = '1'
        self.shell.read(3)

        self.assertEqual(1, self.mk_ssd.read.call_count)

    def test_call_ssd_read_when_shell_fullread(self):
        self.mk_ssd.read.return_value = '1'
        self.shell.fullread()

        self.assertEqual(100, self.mk_ssd.read.call_count)

    def test_call_ssd_write_when_shell_write(self):
        self.mk_ssd.write.return_value = '1'
        self.shell.write(3, '0xAAAABBBB')

        self.assertEqual(1, self.mk_ssd.write.call_count)

    def test_call_ssd_write_100_when_shell_fullwrite(self):
        self.mk_ssd.write.return_value = '1'
        self.shell.fullwrite('0xAAAABBBB')

        self.assertEqual(100, self.mk_ssd.write.call_count)

    def test_verify_read_incorrect_address(self):
        self.assertEqual(False, self.shell.run("read 100"))
        self.assertEqual(False, self.shell.run("read -1"))
        self.assertEqual(False, self.shell.run("read"))

    def test_verify_fullwrite_incorrect_address(self):
        self.assertEqual(False, self.shell.run("fullwrite 50 OxAAAABBBB"))
        self.assertEqual(False, self.shell.run("fullwrite"))
        self.assertEqual(False, self.shell.run("fullwrite 0x11"))
        self.assertEqual(False, self.shell.run("fullwrite 0xAABBFFTT"))

    def test_verify_fullread_incorrect_address(self):
        self.assertEqual(False, self.shell.run("fullread 10"))
        self.assertEqual(False, self.shell.run("fullread 0x111100000"))

    def test_verify_help_incorrect_command(self):
        self.assertEqual(False, self.shell.run("help 10"))
        self.assertEqual(False, self.shell.run("help 10 0x11110000"))

    @patch('builtins.print')
    def test_verify_help_correct_command(self, mock_print):
        self.shell.run("help")
        mock_print.assert_called_with('-' * 10, 'HOW TO TEST SSD', '-' * 10,
                                      'To WRITE new data : write {LBA index} {data}',
                                      'To READ written data : read {LBA index}',
                                      'To WRITE data on all LBA : fullwrite {data}',
                                      'To READ every data from 0~99 LBA : fullread',
                                      'To finish this app : exit',
                                      'To repeat this information : help',
                                      sep='\n')
