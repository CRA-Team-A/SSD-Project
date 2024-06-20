class Command:
    def __init__(self, driver):
        self.driver = driver

    def execute(self):
        pass


class WriteCommand:
    def __init__(self, driver):
        self.driver = driver


class EraseCommand:
    def __init__(self, driver):
        self.driver = driver


CMD_WRITE = "W"
CMD_ERASE = "E"


class SSDBuffer:
    def __init__(self, driver):
        self.driver = driver
        self.commands = self.load_db()
        self.cnt = 0
        self.db_path = "../buffer.txt"

    def update(self, command_type, address, value=None):
        if command_type == "R":
            self.read(address)
            return

        command = self.create_command(command_type, address, value)
        self.commands[address] = command
        self.optimize()
        if self.need_buffer_flush():
            self.flush()

    def read(self, address):
        ret = self.find(address)
        if ret is None:
            ret = self.driver.read(address)
        return ret

    def create_command(self, command_type, address, value):
        if command_type == CMD_WRITE:
            return WriteCommand(self.driver, address, value)
        elif command_type == CMD_ERASE:
            return EraseCommand(self.driver, address, value)
        return Command(self.driver)

    def save_db(self):
        with open(self.db_path, "w+") as f:
            # TODO
            f.write(str(self.commands))

    def load_db(self):
        return {}

    def find(self, address):
        if address in self.commands:
            return self.commands[address].get_value()
        return None

    def optimize(self):
        pass

    def need_buffer_flush(self):
        return self.cnt >= 10

    def flush(self):
        pass
