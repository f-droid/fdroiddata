<!--Please make sure your repo is public and your branch is not protected. See https://docs.gitlab.com/ee/user/project/protected_branches.html. We enable fast-forward merges by default. If your branch is protected, we can't rebase it before merge it.-->
## Required
<!--Please ensure that your MR meet following requirements-->
* [ ] The app complies with the [inclusion criteria](https://f-droid.org/docs/Inclusion_Policy)
* [ ] The original app author has been notified (and does not oppose the inclusion) <!--If you are not the author, please paste the link of the reply from the author.-->
* [ ] All related [fdroiddata](https://gitlab.com/fdroid/fdroiddata/issues) and [RFP issues](https://gitlab.com/fdroid/rfp/issues) have been referenced in this merge request
* [ ] Builds with `fdroid build`

## Strongly Recommended
<!--We highly encourage you doing these thing.-->
* [ ] The upstream app source code repo contains the app metadata _(summary/description/images/changelog/etc)_ in a [Fastlane](https://gitlab.com/snippets/1895688) or [Triple-T](https://gitlab.com/snippets/1901490) folder structure <!--If you are the author, please do add metadata in your repo; If you are not the author, please at least open an issue upstream for the metadata. With metadata in your repo, you can maintain it directly.-->
* [ ] Releases are tagged <!--Our autoupdate workflow relies on the tag. Without this you have to add every version manually.-->

## Suggested
<!--These suggestions may be difficult to apply on your app. Please have a try.-->
* [ ] External repos are added as git submodules instead of srclibs <!--You can update git submodules without opening an MR in this repo and the submodule is covered by our scanner.-->
* [ ] Enable [Reproducible Builds](https://f-droid.org/docs/Reproducible_Builds) <!--We'll use your signature for improved security/reliability, also allowing users to switch between different channels.-->
* [ ] Multiple apks for native code <!--If your app has native code and the size is large, please consider building multiple apks instead of one universal apk.-->

---------------------

<!--Add the corresponding issue number or remove this if this merge request does not close an issue at rfp.-->
Closes rfp#<RFP issue number>

<!--Add the corresponding issue number or remove this if this merge request does not close an issue at fdroiddata.-->
Closes fdroiddata#<fdroiddata issue number>

/label ~"New App"
