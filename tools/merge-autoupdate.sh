#! /usr/bin/env bash

set -e

cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")"

glab="glab --repo fdroid/fdroiddata"
mr_list=$($glab mr list --author checkupdates-bot -F json | jq -r 'map(.iid)[]')
for mr in $mr_list; do
  mr_stat=$($glab mr view $mr -F json)
  if [[ $(echo $mr_stat | jq -r '.labels | map(. == "fdroid-bot") | any') == "false" ]]; then
    $glab mr update $mr --label "fdroid-bot"
  fi
  draft=$(echo $mr_stat | jq -r '.draft')
  if [[ $(echo $mr_stat | jq -r '.title | test("bot: Update CurrentVersion of .*")') == "true" && $draft == "false" ]]; then
    $glab mr update --draft
    draft="true"
  fi
  if [[ $(echo $mr_stat | jq -r '.pipeline.status == "success"') == "true" && $draft == "false" ]]; then
    echo "Merging $mr..."
    ./tools/auto-merge.sh $mr
  fi
done
