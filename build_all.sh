#!/bin/bash

echo installing gensokyo...
cd gensokyo
python setup.py install --root ../testing
echo installing TouhouS...
cd ../TouhouS
python setup.py install --root ../testing
