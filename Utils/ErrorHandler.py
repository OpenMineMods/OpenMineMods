from PyQt5.QtCore import QStandardPaths

from API.CurseAPI import CurseAPI

from traceback import format_tb
from platform import platform
from os import path

from GUI.ErrorDialogWrapper import ErrorDialog

from Utils.Analytics import censor_string


def handle_exception(etype, val, traceback):
    data_dir = path.join(QStandardPaths.writableLocation(QStandardPaths.GenericDataLocation), "openminemods")
    cache_dir = path.join(QStandardPaths.writableLocation(QStandardPaths.GenericCacheLocation), "openminemods")

    exc = "----------\nSTACKTRACE\n----------\n" + "\n".join(format_tb(traceback))

    sys_info = "----------\nSYSTEM INFORMATION\n----------"
    sys_info += "\nPlatform: {}".format(platform())
    sys_info += "\nOpenMineMods Version: {}".format(CurseAPI.version)
    sys_info += "\nData Location: {}".format(data_dir)
    sys_info += "\nCache Location: {}".format(cache_dir)

    settings = "----------\nSETTINGS\n----------\n"
    try:
        settings += open(path.join(data_dir, "settings.ini")).read()
    except FileNotFoundError:
        settings += "(Unable to read)"

    ErrorDialog(censor_string("{}\n{}\n{}".format(sys_info, exc, settings)))
