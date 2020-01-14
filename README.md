# F-Droid Data

[![build status](https://gitlab.com/fdroid/fdroiddata/badges/master/build.svg)](https://gitlab.com/fdroid/fdroiddata/builds)
[![Liberapay receiving](https://img.shields.io/liberapay/receives/F-Droid-Data.svg)
 ![Donate](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/F-Droid-Data/)
**[Current Buildserver Activity](https://f-droid.org/wiki/index.php?title=Special:RecentChanges&days=7&from=&hidebots=0&hideanons=1&hideliu=1&limit=500)**

Build logs can be found at `https://f-droid.org/repo/$APPID_$VERCODE.log.gz`.

This repository holds general and build information for all the apps on our
main repo on f-droid.org.

## Quickstart

Install [fdroidserver](https://gitlab.com/fdroid/fdroidserver), or just
use it directly from master:

	git clone https://gitlab.com/fdroid/fdroidserver.git
	export PATH="$PATH:$PWD/fdroidserver"

Clone fdroiddata (or your fork) and enter it:

	git clone https://gitlab.com/fdroid/fdroiddata.git
	cd fdroiddata

Optionally create a base config.py and signing keys with:

    fdroid init

Make sure fdroid works and reads the metadata files properly:

	fdroid readmeta

## Contributing

See the [Contributing](CONTRIBUTING.md) doc.

## More information

You can find more details on the [docs](https://f-droid.org/docs/).

## Translation

Many app summaries and some descriptions can be translated as part of F-Droid. See [Translation and Localization](https://f-droid.org/docs/Translation_and_Localization)
for more info.

[![translation status](https://hosted.weblate.org/widgets/f-droid/-/fdroiddata/multi-auto.svg)](https://hosted.weblate.org/engage/f-droid/?utm_source=widget)
