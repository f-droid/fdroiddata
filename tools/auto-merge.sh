#! /usr/bin/env bash

set -e

cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")"

mr=$1
glab="glab --repo fdroid/fdroiddata"
function retry {
  msg=$1
  shift
  while output=$("$@" 2>&1); [[ $? != 0 ]]; do
    # Return 1 if there is an error needed to be handled
    [[ "$msg" ]] && echo "$output" | grep -qE "$msg" && echo "$output" && return 1
  done
  echo "$output"
}

echo "Merging..."
while status=$(retry "" glab api projects/:id/merge_requests/$mr | jq -r '.detailed_merge_status'); do
  if [[ $status = "approvals_syncing" || $status = "checking" || $statue = "preparing" ]]; then
    continue
  elif [[ $status = "need_rebase" ]]; then
    echo "Rebasing..."
    retry "Source branch does not exist|Cannot push to source branch" $glab mr rebase $mr --skip-ci || exit 0
    sleep 2
  elif [[ $status = "mergeable" ]]; then
    retry "HTTP" glab api --method PUT projects/:id/merge_requests/$mr/merge > /dev/null && break
  else
    echo "Failed to merge $mr: $status"
    exit 0
  fi
done

echo "Canceling pipelines..."
merged_commit=$(retry "" $glab mr view $mr -F json | jq -r 'if .squash then .squash_commit_sha else .sha end')
head_pipelines=$(retry "" $glab ci list -F json | jq -r 'map(select(.sha == "'$merged_commit'" and (.source == "push" or .source == "merge_request_event")) | .id)[]')
for pipeline in $head_pipelines; do
  retry "" glab api --method POST --silent projects/:id/pipelines/$pipeline/cancel
done

echo "Done!"
