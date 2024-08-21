**Please make sure your repo is public and your branch is not protected. See https://docs.gitlab.com/ee/user/project/protected_branches.html. We enable fast-forward merges by default. If your branch is protected, we can't rebase it before merge it.**

**Please read [the guide](https://gitlab.com/fdroid/fdroiddata/-/blob/master/CONTRIBUTING.md) first if this is your first contribution. Please make sure your metadata follows the best practice in [our templates](https://gitlab.com/fdroid/fdroiddata/tree/master/templates).**

**Please try your best to make sure all pipelines passed before open a merge request. If a test pipeline fails please check the log. Please check that the build pipeline does build your app. If the build pipeline succeeds but there is no APK files produced then you may have a mistake. Please check if you disable the build. Do not submit a metadata generated with `fdroid import` directly, please remove the disable line at least. Please check if the metadata file is in the correct path. It must be put in `metadata/` and the extension must be `.yml`.**

**After all pipelines pass you can trigger the issue bot manually but do not trigger it too much which bloats the merge request.**

**F-Droid CI runners are under Gitlab's FOSS program, so there's no need for you to pay for any CI time. If Gitlab starts asking for phone numbers or credit cards don't submit anything, just leave a note in the MR so we know we need to trigger the CI.**

**Please remove above lines!**


## Required
<!--Please ensure that your MR meet following requirements-->
* [ ] The app complies with the [inclusion criteria](https://f-droid.org/docs/Inclusion_Policy)
* [ ] The original app author has been notified (and does not oppose the inclusion) <!--If you are not the author, please paste the link of the reply from the author.-->
* [ ] All related [fdroiddata](https://gitlab.com/fdroid/fdroiddata/issues) and [RFP issues](https://gitlab.com/fdroid/rfp/issues) have been referenced in this merge request
* [ ] Builds with `fdroid build` and all pipelines pass

## Strongly Recommended
<!--We highly encourage you doing these things. They are not hard requirements but unless there are special reasons they are required.-->
* [ ] The upstream app source code repo contains the app metadata _(summary/description/images/changelog/etc)_ in a [Fastlane](https://gitlab.com/snippets/1895688) or [Triple-T](https://gitlab.com/snippets/1901490) folder structure <!--If you are the author, please do add metadata in your repo; If you are not the author, please at least open an issue upstream for the metadata. With metadata in your repo, you can maintain it directly.-->
* [ ] Releases are tagged <!--Our autoupdate workflow relies on the tag. Without this you have to add every version manually.-->

## Suggested
<!--These suggestions may be difficult to apply on your app. Please have a try.-->
* [ ] External repos are added as git submodules instead of srclibs <!--You can update git submodules without opening an MR in this repo and the submodule is covered by our scanner.-->
* [ ] Enable [Reproducible Builds](https://f-droid.org/docs/Reproducible_Builds) <!--We'll use your signature for improved security/reliability, also allowing users to switch between different channels. If you don't want reproducible build, please add `No, I don't want this.` here.-->
* [ ] Multiple apks for native code <!--If your app has native code and the size is large, please consider building multiple APK files instead of one universal apk.-->

---------------------

<!--Add the corresponding issue number or remove this if this merge request does not close an issue at rfp.-->
Closes rfp#<RFP issue number>

<!--Add the corresponding issue number or remove this if this merge request does not close an issue at fdroiddata.-->
Closes fdroiddata#<fdroiddata issue number>

/label ~"New App"
