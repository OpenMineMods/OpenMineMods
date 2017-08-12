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


@get("/browse-packs")
@view("packbrowse")
def modbrowse():
    packs = curse.get_modpacks()
    return {"version": CurseAPI.version, "packs": packs}


@get("/edit/<uuid>/add/<modid>")
def addmodd(uuid, modid):
    if uuid not in mmc.instanceMap:
        abort(404, "Instance Not Found")
    instance = mmc.instanceMap[uuid]
    files = [i for i in curse.get_files(modid)]
    if len(files) < 1:
        abort(404, "No file for {} found".format(instance.version))
    file = files[0]
    instance.install_mod(file, curse)
    redirect("/edit/{}?installed=1".format(instance.uuid))


@get("/edit/<uuid>/remove/<modid>")
def delmod(uuid, modid):
    if uuid not in mmc.instanceMap:
        abort(404, "Instance Not Found")
    instance = mmc.instanceMap[uuid]
    mod = False
    for imod in instance.mods:
        if imod.name == modid:
            mod = imod
    if not mod:
        abort(404, "Mod not found")
    instance.uninstall_mod(mod.filename)
    redirect("/edit/{}?removed=1".format(instance.uuid))

run(port=8096)