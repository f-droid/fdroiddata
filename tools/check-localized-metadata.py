#!/usr/bin/env python3

import glob
import os
import re
import sys

os.chdir(os.path.dirname(__file__) + '/../')

count = 0

locales = dict()
for f in sorted(glob.glob('metadata/*/*/*.txt')):
    name, _ = os.path.splitext(os.path.basename(f))
    if name == 'full_description':
        print(f, 'should use fdroid name', re.sub('full_description', 'description', f))
        count += 1
    elif name == 'short_description':
        print(f, 'should use fdroid name', re.sub('short_description', 'summary', f))
        count += 1
    elif name == 'title':
        print(f, 'should use fdroid name', re.sub('title', 'name', f))
        count += 1
    elif name not in ('summary', 'description', 'name'):
        print(f, 'has invalid filename', name)

    packageName, locale = f.split('/')[1:3]
    if packageName not in locales:
        locales[packageName] = []
    locales[packageName].append(locale)

for k, v in locales.items():
    if 'en-US' not in v:
        print(k, 'is missing source locale en-US!')
        count += 1

sys.exit(count)
