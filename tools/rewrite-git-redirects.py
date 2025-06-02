#!/usr/bin/env python3
#
# GitLab gives a warning every time if the git URL is redirected.  So
# this rewrites all GitLab URLs so they are no longer a redirect.
# This also allows the gitlab.com URLs to be used with Tor, and gives
# other benefits, like a simplier security attack surface.

import glob
import json
import os
import re
import subprocess
import sys
import yaml


REPO_PATTERN = re.compile(r'Repo: .*')
CODEQUALITY_REPORT = list()
CHECK_NAME = os.path.basename(__file__)


def is_git_redirect(url):
    """Check if git is served a redirect"""
    host = url.split('/')[2]
    p = subprocess.run(
        [
            'git',
            '-c',
            'core.askpass=/bin/true',
            '-c',
            'credential.helper=/bin/true',
            '-c',
            'http.emptyAuth=true',
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


def scan_app_file(f, include_srclibs=True):
    with open(f) as fp:
        data = yaml.safe_load(fp)
    repo_url = data.get('Repo', '').strip()
    if (
        'Repo' not in data
        or data.get('RepoType') != 'git'
        or data.get('ArchivePolicy') == '0 versions'
    ):
        return

    if include_srclibs:
        srclibs_to_scan = set()
        for build in data.get('Builds', []):
            for srclib in build.get('srclibs', []):
                srclibf = 'srclibs/%s.yml' % srclib.split('@')[0]
                srclibs_to_scan.add(srclibf)
        for srclib in srclibs_to_scan:
            scan_app_file(srclib)

    if not is_git_redirect(repo_url):
        return

    new_url = None
    for url in [
        repo_url.rstrip('/') + '.git',
        repo_url.rstrip('/'),
    ]:
        if not is_git_redirect(url):
            new_url = url
            break

    if new_url:
        with open(f) as fp:
            for num, line in enumerate(fp, 1):
                if line.startswith('Repo:'):
                    begin = num
                    break
        CODEQUALITY_REPORT.append(
            {
                "categories": ["Bug Risk"],
                "check_name": CHECK_NAME,
                "content": "`fdroid` is based on building a strong connection from source code to compiled binary.  Therefore, the whole path should be as explicit, visible and reproducible as possible. Additionally, `git://` and `http://` URLs in submodules could be abused to direct to malicious content.",
                "description": '`Repo:` URLs should not use redirects.',
                "fingerprint": f"""{CHECK_NAME}|{repo_url}""",
                "location": {"path": f, "lines": {"begin": begin}},
                "severity": "blocker",
                "type": "issue",
            }
        )
        print("Repo:", data['Repo'], "\n -->  " + new_url + "'")
        with open(f) as fp:
            raw = fp.read()
        with open(f, 'w') as fp:
            fp.write(REPO_PATTERN.sub('Repo: ' + new_url, raw))


def main():
    os.chdir(os.path.dirname(__file__) + '/../')

    if len(sys.argv) > 1:
        files = ['metadata/%s.yml' % f for f in sys.argv[1:]]
        include_srclibs = True
    else:
        files = sorted(glob.glob('metadata/*.yml') + glob.glob('srclibs/*.yml'))
        include_srclibs = False

    for f in files:
        scan_app_file(f, include_srclibs)

    with open(f"codequality.json", "w") as fp:
        json.dump(CODEQUALITY_REPORT, fp)

if __name__ == "__main__":
    main()
