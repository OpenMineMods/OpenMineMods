from bottle import get, view, run, abort
from CurseAPI import CurseAPI
from MultiMC import MultiMC

curse = CurseAPI()

mmc = MultiMC(curse.baseDir)


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

run(port=8096)