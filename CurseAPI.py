import requests
import re

from bs4 import BeautifulSoup

useUserAgent = "Mozilla/5.0 (Windows NT 10.0; rv:50.0) Gecko/20100101 Firefox/50.0"

class CurseAPI:
    def __init__(self):
        self.baseUrl = "https://mods.curse.com/mc-mods/minecraft"
        self.forgeUrl = "https://minecraft.curseforge.com/projects"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": useUserAgent})

    def getModList(self, version="", page=0):
        parsed = self.get(params = {
            "filter-project-game-version": version,
            "page": page
        })
        projects = parsed.body.find_all("ul", attrs = { "class": "project-listing" })[1]
        projects = [CurseProject(i) for i in projects.select("li > ul")]
        return projects

    def getFiles(self, pid):
        parsed = self.get(path="/{}/files".format(pid), host=self.forgeUrl)
        return [CurseFile(i) for i in parsed.select(".project-file-list-item")]

    def getVersionList(self):
        parsed = self.get()
        options = parsed.select("#filter-project-game-version > option")
        return [i["value"] for i in options if i["value"] != ""]

    def get(self, params={}, path="", host=False):
        if not host:
            host = self.baseUrl
        html = self.session.get(host+path, params=params).text
        return BeautifulSoup(html, "html.parser")

class CurseProject:
    def __init__(self, element):
        self.el = element

        self.title = self.getContent("h4 > a")
        self.id = self.el.select("h4 > a")[0]["href"].split("/")[-1].split("-")[0]

        self.updated = self.getContent(".updated")[8:]
        self.created = self.getContent(".updated", 1)[8:]

        self.monthly = int(self.getContent(".average-downloads")[:-8].replace(',', ''))
        self.total = int(self.getContent(".download-total")[:-6].replace(',', ''))

        self.likes = int(self.getContent(".grats")[:-6].replace(',', ''))

        self.latestVersion = self.getContent(".version")[10:]

    def getContent(self, selector, index=0):
        return self.el.select(selector)[index].contents[0]

class CurseFile:
    def __init__(self, element):
        self.el = element

        self.name = self.getContent(".project-file-name-container > a")

        self.releaseType = self.getThing(".project-file-release-type > div", "title")
        self.uploaded = self.getContent(".standard-datetime")

        self.url = self.getThing(".fa-icon-download", "href")
        self.size = float(self.getContent(".project-file-size")[14:-13])

        self.version = self.getContent(".version-label")

        self.downloads = int(self.getContent(".project-file-downloads")[14:-10].replace(',', ''))

    def getThing(self, selector, tag, index=0):
        return self.el.select(selector)[index][tag]

    def getContent(self, selector, index=0):
        return self.el.select(selector)[index].contents[0]

curse = CurseAPI()
