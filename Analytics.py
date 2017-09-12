from requests import post
from getpass import getuser
from os import path

from CurseAPI import CurseAPI


def send_data(curse: CurseAPI):
    post("https://digitalfishfun.com/openminemod_analytics/installed",
         json={
             "uuid": curse.uuid,
             "ver": CurseAPI.version,
             "mmc": censor_string(curse.baseDir),
             "inst": censor_string(path.dirname(path.realpath(__file__)))
         })


def censor_string(text: str):
    text = text.replace(getuser(), "{USER}")
    return text
