from PyQt5.QtCore import QStandardPaths

from API.CurseAPI import CurseAPI

from traceback import format_tb
from platform import platform
from locale import getdefaultlocale
from os import path
from time import time

from GUI.ErrorDialogWrapper import ErrorDialog

from Utils.Config import Config, Setting
from Utils.Analytics import censor_string


def handle_exception(etype, val, traceback):
    data_dir = path.join(QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation), "openminemods")
    cache_dir = path.join(QStandardPaths.writableLocation(QStandardPaths.GenericCacheLocation), "openminemods")

    exc = "----------\nSTACKTRACE\n----------"
    exc += "\n{}: {}".format(etype.__name__, val)
    exc += "\n\n{}".format("\n".join(format_tb(traceback)))

    sys_info = "----------\nSYSTEM INFORMATION\n----------"
    sys_info += "\nPlatform: {}".format(platform())
    sys_info += "\nOpenMineMods Version: {}".format(CurseAPI.version)
    sys_info += "\nLocale: {}".format(getdefaultlocale())
    sys_info += "\nData Location: {}".format(data_dir)
    sys_info += "\nCache Location: {}".format(cache_dir)
    sys_info += "\nTime: {}".format(int(time()))

    settings = "----------\nSETTINGS\n----------\n"
    try:
        settings += open(path.join(data_dir, "settings.ini")).read()
        conf = Config(data_dir)
    except FileNotFoundError:
        settings += "(Unable to read)"
        conf = False

    mmc = "----------\nMULTIMC INFO\n----------\n"
    if conf and conf.read(Setting.location):
        mmc += "\nInstall Folder: {}".format(conf.read(Setting.location))
    else:
        mmc += "Unable to find"

    ErrorDialog(censor_string("{}\n{}\n{}".format(sys_info, exc, settings)))
