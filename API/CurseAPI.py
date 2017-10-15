import requests
import os

from bs4 import BeautifulSoup
from zipfile import ZipFile
from json import loads, dumps
from pathlib import Path
from urllib.parse import unquote
from sys import stdout
from API.MultiMC import InstanceCfg, ForgePatch
from shutil import copytree, rmtree

from Utils.Utils import moveTree
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

    version = "2.1.5"
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
        mods = self.db.get_popular("mod", 25, version)
        return [self.get_project(i) for i in mods]

    def get_project(self, pid: int):
        mod = self.db.get_project(pid)
        if not mod:
            return False
        return CurseProject(mod)

    def get_file(self, fid: int):
        file = self.db.get_file(fid)
        if not file:
            return False
        return CurseFile(file)

    # END SECTION

    # SECTION MODPACKS

    def get_modpacks(self, version="*"):
        packs = self.db.search_projects("", "modpack", version=version)
        return [CurseProject(i) for i in packs]

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
        with open(filepath + "/" + fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    prog += len(chunk)
                    if progf:
                        progf(int(step * prog))
                    f.write(chunk)
        if progf:
            progf(0)
        return filepath + "/" + fname

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

        self.id = self.meta["id"]

        self.type = self.meta["type"]

        self.name = self.meta["title"]
        self.author = self.meta["primaryAuthor"]
        self.desc = self.meta["desc"]

        self.page = self.meta["site"]

        self.versions = self.meta["versions"]
        self.files = self.meta["files"]

        self.popularity = float(self.meta["popularity"])
        self.downloads = float(self.meta["downloads"])
        self.authors = self.meta["authors"]

        self.attachments = self.meta["attachments"]
        if len(self.attachments) > 0:
            self.default_attachment = [i for i in self.attachments if i["default"]][0]
        else:
            self.default_attachment = False

        if self.default_attachment:
            self.icon_url = self.default_attachment["url"]
            self.icon_name = "{}.{}".format(self.id, self.icon_url.split(".")[-1])
        else:
            self.icon_url = None
            self.icon_name = None

    def download_icon(self, api, dir):
        if self.icon_url is not None:
            extension = self.icon_url.split(".")[-1]
            file = "{}.{}".format(self.id, extension)
            full_path = os.path.join(dir, file)
            if not os.path.isfile(full_path):
                api.download_file(self.icon_url, dir,
                              file, progf=False)
            return full_path
        return None


class CurseFile:
    def __init__(self, f: dict):
        self.f = f

        self.id = self.f["id"]
        self.pub_time = self.f["date"]
        self.versions = self.f["versions"]

        self.deps = self.f["dependencies"]

        self.dl = self.f["url"]

        self.filename = self.f["filename"]
        self.project = self.f["project"]


class CurseModpack:
    """Get information from a modpack"""

    from API.MultiMC import MultiMC

    def __init__(self, project: CurseProject, curse: CurseAPI, mmc: MultiMC):
        self.project = project
        self.curse = curse
        self.mmc = mmc

        self.installed = False

        if os.name == "nt":
            self.installLocation = "{}\\instances\\{}\\".format(self.mmc.path, self.project.name)
        else:
            self.installLocation = "{}/instances/{}/".format(self.mmc.path, self.project.name)

        self.mmc = mmc

    def install(self, file: CurseFile, prog_label, progbar_1, progbar_2, is_update=False):
        if is_update:
            print("WARNING: UPDATING IS STILL EXPERIMENTAL")

        safe_name = self.project.name + ""
        for c in "\\/:*?\"<>|":
            safe_name = safe_name.replace(c, '')

        tempPath = "{}/instances/_MMC_TEMP/{}".format(self.mmc.path, safe_name)

        progbar_1(0)

        prog_label(translate("downloading.icon"))

        if os.path.exists(tempPath):
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
        else:
            os.makedirs(mcPath)

        # Make mods folder
        modPath = "{}/mods".format(mcPath)
        if not os.path.exists(modPath):
            os.makedirs(modPath)

        # Make Patches Folder
        patchPath = "{}/patches".format(tempPath)
        if not os.path.exists(patchPath):
            os.makedirs(patchPath)

        # Configure Instance
        instanceCfg = InstanceCfg(manifest.mcVersion, manifest.forgeVersion, self.project.name,
                                  icon=str(self.project.id))
        instanceCfg.write("{}/instance.cfg".format(tempPath))

        # Configure Forge
        forgeCfg = ForgePatch(manifest.mcVersion, manifest.forgeVersion)
        forgeCfg.write(patchPath + "/net.minecraftforge.json")

        modlist = list()

        progbar_1(10)

        modf = (90 / len(manifest.mods))

        newPath = "{}/instances/{}".format(self.mmc.path, safe_name)

        ignore_files = list()

        if not is_update:
            while os.path.exists(newPath):
                newPath += "_"
        else:
            from API.MultiMC import MultiMCInstance
            inst = MultiMCInstance(newPath)

            nmds = [i[1] for i in manifest.mods]
            npids = [i[0] for i in manifest.mods]

            for mod in inst.mods:
                if mod["id"] in nmds:
                    ignore_files.append(mod["id"])
                    modlist.append(mod)
                elif not mod["manual"] or self.curse.get_file(mod["id"]).project in npids:
                    inst.uninstall_mod(mod["path"])
                else:
                    modlist.append(mod)

        for x, mod in enumerate(manifest.mods):
            if mod[1] in ignore_files:
                continue
            # stdout.write("\rDownloading mod {}/{}".format(x+1, len(manifest.mods)))
            f = self.curse.get_file(mod[1])
            if not f:
                continue

            prog_label(translate("downloading.mod").format(f.filename))
            progbar_1(10 + (x * modf))
            mpath = self.curse.download_file(f.dl, modPath, progf=progbar_2)
            modlist.append({"id": mod[1], "path": mpath.replace(tempPath, newPath), "manual": False})
        stdout.write("\n\r")

        open("{}/omm_dat.json".format(tempPath), "w+").write(dumps({
            "file": file.id,
            "mods": modlist
        }, indent=4))

        rmtree("{}/raw".format(tempPath))

        if not os.path.exists(newPath):
            os.makedirs(newPath)
        moveTree(tempPath, newPath)
        if os.path.exists(tempPath):
            rmtree(tempPath)


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
