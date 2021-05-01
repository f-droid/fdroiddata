<!--Please make sure your branch is not protected. See https://docs.gitlab.com/ee/user/project/protected_branches.html. We enable fast-forward merges by default. If your branch is protected, we can't rebase it before merge it.-->
* [ ] The app complies with the [inclusion criteria](https://f-droid.org/docs/Inclusion_Policy)
* [ ] The original app author has been notified (and does not oppose the inclusion)<!--If you are not the author, please paste the link of the reply from the author.-->
* [ ] All related [fdroiddata](https://gitlab.com/fdroid/fdroiddata/issues) and [RFP issues](https://gitlab.com/fdroid/rfp/issues) have been referenced in this merge request
* [ ] The upstream app source code repo contains the app metadata _(summary/description/images/changelog/etc)_ in a [Fastlane](https://gitlab.com/snippets/1895688) or [Triple-T](https://gitlab.com/snippets/1901490) folder structure<!--If you are the author, please do add metadata in your repo; If you are not the author, please at least open an issue upstream for the metadata.-->
* [ ] Builds with `fdroid build`
* [ ] Releases are tagged

---------------------

<!--Add the corresponding issue number or remove this if this merge request does not close an issue at rfp.-->
Closes rfp#<RFP issue number>

<!--Add the corresponding issue number or remove this if this merge request does not close an issue at fdroiddata.-->
Closes fdroiddata#<fdroiddata issue number>

/label ~"New App"
