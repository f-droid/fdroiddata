#!/bin/sh

# Verify that rewritemeta has been run.

set -e

err() {
	echo "$@" >&2
	exit 1
}

has_changed_files() {
	git update-index -q --refresh
	git diff-index --quiet HEAD -- && return 1 || return 0
}

list_changed_files() {
	git diff-index --name-only HEAD -- || return 0
}

if has_changed_files; then
	list_changed_files
	err "Unstaged changes found; refusing to continue."
fi

fdroid rewritemeta

if has_changed_files; then
	list_changed_files
	err "Run rewritemeta to fix formatting on those files."
fi
