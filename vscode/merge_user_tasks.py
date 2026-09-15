#!/usr/bin/env python3
"""Merge this kit's tasks.json into VS Code User tasks.json.

- Unions tasks by `label` (does not overwrite existing user tasks).
- Preserves user custom tasks.
"""
from __future__ import print_function

import json
import os
import re
import shutil
import sys
from datetime import datetime


def kit_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)


def vscode_user_tasks_path():
    override = os.environ.get("VSCODE_USER_TASKS")
    if override:
        return override
    override_settings = os.environ.get("VSCODE_USER_SETTINGS")
    if override_settings:
        return os.path.join(os.path.dirname(override_settings), "tasks.json")
    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise SystemExit("APPDATA is not set")
        return os.path.join(appdata, "Code", "User", "tasks.json")
    home = os.path.expanduser("~")
    if sys.platform == "darwin":
        return os.path.join(
            home, "Library", "Application Support", "Code", "User", "tasks.json"
        )
    return os.path.join(home, ".config", "Code", "User", "tasks.json")


def load_json(path, default):
    if not os.path.isfile(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return default
    try:
        return json.loads(text)
    except Exception:
        # 移除 // 單行註解後再試一次，相容 VS Code jsonc 格式
        cleaned = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
        return json.loads(cleaned)


def main():
    root = kit_root()
    kit_tasks_file = os.path.join(root, "vscode", "tasks.json")
    if not os.path.isfile(kit_tasks_file):
        print("未找到 %s，略過 tasks 合併" % kit_tasks_file)
        return

    incoming_doc = load_json(kit_tasks_file, {})
    incoming_tasks = incoming_doc.get("tasks", [])
    if not incoming_tasks:
        print("tasks.json 內無 task 定義")
        return

    tasks_path = vscode_user_tasks_path()
    user_dir = os.path.dirname(tasks_path)
    if not os.path.isdir(user_dir):
        os.makedirs(user_dir)

    current_doc = load_json(tasks_path, {"version": "2.0.0", "tasks": []})
    if not isinstance(current_doc, dict):
        raise SystemExit("%s is not a JSON object" % tasks_path)

    if "version" not in current_doc:
        current_doc["version"] = incoming_doc.get("version", "2.0.0")

    existing_tasks = current_doc.get("tasks")
    if not isinstance(existing_tasks, list):
        existing_tasks = []
        current_doc["tasks"] = existing_tasks

    task_map = {
        t.get("label"): i for i, t in enumerate(existing_tasks) if isinstance(t, dict) and "label" in t
    }

    added = []
    updated = []
    for task in incoming_tasks:
        if not isinstance(task, dict):
            continue
        label = task.get("label")
        if not label:
            continue
        if label in task_map:
            idx = task_map[label]
            if existing_tasks[idx] != task:
                existing_tasks[idx] = task
                updated.append(label)
        else:
            existing_tasks.append(task)
            task_map[label] = len(existing_tasks) - 1
            added.append(label)

    changed = bool(added or updated)
    if os.path.isfile(tasks_path) and changed:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = tasks_path + ".bak-" + stamp
        shutil.copy2(tasks_path, backup)
        print("backup %s" % backup)

    if changed or not os.path.isfile(tasks_path):
        tmp = tasks_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(current_doc, f, indent=4, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, tasks_path)
        print("wrote %s" % tasks_path)

    if added:
        print("added user tasks (%d): %s" % (len(added), ", ".join(added)))
    if updated:
        print("updated user tasks (%d): %s" % (len(updated), ", ".join(updated)))
    if not changed:
        print("no changes in user tasks (all up to date)")


if __name__ == "__main__":
    main()
