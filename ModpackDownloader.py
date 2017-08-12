from CurseAPI import CurseAPI, CurseModpack
from sys import exit

motd = """
  _|_|    _|      _|  _|      _|  
_|    _|  _|_|  _|_|  _|_|  _|_|  
_|    _|  _|  _|  _|  _|  _|  _|  
_|    _|  _|      _|  _|      _|  
  _|_|    _|      _|  _|      _|  

        OpenMineMods V0.1
"""

disclaimer = """
THIS SOFTWARE IS PROVIDED "AS IS" WITH NO WARRANTY, EXPRESS OR IMPLIED
This is a ALPHA version, there might still be issues.
Please run `tests.py` and send `output.json` to the author.
"""

curse = CurseAPI()

print(motd)
print(disclaimer)

print("Enter a search term!")
print("q to quit")
term = input(">>> ")

if term.lower() == "q":
    print("Goodbye!")
    exit(0)

packs = curse.search(term, stype=CurseAPI.search_types["modpack"])

if len(packs) < 1:
    print("No packs found for search term!")
    exit(0)

print("Found {} modpacks".format(len(packs)))
for i, pack in enumerate(packs):
    print("{}) \"{}\" - By {}".format(i+1, pack.name, pack.author))

print("Select a pack to download")
print("q to quit")

pack = input(">>> ")

if pack == "q":
    print("Goodbye!")
    exit(0)

try:
    pack = int(pack)-1
    selected = packs[pack].get_further_details()
except:
    print("Invalid pack selected!")
    print("Goodbye!")
    exit(0)

print("{} - Created on {}".format(selected.title, selected.created))
print("Minecraft {}".format(selected.latestVersion))
print("Last updated: {}".format(selected.updated))
print("Likes: {}".format(selected.likes))
print("Downloads: {}".format(selected.total))
print("Download this pack? [Y/n]")

inp = input(">>> ").lower()

if inp != "y":
    print("Goodbye!")
    exit(0)

modpack = CurseModpack(selected, curse)
print("Starting download of {}".format(modpack.availableFiles[0].name))
modpack.install(modpack.availableFiles[0])

print("Installation of {} complete!".format(selected.title))
print("You may need to reload MultiMC to see the instance")
