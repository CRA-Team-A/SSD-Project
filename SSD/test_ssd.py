import subprocess
from unittest import TestCase
from unittest.mock import Mock, patch

from ssd_interface import SSDInterface
from ssd import SSDDriverComma, SSDDriver, SSDDriverEnter
import os

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
MAIN = "ssd_interface.py"
MAX_DATA_LENGTH = 100
NAND_PATH = os.path.join(ROOT_DIR, 'nand.txt')
RESULT_PATH = os.path.join(ROOT_DIR, 'result.txt')
INITIAL_VALUE = "0x00000000"
WRITE_ADDRESS = 50
WRITE_VALUE = '0x00ABCDEF'


class TestSSD(TestCase):
    mock = False
    driver_type = "comma"

    def setUp(self):
        self.app = SSDInterface()

    def tearDown(self):
        self.clear_test_files(NAND_PATH, RESULT_PATH)

    def test_init_ssd_driver_comma(self):
        ssd_comma = SSDDriverComma(NAND_PATH, RESULT_PATH)
        self.assertTrue(os.path.isfile(NAND_PATH))

    def test_read_ssd_driver_comma(self):
        self.setup_nand_1_100(NAND_PATH)
        ssd_comma = SSDDriverComma(NAND_PATH, RESULT_PATH)

        for i in range(10):
            with self.subTest('subtest_' + str(i)):
                ssd_comma.read(i)
                data = self.get_value(RESULT_PATH)
                self.assertEqual(self.convert_to_hex(i), data)

    def test_read_empty_ssd_driver_comma(self):
        ssd_comma = SSDDriverComma(NAND_PATH, RESULT_PATH)

        ssd_comma.read(0)
        data = self.get_value(RESULT_PATH)
        self.assertEqual(self.convert_to_hex(0), data)

    def test_write_ssd_driver_comma(self):
        ssd_comma = SSDDriverComma(NAND_PATH, RESULT_PATH)

        ssd_comma.write(WRITE_ADDRESS, WRITE_VALUE)
        ssd_comma.read(WRITE_ADDRESS)
        data = self.get_value(RESULT_PATH)

        self.assertEqual(WRITE_VALUE, data)

    def test_read_empty_ssd_driver_enter(self):
        ssd_enter = SSDDriverEnter(NAND_PATH, RESULT_PATH)

        ssd_enter.read(0)

        result = self.get_value(RESULT_PATH)
        self.assertEqual(INITIAL_VALUE, result)

    def test_write_ssd_driver_enter(self):
        ssd_enter = SSDDriverEnter(NAND_PATH, RESULT_PATH)

        ssd_enter.write(WRITE_ADDRESS, WRITE_VALUE)

        with open(NAND_PATH, 'r') as nand_file:
            nand_data = list(map(int, nand_file.read().split('\n')[:MAX_DATA_LENGTH]))
        self.assertEqual(self.convert_hex_to_decimal(WRITE_VALUE), nand_data[WRITE_ADDRESS])

    def test_read_after_write_ssd_driver_enter(self):
        ssd_enter = SSDDriverEnter(NAND_PATH, RESULT_PATH)

        ssd_enter.write(WRITE_ADDRESS, WRITE_VALUE)
        ssd_enter.read(WRITE_ADDRESS)

        result = self.get_value(RESULT_PATH)
        self.assertEqual(WRITE_VALUE, result)

    def test_invalid_input_write_operation_ssd_driver_interface(self):
        test_case = [
            ["W"],
            ["W", "-1", "INVALID"],
            ["W", "INVALID", "0x00000000"],
            ["W", "-1", "0x00000000"],
            ["W", "100", "0x00000000"],
            ["W", "0", "1"],
            ["W", "0", "0xFF"],
            ["W", "0", "0x123456789"],
            ["W", "0", "11123456789"]
        ]
        for tc in test_case:
            with self.subTest('sub_test arg : ' + " ".join(tc)):
                self.send_to_main(tc)
            if os.path.exists(NAND_PATH):
                self.fail()

    def test_real_write_operation_ssd_driver_interface(self):
        self.send_to_main(["W", str(WRITE_ADDRESS), WRITE_VALUE])
        self.send_to_main(["R", str(WRITE_ADDRESS)])
        ret = self.read(RESULT_PATH)
        self.assertEqual(ret, WRITE_VALUE)

    def test_invalid_input_read_operation_ssd_driver_interface(self):
        test_cases = [
            ["R", "-1"],
            ["R", "100"],
            ["R", "INVALID"],
            ["R"]
        ]

        for tc in test_cases:
            self.send_to_main(tc)
            if os.path.exists(NAND_PATH):
                self.fail()

    def test_real_read_operation_ssd_driver_interface(self):
        self.send_to_main(["R", "0"])
        ret = self.read(RESULT_PATH)
        self.assertEqual(ret, "0x00000000")

    def test_invalid_operation_ssd_driver_interface(self):
        with self.assertRaises(SystemExit):
            ret = self.app.main(["INVALID"])

    def read(self, file):
        sep = ',' if self.driver_type == "comma" else '\n'
        with open(file, "r") as f:
            return f.read().strip()

    @staticmethod
    def clear_test_files(nand_path: str, result_path: str):
        if os.path.exists(nand_path):
            os.remove(nand_path)
        if os.path.exists(result_path):
            os.remove(result_path)
        pass

    @staticmethod
    def setup_nand_1_100(nand_path: str):
        with open(nand_path, 'w') as file:
            file.write(','.join([str(n) for n in range(100)]))

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

    @staticmethod
    def send_to_main(tc):
        full_command = f"python {MAIN} {' '.join(tc)}"
        p = subprocess.Popen(full_command)
        return p.communicate()


class TestSSD_Class(TestSSD):
    def send_to_main(self, tc):
        try:
            self.app.main(tc)
            return True
        except SystemExit:
            return False
