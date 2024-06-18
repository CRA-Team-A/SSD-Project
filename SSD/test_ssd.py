import os
from unittest import TestCase

from SSD.ssd import SSDDriverEnter


class TestSSDDriverEnter(TestCase):
    def test_read_file_exists(self):
        initial_data = ""
        for i in range(20):
            initial_data += "0" + "\n"
        nand_path = os.path.dirname(os.getcwd()) + '\\nand_tmp.txt'
        result_path = os.path.dirname(os.getcwd()) + '\\result_tmp.txt'
        with open(nand_path, 'w') as nand_file:
            nand_file.write(initial_data)
        ssd_driver = SSDDriverEnter(nand_path, result_path)
        ssd_driver.read(0)
        result = ""
        with open(result_path, 'r') as result_file:
            result += result_file.read()
        os.remove(nand_path)
        os.remove(result_path)
        self.assertEqual("0x00000000", result)
