import subprocess
from unittest import TestCase
from unittest.mock import Mock, patch

from ssd_main import SSDApplication
from ssd import SSDDriverComma, SSDDriver, SSDDriverEnter
import os

CLASS = "class"

CMD = "cmd"

MAIN = "ssd_main.py"
MAX_DATA_LENGTH = 100
NAND_PATH = 'nand.txt'
RESULT_PATH = 'result.txt'
INITIAL_VALUE = "0x00000000"
PYTHON_PATH = ".venv/Scripts/python.exe"
WRITE_ADDRESS = 50
WRITE_VALUE = '0x00ABCDEF'


class TestSSD(TestCase):
    mock = False
    driver_type = "comma"

    def setUp(self):
        self.app = SSDApplication()

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
        ret = [int(x) for x in self.read(NAND_PATH)]
        self.assertEqual(ret[WRITE_ADDRESS], int(WRITE_VALUE, 16))

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
        self.assertEqual(ret[0], "0x00000000")

    def test_invalid_operation_ssd_driver_interface(self):
        ret = self.app.main(["INVALID"])
        self.assertEqual(ret, False)

    def read(self, file):
        sep = ',' if self.driver_type == "comma" else '\n'
        with open(file, "r") as f:
            return f.read().strip().split(sep)

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
        python_path = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), PYTHON_PATH)
        full_command = f"{python_path} {MAIN} {' '.join(tc)}"
        p = subprocess.Popen(full_command)
        return p.communicate()




# class TestSSDMain(TestCase):
#     mock = False
#     driver_type = "comma"
#
#     def setUp(self):
#         if self.driver_type == "comma":
#             self.NAND_PATH = NAND_PATH
#             self.RESULT_PATH = RESULT_PATH
#         if self.driver_type == "enter":
#             self.NAND_PATH = NAND_PATH
#             self.RESULT_PATH = RESULT_PATH
#         self.app = SSDApplication(self.NAND_PATH, self.RESULT_PATH)
#
#     def tearDown(self):
#         self.clear_files("nand.txt", "result.txt")
#
#     # def test_main_invalid_input_read(self):
#     #     test_cases = [
#     #         ["R", "-1"],
#     #         ["R", "100"],
#     #         ["R", "INVALID"],
#     #         ["R"]
#     #     ]
#     #
#     #     for tc in test_cases:
#     #         self.send_to_main(tc)
#     #         if os.path.exists(self.NAND_PATH):
#     #             self.fail()
#
#     # @patch.object(SSDApplication, "create_ssd_driver")
#     # def test_main_read(self, mk_driver_factory):
#     #     mk = self.create_ssd_driver()
#     #     mk_driver_factory.return_value = mk
#     #     self.send_to_main(["R", "0"])
#     #     ret = self.read(self.RESULT_PATH)
#     #     self.assertEqual(ret[0], "0x00000000")
#
#     # def test_main_invalid_input_write(self):
#     #     test_case = [
#     #         ["W"],
#     #         ["W", "-1", "INVALID"],
#     #         ["W", "INVALID", "0x00000000"],
#     #         ["W", "-1", "0x00000000"],
#     #         ["W", "100", "0x00000000"],
#     #         ["W", "0", "1"],
#     #         ["W", "0", "0xFF"],
#     #         ["W", "0", "0x123456789"],
#     #         ["W", "0", "11123456789"]
#     #     ]
#     #     for tc in test_case:
#     #         with self.subTest('sub_test arg : ' + " ".join(tc)):
#     #             self.send_to_main(tc)
#     #         if os.path.exists(self.NAND_PATH):
#     #             self.fail()
#
#     @patch.object(SSDApplication, "create_ssd_driver")
#     def test_main_write(self, mk_driver_factory):
#         mk = self.create_ssd_driver()
#         mk_driver_factory.return_value = mk
#         self.send_to_main(["W", "0", "0x12345678"])
#         ret = [int(x) for x in self.read(self.NAND_PATH)]
#         self.assertEqual(ret[0], int("0x12345678", 16))
#
#
#     def create_ssd_driver(self) -> SSDDriver:
#         if self.mock:
#             mk: SSDDriver = Mock(spec=SSDDriver)
#             mk.read.side_effect = "driver : read"
#             mk.write.side_effect = "driver : write"
#             return mk
#         elif self.driver_type == "comma":
#             return SSDDriverComma(NAND_PATH, RESULT_PATH)
#         elif self.driver_type == "enter":
#             return SSDDriverEnter(NAND_PATH, RESULT_PATH)
#
#     def clear_files(self, nand_path, result_path):
#         if os.path.exists(nand_path):
#             os.remove(nand_path)
#         if os.path.exists(result_path):
#             os.remove(result_path)
#
#     def send_to_main(self, tc):
#         python_path = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), PYTHON_PATH)
#         full_command = f"{python_path} {MAIN} {' '.join(tc)}"
#         print(full_command)
#         p = subprocess.Popen(full_command)
#         return p.communicate()
#
#     def read(self, file):
#         sep = ',' if self.driver_type == "comma" else '\n'
#         with open(file, "r") as f:
#             return f.read().strip().split(sep)
