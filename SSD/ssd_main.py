import argparse
import sys


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

        # 명령어에 따라 처리
        if args.operation == 'R':
            pass
        elif args.operation == 'W':
            if self.is_invalid_value(args.value):
                return False
        else:
            pass
        return True

    def is_invalid_address(self, address: int) -> bool:
        if address is None:
            return True
        try:
            return not (0 <= address <= 99)
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


if __name__ == '__main__':
    app = SSDApplication()
    print(app.main(sys.argv[1:]))
