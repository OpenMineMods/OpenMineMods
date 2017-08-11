from CurseAPI import CurseAPI, CurseModpack
from traceback import format_exc
from json import dumps
from os import remove

results = {
    "multimc_folder": {},
    "version_list": {},
    "mod_list": {},
    "mod_files": {},
    "modpack_list": {},
    "modpack_data": {},
    "modpack_install": {},
    "mod_search": {},
    "mod_download": {}
}

print("Testing MultiMC folder detection")
curse = CurseAPI()
results["multimc_folder"]["show"] = bool(curse.baseDir)
results["multimc_folder"]["err"] = curse.baseDir

print("Testing version listing")
try:
    vers = curse.get_version_list()
    results["version_list"]["show"] = len(vers) > 0
except:
    results["version_list"]["err"] = format_exc()
    results["version_list"]["show"] = False

print("Testing mod listing")
try:
    mods = curse.get_mod_list()
    results["mod_list"]["show"] = len(mods) > 0
except:
    results["mod_list"]["err"] = format_exc()
    results["mod_list"]["show"] = False

print("Testing mod files")
try:
    files = curse.get_files(mods[0].id)
    results["mod_files"]["show"] = len(files) > 0
except:
    results["mod_files"]["err"] = format_exc()
    results["mod_files"]["show"] = False

print("Testing modpack listing")
try:
    packs = curse.get_modpacks()
    results["modpack_list"]["show"] = len(packs) > 0
except:
    results["modpack_list"]["err"] = format_exc()
    results["modpack_list"]["show"] = False

print("Testing modpack data")
try:
    pack = CurseModpack(packs[0], curse)
    results["modpack_data"]["show"] = True
except:
    results["modpack_data"]["err"] = format_exc()
    results["modpack_data"]["show"] = False

print("Testing modpack installation")
try:
    pack.install(pack.availableFiles[0])
    results["modpack_install"]["show"] = True
except:
    results["modpack_install"]["err"] = format_exc()
    results["modpack_install"]["show"] = False

print("Testing mod search")
try:
    res = curse.search("mekanism")
    results["mod_search"]["show"] = res[0].name == "Mekanism"
except:
    results["mod_search"]["err"] = format_exc()
    results["mod_search"]["show"] = False

print("Testing mod downloading")
try:
    downloadedFile = curse.download_file(files[0].host+files[0].url, ".")
    results["mod_download"]["show"] = True
    remove(downloadedFile)
except:
    results["mod_download"]["err"] = format_exc()
    results["mod_download"]["show"] = False

print("\n{} out of {} passed\n".format(len([i for i in results if results[i]["show"]]), len(results.keys())))

for i in results:
    print("{}: {}".format(i, ["Fail", "Pass"][results[i]["show"]]))

open("results.json", 'w+').write(dumps(results, indent=4))
print("Written results to `results.json`")
