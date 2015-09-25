#!/bin/sh

# Verify that rewritemeta has been run.

set -e

files=$(fdroid rewritemeta -l)

if [[ -n "$files" ]]; then
	echo "Run fdroid rewritemeta to fix formatting on these files:"
	echo "$files"
	exit 1
fi

exit 0
