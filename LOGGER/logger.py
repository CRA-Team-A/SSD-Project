import os
from os.path import join
from datetime import datetime
from pathlib import Path

from .Singleton import SingletonClass

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
LOG_EXT = ".log"
ZIP_EXT = ".zip"


class Logger(SingletonClass):
    def __init__(self):
        self.root = ROOT_DIR
        self.latest = Path(join(self.root, 'latest.log'))
        self.threshold = 10240  # 10KB = 10 * 1024 bytes

    def log(self, func_name, message):
        func = func_name + "()"
        text = f"[{self.get_now()}] {func:<30}: {message}\n"
        with open(self.latest, 'a') as log_file:
            log_file.write(text)
        if self.latest.stat().st_size > self.threshold:
            log_name = join(self.root, f"until_{self.get_now()}.log")
            self.latest.rename(log_name)
            self.latest.touch(exist_ok=True)
            previous_file_list = sorted([Path(join(self.root, file)) for file in os.listdir(self.root) if file.endswith('.log') and file.startswith('until_')],
                               key=lambda f: os.path.getctime(os.path.join(self.root, f)), reverse=True)
            for file in previous_file_list[:-1]:
                file.rename(str(file).replace('.log', '.zip'))

    @staticmethod
    def get_now():
        return datetime.now().strftime('%y-%m-%d_%H-%M-%S')




