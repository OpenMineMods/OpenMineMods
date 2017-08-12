from CurseAPI import CurseAPI, CurseModpack
from MultiMC import MultiMC
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

Note: As of now, `AddMod.py` doesn't check version compatibility.
Please be careful.
"""

curse = CurseAPI()

print(motd)
print(disclaimer)

mmc = MultiMC(curse.baseDir)

print("Found instances:")
for x, instance in enumerate(mmc.instances):
    print("{}) {} (Minecraft {})".format(x + 1, instance.name, instance.version))

print("Select an instance to add mods")
print("q to quit")

instance = input(">>> ")

if instance == "q":
    print("Goodbye!")
    exit(0)

try:
    instance = int(instance)-1
    instance = mmc.instances[instance]
except:
    print("Invalid pack selected!")
    print("Goodbye!")
    exit(0)

while True:
    print("Enter a search term!")
    print("q to quit")
    term = input(">>> ")

    if term.lower() == "q":
        print("Goodbye!")
        exit(0)

    mods = curse.search(term)

    if len(mods) < 1:
        print("No mods found for search term!")
        continue

    print("Found {} mods".format(len(mods)))
    for i, mod in enumerate(mods):
        print("{}) \"{}\" - By {}".format(i+1, mod.name, mod.author))

    print("Select a mod to install")
    print("c to cancel")

    mod = input(">>> ")

    if mod == "c":
        continue

    try:
        mod = int(mod)-1
        mod = mods[mod].get_further_details()
    except:
        print("Invalid mod selected!")
        continue

    print("Getting files for {}".format(mod.title))
    files = curse.get_files(mod.id)

    if len(files) < 1:
        print("No files found for mod!")
        continue

    print("Found {} files".format(len(files)))
    for i, file in enumerate(files):
        print("{}) {} (Minecraft {}) [{} MB] {{{}}}".format(i + 1, file.name, file.version, file.size, file.releaseType))

    print("Select a file to install")
    print("c to cancel")

    file = input(">>> ")

    if file == "c":
        continue

    try:
        file = int(file) - 1
        file = files[file]
    except:
        print("Invalid file selected!")
        continue

    curse.download_file(file.host+file.url, "{}/minecraft/mods".format(instance.path))
    print("Mod installed!")


print("Goodbye!")
