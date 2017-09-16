#!/bin/bash

for f in *.ui; do
	pyn=$(echo $f | sed 's/.ui/.py/')
	echo "Building $f to $pyn"
	python -m PyQt5.uic.pyuic $f -o $pyn
done
