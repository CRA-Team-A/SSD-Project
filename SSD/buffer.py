import os.path

from LOGGER.logger import Logger
from SSD.command import Command, WriteCommand, EraseCommand
from SSD.ssd import SSDDriver

CMD_WRITE = "W"
CMD_ERASE = "E"
if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)


class SSDBuffer:
    def __init__(self, driver: SSDDriver):
        self.db_path = os.path.join(ROOT_DIR, "buffer.txt")
        self.logger = Logger()
        self.driver = driver
        self.commands = self.load_db()
        self.cnt = 0

    def update(self, command_type: str, address: int, value: str = None):
        try:
            if command_type == "R":
                self.read(address)
                return
            elif command_type == "F":
                self.flush()
                return

            command = self.create_command(command_type, address, value)
            if not command:
                return

            self.add_command(command)
            if self.need_buffer_flush():
                self.flush()
            self.save_db()
            self.cnt += 1
        except Exception as e:
            self.logger.log(f"Buffer Error : {e}")

    def read(self, address: int):
        ret = self.find(address)
        if ret is None:
            self.driver.read(address)
        else:
            with open(self.driver.result_path, 'w') as file:
                file.write(ret)

    def flush(self):
        for command in self.commands:
            command.execute()

        self.commands.clear()
        self.save_db()

    def create_command(self, command_type: str, address: int, value: str):
        if command_type == CMD_WRITE:
            return WriteCommand(self.driver, address, value)
        elif command_type == CMD_ERASE:
            return EraseCommand(self.driver, address, value)
        self.logger.log(f"invalid command type {command_type}")

    def add_command(self, command: Command):
        # optimize
        for command in self.commands:
            if isinstance(command, WriteCommand):
                pass
            if isinstance(command, EraseCommand):
                pass

        self.commands.append(command)

    def save_db(self):
        data = self.make_db()
        with open(self.db_path, "w") as f:
            f.write(data)

    def load_db(self) -> [Command]:
        if not os.path.exists(self.db_path):
            return []

        ret = []
        with open(self.db_path, "r") as f:
            self.cnt = f.readline()
            for line in f:
                args = line.strip().split(" ")
                if len(args) < 3:
                    continue
                ret.append(self.create_command(args[0], int(args[1]), args[2]))
        return ret

    def find(self, address: int):
        for command in self.commands:
            if isinstance(command, WriteCommand):
                if command.address == address:
                    return f'{command.value}'
            elif isinstance(command, EraseCommand):
                if command.address <= address < command.address + command.value:
                    return f'0x00000000'

        return None

    def need_buffer_flush(self) -> bool:
        return self.cnt >= 10

    def make_db(self) -> str:
        content = f"{self.cnt}\n"
        for command in self.commands:
            command_type = self.get_command_type(command)
            content += f"{command_type} {command.address} {command.value}\n"
        return content

    def get_command_type(self, command):
        if isinstance(command, WriteCommand):
            return "W"
        elif isinstance(command, EraseCommand):
            return "E"
