#!/bin/bash

python setup.py build
sphinx-apidoc -f -o doc/ build/lib.linux-x86_64-3.2/gensokyo
cd doc
make html
