from requests import post
from getpass import getuser
from os import path
from platform import system, release, processor

from API.CurseAPI import CurseAPI


def send_data(curse: CurseAPI):
    post("https://digitalfishfun.com/openminemod_analytics/installed",
         json={
             "uuid": curse.uuid,
             "ver": CurseAPI.version,
             "mmc": censor_string(curse.baseDir),
             "inst": censor_string(path.dirname(path.realpath(__file__))),
             "sys": get_system()
         })


def censor_string(text: str):
    text = text.replace(getuser(), "{USER}")
    return text


def get_system():
    return "{} {} ({})".format(system(), release(), processor())
