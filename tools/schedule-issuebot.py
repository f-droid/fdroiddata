#!/usr/bin/env python3

import json
import os
import pprint
import re
import subprocess

import gitlab

os.chdir(os.path.join(os.path.dirname(__file__), '..'))

private_token = os.getenv('PERSONAL_ACCESS_TOKEN')
gl = gitlab.Gitlab('https://gitlab.com', private_token=private_token)
project = gl.projects.get(os.getenv('CI_PROJECT_PATH'), lazy=True)

TRIGGER_COMMIT_PAT = re.compile(r'<tt>([0-9a-f]{40})</tt>')

for mr in project.mergerequests.list(state='opened', order_by='updated_at'):
    commit_ids = []
    found_issuebot_post = False
    for discussion in mr.discussions.list():
        for note in discussion.attributes['notes']:
            if note['author']['username'] == 'fdroid-bot':
                found_issuebot_post = True
                m = TRIGGER_COMMIT_PAT.search(note.get('body', ''))
                if m:
                    commit_ids.append(m.group(1))
    if not commit_ids and found_issuebot_post:
        print(
            mr.iid, 'issuebot has posted without trigger commit ID, not running again'
        )
    elif mr.sha in commit_ids:
        print(mr.iid, 'issuebot has run on %s, not running again' % mr.sha)
    else:
        print(mr.iid, '"%s" needs issuebot run' % mr.title)
        # insecure "captcha"
        with open('.issuebot') as fp:
            token = subprocess.check_output(
                [
                    'bash',
                    '-c',
                    's=$((4`printf "$CI_COMMIT_SHA" | wc -c`-10));'
                    'e=$((s+`echo "$CI_SERVER_HOST" | wc -c`+18));'
                    'cut -b${s}-${e}',
                ],
                stdin=fp,
                env=os.environ,
            )
        # All of these are describing the project and merge request,
        # so FROM_CI_JOB_ID, FROM_CI_PIPELINE_ID, etc. are not relevant,
        # since this is not running the context of the user-submitted
        # merge request.
        cmd = [
            'curl',
            '--silent',
            '--request',
            'POST',
            '--form',
            'token=%s' % token.decode().strip(),
            '--form',
            'ref=master',
            '--form',
            'variables[FROM_CI_COMMIT_REF_NAME]=%s' % mr.source_branch,
            '--form',
            'variables[FROM_CI_COMMIT_REF_SLUG]=%s' % mr.source_branch,
            '--form',
            'variables[FROM_CI_COMMIT_SHA]=%s' % mr.sha,
            '--form',
            'variables[FROM_CI_MERGE_REQUEST_IID]=%s' % mr.iid,
            '%s/projects/36528/trigger/pipeline' % os.getenv('CI_API_V4_URL'),
        ]
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        pprint.pprint(json.loads(p.stdout))
        exit()
