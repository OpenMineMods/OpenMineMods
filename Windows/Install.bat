@ECHO OFF

bitsadmin.exe /Transfer "PyInstall" /download "https://www.python.org/ftp/python/3.6.2/python-3.6.2-amd64.exe" "%~dp0\pyinstall.exe"
%~dp0\pyinstall.exe /passive Include_launcher=0 Include_tcltk=1 SimpleInstall=1 PrependPath=1 TargetDir="%~dp0\python"
%~dp0\python\Scripts\pip.exe install requests beautifulsoup4 bottle easygui pyqt5