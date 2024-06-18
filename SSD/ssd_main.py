import argparse
import sys

from ssd import SSDDriverComma

RESULT_PATH = "result.txt"
NAND_PATH = "nand.txt"
COMMA_TYPE = "comma"


class SSDApplication:
    def main(self, args: list) -> int:
        parser = argparse.ArgumentParser(description='SSD Memory Operation')

        # 명령어와 관련된 인수 추가
        parser.add_argument('operation', choices=['W', 'R'], help='Operation type: W for write, R for read')
        parser.add_argument('address', type=int, help='Memory address in hexadecimal')
        parser.add_argument('value', help='Value to write or read offset (ignored if read)', nargs='?')

        args = parser.parse_args(args)
        if self.is_invalid_address(args.address):
            return False

        driver = self.create_ssd_driver(COMMA_TYPE)

        # 명령어에 따라 처리
        if args.operation == 'R':
            driver.read(args.address)
        elif args.operation == 'W':
            if self.is_invalid_value(args.value):
                return False
            driver.write(args.address, args.value)
        else:
            return False

        return True

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

    def create_ssd_driver(self, driver_type):
        if driver_type == COMMA_TYPE:
            return SSDDriverComma(NAND_PATH, RESULT_PATH)


if __name__ == '__main__':
    app = SSDApplication()
    print(app.main(sys.argv[1:]))
