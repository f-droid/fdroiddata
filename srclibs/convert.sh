#!/bin/zsh

repo=false
writing=false

while read -r line; do
    if $repo; then
        echo "Repo:${${line%\'*}#*\'}\n" >> $file
        repo=false
    elif $writing; then
        if [[ "$line" == *"pp.close()"* ]]; then
            writing=false
            echo "\" >> project.properties\n" >> $file
        else
            echo -nE "${${line%\'*}#*\'}" >> $file
        fi
    elif [[ "$line" == *"getvcs("* ]]; then
        echo "Repo Type:${${line%\'*}#*\'}" >> $file
        repo=true
    elif [[ "$line" == *"libdir = "* ]]; then
        echo "Subdir:${${line%\'*}#*\'}\n" >> $file
    elif [[ "$line" == *"'update', 'project'"* ]]; then
        echo "Update Project:Yes\n" >> $file
    elif [[ "$line" == *"pp = open("* ]]; then
        writing=true
        echo -n "Prepare:echo \"" >> $file
    elif [[ "$line" == "if name =="* ]]; then
        cur=${${line%\'*}#*\'}
        file=$cur.txt
        : >! $file
    fi
done < source
