from bottle import get, view, run, abort, static_file
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

run(port=8096)