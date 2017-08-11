class MultiMC:
    """Class for managing MultiMC instances"""
    def __init__(self):
        pass

class InstanceCfg:
    """MultiMC instance config"""
    def __init__(self, mcver: str, name: str, notes=""):
        self.InstanceType = "OneSix"
        self.IntendedVersion = mcver
        self.OverrideCommands = False
        self.OverrideConsole = False
        self.OverrideJavaArgs = False
        self.OverrideJavaLocation = False
        self.OverrideMemory = False
        self.OverrideWindow = False
        self.iconKey = "default"
        self.name = name
        self.notes = notes

    def write(self, path: str):
        with open(path, 'w+') as file:
            for i in self.__dict__:
                v = self.__dict__[i]
                if type(v) == bool:
                    file.write(i+"="+["false", "true"][v]+"\n")
                if type(v) == str:
                    file.write(i+"="+v+"\n")