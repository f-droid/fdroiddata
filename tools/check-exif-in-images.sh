#!/bin/bash -x
#

find metadata/ -name '*.jp*g' -o -name '*.png' | xargs exiftool -all=
msg="these images have EXIF that must be stripped:"
echo $msg
git diff --stat
check_name=$(basename $0)
# Output a single JSON file per file because JSON commas are hard in
# bash. And this job combines *.json into a single JSON report anyway.
for f in $(git diff --name-only); do
    fingerprint=$(sha256sum "$f" | awk '{print $1}')
    cat <<EOF > $check_name-$(echo $f | sed 's,[^a-zA-Z0-9],_,g').json
[
{
  "description": "$msg",
  "check_name": "$check_name",
  "fingerprint": "$fingerprint",
  "severity": "critical",
  "location": {"path": "$f", "lines": {"begin": 0}}
}
]
EOF
done
git diff --name-only --exit-code
