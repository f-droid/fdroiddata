#!/bin/sh
#
# Install all the client hooks

BASE_DIR=$(dirname $0)
HOOK_NAMES="applypatch-msg pre-applypatch post-applypatch pre-commit prepare-commit-msg commit-msg post-commit pre-rebase post-checkout post-merge pre-receive update post-receive post-update pre-auto-gc"
HOOK_DIR=$(git rev-parse --show-toplevel)/.git/hooks

for hook in $HOOK_NAMES; do

	shipped_hook=$BASE_DIR/$hook
	installed_hook=$HOOK_DIR/$hook

	# If we don't distribute it, continue
	if [ ! -f $shipped_hook ]; then
		continue
	fi

	# If the hook already exists, continue
	if [ -e $installed_hook -o -h $installed_hook ]; then
		echo "$installed_hook hook already exists."
		continue
	fi

	# Create the symlink
	echo "ln -s $shipped_hook $installed_hook"
	ln -s $shipped_hook $installed_hook

done
