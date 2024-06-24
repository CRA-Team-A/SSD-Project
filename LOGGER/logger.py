import os
from os.path import join
from datetime import datetime
from pathlib import Path
import inspect

from LOGGER.singleton import SingletonClass

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
LOG_EXT = ".log"
ZIP_EXT = ".zip"
PREFIX = "until_"


class Logger(SingletonClass):
    def __init__(self):
        self.root = ROOT_DIR
        self.latest = Path(join(self.root, 'latest.log'))
        self.threshold = 10240  # 10KB = 10 * 1024 bytes

    def log(self, message):
        class_name = inspect.currentframe().f_back.f_locals['self'].__class__.__name__
        method_name = inspect.getframeinfo(inspect.currentframe().f_back).function + "()"
        self.save_latest(f"[{self.get_now()}] {class_name + '.' + method_name:<30}: {message}\n")
        if self.is_oversized_latest():
            self.save_oversized_log()
            self.covert_log_to_zip()

    def covert_log_to_zip(self):
        previous_file_list = self.get_log_list()
        for file in previous_file_list[:-1]:
            file.rename(str(file).replace(LOG_EXT, ZIP_EXT))

    def save_oversized_log(self):
        log_name = join(self.root, PREFIX + self.get_now())
        self.rename_latest(log_name)
        self.latest.touch(exist_ok=True)

    def rename_latest(self, log_name):
        num = 0
        while True:
            save_name = log_name + '-' + str(num) + LOG_EXT
            if not os.path.exists(save_name):
                self.latest.rename(save_name)
                break
            num += 1

    def is_oversized_latest(self):
        return self.latest.stat().st_size > self.threshold

    def save_latest(self, log_text):
        with open(self.latest, 'a') as log_file:
            log_file.write(log_text)

    def get_log_list(self):
        log_list = [Path(join(self.root, file)) for file in os.listdir(self.root)
                    if file.endswith(LOG_EXT) and file.startswith(PREFIX)]
        return sorted(log_list, key=lambda f: os.path.getctime(os.path.join(self.root, f)), reverse=True)

    @staticmethod
    def get_now():
        return datetime.now().strftime('%y-%m-%d_%H-%M-%S')
