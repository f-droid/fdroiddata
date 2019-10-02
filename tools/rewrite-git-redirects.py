#!/usr/bin/env python3
#
#
# GitLab gives a warning every time if the git URL is redirected.  So this
# rewrites all GitLab URLs so they are no longer a redirect.

import glob
import os
import re
import sys
import yaml

os.chdir(os.path.dirname(__file__) + '/../')

if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = sorted(glob.glob('metadata/*.yml'))

pattern = re.compile(r'Repo: .*')
for f in files:
    with open(f) as fp:
        data = yaml.load(fp)
    repo_url = None
    if 'Repo' in data:
        repo_url = data['Repo'].strip().rstrip('/')
    if repo_url and not repo_url.endswith('.git') and repo_url.startswith('https://gitlab'):
        new_url = repo_url + '.git'
        print("Repo:", data['Repo'], "\n -->  " + new_url + "'")
        with open(f) as fp:
            raw = fp.read()
        with open(f, 'w') as fp:
            fp.write(pattern.sub('Repo: ' + new_url, raw))
