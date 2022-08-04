import os
from functools import wraps
from threading import Lock


# >>> log utils
# output mutex lock
log_lock = Lock()


def writeFailLog(text: str):
    """[summary]
    append text in fail_log.txt
    """
    with log_lock:
        with open("fail_log.txt", "a+") as f:
            f.write(text)


def timeLog(func):
    @wraps(func)
    def clocked(*args, **kwargs):
        from time import time
        start_time = time()
        ret = func(*args, **kwargs)
        print("{}() finishes after {:.2f} s".format(
            func.__name__, time() - start_time))
        return ret
    return clocked


def printInfo(msg):
    print("[INFO]: {}".format(msg))


def printWarn(expr: bool, msg):
    if expr:
        print("[WARN]: {}".format(msg))


def printError(expr: bool, msg):
    if expr:
        print("[ERROR]: {}".format(msg))
        raise RuntimeError()

# <<< log utils


def checkDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        printInfo(f"create {dir_path}")
