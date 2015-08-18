#!/bin/sh
#
# this replaces http:// urls with https:// urls on all sites that default to
# https, or support it well.  This is important even for downloads that are
# verified using a hash sum or signature because it both provides an
# alternate, backup method of verifying the download, but also greatly reduces
# meta data leaks.

for f in metadata/*.txt; do
	# this shows progress based on 1st letter of package name
	printf `echo $f | cut -b10`
	sed -i -e 's,http://dl.google.com,https://dl.google.com,g' \
		-e 's,http://pypi,https://pypi,g' \
		-e 's,http://code.google.com,https://code.google.com,g' \
		-e 's,http://github.com,https://github.com,g' \
		-e 's,git://github.com,https://github.com,g' \
		-e 's,http://\([^.]*\).googlecode.com/svn,https://\1.googlecode.com/svn,g' \
		-e 's,http://svn.apache.org/repos,https://svn.apache.org/repos,g' \
		-e 's,http://svn.code.sf.net,https://svn.code.sf.net,g' \
		-e 's,svn://svn.code.sf.net,https://svn.code.sf.net,g' \
		-e 's,http://gitorious.org,https://gitorious.org,g' \
		-e 's,git://gitorious.org,https://gitorious.org,g' $f
done
echo
