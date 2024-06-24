import os
from io import StringIO
from unittest import TestCase, skip
from unittest.mock import patch
from SHELL.test_shell_application import TestShellApplication

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
NAND_PATH = os.path.join(ROOT_DIR, 'nand.txt')
RESULT_PATH = os.path.join(ROOT_DIR, 'result.txt')


class TestTestShellApplication(TestCase):
    def setUp(self):
        self.shell = TestShellApplication()

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_write_address(self, mock_stdout):
        # arrange
        tc = [["write", "100", "OxAAAABBBB"],
              ["write", "-1", "OxAAAABBBB"],
              ["write", "0x11", "OxAAAABBBB"]]

        for n in range(len(tc)):
            with self.subTest(f"subtest {n}"):
                # action
                self.run_testcase(tc[n])

                # assert
                self.check_stdout("INVALID COMMAND", mock_stdout)
                self.assertFalse(os.path.isfile(RESULT_PATH))

                self.reset_nand(NAND_PATH)
                self.clear_result_files(RESULT_PATH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_write_data(self, mock_stdout):
        # arrange
        tc = [["write", "3", "OxAAAABBBB"],
              ["write", "3", "0xAABBBB"],
              ["write", "3", "0xAAAABBBBCC"]]

        for n in range(len(tc)):
            with self.subTest(f"subtest {n}"):
                # action & assert
                self.run_testcase(tc[n])
                self.check_stdout("INVALID COMMAND", mock_stdout)
                self.check_right_data(tc[n][1], self.convert_to_hex(0), mock_stdout)

                self.reset_nand(NAND_PATH)
                self.clear_result_files(RESULT_PATH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_write_read(self, mock_stdout):
        # arrange
        tc = [["write", "3", "0xAAAABBBB"],
              ["write", "0", "0x00000007"]]

        for n in range(len(tc)):
            with self.subTest(f"subtest {n}"):
                # action
                self.run_testcase(tc[n])
                self.shell.run(f"read {tc[n][1]}")

                # assert
                self.check_stdout(tc[n][2], mock_stdout)

                self.reset_nand(NAND_PATH)
                self.clear_result_files(RESULT_PATH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_read_address(self, mock_stdout):
        # arrange
        tc = [["read", "100"],
              ["read", "-1"],
              ["read"]]

        for n in range(len(tc)):
            with self.subTest(f"subtest {n}"):
                # action
                self.run_testcase(tc[n])

                # assert
                self.check_stdout("INVALID COMMAND", mock_stdout)
                self.assertFalse(os.path.isfile(RESULT_PATH))

                self.reset_nand(NAND_PATH)
                self.clear_result_files(RESULT_PATH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_fullwrite_address(self, mock_stdout):
        # arrange
        sample_points = [0, 49, 99]
        tc = [["fullwrite", "50", "OxAAAABBBB"],
              ["fullwrite"],
              ["fullwrite", "0x11"],
              ["fullwrite", "0xAABBFFTT"]]

        for n in range(len(tc)):
            with self.subTest(f"subtest {n}"):
                # action
                self.run_testcase(tc[n])

                # assert
                self.check_stdout("INVALID COMMAND", mock_stdout)
                for p in sample_points:
                    self.check_right_data(p, self.convert_to_hex(0), mock_stdout)

                self.reset_nand(NAND_PATH)
                self.clear_result_files(RESULT_PATH)

    @skip
    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_fullwrite(self, mock_stdout):
        # arrange
        sample_points = [0, 49, 99]
        tc = [["fullwrite", "0xAAAABBBB"],
              ["fullwrite", "0x00000001"]]

        for n in range(len(tc)):
            with self.subTest(f"subtest {n}"):
                # action
                self.run_testcase(tc[n])

                # assert
                for p in sample_points:
                    self.check_right_data(p, tc[n][1], mock_stdout)

                self.reset_nand(NAND_PATH)
                self.clear_result_files(RESULT_PATH)

    @skip
    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_fullread(self, mock_stdout):
        # arrange
        sample_points = [0, 49, 99]
        self.setup_nand_1_100(NAND_PATH)

        # action
        self.shell.run("fullread")

        # assert
        for lba in sample_points:
            self.check_right_data(lba, self.convert_to_hex(lba), mock_stdout)

        self.reset_nand(NAND_PATH)
        self.clear_result_files(RESULT_PATH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_fullread(self, mock_stdout):
        # arrange
        tc = [["fullread", "10"],
              ["fullread", "0x111100000"]]

        for n in range(len(tc)):
            # action
            self.run_testcase(tc[n])

            # assert
            self.check_stdout("INVALID COMMAND", mock_stdout)

        self.reset_nand(NAND_PATH)
        self.clear_result_files(RESULT_PATH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_help(self, mock_stdout):
        # arrange
        tc = [["help", "10"],
              ["help", "10", "0x111100000"]]

        for n in range(len(tc)):
            # action
            self.run_testcase(tc[n])

            # assert
            self.check_stdout("INVALID COMMAND", mock_stdout)

    @skip
    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_testapp1(self, mock_stdout):
        # arrange
        write_data = '0xABCDFFFF'
        expected = '\n'.join([write_data] * 100 + ["Pass"])

        # action
        self.shell.run("testapp1")

        # assert
        self.assertEqual(expected, mock_stdout.getvalue().strip())

        self.reset_nand(NAND_PATH)
        self.clear_result_files(RESULT_PATH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_help(self, mock_stdout):
        # arrange
        expected = '\n'.join(('HOW TO TEST SSD',
                              'To WRITE new data : write {LBA index} {data}',
                              'To READ written data : read {LBA index}',
                              'To WRITE data on all LBA : fullwrite {data}',
                              'To READ every data from 0~99 LBA : fullread',
                              'To finish this app : exit',
                              'To repeat this information : help'))

        # action
        self.shell.run("help")

        # assert
        self.assertEqual(expected, mock_stdout.getvalue().strip())

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_command(self, mock_stdout):
        # arrange
        tc = [[""],
              ["noname"]]

        for n in range(len(tc)):
            # action
            self.run_testcase(tc[n])

            # assert
            self.check_stdout("INVALID COMMAND", mock_stdout)

    @skip
    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_testapp2(self, mock_stdout):
        # arrange
        expected = '\n'.join(["0x12345678"] * 6 + ["Pass"])

        # action
        self.shell.run("testapp2")

        # assert
        self.assertEqual(expected, mock_stdout.getvalue().strip())

        self.reset_nand(NAND_PATH)
        self.clear_result_files(RESULT_PATH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_erase(self, mock_stdout):
        # arrange
        tc = [["erase", "3", "17"],
              ["erase", "3", "10"]]
        for n in range(len(tc)):
            self.setup_nand_1_100(NAND_PATH)

            # action
            self.run_testcase(tc[n])

            # assert
            start = max(int(tc[n][1]), 0)
            end = min(start + int(tc[n][2]), 100)
            self.check_right_data(start, self.convert_to_hex(0), mock_stdout)
            self.check_right_data(end - 1, self.convert_to_hex(0), mock_stdout)
            if start != 0:
                self.check_right_data(start - 1, self.convert_to_hex(start - 1), mock_stdout)
            if end != 100:
                self.check_right_data(end, self.convert_to_hex(end), mock_stdout)

        self.reset_nand(NAND_PATH)
        self.clear_result_files(RESULT_PATH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_erase(self, mock_stdout):
        # arrange
        tc = [["erase", "3"],
              ["erase", "3", "0"],
              ["erase", "95", "10"]]
        for n in range(len(tc)):
            self.setup_nand_1_100(NAND_PATH)

            # action
            self.run_testcase(tc[n])

            # assert
            start = int(tc[n][1])
            end = start + int(tc[n][2]) if len(tc[n]) == 3 else start
            for lba in range(max(start, 0), min(end, 100)):
                self.check_right_data(lba, self.convert_to_hex(lba), mock_stdout)

    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_erase_range(self, mock_stdout):
        # arrange
        tc = [["erase_range", "3", "13"],
              ["erase_range", "3", "24"]]
        for n in range(len(tc)):
            self.setup_nand_1_100(NAND_PATH)

            # action
            self.run_testcase(tc[n])

            # assert
            start = max(int(tc[n][1]), 0)
            end = min(int(tc[n][2]), 100)
            self.check_right_data(start, self.convert_to_hex(0), mock_stdout)
            self.check_right_data(end - 1, self.convert_to_hex(0), mock_stdout)
            if start != 0:
                self.check_right_data(start - 1, self.convert_to_hex(start - 1), mock_stdout)
            if end != 100:
                self.check_right_data(end, self.convert_to_hex(end), mock_stdout)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_erase_range(self, mock_stdout):
        # arrange
        tc = [["erase_range", "3"],
              ["erase_range", "3", "2"],
              ["erase_range", "95", "105"]]
        for n in range(len(tc)):
            self.setup_nand_1_100(NAND_PATH)

            # action
            self.run_testcase(tc[n])

            # assert
            self.check_stdout("INVALID COMMAND", mock_stdout)
            start = int(tc[n][1])
            end = int(tc[n][2]) if len(tc[n]) == 3 else start
            for lba in range(max(start, 0), min(end, 100)):
                self.check_right_data(lba, self.convert_to_hex(lba), mock_stdout)

    def run_testcase(self, testcase: list):
        self.shell.run(' '.join(testcase))

    def check_right_data(self, addr, expected: str, mock):
        self.shell.run(f"read {addr}")
        self.check_stdout(expected, mock)

    @staticmethod
    def clear_result_files(result_path: str):
        if os.path.exists(result_path):
            os.remove(result_path)

    @staticmethod
    def setup_nand_1_100(nand_path: str):
        with open(nand_path, 'w') as file:
            file.write(','.join([str(n) for n in range(100)]))

    @staticmethod
    def reset_nand(nand_path: str):
        with open(nand_path, 'w') as file:
            file.write(','.join([str(0) for _ in range(100)]))

    @staticmethod
    def get_value(path: str) -> str:
        with open(path, 'r') as file:
            data = file.readline().strip()
        return data

    @staticmethod
    def convert_to_hex(decimal: int) -> str:
        return '0x' + '{:08x}'.format(decimal).upper()

    @staticmethod
    def convert_hex_to_decimal(value: str):
        return int(value, 16)

    def check_stdout(self, text, mock):
        self.assertEqual(text, mock.getvalue().strip().split("\n")[-1])
