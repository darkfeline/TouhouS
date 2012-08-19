#!/usr/bin/env python3

import os
import os.path

def say(x, path):
    print("'{}/{}', ".format(path, x), end="")

def main(dir):
    recurse(dir)

def recurse(dir):
    ls = os.listdir(dir)
    dirs = []
    for f in ls:
        if os.path.isdir(os.path.join(dir, f)):
            dirs.append(f)
        else:
            say(f, dir)
    for d in dirs:
        recurse(os.path.join(dir, d))

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
