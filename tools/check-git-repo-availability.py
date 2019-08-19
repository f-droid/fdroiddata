#!/usr/bin/env python3

import glob
import re
import subprocess
import sys
import yaml

if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = sorted(glob.glob('metadata/*.yml'))

errors = dict()
for f in files:
    if not f.endswith('.yml'):
        print('\n' + f + ':\nThis only runs on YAML files (.yml), ignoring.')
        continue
    with open(f) as fp:
        data = yaml.load(fp)

    url = data.get('Repo')
    if not url or 'NoSourceSince' in data.keys():
        continue
    if data['RepoType'] != 'git':
        continue

    # from class vcs_git() in fdroidserver/common.py
    git_config = [
        '-c', 'core.askpass=/bin/true',
        '-c', 'core.sshCommand=/bin/false',
        '-c', 'url.https://.insteadOf=ssh://',
    ]
    for domain in ('bitbucket.org', 'github.com', 'gitlab.com'):
        git_config.append('-c')
        git_config.append('url.https://u:p@' + domain + '/.insteadOf=git@' + domain + ':')
        git_config.append('-c')
        git_config.append('url.https://u:p@' + domain + '.insteadOf=git://' + domain)
        git_config.append('-c')
        git_config.append('url.https://u:p@' + domain + '.insteadOf=https://' + domain)
    env = {
        'GIT_TERMINAL_PROMPT': '0',
        'GIT_ASKPASS': '/bin/true',
        'SSH_ASKPASS': '/bin/true',
        'GIT_SSH': '/bin/false',  # for git < 2.3
    }

    p = subprocess.run(['git', ] + git_config + ['ls-remote', '--exit-code', '-h', url],
                       env=env,
                       capture_output=True)
    if p.returncode != 0:
        with open(f) as fp:
            raw = fp.read()
        with open(f, 'w') as fp:
            fp.write(re.sub(r'(Repo|RepoType):.*\n{1,2}', r'', raw))
            builds = data.get('Builds')
            if builds:
                versionName = str(builds[-1]['versionName'])
                # if YAML will think its a float, quote it
                try:
                    float(versionName)
                    fp.write("\nNoSourceSince: '" + versionName + "'")
                except ValueError:
                    fp.write("\nNoSourceSince: " + versionName)
                fp.write('\n')

        print('\n' + f + ':')
        print(p.stderr.decode())
        errors[f] = p.stderr

errorcount = len(errors)
if errorcount > 0:
    print('\nFound', errorcount, 'errors.')
sys.exit(errorcount)
