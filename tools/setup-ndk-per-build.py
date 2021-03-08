#!/usr/bin/env python3
#
# Install NDK when a build in GitLab CI `fdroid build` job needs it.

import os
import re
import subprocess
import sys
import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


def get_ndk_version(ndk_path):
    source_properties = os.path.join(ndk_path, 'source.properties')
    if os.path.exists(source_properties):
        with open(source_properties) as fp:
            m = re.search(r'^Pkg.Revision *= *(.+)', fp.read(), flags=re.MULTILINE)
            if m:
                return m.group(1)


if len(sys.argv) != 3:
    print(
        'Usage:\n\texport CI_PROJECT_DIR=%s\n\t%s app.id:12 /path/to/ndk_base'
        % (os.path.dirname(os.path.dirname(os.path.abspath(__file__))), __file__)
    )
    exit(1)

appid, versionCode = sys.argv[1].split(':')
with open('metadata/%s.yml' % appid) as fp:
    data = yaml.load(fp, Loader=SafeLoader)

ndk_base = sys.argv[2]
os.makedirs(ndk_base, exist_ok=True)
os.chdir(ndk_base)

for build in data.get('Builds', []):
    if build.get('disable'):
        continue
    if str(build['versionCode']) != str(versionCode):
        continue
    ndk = build.get('ndk')
    if not ndk:
        continue
    version = get_ndk_version(os.path.join(ndk_base, ndk))
    if version:
        print('Found existing setup for NDK %s (%s)' % (ndk, version))
        continue
    ndk_name = 'android-ndk-' + ndk
    zipball = ndk_name + '-linux-x86_64.zip'
    subprocess.run(
        [
            '/usr/bin/wget',
            '--quiet',
            '--continue',
            'https://dl.google.com/android/repository/' + zipball,
        ]
    )
    if not os.path.exists(ndk_name):
        subprocess.run(['/usr/bin/unzip', '-q', zipball])
    os.remove(zipball)
    if os.path.exists(ndk):
        os.remove(ndk)
    os.symlink(ndk_name, ndk)

    config_yml = os.path.join(os.getenv('CI_PROJECT_DIR'), 'config.yml')
    if os.path.exists(config_yml):
        with open(config_yml) as fp:
            config = yaml.load(fp, Loader=SafeLoader)
    else:
        config = dict()
    if 'ndk_paths' not in config:
        config['ndk_paths'] = dict()
    config['ndk_paths'][ndk] = os.path.join(ndk_base, ndk_name)
    with open(config_yml, 'w') as fp:
        yaml.dump(config, fp)

    version = get_ndk_version(os.path.join(ndk_base, ndk))
    if version:
        print('Setup NDK %s (%s)' % (ndk, version))
