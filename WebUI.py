from bottle import get, view, run, abort, static_file, redirect
from CurseAPI import CurseAPI
from MultiMC import MultiMC

curse = CurseAPI()

mmc = MultiMC(curse.baseDir)


@get("/static/:filename")
def serve_static(filename):
    return static_file(filename, root="static")


@get("/")
@view("index")
def index():
    return {"name": "OpenMineMods", "version": CurseAPI.version, "packs": mmc.instances}


@get("/edit/<uuid>")
@view("edit")
def edit(uuid):
    if uuid not in mmc.instanceMap:
        abort(404, "Instance Not Found")
    return {"version": CurseAPI.version, "instance": mmc.instanceMap[uuid]}


@get("/edit/<uuid>/browse-mods")
@view("modbrowse")
def modbrowse(uuid):
    if uuid not in mmc.instanceMap:
        abort(404, "Instance Not Found")
    instance = mmc.instanceMap[uuid]
    mods = curse.get_mod_list(instance.version)
    return {"version": CurseAPI.version, "instance": mmc.instanceMap[uuid], "mods": mods}

@get("/edit/<uuid>/add/<modid>")
def addmodd(uuid, modid):
    if uuid not in mmc.instanceMap:
        abort(404, "Instance Not Found")
    instance = mmc.instanceMap[uuid]
    files = [i for i in curse.get_files(modid) if i.version == instance.version]
    if len(files) < 1:
        abort(404, "No file for {} found".format(instance.version))
    file = files[0]
    curse.download_file(file.host + file.url, "{}/minecraft/mods".format(instance.path))
    instance.install_mod(file)
    redirect("/edit/{}".format(instance.uuid))

run(port=8096)