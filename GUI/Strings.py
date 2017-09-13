import Utils.Logger as Logger
from locale import getlocale

translations = {
    "en_US": {

        # SECTION PROMPTS
        "prompt.mmc": "Please select your MultiMC folder.",
        "prompt.delete": "Are you sure you want to delete {}?",
        "prompt.update":
"A new version of OpenMineMods is available!\n\
Would you like to update to v{}?",
        "prompt.analytics":
"Would you like to enable basic analytics?\n\
More information is availible at the URL below.\n\
https://github.com/joonatoona/OpenMineMods/blob/master/ExampleAnalytics.md",

        # SECTION TOOLTIPS
        "tooltip.refresh.instances": "Refresh Instances",
        "tooltip.configure.omm": "Configure OpenMineMods",
        "tooltip.edit.instance": "Edit Instance",
        "tooltip.delete.instance": "Delete Instance",
        "tooltip.browse.mods": "Browse Mods",
        "tooltip.delete.mod": "Remove Mod",

        # SECTION LABELS
        "label.instances": "Instances",
        "label.installed": "Installed Mods",

        # SECTION TITLES
        "title.editing": "Editing {}"
    }
}


class Strings:
    def __init__(self):
        self.lang = getlocale()[0]
        if self.lang not in translations:
            Logger.err("Locale {} is not translated!".format(self.lang))
            self.lang = "en_US"

    def get(self, key: str):
        if key in translations[self.lang]:
            return translations[self.lang][key].replace('\t', '')
        Logger.err("String {} is not translated to {}!".format(key, self.lang))
        if key not in translations["en_US"]:
            Logger.err("String {} is not translated at all!".format(key))
            return "[Missing String]"
        return translations["en_US"][key].replace('\t', '')
