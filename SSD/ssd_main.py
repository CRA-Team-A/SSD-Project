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
    def __init__(self, nand_path="nand.txt", result_path="result.txt"):
        self.nand_path = nand_path
        self.result_path = result_path
        self.args = None

    def main(self, inputs: list) -> int:
        self.args = self.get_parsed_arg(inputs)
        self.check_arguments()
        # if self.is_invalid_address(self.args.address):
        #     return False

        if self.args.operation == 'R':
            driver = self.create_ssd_driver(COMMA_TYPE)
            driver.read(int(self.args.address))
        elif self.args.operation == 'W':
            if self.is_invalid_value(self.args.value):
                return False
            driver = self.create_ssd_driver(COMMA_TYPE)
            driver.write(int(self.args.address), self.args.value)
        else:
            self.error()

        return True

    def get_parsed_arg(self, args: list) -> Argument:
        if len(args) < ARG_LEN:
            args += [None] * (ARG_LEN - len(args))
        return Argument(args[0], args[1], args[2])

    def check_arguments(self):
        if self.args.operation == 'R':
            try:
                int(self.args.address)
            except Exception:
                self.error()
            if not 0 <= self.args.address <= 99:
                self.error()
        elif self.args.operation == 'W':
            try:
                int(self.args.address)
            except Exception:
                self.error()
            if not 0 <= self.args.address <= 99:
                self.error()


            try:
                int(self.args.value, 16)
            except Exception():
                self.error()
            if len(self.args.value) != 10:
                self.error()
        else:
            self.error()


    @staticmethod
    def error():
        print('Invalid Arguments!')
        sys.exit(1)

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
