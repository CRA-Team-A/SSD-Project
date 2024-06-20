import os
from unittest import TestCase

from SSD.command import WriteCommand
from SSD.ssd import SSDDriverCommon


class TestCommand(TestCase):
    def test_execute_write_read_success(self):
        current_dir = None
        if os.path.dirname(__file__) == '':
            current_dir = os.getcwd()
        else:
            current_dir = os.path.dirname(__file__)
        ssd_driver = SSDDriverCommon('\n', os.path.join(os.path.dirname(current_dir), 'nand.txt'),
                                     os.path.join(os.path.dirname(current_dir), 'result.txt'))
        write_command = WriteCommand(ssd_driver)
        write_command.execute(1, value="0x00000001")
        ssd_driver.read(1)
        with open(os.path.join(os.path.dirname(current_dir), 'result.txt'), "r") as f:
            result_value = f.read()
        self.assertEqual(result_value, "0x00000001")
