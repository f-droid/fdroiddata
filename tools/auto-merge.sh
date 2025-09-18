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

echo "Merging..."
while status=$(glab api projects/:id/merge_requests/$mr | jq -r '.detailed_merge_status'); do
  if [[ $status = "approvals_syncing" || $status = "checking" ]]; then
    continue
  elif [[ $status = "need_rebase" ]]; then
    echo "Rebasing..."
    retry $glab mr rebase $mr --skip-ci
  elif [[ $status = "mergeable" ]]; then
    glab api --method PUT projects/:id/merge_requests/$mr/merge 2>&1 > /dev/null
    if [[ $? = 0 ]]; then
      break
    fi
  else
    echo "Failed to merge $mr: $status"
    exit 0
  fi
done

echo "Canceling pipelines..."
merged_commit=$(retry $glab mr view $mr -F json | jq -r 'if .squash then .squash_commit_sha else .sha end')
head_pipelines=$(retry $glab ci list -F json | jq -r 'map(select(.sha == "'$merged_commit'" and (.source == "push" or .source == "merge_request_event")) | .id)[]')
for pipeline in $head_pipelines; do
  retry glab api --method POST --silent projects/:id/pipelines/$pipeline/cancel
done

echo "Done!"
