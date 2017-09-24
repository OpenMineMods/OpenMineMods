from os import path
from configparser import ConfigParser
from uuid import uuid4


class Config:
    def __init__(self, config_dir):
        self.config_file = path.join(config_dir, "settings.ini")
        self.config = ConfigParser()
        if path.isfile(self.config_file):
            self.config.read(self.config_file)
        else:
            self.config["Settings"] = {
                "Analytics": False,
                "AutoUpdate": True,
                "AskFile": False,
                "CurrentVersion": "0.0",
                "UUID": str(uuid4())
            }
            self.config["MultiMC"] = {
                "Location": ""
            }
            self._save()

    def write(self, key: tuple, val):
        self.config[key[0]][key[1]] = str(val)
        self._save()

    def read(self, key: tuple):
        if key[2] == bool:
            return {"True": True, "False": False}[self.config[key[0]][key[1]]]
        return key[2](self.config[key[0]][key[1]])

    def _save(self):
        with open(self.config_file, "w+") as f:
            self.config.write(f)


class Setting:
    analytics = ("Settings", "Analytics", bool)
    update = ("Settings", "AutoUpdate", bool)
    ask_file = ("Settings", "AskFile", bool)
    current_version = ("Settings", "CurrentVersion", str)
    uuid = ("Settings", "UUID", str)

    location = ("MultiMC", "Location", str)
