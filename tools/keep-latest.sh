#! /usr/bin/env bash

set -e

last_commit=$(git log --grep='Update known apks' | grep commit | head -n 1 | sed -E -n 's/commit (.*)/\1/p')
echo "Last known apks update at: $last_commit"
echo "HEAD at: $(git rev-parse HEAD)"
changed_files=$(git diff --name-only --diff-filter=AM "$last_commit" HEAD)

for file in $changed_files; do
  grep -q "AutoUpdateMode: None" $file && continue
  if [[ $file == *.yml && $(dirname "$file") == "metadata" ]]; then
    diff=$(git diff "$last_commit" HEAD -- "$file")
    removed_versions=$(grep "\-    versionCode: " <<< "$diff" | sed -E -n "s/.*versionCode: ([0-9]+)/\1/p")
    new_versions=$(grep "+    versionCode: "  <<< "$diff" | sed -E -n "s/.*versionCode: ([0-9]+)/\1/p")
    # When an old version is removed the diff may have both deletion and addition for the same version
    for version in $removed_versions; do
      new_versions=$(sed "/^${version}$/d" <<< "$new_versions")
    done
    new_version_num=$(wc -l <<< "$new_versions")

    keep_num=$(sed -z -E -n 's/.*VercodeOperation:\n((  -[^\n]*\n)+).*/\1/p' "$file" | wc -l)
    [[ $keep_num == 0 ]] && keep_num=1

    if [[ $new_version_num -gt $keep_num ]]; then
      remove_versions=$(head -n -"$keep_num" <<< "$new_versions")
      echo "Cleaning $file: ${remove_versions//$'\n'/ }"
      for version in $remove_versions; do
        sed -i "/versionCode: $version/,/^$/d" "$file"
        sed -i -E -z 's/\n  - versionName:[^\n]+\n  -/\n  -/' "$file"
      done
    fi
  fi
done
