# F-Droid Data

[![build status](https://gitlab.com/ci/projects/5274/status.png?ref=master)](https://gitlab.com/ci/projects/5274?ref=master)

This repository holds general and build information for all the apps on our
main repo on f-droid.org.

## Quickstart

Clone [fdroidserver](https://gitlab.com/fdroid/fdroidserver):

	git clone https://gitlab.com/fdroid/fdroidserver.git

Add the cloned dir to your `PATH`:

	export PATH="$PATH:$PWD/fdroidserver"

Enter it:

	cd fdroiddata

An empty configuration file should work as a start:

	touch config.py

Make sure fdroid works and reads the metadata files properly:

	fdroid readmeta

## Contributing

See the [Contributing](CONTRIBUTING.md) doc.

## More information

You can find more details on [the manual](https://f-droid.org/manual/).
