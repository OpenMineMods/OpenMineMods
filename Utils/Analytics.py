from requests import post
from getpass import getuser
from platform import system, release, processor
from threading import Thread

from Utils.Utils import getInstallDir
from Utils.Config import Config, Setting

from API.CurseAPI import CurseAPI


def send_data(conf: Config):
    Thread(send_thread(conf)).start()


def send_thread(conf: Config):
    post("https://openminemods.digitalfishfun.com/analytics/installed",
         json={
             "uuid": conf.read(Setting.uuid),
             "ver": CurseAPI.version,
             "mmc": censor_string(conf.read(Setting.location)),
             "inst": censor_string(getInstallDir()),
             "sys": get_system()
         })


def censor_string(text: str):
    text = text.replace(getuser(), "{USER}")
    return text


def get_system():
    return "{} {} ({})".format(system(), release(), processor())
