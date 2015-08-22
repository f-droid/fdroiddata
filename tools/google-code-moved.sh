#!/bin/sh

# This fetches all google code source pages and reports those that have moved
# to github.

set -e

sed -n 's@Source Code:\(.*code\.google\.com.*/source\)@\1@p' metadata/*.txt | sort -u | while read url; do
	echo $url
	
	found=$(curl -s $url/checkout | sed -n 's/.*<A HREF="\(.*\)">here<\/A>.*/\1/p')
	if [ -n "$found" ]; then
		printf "\tProject moved: %s\n" $found
	fi
done
