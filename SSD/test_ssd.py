from unittest import TestCase
from unittest.mock import Mock, patch

from ssd_main import SSDApplication
from ssd import SSDDriverComma, SSDDriver, SSDDriverEnter
import os

MAX_DATA_LENGTH = 20

TEST_RESULT_FILE_PATH = 'result_tmp.txt'

TEST_NAND_FILE_PATH = 'nand_tmp.txt'

INITIAL_VALUE = "0x00000000"


class TestSSDDriver(TestCase):
    def test_init_SSDDriverComma(self):
        nand_path = TEST_NAND_FILE_PATH
        result_path = TEST_RESULT_FILE_PATH
        ssd = SSDDriverComma(nand_path, result_path)
        self.assertTrue(os.path.isfile(nand_path))
        self.clear_files(nand_path, result_path)

    def test_write_SSDDriverComma(self):
        nand_path = TEST_NAND_FILE_PATH
        result_path = TEST_RESULT_FILE_PATH
        ssd = SSDDriverComma(nand_path, result_path)
        ssd.write()
        self.assertTrue(os.path.isfile(nand_path))
        self.clear_files(nand_path, result_path)

    def clear_files(self, nand_path, result_path):
        if os.path.exists(nand_path):
            os.remove(nand_path)
        if os.path.exists(result_path):
            os.remove(result_path)


class TestSSDMain(TestCase):
    def setUp(self):
        self.app = SSDApplication()

    def test_main_invalid_input_read(self):
        ret = self.app.main(["R", "-1"])
        self.assertEqual(ret, False)
        ret = self.app.main(["R", "100"])
        self.assertEqual(ret, False)

    @patch.object(SSDApplication, "create_ssd_driver")
    def test_main_read(self, mk_driver_factory):
        mk = self.create_mock_ssd_driver()
        mk_driver_factory.return_value = mk
        ret = self.app.main(["R", "0"])
        self.assertEqual(ret, True)
        self.assertEqual(mk.read.call_count, 1)

    def test_main_invalid_input_write(self):
        test_case = [
            ["W", "-1", "0x00000000"],
            ["W", "100", "0x00000000"],
            ["W", "0", "1"],
            ["W", "0", "0xFF"],
            ["W", "0", "0x123456789"]
        ]
        for tc in test_case:
            with self.subTest('sub_test arg : ' + " ".join(tc)):
                ret = self.app.main(tc)
                self.assertEqual(ret, False)

    @patch.object(SSDApplication, "create_ssd_driver")
    def test_main_write(self, mk_driver_factory):
        mk = self.create_mock_ssd_driver()
        mk_driver_factory.return_value = mk
        ret = self.app.main(["W", "0", "0x12345678"])
        self.assertEqual(ret, True)
        self.assertEqual(mk.write.call_count, 1)

    def create_mock_ssd_driver(self):
        mk = Mock(spec=SSDDriver)
        mk.read.side_effect = "driver : read"
        mk.write.side_effect = "driver : write"
        return mk


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
