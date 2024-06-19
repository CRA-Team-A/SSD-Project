import subprocess
from unittest import TestCase
from unittest.mock import Mock, patch

from ssd_main import SSDApplication
from ssd import SSDDriverComma, SSDDriver, SSDDriverEnter
import os

MAIN = "ssd_main.py"
MAX_DATA_LENGTH = 100
TEST_NAND_PATH = 'nand_temp.txt'
TEST_RESULT_PATH = 'result_temp.txt'
TEST_RESULT_FILE_PATH = 'result_tmp.txt'
TEST_NAND_FILE_PATH = 'nand_tmp.txt'
INITIAL_VALUE = "0x00000000"
PYTHON_PATH = ".venv/Scripts/python.exe"


class TestSSDDriver(TestCase):
    def setUp(self):
        self.ssd_comma = SSDDriverComma(TEST_NAND_PATH, TEST_RESULT_PATH)

    def test_init_SSDDriverComma(self):
        self.assertTrue(os.path.isfile(TEST_NAND_PATH))
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    def test_read_SSDDriverComma(self):
        self.setup_nand_1_100(TEST_NAND_PATH)
        ssd_comma = SSDDriverComma(TEST_NAND_PATH, TEST_RESULT_PATH)

        for i in range(100):
            with self.subTest('subtest_' + str(i)):
                ssd_comma.read(i)
                data = self.get_result_value(TEST_RESULT_PATH)
                self.assertEquals(self.convert_to_hex(i), data)
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    def test_read_empty_SSDDriverComma(self):
        ssd_comma = SSDDriverComma(TEST_NAND_PATH, TEST_RESULT_PATH)

        ssd_comma.read(0)
        data = self.get_result_value(TEST_RESULT_PATH)
        self.assertEquals(self.convert_to_hex(0), data)
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    def test_write_SSDDriverComma(self):
        address = 50
        value = '0xFFFFFFFF'
        ssd_comma = SSDDriverComma(TEST_NAND_PATH, TEST_RESULT_PATH)

        ssd_comma.write(address, value)
        ssd_comma.read(address)
        data = self.get_result_value(TEST_RESULT_PATH)

        self.assertEquals(value, data)
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    @staticmethod
    def clear_files(nand_path: str, result_path: str):
        if os.path.exists(nand_path):
            os.remove(nand_path)
        if os.path.exists(result_path):
            os.remove(result_path)

    @staticmethod
    def setup_nand_1_100(nand_path: str):
        with open(nand_path, 'w') as file:
            file.write(','.join([str(n) for n in range(100)]))

    @staticmethod
    def get_result_value(result_path: str) -> str:
        with open(result_path, 'r') as result:
            data = result.readline().strip()
        return data

    @staticmethod
    def convert_to_hex(decimal: int) -> str:
        return '0x' + '{:08x}'.format(decimal).upper()


class TestSSDMain(TestCase):
    MOCK = False
    DRIVER_TYPE = "comma"

    @patch('ssd_main.SSDApplication.NAND_PATH', TEST_NAND_FILE_PATH)
    @patch('ssd_main.SSDApplication.RESULT_PATH', TEST_RESULT_FILE_PATH)
    def setUp(self):
        super().setUp()
        self.app = SSDApplication()

    def tearDown(self):
        self.clear_files(TEST_NAND_FILE_PATH, TEST_RESULT_FILE_PATH)
        super().tearDown()

    def test_main_invalid_input_read(self):
        test_cases = [
            ["R", "-1"],
            ["R", "100"],
            ["R", "INVALID"],
            ["R"]
        ]

        for tc in test_cases:
            self.send_to_main(tc)
            if os.path.exists(TEST_RESULT_FILE_PATH):
                self.fail()

    @patch.object(SSDApplication, "create_ssd_driver")
    def test_main_read(self, mk_driver_factory):
        mk = self.create_ssd_driver()
        mk_driver_factory.return_value = mk
        ret = self.app.main(["R", "0"])
        self.assertEqual(ret, True)

    def test_main_invalid_input_write(self):
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
            if os.path.exists(TEST_NAND_FILE_PATH):
                self.fail()

    @patch.object(SSDApplication, "create_ssd_driver")
    def test_main_write(self, mk_driver_factory):
        mk = self.create_ssd_driver()
        mk_driver_factory.return_value = mk
        ret = self.app.main(["W", "0", "0x12345678"])
        self.assertEqual(ret, True)
        self.assertEqual(mk.write.call_count, 1)

    def test_invalid_operation(self):
        ret = self.app.main(["INVALID"])
        self.assertEqual(ret, False)

    def create_ssd_driver(self) -> SSDDriver:
        mk: SSDDriver = Mock(spec=SSDDriver)
        if self.MOCK:
            mk.read.side_effect = "driver : read"
            mk.write.side_effect = "driver : write"
        else:
            return self.app.create_ssd_driver(self.DRIVER_TYPE)

    def clear_files(self, nand_path, result_path):
        if os.path.exists(nand_path):
            os.remove(nand_path)
        if os.path.exists(result_path):
            os.remove(result_path)

    def send_to_main(self, tc):
        python_path = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), PYTHON_PATH)
        print(python_path)
        p = subprocess.Popen(f"{python_path} {MAIN} {' '.join(tc)}")
        return p.communicate()

    def read_file(self, path):
        with open(path, "r") as f:
            return f.readlines()

            
class TestSSDDriverEnter(TestCase):
    def setUp(self):
        self.nand_path = os.path.dirname(os.getcwd()) + '\\' + TEST_NAND_FILE_PATH
        self.result_path = os.path.dirname(os.getcwd()) + '\\' + TEST_RESULT_FILE_PATH
        self.ssd_driver = SSDDriverEnter(self.nand_path, self.result_path)

    def tearDown(self):
        self.clear_test_files()

    def clear_test_files(self):
        if os.path.exists(self.nand_path):
            os.remove(self.nand_path)
        if os.path.exists(self.result_path):
            os.remove(self.result_path)

    def test_read_initialized_file(self):
        self.ssd_driver.read(0)
        result = ''
        with open(self.result_path, 'r') as result_file:
            result += result_file.read()
        self.assertEqual(INITIAL_VALUE, result)

    def test_write_success(self):
        self.ssd_driver.write(2, '0xFFFFABCD')
        nand_data = None
        with open(self.nand_path, 'r') as nand_file:
            nand_data = list(map(int, nand_file.read().split('\n')[:MAX_DATA_LENGTH]))
        self.assertEqual(4294945741, nand_data[2])

    def test_read_after_write(self):
        self.ssd_driver.write(2, '0xFFFF1234')
        self.ssd_driver.read(2)
        result = ''
        with open(self.result_path, 'r') as result_file:
            result += result_file.read()
        self.assertEqual('0xFFFF1234', result)
