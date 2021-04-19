#!/usr/bin/env python3

import glob
import os
import subprocess
import sys
import yaml
from colorama import Fore, Style

if len(sys.argv) != 2:
    print(Fore.RED + ('ERROR: incorrect number of arguments') + Style.RESET_ALL)
    exit(1)

appid, versionCode = sys.argv[1].split(':')

if not glob.glob('metadata/%s/signatures/%s/*' % (appid, versionCode)):
    print(Fore.RED + ('ERROR: no signatures found') + Style.RESET_ALL)
    exit(1)

for f in glob.glob('tmp/%s_%s.apk' % (appid, versionCode)):
    os.rename(f, f.replace('tmp/', 'unsigned/'))

if not glob.glob('unsigned/%s_%s.apk' % (appid, versionCode)):
    exit(1)
