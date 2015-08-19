# Contributing to F-Droid

## Issue Tracker

You may use the issue tracker to report issues on app metadata and issues with
the packages distributed through our repository.

Please note that app submissions belong in the
[submission queue](https://f-droid.org/forums/forum/submission-queue/).

Before opening an issue about an outdated app, have a look at its metadata
file and make sure that updating the app is actually possible. Issues opened
about apps that can no longer be built will be closed.

## Merge Requests

### General recommendations

* [Squash](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html) your commits

### Setting up fdroiddata for merge requests

* [Register on GitLab](http://gitlab.com)

* Visit and fork the [fdroiddata repository](https://gitlab.com/fdroid/fdroiddata)

* Follow the [Quickstart](README.md#quickstart), but using the url
  `git@gitlab.com:yourusername/fdroiddata.git` when cloning

### Adding a new app

If you want to add a new app you will have to add a new metadata file to the
repository, like `metadata/app.id.txt`. Here is how to write that file.

* If the app is on GitHub, GitLab or Bitbucket, use `fdroid import`:

	fdroid import --url https://github.com/foo/bar --subdir app

* Alternatively, start the metadata file from scratch:

	cp templates/app-minimal metadata/app.id.txt

Now that the file is created, you need to fill up all the app information and
add a working build recipe.

You can use the [metadata section](https://f-droid.org/manual/html_node/Metadata.html)
in the manual for reference, or the full template at `templates/app-full` for
some suggestions.

As for the build recipe, you can have a look at the build templates at
`templates/build-*` for some quick suggestions. Otherwise, follow the manual
and look at how other apps are built.

* Once you're done, see if `fdroid readmeta` runs without any errors. If it
  doesn't, there are syntax errors in your metadata file.

* Run `fdroid rewritemeta app.id` to clean up your file

* Run `fdroid checkupdates app.id` to fill automated fields like `Auto Name`
  and `Current Version`

* Make sure that `fdroid lint app.id` doesn't report any warnings. If it does,
  fix them.

* Test your build recipe with `fdroid build -v -l app.id`

Congratulations! You can now open a merge request to add your app.

Our buildserver runs builds once a day, so it may take up to 24h for your app
to appear in our repository.
