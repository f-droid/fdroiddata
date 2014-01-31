#!/bin/sh
#
# this replaces http:// urls with https:// urls on all sites that default to
# https, or support it well.  This is important even for downloads that are
# verified using a hash sum or signature because it both provides an
# alternate, backup method of verifying the download, but also greatly reduces
# meta data leaks.

for f in *.txt; do
    printf `echo $f | cut -b1`
    sed -i 's,http://dl.google.com,https://dl.google.com,g' $f
    sed -i 's,http://pypi,https://pypi,g' $f
    sed -i 's,http://code.google.com,https://code.google.com,g' $f
    sed -i 's,http://github.com,https://github.com,g' $f
    sed -i 's,http://\([^.]*\).googlecode.com/svn,https://\1.googlecode.com/svn,g' $f
    sed -i 's,http://svn.apache.org/repos,https://svn.apache.org/repos,g' $f
    sed -i 's,http://svn.code.sf.net,https://svn.code.sf.net,g' $f
    sed -i 's,http://gitorious.org,https://gitorious.org,g' $f
done
echo ""
