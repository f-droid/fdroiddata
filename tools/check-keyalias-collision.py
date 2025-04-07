#!/usr/bin/env python3

import glob
import hashlib
import inspect
import json
import os
import urllib.request
import sys


def generate_keyalias(s):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()[:8]


metadata_files = glob.glob("metadata/*.yml")

CODEQUALITY_REPORT = list()
CHECK_NAME = os.path.basename(__file__)

if not metadata_files:
    print("No metadata files found!")
    sys.exit(1)

errors = 0
keyaliases = dict()
for f in metadata_files:
    appid = os.path.basename(f)[:-4]
    keyalias = generate_keyalias(appid)
    if keyalias in keyaliases:
        errors += 1
        original = appid
        conflicting = keyaliases[keyalias]
        try:
            url = f'https://f-droid.org/api/v1/packages/{appid}'
            r = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(r) as response:
                if response.status == 200:
                    original = keyaliases[keyalias]
                    conflicting = appid
        except urllib.error.URLError:
            pass
        msg = f"{conflicting} keyalias conflicts with {original}"
        path = f'metadata/{conflicting}.yml'
        print(msg)
        CODEQUALITY_REPORT.append(
            {
                "description": msg,
                "check_name": CHECK_NAME,
                "fingerprint": CHECK_NAME + keyalias + f + path,
                "severity": "blocker",
                "location": {"path": path, "lines": {"begin": 0}},
            }
        )
    keyaliases[keyalias] = appid

with open(f"{CHECK_NAME}.json", "w") as fp:
    json.dump(CODEQUALITY_REPORT, fp)

sys.exit(errors)
