import os
import subprocess


SSD_PATH = 'SSD/ssd_interface.py'


class SSDHandler:
    def __init__(self):
        if os.path.dirname(__file__) == '':
            current_dir = os.getcwd()
        else:
            current_dir = os.path.dirname(__file__)
        root_dir = os.path.dirname(current_dir)
        self.path = os.path.join(root_dir, SSD_PATH)

    def read(self, *args):
        ret = subprocess.run(["python", self.path, "R"] + [str(i) for i in args], capture_output=True, text=True, check=True)
        return ret.returncode

    def write(self, *args):
        ret = subprocess.run(["python", self.path, "W"] + [str(i) for i in args], capture_output=True, text=True, check=True)
        return ret.returncode

    def erase(self, *args):
        ret = subprocess.run(["python", self.path, "E"] + [str(i) for i in args], capture_output=True, text=True, check=True)
        return ret.returncode
