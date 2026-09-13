#!/usr/bin/env python3
"""Merge this kit's Dev Container defaults into VS Code User settings.

- Unions extension IDs into dev.containers.defaultExtensions (does not remove extras).
- Copies keys from common-settings.json only when the user does not already have them.
"""
from __future__ import print_function

import json
import os
import shutil
import sys
from datetime import datetime


def kit_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)


def vscode_user_settings_path():
    override = os.environ.get("VSCODE_USER_SETTINGS")
    if override:
        return override
    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise SystemExit("APPDATA is not set")
        return os.path.join(appdata, "Code", "User", "settings.json")
    home = os.path.expanduser("~")
    if sys.platform == "darwin":
        return os.path.join(
            home, "Library", "Application Support", "Code", "User", "settings.json"
        )
    return os.path.join(home, ".config", "Code", "User", "settings.json")


def load_json(path, default):
    if not os.path.isfile(path):
        return default
    with open(path, "r") as f:
        text = f.read().strip()
    if not text:
        return default
    return json.loads(text)


def flatten_extensions(data):
    ids = []
    seen = set()
    if isinstance(data, list):
        seq = data
    else:
        seq = list(data.get("extensions") or [])
        if not seq:
            for key in ("common", "python"):
                seq.extend(data.get(key) or [])
    for ext in seq:
        if ext not in seen:
            seen.add(ext)
            ids.append(ext)
    return ids


def main():
    root = kit_root()
    grouped = load_json(os.path.join(root, "devcontainer", "extensions.json"), {})
    patch = load_json(os.path.join(root, "devcontainer", "common-settings.json"), {})
    wanted = flatten_extensions(grouped)
    settings_path = vscode_user_settings_path()
    user_dir = os.path.dirname(settings_path)
    if not os.path.isdir(user_dir):
        os.makedirs(user_dir)

    current = load_json(settings_path, {})
    if not isinstance(current, dict):
        raise SystemExit("%s is not a JSON object" % settings_path)

    if os.path.isfile(settings_path):
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = settings_path + ".bak-" + stamp
        shutil.copy2(settings_path, backup)
        print("backup %s" % backup)

    existing = current.get("dev.containers.defaultExtensions") or []
    if not isinstance(existing, list):
        existing = []
    merged = []
    seen = set()
    for ext in existing + wanted:
        if ext not in seen:
            seen.add(ext)
            merged.append(ext)
    current["dev.containers.defaultExtensions"] = merged

    added_settings = []
    for key, value in patch.items():
        if key not in current:
            current[key] = value
            added_settings.append(key)

    tmp = settings_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(current, f, indent=4, sort_keys=False)
        f.write("\n")
    os.replace(tmp, settings_path)

    print("wrote %s" % settings_path)
    print("defaultExtensions (%d): %s" % (len(merged), ", ".join(merged)))
    if added_settings:
        print("added settings: %s" % ", ".join(added_settings))
    else:
        print("no new editor settings (existing keys kept)")


if __name__ == "__main__":
    main()
