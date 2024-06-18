from unittest import TestCase
from ssd import SSDDriverComma
import os


class TestSSDDriver(TestCase):
    def test_init_SSDDriverComma(self):
        nand_path = 'nand_temp.txt'
        result_path = 'result_temp.txt'
        ssd = SSDDriverComma(nand_path, result_path)
        self.assertTrue(os.path.isfile(nand_path))
        self.clear_files(nand_path, result_path)

    def test_read_SSDDriverComma(self):
        nand_path = 'nand_temp.txt'
        result_path = 'result_temp.txt'
        self.setup_nand(nand_path)
        ssd = SSDDriverComma(nand_path, result_path)
        for i in range(100):
            with self.subTest('subtest_'+str(i)):
                ssd.read(i)
                with open(result_path, 'r') as result:
                    data = result.readline().strip()
                self.assertEquals(str(hex(i)), data)
        self.clear_files(nand_path, result_path)

    def test_write_SSDDriverComma(self):
        address = 50
        nand_path = 'nand_temp.txt'
        result_path = 'result_temp.txt'
        ssd = SSDDriverComma(nand_path, result_path)
        ssd.write(address, '0xFFFFFFFF')
        self.assertTrue(os.path.isfile(nand_path))
        self.clear_files(nand_path, result_path)

    def clear_files(self, nand_path, result_path):
        if os.path.exists(nand_path):
            os.remove(nand_path)
        if os.path.exists(result_path):
            os.remove(result_path)

    def setup_nand(self, nand_path):
        with open(nand_path, 'w') as file:
            file.write(','.join([str(n) for n in range(100)]))