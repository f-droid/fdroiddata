#! /usr/bin/env bash

set -e

cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")"

mr=$1
glab="glab --repo fdroid/fdroiddata"
function retry {
  while output=$("$@" 2>&1); [[ $? != 0 ]]; do
    echo $output | grep -q "Source branch does not exist" && exit 0
    echo $output | grep -q "this merge request has already been merged" && exit 0
    continue
  done
  echo $output
}

echo "Rebasing..."
retry $glab mr rebase $mr --skip-ci

echo "Merging..."
retry $glab mr merge $mr --auto-merge=false --rebase --yes
echo "Canceling pipelines..."
merged_commit=$(retry $glab mr view $mr -F json | jq -r 'if .squash then .squash_commit_sha else .sha end')
head_pipelines=$(retry $glab ci list -F json | jq -r 'map(select(.sha == "'$merged_commit'" and (.source == "push" or .source == "merge_request_event")) | .id)[]')
for pipeline in $head_pipelines; do
  retry glab api --method POST --silent projects/:id/pipelines/$pipeline/cancel
done

echo "Done!"
