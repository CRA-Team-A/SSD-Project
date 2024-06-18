import argparse
import sys


class SSDApplication:
    def main(self, args: list) -> int:
        parser = argparse.ArgumentParser(description='SSD Memory Operation')

        # 명령어와 관련된 인수 추가
        parser.add_argument('operation', choices=['W', 'R'], help='Operation type: W for write, R for read')
        parser.add_argument('address', type=lambda x: int(x, 16), help='Memory address in hexadecimal')
        parser.add_argument('value', type=int, help='Value to write or read offset (ignored if read)', nargs='?')

        args = parser.parse_args(args)
        if self.is_invalid_address(args.address):
            return False

        # 명령어에 따라 처리
        if args.operation == 'R':
            pass
        elif args.operation == 'W':
            pass
        else:
            pass

        return True

    def is_invalid_address(self, address: str) -> bool:
        if address is None:
            return True
        try:
            return not (0 <= int(address) <= 99)
        except Exception:
            return True


if __name__ == '__main__':
    app = SSDApplication()
    print(app.main(sys.argv[1:]))
