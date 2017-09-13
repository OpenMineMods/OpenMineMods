from requests import post
from getpass import getuser
from platform import system, release, processor

from Utils.Utils import getInstallDir

from API.CurseAPI import CurseAPI


def send_data(curse: CurseAPI):
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
