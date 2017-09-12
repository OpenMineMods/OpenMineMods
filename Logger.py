from sys import stdout, stderr
from time import strftime


def log(text, ltype):
    out = {"INFO": stdout, "ERROR": stderr}[ltype]
    out.write(
        "[{}][{}] {}\r\n".format(
            strftime("%D %D"),
            ltype,
            str(text)
        )
    )
    out.flush()


def info(text):
    log(text, "INFO")


def err(text):
    log(text, "ERROR")
