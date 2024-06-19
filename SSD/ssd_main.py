import argparse
import sys

from ssd import SSDDriverComma, SSDDriver, SSDDriverEnter

COMMA_TYPE = "comma"
ENTER_TYPE = "enter"


class SSDApplication:
    RESULT_PATH = "result.txt"
    NAND_PATH = "nand.txt"

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='SSD Memory Operation')

        self.parser.add_argument('operation', help='Operation type: W for write, R for read',
                                 nargs='?')
        self.parser.add_argument('address', help='Memory address in integer',
                                 nargs='?')
        self.parser.add_argument('value',
                                 help='Value to write or read offset in hexadecimal (ignored if read)',
                                 nargs='?')

    def main(self, args: list) -> int:
        args = self.get_parsed_arg(args)
        if self.is_invalid_address(args.address):
            return False

        if args.operation == 'R':
            driver = self.create_ssd_driver(COMMA_TYPE)
            driver.read(int(args.address))
        elif args.operation == 'W':
            if self.is_invalid_value(args.value):
                return False
            driver = self.create_ssd_driver(COMMA_TYPE)
            driver.write(int(args.address), args.value)
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
            return SSDDriverComma(self.NAND_PATH, self.RESULT_PATH)
        elif driver_type == ENTER_TYPE:
            return SSDDriverEnter(self.NAND_PATH, self.RESULT_PATH)


if __name__ == '__main__':
    app = SSDApplication()
    print(app.main(sys.argv[1:]))
