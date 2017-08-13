# An alternative to the Twitch/Curse launcher for MultiMC

Requirements:
* Python 3.6.2
* BeautifulSoup 4.6.0
* Requests 2.18.3
* Bottle v0.12.13
* EasyGUI v<idfk, latest?>
* PyQt5 v<idfk, latest?>

(Other versions may work, but those are the tested ones)

---

# TL;DR:

## Windows

* Download and unzip https://github.com/joonatoona/OpenMineMods/archive/master.zip
* Run `Windows\Install.bat` in the unzipped folder
* Run `Windows\GUI.bat` in the unzipped folder

---

# Installing Requirements

## Linux

### Arch Linux

```
sudo pacman -S python python-beautifulsoup4 python-requests
```

### Other

```
pip3 install beautifulsoup4 requests
```

## MacOS

```
pip3 install beautifulsoup4 requests
```

## Windows

Download `https://github.com/joonatoona/OpenMineMods/archive/master.zip` and unzip it somewhere.  
In `UnzippedFolder/Installers` run `Windows`

Note: If it doesn't work, you need to uninstall Python 3.6.2 first.

---

# Using

## Install

### Linux

```
git clone https://github.com/joonatoona/OpenMineMods.git
cd OpenMineMods
```

(I will make a pip package at some point)

### MacOS

Same as Linux

### Windows

Run `Mods_Win` or `Pack_Win` in the unzipped folder

## Test

```
python3 tests.py
```

If not every test passed, please open an issue with `results.json` and your MultiMC installation folder.
