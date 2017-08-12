from bottle import get, post, run, request, response, template
from CurseAPI import CurseAPI
from MultiMC import MultiMC

curse = CurseAPI()

while not curse.baseDir:
    print("MultiMC folder not found!")
    print("Please enter your MultiMC folder.")
    curse.baseDir = input(">>> ")
    print("To avoid this in the future, please send your MultiMC folder location to the developers!")

mmc = MultiMC(curse.baseDir)

@get("/")
def index():
    return template("<b>Hello, {{world}}!", world="World")

run(port=8096)