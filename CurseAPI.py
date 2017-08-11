import requests


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

    # SECTION MODS
    def get_mod_list(self, version="", page=0):
        """Get an array of `CurseProject`s"""
        parsed = self.get(params={
            "filter-project-game-version": version,
            "page": page
        })
        projects = parsed.body.find_all("ul", attrs={"class": "project-listing"})[1]
        projects = [CurseProject(i) for i in projects.select("li > ul")]
        return projects

    def get_files(self, pid):
        """Get an array of `CurseFile`s from a project ID"""
        parsed = self.get(path="/projects/{}/files".format(pid), host=self.forgeUrl)
        return [CurseFile(i) for i in parsed.select(".project-file-list-item")]

    def get_version_list(self):
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

    # END SECTION

    # SECTION UTILS

    def download_file(self, url, filepath):
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

        self.title = self.get_content("h4 > a")
        self.id = self.el.select("h4 > a")[0]["href"].split("/")[-1].split("-")[0]

        self.updated = self.get_content(".updated")[8:]
        self.created = self.get_content(".updated", 1)[8:]

        self.monthly = int(self.get_content(".average-downloads")[:-8].replace(',', ''))
        self.total = int(self.get_content(".download-total")[:-6].replace(',', ''))

        self.likes = int(self.get_content(".grats")[:-6].replace(',', ''))

        self.latestVersion = self.get_content(".version")[10:]

    def get_content(self, selector, index=0):
        return self.el.select(selector)[index].contents[0]


class CurseFile:
    """Class for getting information from a file element"""
    def __init__(self, element):
        self.el = element

        self.name = self.get_content(".project-file-name-container > a")

        self.releaseType = self.get_tag(".project-file-release-type > div", "title")
        self.uploaded = self.get_content(".standard-datetime")

        self.url = self.get_tag(".fa-icon-download", "href")
        self.size = float(self.get_content(".project-file-size")[14:-13])

        self.version = self.get_content(".version-label")

        self.downloads = int(self.get_content(".project-file-downloads")[14:-10].replace(',', ''))

    def get_tag(self, selector, tag, index=0):
        return self.el.select(selector)[index][tag]

    def get_content(self, selector, index=0):
        return self.el.select(selector)[index].contents[0]