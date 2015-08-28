#!/bin/sh

# This fetches all google code source pages and reports those that have moved
# to github.

set -e

all=$(sed -n 's@Source Code:\(.*code\.google\.com.*/source\)@\1@p' metadata/*.txt | sort -u)
len=$(echo "$all" | wc -l)

echo "$len apps left"

echo "$all" | sort -u | shuf | while read url; do
	printf "."
	
	found=$(curl -s $url/checkout | sed -n 's/.*<A HREF="\(.*\)">here<\/A>.*/\1/p')
	if [ -n "$found" ]; then
		printf "\n%s\n" $url
		printf "\tProject moved: %s\n" $found
	fi
done
