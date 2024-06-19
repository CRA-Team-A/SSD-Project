import sys

from ssd import SSDDriverComma, SSDDriver, SSDDriverEnter

COMMA_TYPE = "comma"
ENTER_TYPE = "enter"
ARG_LEN = 3


class Argument:
    def __init__(self, operation, address, value=None):
        self.operation = operation
        self.address = address
        self.value = value

    def set_operation(self, op):
        self.operation = op

    def set_address(self, addr):
        self.address = addr

    def set_value(self, val):
        self.value = val


class SSDApplication:
    RESULT_PATH = "result.txt"
    NAND_PATH = "nand.txt"
    
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

    def get_parsed_arg(self, args: list) -> Argument:
        if len(args) < ARG_LEN:
            args += [None] * (ARG_LEN - len(args))
        return Argument(args[0], args[1], args[2])

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
            return SSDDriverComma(self.nand_path, self.result_path)
        elif driver_type == ENTER_TYPE:
            return SSDDriverEnter(self.nand_path, self.result_path)


if __name__ == '__main__':
    app = SSDApplication()
    print(app.main(sys.argv[1:]))
