# Some tools for F-Droid Data written in Python

## audit-gradle.py

## build-contains-signatures.py
### Dependencies
- [colorama]

## check-for-unattached-signatures.py
> Apps with reproducible builds include the APK Signature files in the
> metadata.  If there is no matching entry in Builds:, then those
> files are useless cruft.

### Dependencies
- [PyYAML]

## check-git-repo-availability.py
### Dependencies
- [colorama]
- [PyYAML]

## check-keyalias-collision.py

## check-localized-metadata.py

## check-metadata-summary-whitespace.py

## find-changed-builds.py
### Dependencies
- [colorama]
- [PyYAML]

## make-summary-translatable.py
### Dependencies
- [PyYAML]

## rewrite-git-redirects.py
### Dependencies
- [PyYAML]

## schedule-issuebot.py
### Dependencies
- [python-gitlab]


[colorama]: https://pypi.org/project/colorama
[PyYAML]: https://pypi.org/project/PyYAML
[python-gitlab]: https://pypi.org/project/python-gitlab
