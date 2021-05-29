#!/usr/bin/env python3
#
#
# Apps with reproducible builds include the APK Signature files in the
# metadata.  If there is no matching entry in Builds:, then those
# files are useless cruft.

import glob
import os

import yaml

errors = 0
for d in glob.glob('metadata/*/signatures/[0-9]*'):
    appid = os.path.basename(os.path.dirname(os.path.dirname(d)))
    with open(os.path.join('metadata', appid + '.yml')) as fp:
        app = yaml.safe_load(fp)
    versionCode = os.path.basename(d)
    found = False
    for build in app['Builds']:
        if int(versionCode) == int(build['versionCode']):
            found = True
            break
    if not found:
        print('ERROR: found signatures files with no matching build:')
        for f in os.listdir(d):
            print('\t', os.path.join(d, f))

exit(errors)
