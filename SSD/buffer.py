import os.path

from LOGGER.logger import Logger
from SSD.command import Command, WriteCommand, EraseCommand
from SSD.ssd import SSDDriver

ZERO_VALUE = "0x00000000"

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

    def update(self, command_type: str, address: int = None, value: str = None):
        try:
            if command_type == "F":
                self.flush()
                return
            elif command_type == "R":
                self.read(address)
                return

            command = self.create_command(command_type, address, value)
            if not command:
                return

            self.add_command(command)
            if self.need_buffer_flush():
                self.flush()
            self.save_db()
        except Exception as e:
            self.logger.log(f"Buffer Error : {e}")

    def read(self, address: int):
        ret = self.find(address)
        if ret is None:
            self.driver.read(address)
        else:
            with open(self.driver.result_path, 'w') as file:
                file.write(ret)

    def create_command(self, command_type: str, address: int, value: str):
        if command_type == CMD_WRITE:
            return WriteCommand(self.driver, address, value)
        elif command_type == CMD_ERASE:
            return EraseCommand(self.driver, address, value)
        self.logger.log(f"invalid command type {command_type}")

    def flush(self):
        for command in self.commands:
            command.execute()

        self.commands.clear()
        self.cnt = 0
        self.save_db()

    def add_command(self, command: Command):
        self.cnt += 1
        self.commands.append(command)
        self.optimize_commands()

    def optimize_commands(self):
        command_cache = [None for _ in range(100)]
        for _cmd in self.commands:
            if isinstance(_cmd, WriteCommand):
                if _cmd.value == ZERO_VALUE:
                    command_cache[_cmd.address] = CMD_ERASE
                else:
                    command_cache[_cmd.address] = _cmd
            if isinstance(_cmd, EraseCommand):
                for offset in range(int(_cmd.value)):
                    command_cache[_cmd.address + offset] = CMD_ERASE

        erase_commands = []
        start = -1
        end = -1
        for idx, _cmd in enumerate(command_cache):
            if _cmd == CMD_ERASE:
                if start == -1:
                    start = idx
                    end = idx
                else:
                    if idx - start + 1 >= 10:
                        erase_commands.append(self.create_command(CMD_ERASE, start, str(end - start + 1)))
                        start = -1
                        end = -1
                    else:
                        end = idx
            elif _cmd is None and start != -1:
                erase_commands.append(self.create_command(CMD_ERASE, start, str(end - start + 1)))
                start = -1
                end = -1

        if start != -1:
            erase_commands.append(self.create_command(CMD_ERASE, start, str(end - start)))

        write_commands = [command for command in command_cache if isinstance(command, Command)]
        new_commands = erase_commands + write_commands
        if len(new_commands) <= len(self.commands):
            self.commands = new_commands

    def need_buffer_flush(self) -> bool:
        return len(self.commands) > 10

    def save_db(self):
        data = self.make_db_data()
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
                if command.address <= address < command.address + int(command.value):
                    return f'0x00000000'

        return None

    def make_db_data(self) -> str:
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
