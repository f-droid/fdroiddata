# F-Droid Data

[![build status](https://gitlab.com/fdroid/fdroiddata/badges/master/build.svg)](https://gitlab.com/fdroid/fdroiddata/builds)

This repository holds general and build information for all the apps on our
main repo on f-droid.org.

## Quickstart

Install [fdroidserver](https://gitlab.com/fdroid/fdroidserver), or just
use it directly from master:

	git clone https://gitlab.com/fdroid/fdroidserver.git
	export PATH="$PATH:$PWD/fdroidserver"

Enter your fdroiddata clone:

	cd fdroiddata

An empty config file should work for most setups:

	touch config.py

Make sure fdroid works and reads the metadata files properly:

	fdroid readmeta

## Contributing

See the [Contributing](CONTRIBUTING.md) doc.

## More information

You can find more details on [the manual](https://f-droid.org/manual/).
