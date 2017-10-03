from os import path
from configparser import ConfigParser
from uuid import uuid4


class Setting:
    """Settings in format (Section, Key, Default)"""
    analytics = ("Settings", "Analytics", False)
    update = ("Settings", "AutoUpdate", True)
    ask_file = ("Settings", "AskFile", False)
    current_version = ("Settings", "CurrentVersion", "0.0")
    uuid = ("Settings", "UUID", str(uuid4()))
    live_search = ("Settings", "LiveSearch", False)
    meta_interval = ("Settings", "MetaInterval", 24)
    client_interval = ("Settings", "ClientInterval", 48)

    location = ("MultiMC", "Location", "")

    last_client = ("Timestamps", "LastClient", 0)
    last_meta = ("Timestamps", "LastMeta", 0)


class Config:
    def __init__(self, config_dir):
        settings = [i for i in Setting.__dict__.values() if type(i) == tuple]
        self.config_file = path.join(config_dir, "settings.ini")
        self.config = ConfigParser()
        if path.isfile(self.config_file):
            self.config.read(self.config_file)
        else:
            for setting in settings:
                self.write(setting, setting[2])
            self._save()

    def write(self, key: tuple, val):
        if not self.config.has_section(key[0]):
            self.config.add_section(key[0])
        self.config.set(key[0], key[1], str(val))
        self._save()

    def read(self, key: tuple):
        if not self.config.has_option(key[0], key[1]):
            self.config.set(key[0], key[1], str(key[2]))
        if type(key[2]) == bool:
            return {"True": True, "False": False}[self.config.get(key[0], key[1])]
        return type(key[2])(self.config.get(key[0], key[1]))

    def _save(self):
        with open(self.config_file, "w+") as f:
            self.config.write(f)

