#!/usr/bin/env python3
#
# GitLab gives a warning every time if the git URL is redirected.  So
# this rewrites all GitLab URLs so they are no longer a redirect.
# This also allows the gitlab.com URLs to be used with Tor, and gives
# other benefits, like a simplier security attack surface.

import glob
import os
import re
import subprocess
import sys
import yaml


def is_git_redirect(url):
    """Check if git is served a redirect"""
    host = url.split('/')[2]
    p = subprocess.run(
        [
            'git',
            '-c',
            'url.https://git:nopw@{host}.insteadOf=https://{host}'.format(host=host),
            '-c',
            'http.followRedirects=false',
            'ls-remote',
            '--heads',
            url,
            'main',
        ],
        capture_output=True,
    )
    return p.returncode != 0


os.chdir(os.path.dirname(__file__) + '/../')

if len(sys.argv) > 1:
    files = ['metadata/%s.yml' % f for f in sys.argv[1:]]
else:
    files = sorted(glob.glob('metadata/*.yml'))

pattern = re.compile(r'Repo: .*')
for f in files:
    with open(f) as fp:
        data = yaml.safe_load(fp)
    repo_url = data.get('Repo', '').strip()
    if (
        'Repo' not in data
        or data.get('RepoType') != 'git'
        or data.get('ArchivePolicy') == '0 versions'
    ):
        continue

    if not is_git_redirect(repo_url):
        continue

    new_url = None
    for url in [
        repo_url.rstrip('/') + '.git',
        repo_url.rstrip('/'),
    ]:
        if not is_git_redirect(url):
            new_url = url
            break

    if new_url:
        print("Repo:", data['Repo'], "\n -->  " + new_url + "'")
        with open(f) as fp:
            raw = fp.read()
        with open(f, 'w') as fp:
            fp.write(pattern.sub('Repo: ' + new_url, raw))
