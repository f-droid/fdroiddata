#!/bin/bash

# Check that there are no errors in the metadata files and that they are
# formatted correctly.

set -o errexit
set -o nounset
set -o pipefail

files=$(fdroid rewritemeta -l)
if [[ -n "$files" ]]; then
	echo "ERROR: Run rewritemeta to fix formatting on these files:"
	echo "$files"
	exit 1
fi
