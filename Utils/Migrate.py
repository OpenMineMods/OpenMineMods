def migrate(db):
    from API.MultiMC import InstalledMod
    from API.CurseAPI import JsonCurseFile

    for instance in db:
        if type(db[instance]) == list:
            newDb = list()
            doMigrate = False
            for mod in db[instance]:
                if type(mod) == JsonCurseFile:
                    newDb.append(InstalledMod(mod, False, mod.filename))
                    doMigrate = True
                else:
                    break
            if doMigrate:
                db[instance] = dict()
                db[instance]["mods"] = newDb
                db[instance]["pack"] = None
                print("Migrated instance {}".format(instance))
