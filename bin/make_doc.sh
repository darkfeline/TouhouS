#!/bin/bash

python setup.py install
sphinx-apidoc -f -o doc/ src/gensokyo
cd doc
make html
