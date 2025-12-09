#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path

import ruamel.yaml
from fdroidserver import common, metadata, update

BCP47_LOCALE_TAG_PATTERN = re.compile(r"[a-z]{2,3}(-([A-Z][a-zA-Z]+|\d+|[a-z]+))*")


def check_fastlane(app: metadata.App) -> list[dict[str, str]]:
    config = dict()
    common.fill_config_defaults(config)
    update.config = config
    for file in config["char_limits"].keys():
        config["char_limits"][file] += 1

    update.copy_triple_t_store_metadata({app.id: app})
    update.insert_localized_app_metadata({app.id: app})

    reports = []
    if not "localized" in app:
        reports.append(
            {
                "description": "Fastlane/Triple-T is not found",
                "fingerprint": "fastlane not found",
                "severity": "critical",
            }
        )
        return reports

    localized = app["localized"]
    if not localized.get("en-US") or not localized["en-US"].get("summary"):
        reports.append(
            {
                "description": "Fastlane/Triple-T for en-US not found or incomplete",
                "fingerprint": "fastlane en-US not found",
                "severity": "critical",
            }
        )
    for locale, v in localized.items():
        if not BCP47_LOCALE_TAG_PATTERN.fullmatch(locale):
            for replace in (("_", "-"), ("-r", "-"), ("_r", "-")):
                if BCP47_LOCALE_TAG_PATTERN.fullmatch(locale.replace(*replace)):
                    reports.append(
                        {
                            "description": f"Fastlane/Triple-T has invalid locale {locale}, maybe a typo of {locale.replace(*replace)}",
                            "fingerprint": f"fastlane invalid locale {locale}",
                            "severity": "major",
                        }
                    )
                    break
            else:
                reports.append(
                    {
                        "description": f"Fastlane/Triple-T has invalid locale {locale}",
                        "fingerprint": f"fastlane invalid locale {locale}",
                        "severity": "major",
                    }
                )

        for file, limit in config["char_limits"].items():
            if v.get(file) and len(v[file]) == limit:
                reports.append(
                    {
                        "description": f"Fastlane/Triple-T {file} in {locale} should be shorter than {limit - 1} characters",
                        "fingerprint": f"fastlane {locale} {file} exceed",
                        "severity": "minor",
                    }
                )

        items = list(v.keys())
        if (repo_dir := Path("repo") / app.id / locale).is_dir():
            for child in repo_dir.iterdir():
                if child.is_file():
                    items.append(child.stem)
                elif child.is_dir():
                    items.append(f"{child.name} ({len(list(child.iterdir()))})")

        reports.append(
            {
                "description": f"Fastlane/Triple-T in {locale}: {', '.join(items)}",
                "fingerprint": f"fastlane {locale} found",
                "severity": "info",
            }
        )

    return reports


def main():
    reports = []
    yaml = ruamel.yaml.YAML(typ="rt")
    for appid in sys.argv[1:]:
        print(f"Checking {appid}...", file=sys.stderr)
        metadata_file = f"metadata/{appid}.yml"
        app = metadata.parse_metadata(metadata_file)
        if not app.Builds:
            print(f"No build in {appid}, skip", file=sys.stderr)
            continue
        build = app.Builds[-1]
        if app.RepoType == "srclib":
            # fastlane in srclibs is not supported
            print(f"RepoType of {appid} is srclib, skip", file=sys.stderr)
            continue
        else:
            build_dir = Path("build") / appid
        vcs = common.getvcs(app.RepoType, app.Repo, build_dir)
        vcs.gotorevision(build.commit, True)
        if build.submodules:
            vcs.initsubmodules()
        app.Builds = [build]
        for b in (yaml.load(Path(metadata_file).read_text()) or {}).get("Builds", []):
            if b.get("versionCode") == build.versionCode:
                line_number = b.lc.line + 1
                break
        else:
            print(f"Can't find {build.versionCode} build in {metadata_file}, skip")
            continue
        reports.extend(
            [
                report
                | {
                    "location": {
                        "path": metadata_file,
                        "lines": {"begin": line_number},
                    },
                    "check_name": "fastlane",
                }
                for report in check_fastlane(app)
            ]
        )

    print(json.dumps(reports))


if __name__ == "__main__":
    main()
