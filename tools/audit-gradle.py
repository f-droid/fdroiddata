#!/usr/bin/env python3

import os
import re
import sys

# find all repositories that use plain HTTP urls (e.g. not HTTPS)
url_pattern = re.compile(
    r'repositories\s*{[^}]*http://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|%[0-9a-fA-F][0-9a-fA-F])+[^}]*}',
    re.DOTALL,
)

exit_value = 0
for appid in sys.argv:
    git_dir = os.path.join('build', appid)
    if not os.path.isdir(git_dir):
        continue
    for root, dirs, files in os.walk(git_dir):
        for f in files:
            if f.endswith('.gradle'):
                path = os.path.join(root, f)
                with open(path) as fp:
                    data = fp.read()
                for url in url_pattern.findall(data):
                    print(
                        'Found plain HTTP URL for gradle repository:\n%s\n%s'
                        % (path, url)
                    )
                    exit_value += 1

if exit_value:
    print('gradle build uses plain HTTP URLs for repositories!  This is insecure!')
    print(
        'https://max.computer/blog/how-to-take-over-the-computer-of-any-java-or-clojure-or-scala-developer/'
    )
sys.exit(exit_value)
