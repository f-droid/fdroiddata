#!/usr/bin/env python3

import glob
import os
import re
import subprocess
import sys

import yaml
from colorama import Fore, Style

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = sorted(glob.glob('metadata/*.yml') + glob.glob('srclibs/*.yml'))

errors = dict()
for f in files:
    f = os.path.relpath(f)
    if not f.startswith('metadata/') and not f.startswith('srclibs/'):
        continue
    if not f.endswith('.yml'):
        print('\n' + f + ':\nThis only runs on YAML files (.yml), ignoring.')
        continue
    with open(f) as fp:
        data = yaml.load(fp, Loader=SafeLoader)

    if not data:
        msg = 'ERROR: %s: empty file!' % f
        print(Fore.RED + msg + Style.RESET_ALL)
        errors[f] = msg
        continue
    if 'NoSourceSince' in data.keys():
        continue
    url = data.get('Repo')
    if not url:
        msg = 'ERROR: %s: no Repo: set!' % f
        print(Fore.RED + msg + Style.RESET_ALL)
        errors[f] = msg
        continue
    if data.get('RepoType') != 'git':
        continue

    # from class vcs_git() in fdroidserver/common.py
    git_config = [
        '-c',
        'core.askpass=/bin/true',
        '-c',
        'core.sshCommand=/bin/false',
        '-c',
        'url.https://.insteadOf=ssh://',
    ]
    for domain in ('bitbucket.org', 'github.com', 'gitlab.com'):
        git_config.append('-c')
        git_config.append(
            'url.https://u:p@' + domain + '/.insteadOf=git@' + domain + ':'
        )
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

    p = subprocess.run(
        [
            'git',
        ]
        + git_config
        + ['ls-remote', '--exit-code', '-h', url],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if p.returncode != 0:
        with open(f) as fp:
            raw = fp.read()
        print('\n' + f + ':')
        print('%s%s%s' % (Fore.RED, p.stderr.decode(), Style.RESET_ALL))
        errors[f] = p.stderr

        if not f.startswith('metadata/'):
            continue
        # this rewriting only works with metadata files, not srclibs
        with open(f, 'w') as fp:
            fp.write(re.sub(r'(Repo|RepoType):.*\n{1,2}', r'', raw))
            builds = data.get('Builds')
            if builds:
                versionName = str(builds[-1]['versionName'])
                # if YAML will think its a float, quote it
                try:
                    float(versionName)
                    fp.write("\nNoSourceSince: '%s'" % versionName)
                except ValueError:
                    fp.write("\nNoSourceSince: %s" % versionName)
                fp.write('\n')

error_count = len(errors)
if error_count > 0:
    print(Fore.RED + '\nFound', error_count, 'errors.' + Style.RESET_ALL)
sys.exit(error_count)
