#!/bin/bash

for f in UI/*.ui; do
	pyn=$(echo $f | sed 's/.ui/.py/' | sed 's/UI/GUI/')
	echo "Building $f to $pyn"
	python3 -m PyQt5.uic.pyuic $f -o $pyn
done

python3 -m PyQt5.pyrcc_main Assets/icons.qrc -o icons_rc.py
