@ECHO OFF

python\python.exe "%~dp0\..\WebUI.py"

start "http://127.0.0.1:8096/"
