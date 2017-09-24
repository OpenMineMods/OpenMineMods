import requests
import os

from bs4 import BeautifulSoup
from datetime import datetime
from zipfile import ZipFile
from json import loads
from pathlib import Path
from urllib.parse import unquote
from sys import stdout
from API.MultiMC import InstanceCfg, ForgePatch
from shutil import move, copytree, rmtree
from hashlib import md5

from GUI.Strings import Strings
from CurseMetaDB.DB import DB

useUserAgent = "Mozilla/5.0 (Windows NT 10.0; rv:50.0) Gecko/20100101 Firefox/50.0"

strings = Strings()
translate = strings.get


class CurseAPI:
    """Curse API"""

    motd = """
          _|_|    _|      _|  _|      _|
        _|    _|  _|_|  _|_|  _|_|  _|_|
        _|    _|  _|  _|  _|  _|  _|  _|
        _|    _|  _|      _|  _|      _|
          _|_|    _|      _|  _|      _|
    """

    version = "1.1.0"
    baseUrl = "https://mods.curse.com"
    forgeUrl = "https://minecraft.curseforge.com"

    def __init__(self, db: DB):
        self.db = db

        # Set User Agent header for extra sneakyness
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": useUserAgent})

    # SECTION MODS

    def get_mod_list(self, version="*"):
        """Get an array of `CurseProject`s"""
        mods = self.db.get_popular("mod", 100, version)
        return [self.get_project(i) for i in mods]

    def get_project(self, pid: int):
        mod = self.db.get_project(pid)
        if not mod:
            return False
        return CurseProject(mod)

    # END SECTION

    # SECTION MODPACKS

    def get_modpacks(self, version="*"):
        packs = self.db.get_popular("modpack", 25, version)
        return [CurseProject(self.db.get_project(i)) for i in packs]

    # END SECTION

    # SECTION UTILS

    def search(self, query: str, ptype="mod", version="*"):
        res = self.db.search_projects(query, ptype, 25, version=version)
        return [CurseProject(i) for i in res]

    def download_file(self, url: str, filepath: str, fname="", progf=False):
        """Download a file from `url` to `filepath/name`"""
        r = self.session.get(url, stream=True)
        dlen = r.headers.get("content-length")
        step = (100 / int(dlen))
        prog = 0
        if not fname:
            fname = unquote(Path(r.url).name)
        with open(filepath+"/"+fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    prog += len(chunk)
                    if progf:
                        progf(int(step * prog))
                    f.write(chunk)
        if progf:
            progf(0)
        return filepath+"/"+fname

    def get(self, params={}, path="", host="", includeUrl=False):
        """HTTP GET with HTML parsing"""
        if not host:
            host = self.baseUrl
        r = self.session.get(host + path, params=params)
        html = r.text
        if includeUrl:
            return [BeautifulSoup(html, "html.parser"), r.url]
        return BeautifulSoup(html, "html.parser")

    # END SECTION


class CurseProject:
    def __init__(self, meta: dict):
        self.meta = meta

        self.type = self.meta["type"]

        self.name = self.meta["title"]
        self.author = self.meta["primaryAuthor"]
        self.desc = self.meta["desc"]

        self.page = self.meta["site"]

        self.versions = self.meta["versions"]


class CurseFile:
    def __init__(self, f: dict):
        self.f = f

        self.id = self.f["Id"]
        self.pub_time = datetime.strptime(self.f["FileDate"], "%Y-%m-%dT%H:%M:%S")
        self.mc_ver = self.f["GameVersion"][0]

        self.deps = self.f["Dependencies"]

        self.dl = self.f["DownloadURL"]

        self.filename = self.f["FileNameOnDisk"]

        if "_Project" in self.f:
            self.name = self.f["_Project"]["Name"]
            self.desc = self.f["_Project"]["Summary"]
        else:
            self.name = self.filename
            self.desc = ""


class CurseModpack:
    """Get information from a modpack"""

    from API.MultiMC import MultiMC

    def __init__(self, project: CurseProject, curse: CurseAPI, mmc: MultiMC):
        self.project = project
        self.curse = curse

        self.installed = False

        if os.name == "nt":
            self.installLocation = "{}\\instances\\{}\\".format(self.curse.baseDir, self.project.name)
        else:
            self.installLocation = "{}/instances/{}/".format(self.curse.baseDir, self.project.name)

        self.uuid = md5(self.installLocation.encode()).hexdigest()

        self.mmc = mmc

    def install(self, file: CurseFile, prog_label, progbar_1, progbar_2):

        from API.MultiMC import InstalledMod

        tempPath = "{}/instances/_MMC_TEMP/{}".format(self.curse.baseDir, self.project.name)

        progbar_1(0)

        prog_label(translate("downloading.icon"))

        self.curse.download_file(self.project.icon, "{}/icons".format(self.curse.baseDir),
                                 str(self.project.id)+".png", progf=progbar_2)

        if os.path.exists(tempPath) and self.curse.baseDir:
            rmtree(tempPath)

        # Create instance temp folder if doesn't exist
        if not os.path.exists(tempPath):
            os.makedirs(tempPath)

        progbar_1(5)

        prog_label(translate("downloading.data"))

        packFile = self.curse.download_file(file.dl, tempPath, progf=progbar_2)

        # Unpack zip file
        zipf = ZipFile(packFile)
        zipf.extractall("{}/raw".format(tempPath))
        zipf.close()

        # Delete ZIP file
        os.remove(packFile)

        # Parse Manifest
        manifest = ModpackManifest("{}/raw/manifest.json".format(tempPath))

        # Overrides
        mcPath = "{}/minecraft".format(tempPath)
        if os.path.exists("{}/raw/overrides".format(tempPath)):
            copytree("{}/raw/overrides".format(tempPath), mcPath)

        # Make mods folder
        modPath = "{}/mods".format(mcPath)
        if not os.path.exists(modPath):
            os.makedirs(modPath)

        # Make Patches Folder
        patchPath = "{}/patches".format(tempPath)
        if not os.path.exists(patchPath):
            os.makedirs(patchPath)

        # Configure Instance
        instanceCfg = InstanceCfg(manifest.mcVersion, manifest.forgeVersion, self.project.title,
                                  icon=str(self.project.id))
        instanceCfg.write("{}/instance.cfg".format(tempPath))

        # Configure Forge
        forgeCfg = ForgePatch(manifest.mcVersion, manifest.forgeVersion)
        forgeCfg.write(patchPath+"/net.minecraftforge.json")

        modlist = list()

        progbar_1(10)

        modf = (90 / len(manifest.mods))

        for x, mod in enumerate(manifest.mods):
            stdout.write("\rDownloading mod {}/{}".format(x+1, len(manifest.mods)))
            r = self.curse.get_json("/{}/{}.json".format(mod[0], mod[1]))

            f = CurseFile(r)

            prog_label(translate("downloading.mod").format(f.name))
            progbar_1(10 + (x * modf))
            self.curse.download_file(r["DownloadURL"], modPath, progf=progbar_2)
            modlist.append(InstalledMod(mod[0], f, False, modPath))
        stdout.write("\n\r")

        if self.uuid in self.mmc.metaDb:
            tmp = self.mmc.metaDb[self.uuid]
            tmp["mods"] += modlist
            tmp["pack"] = self.project
            self.mmc.metaDb[self.uuid] = tmp
        else:
            self.mmc.metaDb[self.uuid] = {"mods": modlist, "pack": self.project, "file": file}

        newPath = "{}/instances/{}".format(self.curse.baseDir, self.project.title)

        rmtree("{}/raw/overrides".format(tempPath))

        if os.path.exists(newPath) and self.curse.baseDir:
            rmtree(newPath)
        move(tempPath, "{}/instances".format(self.curse.baseDir))


class ModpackManifest:
    """Parse a modpack's manifest.json"""
    def __init__(self, filename: str):
        self.filename = filename

        self.json = loads(open(self.filename).read())

        self.mcVersion = self.json["minecraft"]["version"]
        self.forgeVersion = self.json["minecraft"]["modLoaders"][0]["id"].replace("forge-", '')

        self.mods = [[i["projectID"], i["fileID"]] for i in self.json["files"]]


class SearchType:
    Mod = "mc-mods"
    Modpack = "modpacks"
    Texturepack = "customiaztion"
