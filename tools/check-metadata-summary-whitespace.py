#!/usr/bin/env python3

import glob
import hashlib
import json
import os
import subprocess

CHECK_NAME = os.path.basename(__file__)
CODEQUALITY_REPORT = list()


def append(myfile):
    m = hashlib.sha256()
    with open(myfile, 'rb') as myfp:
        m.update(myfp.read())
    fingerprint = m.hexdigest()
    CODEQUALITY_REPORT.append(
        {
            "description": "metadata .txt file has incorrect whitespace",
            "check_name": CHECK_NAME,
            "fingerprint": CHECK_NAME + myfile + fingerprint,
            "severity": "minor",
            "location": {"path": myfile, "lines": {"begin": 0}},
        }
    )


os.chdir(os.path.join(os.path.dirname(__file__), '..'))
for f in glob.glob('metadata/*/*/*.txt') + glob.glob('metadata/*/*/*/*.txt'):
    if os.path.getsize(f) == 0:
        append(f)
        os.remove(f)
        continue

    with open(f) as fp:
        data = fp.read()
    with open(f, 'w') as fp:
        fp.write(data.strip().rstrip())
        fp.write('\n')

for f in subprocess.check_output(['git', 'diff', '--name-only']).split():
    append(f.decode())

with open(f"{CHECK_NAME}.json", "w") as fp:
    json.dump(CODEQUALITY_REPORT, fp)
