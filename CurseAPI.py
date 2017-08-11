import requests
import re

from bs4 import BeautifulSoup

useUserAgent = "Mozilla/5.0 (Windows NT 10.0; rv:50.0) Gecko/20100101 Firefox/50.0"

class CurseAPI:
    """Curse API"""
    def __init__(self):
        self.baseUrl = "https://mods.curse.com/mc-mods/minecraft"
        self.forgeUrl = "https://minecraft.curseforge.com"
        # Set User Agent header for extra sneakyness
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": useUserAgent})

    def getModList(self, version="", page=0):
        """Get an array of `CurseProject`s"""
        parsed = self.get(params = {
            "filter-project-game-version": version,
            "page": page
        })
        projects = parsed.body.find_all("ul", attrs = { "class": "project-listing" })[1]
        projects = [CurseProject(i) for i in projects.select("li > ul")]
        return projects

    def getFiles(self, pid):
        """Get an array of `CurseFile`s from a project ID"""
        parsed = self.get(path="/projects/{}/files".format(pid), host=self.forgeUrl)
        return [CurseFile(i) for i in parsed.select(".project-file-list-item")]

    def getVersionList(self):
        """Get all versions availible on Curse"""
        parsed = self.get()
        options = parsed.select("#filter-project-game-version > option")
        return [i["value"] for i in options if i["value"] != ""]

    def get(self, params={}, path="", host=False):
        """HTTP GET with HTML parsing"""
        if not host:
            host = self.baseUrl
        html = self.session.get(host+path, params=params).text
        return BeautifulSoup(html, "html.parser")

    def downloadFile(self, url, filepath):
        """Download a file from `url` to `filepath`"""
        r = self.session.get(url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

class CurseProject:
    """Class for getting project information"""
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
    """Class for getting information from a file element"""
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