#!/bin/sh

# This fetches all google code source pages and reports those that have moved
# to github.

set -e

all=$(sed -n 's@Source Code:\(.*code\.google\.com.*/source\)@\1@p' metadata/*.txt | sort -u)
len=$(echo "$all" | wc -l)

echo "$len apps left"

moved() {
	printf "\n%s\n" $1
	printf "\tProject moved: %s\n" $2
}

echo "$all" | sort -u | shuf | while read url; do
	printf "."

	redurl=$(curl -s -I $url/checkout | perl -n -e '/^Location: (.*)$/ && print "$1\n"')

	if echo $redurl | grep -q hosting/moved; then
		found=$(curl -L -s $url/checkout | sed -n 's/.*View the project at: <a href="\(.*\)">.*/\1/p')
		moved $url $found
		continue
	fi
	if [ -n "$redurl" ] && [ "$redurl" != "$url" ]; then
		moved $url $redurl
		continue
	fi
	
	found=$(curl -L -s $url/checkout | sed -n 's/.*<A HREF="\(.*\)">here<\/A>.*/\1/p')
	if [ -n "$found" ]; then
		moved $url $found
		continue
	fi
done

echo
