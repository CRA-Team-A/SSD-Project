import os
from unittest import TestCase
from unittest.mock import Mock, patch
from SHELL.TestShellApplication import TestShellApplication

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
NAND_PATH = os.path.join(ROOT_DIR, 'nand.txt')


class TestTestShellApplication(TestCase):
    def setUp(self):
        super().setUp()
        self.mk_ssd = Mock()
        self.shell = TestShellApplication()

    def test_verify_write_invalid_address(self):
        self.assertEqual(False, self.shell.run("write 100 OxAAAABBBB"))
        self.assertEqual(False, self.shell.run("write -1 OxAAAABBBB"))
        self.assertEqual(False, self.shell.run("write 0x11 OxAAAABBBB"))

    def test_verify_write_invalid_data(self):
        self.assertEqual(False, self.shell.run("write 3 OxAAAABBBB"))
        self.assertEqual(False, self.shell.run("write 3 0xAABBBB"))
        self.assertEqual(False, self.shell.run("write 3 0xAAAABBBBCC"))

    def test_verify_valid_write_command(self):
        self.assertEqual(True, self.shell.run("write 3 0xAAAABBBB"))
        self.assertEqual(True, self.shell.run("write 0 0x00000007"))
        with open(NAND_PATH, 'r') as fp:
            written_value = fp.readline().split(',')[0]
        self.assertEqual('7', written_value)

    def test_verify_valid_read_command(self):
        self.shell.run("write 0 0x00000007")
        self.assertEqual('0x00000007', self.shell.run("read 0"))

    def test_verify_read_invalid_address(self):
        self.assertEqual(False, self.shell.run("read 100"))
        self.assertEqual(False, self.shell.run("read -1"))
        self.assertEqual(False, self.shell.run("read"))

    def test_verify_fullwrite_invalid_address(self):
        self.assertEqual(False, self.shell.run("fullwrite 50 OxAAAABBBB"))
        self.assertEqual(False, self.shell.run("fullwrite"))
        self.assertEqual(False, self.shell.run("fullwrite 0x11"))
        self.assertEqual(False, self.shell.run("fullwrite 0xAABBFFTT"))

    def test_verify_fullread_invalid_address(self):
        self.assertEqual(False, self.shell.run("fullread 10"))
        self.assertEqual(False, self.shell.run("fullread 0x111100000"))

    def test_verify_help_invalid_command(self):
        self.assertEqual(False, self.shell.run("help 10"))
        self.assertEqual(False, self.shell.run("help 10 0x11110000"))

    def test_testapp1_script(self):
        self.assertEqual(True, self.shell.run("testapp1"))

    @patch('builtins.print')
    def test_verify_help_valid_command(self, mock_print):
        self.shell.run("help")
        mock_print.assert_called_with('HOW TO TEST SSD',
                                      'To WRITE new data : write {LBA index} {data}',
                                      'To READ written data : read {LBA index}',
                                      'To WRITE data on all LBA : fullwrite {data}',
                                      'To READ every data from 0~99 LBA : fullread',
                                      'To finish this app : exit',
                                      'To repeat this information : help',
                                      sep='\n')

    def test_verify_none_command(self):
        self.assertEqual(False, self.shell.run(""))

    def test_verify_testapp2_command(self):
        self.assertTrue(self.shell.run("testapp2"))

    def test_verify_erase_command(self):
        self.assertEqual(True, self.shell.run("erase 3 10"))

        self.assertEqual(False, self.shell.run("erase"))
        self.assertEqual(False, self.shell.run("erase 3"))
        self.assertEqual(False, self.shell.run("erase 3 0"))
        self.assertEqual(False, self.shell.run("erase 95 10"))

    def test_verify_erase_range_command(self):
        self.assertEqual(True, self.shell.run("erase_range 3 13"))
        self.assertEqual(True, self.shell.run("erase_range 3 23"))

        self.assertEqual(False, self.shell.run("erase_range"))
        self.assertEqual(False, self.shell.run("erase_range 3"))
        self.assertEqual(False, self.shell.run("erase_range 3 0"))
        self.assertEqual(False, self.shell.run("erase_range 3 2"))
        self.assertEqual(False, self.shell.run("erase_range 95 100"))
        self.assertEqual(False, self.shell.run("erase_range 95 105"))

