#!/usr/bin/env python3
#
#
# Apps with reproducible builds include the APK Signature files in the
# metadata.  If there is no matching entry in Builds:, then those
# files are useless cruft.

import glob
import hashlib
import json
import os
import sys
import yaml

CODEQUALITY_REPORT = list()
CHECK_NAME = os.path.basename(__file__)

errors = 0
for d in glob.glob("metadata/*/signatures/[0-9]*"):
    appid = os.path.basename(os.path.dirname(os.path.dirname(d)))
    with open(os.path.join("metadata", appid + ".yml")) as fp:
        app = yaml.safe_load(fp)
    versionCode = os.path.basename(d)
    found = False
    for build in app["Builds"]:
        if int(versionCode) == int(build["versionCode"]):
            found = True
            break
    if not found:
        errors += 1
        msg = "found signatures files with no matching build"
        print(f"ERROR: {msg}:")
        for f in os.listdir(d):
            sig_file = os.path.join(d, f)
            print(f"\t{sig_file}")
            m = hashlib.sha256()
            with open(sig_file, 'rb') as fp:
                m.update(fp.read())
            CODEQUALITY_REPORT.append(
                {
                    "description": msg,
                    "check_name": CHECK_NAME,
                    "fingerprint": CHECK_NAME + f + m.hexdigest(),
                    "severity": "major",
                    "location": {"path": sig_file, "lines": {"begin": 0}},
                }
            )

with open(f"{CHECK_NAME}.json", "w") as fp:
    json.dump(CODEQUALITY_REPORT, fp)

sys.exit(errors)
