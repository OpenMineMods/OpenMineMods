import Utils.Logger as Logger
from locale import getdefaultlocale

translations = {
      "en_US": {

        # SECTION PROMPTS
        "prompt.mmc": "Please select your MultiMC folder.",
        "prompt.delete": "Are you sure you want to delete {}?",
        "prompt.update":
"A new version of OpenMineMods is available!\n\
Would you like to update to v{}?",
        "prompt.update.restart": "Please restart OpenMineMods to finish updating!",
        "prompt.analytics":
"Would you like to enable basic analytics?\n\
More information is availible at the URL below.\n\
https://github.com/joonatoona/OpenMineMods/blob/master/ExampleAnalytics.md",
        "prompt.restart": "A restart is required for new settings to take effect.",

        # SECTION TOOLTIPS
        "tooltip.refresh.instances": "Refresh Instances",
        "tooltip.configure.omm": "Configure OpenMineMods",
        "tooltip.edit.instance": "Edit Instance",
        "tooltip.delete.instance": "Delete Instance",
        "tooltip.browse.mods": "Browse Mods",
        "tooltip.delete.mod": "Remove Mod",
        "tooltip.search": "Search",
        "tooltip.install": "Install",
        "tooltip.mmc.change": "Change MultiMC Location",
        "tooltip.toggle.analytics": "Toggle Analytics",

        # SECTION LABELS
        "label.instances": "Instances",
        "label.installed": "Installed Mods",
        "label.search.mods": "Search Mods",
        "label.available.mods": "Available Mods",
        "label.search.packs": "Search Modpacks",
        "label.available.packs": "Available Modpacks",
        "label.mmc.location": "MultiMC Location",
        "label.analytics": "Analytics",

        # SECTION DOWNLOADING

        "downloading.icon": "Downloading Icon",
        "downloading.data": "Downloading Data",
        "downloading.mod": "Downloading {}",
        "downloading.pack": "Installing {}",
        "downloading.update": "Downloading Update",

        # SECTION TITLES
        "title.editing": "Editing {}",
        "title.browsing.mod": "Browsing Mods For {}",
        "title.browsing.packs": "Browsing Modpacks",
        "title.settings": "OpenMineMods Settings"
    },

     "ita_IT": {

        # SECTION PROMPTS
        "prompt.mmc": "Seleziona la cartella contenente MultiMC.",
        "prompt.delete": "Sei sicuro di voler eliminare {}?",
        "prompt.update":
"Una nuova versione di OpenMineMods è disponibile!\n\
Vorresti aggiornare a v{}?",
        "prompt.update.restart": "Per favore riavvia OpenMineMods per finire l'aggiornamento!",
        "prompt.analytics":
"Vorresti attivare le statistiche base?\n\
Maggiori informazioni nell'URL in basso.\n\
https://github.com/joonatoona/OpenMineMods/blob/master/ExampleAnalytics.md",
        "prompt.restart": "Un riavvio è necessario per rendere attivi i cambiamenti.",

        # SECTION TOOLTIPS
        "tooltip.refresh.instances": "Aggiorna Profilo",
        "tooltip.configure.omm": "Configura OpenMineMods",
        "tooltip.edit.instance": "Modifica Profilo",
        "tooltip.delete.instance": "Elimina Profilo",
        "tooltip.browse.mods": "Cerca Mod",
        "tooltip.delete.mod": "Rimuovi Mod",
        "tooltip.search": "Cerca",
        "tooltip.install": "Installa",
        "tooltip.mmc.change": "Cambia la posizione di MultiMC",
        "tooltip.toggle.analytics": "Attiva Statistiche",

        # SECTION LABELS
        "label.instances": "Profili",
        "label.installed": "Mod Installate",
        "label.search.mods": "Cerca Mod",
        "label.available.mods": "Mod Disponibili",
        "label.search.packs": "Cerca Modpack",
        "label.available.packs": "Modpack Disponibili",
        "label.mmc.location": "Posizione MultiMC",
        "label.analytics": "Statistiche",

        # SECTION DOWNLOADING

        "downloading.icon": "Download Icona",
        "downloading.data": "Download File",
        "downloading.mod": "Download {}",
        "downloading.pack": "Installazione {}",
        "downloading.update": "Download Aggiornamento",

        # SECTION TITLES
        "title.editing": "Modifica {}",
        "title.browsing.mod": "Ricerca Mod Per {}",
        "title.browsing.packs": "Ricerca Modpack",
        "title.settings": "Impostazioni OpenMineMods"
    },

    "nl_BE": {
         # SECTION PROMPTS
        "prompt.mmc": "Gelieve de MultiMC hoofdfolder te selecteren.",
        "prompt.delete": "Bent u zeker dat u {} wil verwijderen?",
        "prompt.update":
"Een nieuwe versie van OpenMineMods is beschikbaar!\n\
Wilt u nu updaten naar v{}?",
        "prompt.analytics":
"Wilt u basis analytics inschakelen?\n\
Meer informatie vind u in de link hieronder.\n\
https://github.com/joonatoona/OpenMineMods/blob/master/ExampleAnalytics.md",
        "prompt.update.restart": "herstart OpenMineMods om het updaten te eindigen.",
        "prompt.restart": "Het programma moet herstart worden om de wijzigingen correct uit te voeren.",

        # SECTION TOOLTIPS
        "tooltip.refresh.instances": "Vernieuw instanties",
        "tooltip.configure.omm": "Configureer OpenMineMods",
        "tooltip.edit.instance": "Pas Instantie aan",
        "tooltip.delete.instance": "Verwijder Instance",
        "tooltip.browse.mods": "Blader door mods",
        "tooltip.delete.mod": "Verwijder Mod",
        "tooltip.search": "Zoek",
        "tooltip.install": "Installeer",
        "tooltip.mmc.change": "Wijzig MultiMC Locatie",
        "tooltip.toggle.analytics": "Wijzig optie: Analytics",

        # SECTION LABELS
        "label.instances": "Instanties",
        "label.installed": "Geïnstalleerde mods",
        "label.search.mods": "Zoek Mods",
        "label.available.mods": "Beschikbare Mods",
        "label.search.packs": "Zoek Modpacks",
        "label.available.packs": "Beschikbare Modpacks",
        "label.mmc.location": "MultiMC Locatie",
        "label.analytics": "Analytics",

          # SECTION DOWNLOADING

        "downloading.icon": "Icoon downloaden",
        "downloading.data": "Data downloaden",
        "downloading.mod": "{} aan het downloaden",
        "downloading.pack": "{} aan het installeren",
        "downloading.update": "update aan het downloaden",

        
        # SECTION TITLES
        "title.editing": "Aanpassen: {}",
        "title.browsing.mod": "Bladeren door Mods voor {}",
        "title.browsing.packs": "Bladeren door Modpacks",
        "title.settings": "OpenMineMods Instellingen"
    },
    "nl_NL": {
         # SECTION PROMPTS
        "prompt.mmc": "Gelieve de MultiMC hoofdfolder te selecteren.",
        "prompt.delete": "Bent u zeker dat u {} wil verwijderen?",
        "prompt.update":
"Een nieuwe versie van OpenMineMods is beschikbaar!\n\
Wilt u nu updaten naar v{}?",
        "prompt.analytics":
"Wilt u basis analytics inschakelen?\n\
Meer informatie vind u in de link hieronder.\n\
https://github.com/joonatoona/OpenMineMods/blob/master/ExampleAnalytics.md",
        "prompt.update.restart": "herstart OpenMineMods om het updaten te eindigen.",
        "prompt.restart": "Het programma moet herstart worden om de wijzigingen correct uit te voeren.",

        # SECTION TOOLTIPS
        "tooltip.refresh.instances": "Vernieuw instanties",
        "tooltip.configure.omm": "Configureer OpenMineMods",
        "tooltip.edit.instance": "Pas Instantie aan",
        "tooltip.delete.instance": "Verwijder Instance",
        "tooltip.browse.mods": "Blader door mods",
        "tooltip.delete.mod": "Verwijder Mod",
        "tooltip.search": "Zoek",
        "tooltip.install": "Installeer",
        "tooltip.mmc.change": "Wijzig MultiMC Locatie",
        "tooltip.toggle.analytics": "Wijzig optie: Analytics",

        # SECTION LABELS
        "label.instances": "Instanties",
        "label.installed": "Geïnstalleerde mods",
        "label.search.mods": "Zoek Mods",
        "label.available.mods": "Beschikbare Mods",
        "label.search.packs": "Zoek Modpacks",
        "label.available.packs": "Beschikbare Modpacks",
        "label.mmc.location": "MultiMC Locatie",
        "label.analytics": "Analytics",

          # SECTION DOWNLOADING

        "downloading.icon": "Icoon downloaden",
        "downloading.data": "Data downloaden",
        "downloading.mod": "{} aan het downloaden",
        "downloading.pack": "{} aan het installeren",
        "downloading.update": "update aan het downloaden",

        
        # SECTION TITLES
        "title.editing": "Aanpassen: {}",
        "title.browsing.mod": "Bladeren door Mods voor {}",
        "title.browsing.packs": "Bladeren door Modpacks",
        "title.settings": "OpenMineMods Instellingen"
    },
   
}


class Strings:
    def __init__(self):
        self.lang = getdefaultlocale()[0]
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
