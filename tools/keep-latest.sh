#! /usr/bin/env bash

set -e

current_build=$(curl https://f-droid.org/repo/status/running.json)
if [[ $(jq -r '.subcommand' <<< $current_build) != "build" ]]; then
  current_build=$(curl https://f-droid.org/repo/status/build.json)
fi
update=$(curl https://f-droid.org/repo/status/update.json)

last_commit=$(jq -r '.fdroiddata.commitId' <<< $current_build)
echo "This build cycle started at: $last_commit"
echo "HEAD at: $(git rev-parse HEAD)"
changed_files=$(git diff --name-only --diff-filter=AM "$last_commit" HEAD)
missing_builds=$(jq -r '.failedBuilds' <<< $update)
failed_builds=$(jq -r '.failedBuilds' <<< $current_build)
succuess_builds=$(jq -r '.successfulBuildIds' <<< $current_build)

for file in $changed_files; do
  grep -q "AutoUpdateMode: None" $file && continue
  if [[ $file == *.yml && $(dirname "$file") == "metadata" ]]; then
    appid=$(basename $file .yml)
    diff=$(git diff "$last_commit" HEAD -- "$file")
    keep_num=$(sed -z -E -n 's/.*VercodeOperation:\n((  -[^\n]*\n)+).*/\1/p' "$file" | wc -l)
    [[ $keep_num == 0 ]] && keep_num=1

    removed_versions=$(grep "\-    versionCode: " <<< "$diff" | sed -E -n "s/.*versionCode: ([0-9]+)/\1/p" | jq --slurp '.')
    new_versions=$(grep "+    versionCode: "  <<< "$diff" | sed -E -n "s/.*versionCode: ([0-9]+)/\1/p" | jq --slurp '.')
    missing_versions=$(jq -r ".\"$appid\" // []" <<< "$missing_builds")
    failed_versions=$(jq -r "map(select(.[0] == \"$appid\") | .[1])" <<< "$failed_builds")
    success_versions=$(jq -r "map(select(.[0] == \"$appid\") | .[1])" <<< "$succuess_builds")

    remove_versions=$(jq --slurp -r ".[0] + .[2] + .[3] - .[1] - .[4] | sort | unique | .[:-$keep_num][]" <(printf "$new_versions") <(printf "$removed_versions") <(printf "$missing_versions") <(printf "$failed_versions") <(printf "$success_versions"))

    if [[ -n $remove_versions ]]; then
      echo "Cleaning $appid: ${remove_versions//$'\n'/ }"
      for version in $remove_versions; do
        sed -i "/versionCode: $version/,/^$/d" "$file"
        sed -i -E -z 's/\n  - versionName:[^\n]+\n  -/\n  -/' "$file"
      done
    fi
  fi
done
