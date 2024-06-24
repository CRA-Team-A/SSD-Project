class TestApp2(Scenario):
    def __init__(self):
        super().__init__()
        self.write_1st_value = '0xAAAABBBB'
        self.write_2nd_value = '0x12345678'

    def check_valid(self, *args):
        if len(args) != 0:
            self.logger.log('Invalid argument length')
            return False
        self.logger.log('Valid argument')
        return True

    def run(self, *args):
        is_pass = True

        # write LBA[0:6] * 30
        for i in range(30):
            for addr in range(6):
                self.ssd.write(str(addr), self.write_1st_value)
        self.logger.log('Complete write 30times')
        # write LBA[0:6]
        for addr in range(6):
            self.ssd.write(str(addr), self.write_2nd_value)
        self.logger.log('Complete re-write')
        # read LBA[0:6]
        for addr in range(6):
            self.ssd.read(str(addr))
            with open(RESULT_PATH, 'r') as fp:
                value = fp.readline().strip()
            print(value)
            is_pass &= self.write_2nd_value == value
        self.logger.log('Complete read')
        self.print_pass(is_pass)