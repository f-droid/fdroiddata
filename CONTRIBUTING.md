# Contributing to F-Droid

Thanks so much for contributing to [F-Droid](https://f-droid.org)! Please take
your time to read carefully through this document:

## Issue Tracker

Please note that the tracker is not for app submissions, use the
[submission queue](https://f-droid.org/forums/forum/submission-queue/) instead.

For error reports please provide detailed system (e.g. Android version, used
ROM, hardware specifications) and error information (e.g. What happened? When
did it happen?) and provide the [logcat](https://developer.android.com/tools/help/logcat.html)
-- either by file upload or by inclduing it with the appropriated
[markdown](https://github.com/gitlabhq/gitlabhq/blob/master/doc/markdown/markdown.md).

For update/change requests, please make sure they meet our
[inclusion policy](https://f-droid.org/wiki/page/Inclusion_Policy) and are not already
handled by our [submission queue](https://f-droid.org/forums/forum/submission-queue/),
are not [held](https://f-droid.org/forums/forum/submission-held/) for some reason or already
[marked for an update](https://f-droid.org/wiki/page/Category:Apps_to_Update).
Keep discussions to a minimum or use the forum instead.

However, the easiest way to get an app included, updated or an error fixed is
to provide the required metadata yourself by opening a merge request.

## Merge Requests

Please read through the [inclusion howto](https://f-droid.org/wiki/page/Inclusion_How-To),
the [inclusion policy](https://f-droid.org/wiki/page/Inclusion_Policy) and our
[fdroid manual](https://f-droid.org/manual/fdroid.html).

This section includes some information on the fdroidserver repository as the
tools contained in there can be used standalone to check and build local
metadata files.

### Setting up fdroidserver and build tools

* Follow the instructions in [the manual](https://f-droid.org/manual).

### Setting up fdroiddata and submitting apps

* [Register on GitLab](http://gitlab.com)

* Visit and fork the [fdroiddata repository](https://gitlab.com/fdroid/fdroiddata/)

* Clone your fdroiddata fork

* Copy fdroiddata/metadata/template or fdroiddata/metadata/template-minimal to
  fdroiddata/metadata/app.id.txt

* Update metadata/app.id.txt according to the [manual](https://f-droid.org/manual/html_node/Metadata.html)

* If you have fdroidserver installed:

 * Copy and adjust fdroidserver/examples/config.py to fdroiddata/config.py

 * Instead of copying a template you can run `fdroid import -u github-url` if
   the app is hosted on GitHub

 * Run `fdroid checkupdates app.id`, `fdroid rewritemeta app.id` and `fdroid
   build -v -t -l app.id` before opening a merge request!

* Use `git add`, `git commit` and `git push` to update your fork on GitLab.
  Please squash multiple commits into a single one per app. It's a good style
  to use a separate branch for each app and prefix commit messages with
  "Appname:". For this you might also want to look at the `fd-commit` command
  in the server repo

* Open a merge request via GitLab
