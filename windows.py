import os
import datetime
import time
import psutil


class WindowsInterface:
    @staticmethod
    def is_program_running(name) -> bool:
        print("is_program_running {}".format(name))
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                if name in p.name():
                    return True
            except:
                continue
        return False

    def start_program(self, path, name) -> bool:
        if self.is_program_running(name):
            return True
        print("Starting application {} at {}".format(name, datetime.datetime.now()))
        os.startfile(path)
        time.sleep(3)
        if self.is_program_running(name):
            return True
        print("Starting application {} failed at {}".format(name, datetime.datetime.now()))
        return False
