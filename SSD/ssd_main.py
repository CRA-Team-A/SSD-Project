import argparse
import sys

from ssd import SSDDriverComma, SSDDriver, SSDDriverEnter

RESULT_PATH = "result.txt"
NAND_PATH = "nand.txt"
COMMA_TYPE = "comma"
ENTER_TYPE = "enter"


class SSDApplication:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='SSD Memory Operation')

        self.parser.add_argument('operation', choices=['W', 'R'], help='Operation type: W for write, R for read')
        self.parser.add_argument('address', type=int, help='Memory address in integer')
        self.parser.add_argument('value',
                                 help='Value to write or read offset in hexadecimal (ignored if read)',
                                 nargs='?')

    def main(self, args: list) -> int:
        args = self.get_parsed_arg(args)
        if self.is_invalid_address(args.address):
            return False

        driver = self.create_ssd_driver(COMMA_TYPE)

        if args.operation == 'R':
            driver.read(int(args.address))
        elif args.operation == 'W':
            if self.is_invalid_value(args.value):
                return False
            driver.write(int(args.address), int(args.value, 16))
        else:
            return False

        return True

    def get_parsed_arg(self, args: list) -> argparse.Namespace:
        return self.parser.parse_args(args)

    def is_invalid_address(self, address: str) -> bool:
        if address is None:
            return True
        try:
            return not (0 <= int(address) <= 99)
        except Exception:
            return True

    def is_invalid_value(self, value: str) -> bool:
        if value is None:
            return True
        if len(value) != 10:
            return True
        try:
            return not (0x00000000 <= int(value, 16) <= 0xFFFFFFFF)
        except Exception:
            return True

    def create_ssd_driver(self, driver_type: str) -> SSDDriver:
        if driver_type == COMMA_TYPE:
            return SSDDriverComma(NAND_PATH, RESULT_PATH)
        elif driver_type == ENTER_TYPE:
            return SSDDriverEnter(NAND_PATH, RESULT_PATH)


if __name__ == '__main__':
    app = SSDApplication()
    print(app.main(sys.argv[1:]))
