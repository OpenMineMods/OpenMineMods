import re
import shelve
import os

from json import dumps
from glob import glob
from os import remove, path, makedirs
from shutil import rmtree, move
from sys import setrecursionlimit
from hashlib import md5

from Utils.Utils import noop, moveTree

# Don't worry about it
setrecursionlimit(8096)


class MultiMC:
    """Class for managing MultiMC instances"""
    def __init__(self, fpath: str, db=False):
        self.path = fpath

        if not db:
            self.metaDb = shelve.open("{}/meta.db".format(self.path))
        else:
            self.metaDb = db

        cfgFiles = [i.replace("instance.cfg", '')[:-1] for i in glob("{}/instances/*/instance.cfg".format(self.path))]
        self.instances = [MultiMCInstance(i, self.metaDb) for i in cfgFiles]

        self.instanceMap = dict()

        for instance in self.instances:
            self.instanceMap[instance.uuid] = instance

    def delete_instance(self, instance):
        if instance.uuid in self.metaDb:
            del self.metaDb[instance.uuid]

        del self.instanceMap[instance.uuid]
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


class InstalledMod:
    """Information about a mod"""
    def __init__(self, projectid: str, file, manual: bool, location: str):
        self.file = file
        self.proj = projectid
        self.location = location
        self.manual = manual
        self.enabled = True

    def set_enabled(self, enabled: bool):
        # TODO: Less hacky solution
        if enabled != self.enabled:
            if enabled:
                newLoc = self.location[:-9]
                move(self.location, newLoc)
                self.enabled = True
                return
            newLoc = self.location + ".disabled"
            move(self.location, newLoc)
            self.enabled = False


class MultiMCInstance:
    """MultiMC Instance"""
    def __init__(self, path: str, db: shelve):
        self.path = path
        self.db = db
        self.instanceCfg = open("{}/instance.cfg".format(self.path)).read()
        self.modDir = "{}/minecraft/mods".format(self.path)
        if os.name == "nt":
            self.path = self.path.replace("/", "\\")
            self.uuid = md5((self.path+"\\").encode()).hexdigest()
        else:
            self.uuid = md5((self.path+"/").encode()).hexdigest()

        if self.uuid in self.db:
            self.mods = self.db[self.uuid]["mods"]
            self.pack = self.db[self.uuid]["pack"]
            self.file = self.db[self.uuid]["file"]
        else:
            self.mods = list()
            self.pack = None
            self.file = None
            self._save()

        self.name = re.search("name=(.*)", self.instanceCfg).groups(1)[0]
        self.version = re.search("IntendedVersion=(.*)\n", self.instanceCfg).group(1)

    def install_mod(self, projectid: str, file, curse, manual=False, progress=False):
        if not path.exists(self.modDir):
            makedirs(self.modDir)

        fname = curse.download_file(file.dl, self.modDir, progf=progress)
        file.filename = fname.split("/")[-1]
        mod = InstalledMod(projectid, file, manual, fname)
        self.mods.append(mod)
        self._save()

    def uninstall_mod(self, filename):
        fpath = "{}/minecraft/mods/{}".format(self.path, filename)
        if path.exists(fpath):
            remove(fpath)
        for x, mod in enumerate(self.mods):
            if mod.file.filename == filename:
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

    def update_mod(self, mod: InstalledMod, file, curse, progress=False):
        if mod not in self.mods:
            return False

        self.uninstall_mod(mod.file.filename)
        self.install_mod(mod.proj, file, curse, mod.manual, progress)

    def _save(self):
        self.db[self.uuid] = {"mods": self.mods, "pack": self.pack, "file": self.file}
