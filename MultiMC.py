import re
import shelve
import os

from json import dumps
from glob import glob
from os import remove, path, makedirs
from shutil import rmtree
from sys import setrecursionlimit
from hashlib import md5

# Don't worry about it
setrecursionlimit(8096)


class MultiMC:
    """Class for managing MultiMC instances"""
    def __init__(self, fpath: str):
        self.path = fpath

        self.metaDb = shelve.open("{}/meta.db".format(self.path))

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
            self.mods = self.db[self.uuid]
        else:
            self.mods = list()

        self.name = re.search("name=(.*)", self.instanceCfg).groups(1)[0]
        self.version = re.search("IntendedVersion=(.*)\n", self.instanceCfg).group(1)

    def install_mod(self, file, curse):

        if not path.exists(self.modDir):
            makedirs(self.modDir)

        fname = curse.download_file(file.host + file.url, self.modDir)
        fname = fname.split("/")[-1]
        file.filename = fname
        self.mods.append(file)
        self.db[self.uuid] = self.mods

    def uninstall_mod(self, filename):
        remove("{}/minecraft/mods/{}".format(self.path, filename))
        for x, mod in enumerate(self.mods):
            if mod.filename == filename:
                del self.mods[x]
                break
        self.db[self.uuid] = self.mods
