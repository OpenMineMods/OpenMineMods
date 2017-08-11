from json import dumps


class MultiMC:
    """Class for managing MultiMC instances"""
    def __init__(self, path: str):
        self.path = path


class InstanceCfg:
    """MultiMC instance config"""
    def __init__(self, mcver: str, forgever: str, name: str, notes=""):
        self.ForgeVersion = forgever
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


# TODO: Speak with MultiMC devs about a cleaner way to do this
class ForgePatch:
    """Very hacky net.minecraftforge.json generator"""
    def __init__(self, mcver: str, forgever: str):
        # Don't worry about it
        # Everything is fine
        self.dat = {"+libraries":[{"name":"","url":"http://files.minecraftforge.net/maven/"},{"name":"net.minecraft:launchwrapper:1.12"},{"name":"org.ow2.asm:asm-all:5.0.3"},{"name":"jline:jline:2.13","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"com.typesafe.akka:akka-actor_2.11:2.3.3","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"com.typesafe:config:1.2.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-actors-migration_2.11:1.1.0","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-compiler:2.11.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang.plugins:scala-continuations-library_2.11:1.0.2","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang.plugins:scala-continuations-plugin_2.11.1:1.0.2","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-library:2.11.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-parser-combinators_2.11:1.0.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-reflect:2.11.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-swing_2.11:1.0.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-xml_2.11:1.0.2","url":"http://files.minecraftforge.net/maven/"},{"name":"lzma:lzma:0.0.1"},{"name":"net.sf.jopt-simple:jopt-simple:4.6"},{"name":"java3d:vecmath:1.5.2"},{"name":"net.sf.trove4j:trove4j:3.0.3"}],"+tweakers":["net.minecraftforge.fml.common.launcher.FMLTweaker"],"fileId":"net.minecraftforge","mainClass":"net.minecraft.launchwrapper.Launch","mcVersion":mcver,"name":"Forge","order":5,"version":""}

        # I SAID DON'T WORRY ABOUT IT
        if (mcver[:3] == "1.7"):
            self.dat["+libraries"][0]["name"] = "net.minecraftforge:forge:{0}-{1}-{0}:universal".format(mcver, forgever)
            self.dat["version"] = "{}-{}".format(forgever, mcver)
            self.dat["assets"] = mcver
        else:
            self.dat["+libraries"][0]["name"] = "net.minecraftforge:forge:{}-{}:universal".format(mcver, forgever)
            self.dat["version"] = "{}-{}".format(mcver, forgever)
        # EVERYTHING IS FINE. THIS IS FINE!!!

    def write(self, path: str):
        with open(path, 'w+') as file:
            file.write(dumps(self.dat))
