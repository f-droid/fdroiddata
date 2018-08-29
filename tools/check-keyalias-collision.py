#!/usr/bin/env python3

import glob
import hashlib
import inspect
import os
import sys

def generate_keyalias(s):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()[:8]

base = os.path.realpath(
    os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '..'))
metadatafiles = sorted(glob.glob(base + '/metadata/*.txt')
                       + glob.glob(base + '/metadata/*.yml'))

if not metadatafiles:
    print('No metadata files found!')
    sys.exit(1)

keyaliases = dict()
for f in metadatafiles:
    appid = os.path.basename(f)[:-4]
    keyalias = generate_keyalias(appid)
    if keyalias in keyaliases:
        print(appid, "keyalias conflicts with", keyaliases[keyalias])
        sys.exit(1)
    keyaliases[keyalias] = appid
