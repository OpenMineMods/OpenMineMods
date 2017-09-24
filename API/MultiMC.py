import re

from json import dumps, loads
from glob import glob
from os import remove, path, makedirs
from shutil import rmtree, move
from sys import setrecursionlimit

from Utils.Utils import noop, moveTree

# Don't worry about it
setrecursionlimit(8096)


class MultiMC:
    """Class for managing MultiMC instances"""
    def __init__(self, fpath: str):
        self.path = fpath

        cfgFiles = [i.replace("instance.cfg", '')[:-1] for i in glob("{}/instances/*/instance.cfg".format(self.path))]
        self.instances = [MultiMCInstance(i) for i in cfgFiles]

    def delete_instance(self, instance):
        del self.instances[self.instances.index(instance)]

        rmtree(instance.path)


class InstanceCfg:
    """MultiMC instance config"""
    def __init__(self, mcver: str, forgever: str, name: str, notes="", icon="default"):
        self.ForgeVersion = forgever
        self.InstanceType = "OneSix"
        self.IntendedVersion = mcver
        self.OverrideCommands = False
        self.OverrideConsole = False
        self.OverrideJavaArgs = False
        self.OverrideJavaLocation = False
        self.OverrideMemory = False
        self.OverrideWindow = False
        self.iconKey = icon
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
            file.write("name="+self.name)


# TODO: Speak with MultiMC devs about a cleaner way to do this
class ForgePatch:
    """Very hacky net.minecraftforge.json generator"""
    def __init__(self, mcver: str, forgever: str):
        # Don't worry about it
        # Everything is fine
        self.dat = {"+libraries":[{"name":"","url":"http://files.minecraftforge.net/maven/"},{"name":"net.minecraft:launchwrapper:1.12"},{"name":"org.ow2.asm:asm-all:5.0.3"},{"name":"jline:jline:2.13","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"com.typesafe.akka:akka-actor_2.11:2.3.3","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"com.typesafe:config:1.2.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-actors-migration_2.11:1.1.0","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-compiler:2.11.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang.plugins:scala-continuations-library_2.11:1.0.2","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang.plugins:scala-continuations-plugin_2.11.1:1.0.2","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-library:2.11.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-parser-combinators_2.11:1.0.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-reflect:2.11.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-swing_2.11:1.0.1","url":"http://files.minecraftforge.net/maven/"},{"MMC-hint":"forge-pack-xz","name":"org.scala-lang:scala-xml_2.11:1.0.2","url":"http://files.minecraftforge.net/maven/"},{"name":"lzma:lzma:0.0.1"},{"name":"net.sf.jopt-simple:jopt-simple:4.6"},{"name":"java3d:vecmath:1.5.2"},{"name":"net.sf.trove4j:trove4j:3.0.3"}],"+tweakers":["net.minecraftforge.fml.common.launcher.FMLTweaker"],"fileId":"net.minecraftforge","mainClass":"net.minecraft.launchwrapper.Launch","mcVersion":mcver,"name":"Forge","order":5,"version":""}

        # I SAID DON'T WORRY ABOUT IT
        if mcver[:3] == "1.7":
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


class MultiMCInstance:
    """MultiMC Instance"""
    def __init__(self, ipath: str, new=False):
        self.path = ipath
        if new:
            inst = InstanceCfg(new["forgever"], new["instancever"], new["name"])
            makedirs(self.path)
            inst.write(path.join(self.path, "instance.cfg"))
            patch = ForgePatch(new["mcver"], new["instancever"])
            patchdir = path.join(self.path, "patches")
            makedirs(patchdir)
            patch.write(path.join(patchdir, "net.minecraftforge.json"))

            makedirs(path.join(self.path, "minecraft"))
            makedirs(path.join(self.path, "minecraft/mods"))

        self.instanceCfg = open("{}/instance.cfg".format(self.path)).read()
        self.modDir = "{}/minecraft/mods".format(self.path)

        self.dat_file = path.join(self.path, "omm_dat.json")
        if not path.isfile(self.dat_file):
            self.dat = {
                "file": False,
                "mods": []
            }
            self.mods = []
            self._save()
        else:
            self.dat = loads(open(self.dat_file).read())

        self.mods = self.dat["mods"]
        self.file = self.dat["file"]

        self.name = re.search("name=(.*)", self.instanceCfg).groups(1)[0]
        self.version = re.search("IntendedVersion=(.*)\n", self.instanceCfg).group(1)
        try:
            self.forge = re.search("ForgeVersion=(.*)\n", self.instanceCfg).group(1)
        except AttributeError:
            self.forge = ""

    def install_mod(self, file, curse, progress=False):
        if not path.exists(self.modDir):
            makedirs(self.modDir)

        fname = curse.download_file(file.dl, self.modDir, progf=progress)
        self.mods.append({"id": file.id, "path": fname, "manual": True})
        self._save()

    def uninstall_mod(self, fpath):
        if path.exists(fpath):
            remove(fpath)
        for x, mod in enumerate(self.mods):
            if mod["path"] == fpath:
                del self.mods[x]
                break
        self._save()

    def update(self, file):
        if self.pack is None:
            return False
        for mod in self.mods:
            if not mod.manual:
                self.uninstall_mod(mod.location)
        move(self.path, self.path + ".preupdate")
        self.pack.install(file, noop, noop, noop)
        moveTree(self.path, self.path + ".preupdate")
        move(self.path + ".preupdate", self.path)

    def _save(self):
        self.dat["mods"] = self.mods
        open(self.dat_file, 'w+').write(dumps(self.dat, indent=4))
