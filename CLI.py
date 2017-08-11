from CurseAPI import CurseAPI

motd = """
  _|_|    _|      _|  _|      _|  
_|    _|  _|_|  _|_|  _|_|  _|_|  
_|    _|  _|  _|  _|  _|  _|  _|  
_|    _|  _|      _|  _|      _|  
  _|_|    _|      _|  _|      _|  

        OpenMineMods V1.0
"""

help = """
Commands:
?: Show this message
q: Quit OpenMineMods
b: Browse Mods
"""

curse = CurseAPI()


def show_help(args: list):
    print(help)

def browse_mods(args: list):
    mods = curse.get_mod_list()
    for i in mods:
        print("{} ({})".format(i.title, i.latestVersion))

def parse_cmd(inp: str):
    args = inp.split(" ")
    cmd = args.pop(0)

    if cmd == "?":
        show_help(args)

    if cmd == "b":
        browse_mods(args)

print(motd)

print("? for help, q to quit")

while 1:
    inp = str(input("[OMM] >>> ")).lower()

    if inp == "q":
        break

    parse_cmd(inp)


print("Goodbye!")
