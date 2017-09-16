from requests import post
from getpass import getuser
from platform import system, release, processor
from threading import Thread

from Utils.Utils import getInstallDir

from API.CurseAPI import CurseAPI


def send_data(curse: CurseAPI):
    Thread(send_thread(curse)).start()


def send_thread(curse: CurseAPI):
    post("https://openminemods.digitalfishfun.com/analytics/installed",
         json={
             "uuid": curse.uuid,
             "ver": CurseAPI.version,
             "mmc": censor_string(curse.baseDir),
             "inst": censor_string(getInstallDir()),
             "sys": get_system()
         })


def censor_string(text: str):
    text = text.replace(getuser(), "{USER}")
    return text


def get_system():
    return "{} {} ({})".format(system(), release(), processor())
