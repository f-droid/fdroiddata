#!/bin/bash

# Fix TypographyEllipsis programmatically

exitvalue=0
for d in metadata/*/*; do
    test -d $d || continue
    test $(basename $d) != "signatures" || continue
    sed -i 's/\.\.\./…/g' $d/*.txt
    if [ $exitvalue = 0 ]; then
	git diff $d | grep -Eo '^\+.*…' || exitvalue=1
    fi
done


if [ $exitvalue != 0 ]; then
    echo Fix TypographyEllipsis
fi
exit $exitvalue
