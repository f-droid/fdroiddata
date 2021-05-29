#!/usr/bin/env python3

import glob
import os
import sys

from colorama import Fore, Style

if len(sys.argv) != 2:
    print(
        Fore.RED
        + ('ERROR: incorrect number of arguments: ' + ' '.join(sys.argv[1:]))
        + Style.RESET_ALL
    )
    exit(1)

appid, versionCode = sys.argv[1].split(':')

if not glob.glob('metadata/%s/signatures/%s/*' % (appid, versionCode)):
    print('no signatures found, skipping publish')
    exit(1)

for f in glob.glob('tmp/%s_%s.apk' % (appid, versionCode)):
    os.rename(f, f.replace('tmp/', 'unsigned/'))

if not glob.glob('unsigned/%s_%s.apk' % (appid, versionCode)):
    print('no unsigned APK found, skipping publish')
    exit(1)

print(
    Fore.GREEN
    + ('Found signatures for %s, running publish...' % sys.argv[1])
    + Style.RESET_ALL
)
