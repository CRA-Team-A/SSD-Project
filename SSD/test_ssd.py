from unittest import TestCase
from unittest.mock import Mock, patch

from ssd_main import SSDApplication
from ssd import SSDDriverComma, SSDDriver
import os


class TestSSDDriver(TestCase):
    def test_init_SSDDriverComma(self):
        nand_path = 'nand_temp.txt'
        result_path = 'result_temp.txt'
        ssd = SSDDriverComma(nand_path, result_path)
        self.assertTrue(os.path.isfile(nand_path))
        self.clear_files(nand_path, result_path)

    def test_write_SSDDriverComma(self):
        nand_path = 'nand_temp.txt'
        result_path = 'result_temp.txt'
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
        super().setUp()
        self.app = SSDApplication()

    def tearDown(self):
        from ssd_main import NAND_PATH, RESULT_PATH
        self.clear_files(NAND_PATH, RESULT_PATH)
        super().tearDown()

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
            ["W", "0", "0x123456789"],
            ["W", "0", "11123456789"]
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

    def clear_files(self, nand_path, result_path):
        if os.path.exists(nand_path):
            os.remove(nand_path)
        if os.path.exists(result_path):
            os.remove(result_path)
