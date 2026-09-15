#!/usr/bin/env python3
"""Sync private project tasks from dev-kit/projects/<project>/tasks.json to <project>/.vscode/tasks.json.

- Ensures tasks are workspace-specific (only appear in that project).
- Ensures tasks are never tracked in the project's Git (adds to .git/info/exclude).
- All source definitions are tracked in dev-kit's Git.
"""
from __future__ import print_function

import os
import shutil
import sys


def kit_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)


def main():
    root = kit_root()
    projects_dir = os.path.join(root, "projects")
    if not os.path.isdir(projects_dir):
        return

    workspace_parent = os.path.dirname(root)

    for project_name in os.listdir(projects_dir):
        proj_src_dir = os.path.join(projects_dir, project_name)
        src_tasks = os.path.join(proj_src_dir, "tasks.json")
        if not os.path.isfile(src_tasks):
            continue

        target_project_dir = os.path.join(workspace_parent, project_name)
        if not os.path.isdir(target_project_dir):
            # 支援大小寫微調嘗試
            found = False
            for entry in os.listdir(workspace_parent):
                if entry.lower() == project_name.lower():
                    target_project_dir = os.path.join(workspace_parent, entry)
                    found = True
                    break
            if not found:
                print("略過 %s（父層目錄中未找到 %s 專案資料夾）" % (project_name, project_name))
                continue

        target_vscode = os.path.join(target_project_dir, ".vscode")
        if not os.path.isdir(target_vscode):
            os.makedirs(target_vscode)

        dest_tasks = os.path.join(target_vscode, "tasks.json")
        shutil.copy2(src_tasks, dest_tasks)

        # 雙重防護：確保寫入該專案本地 .git/info/exclude
        git_exclude = os.path.join(target_project_dir, ".git", "info", "exclude")
        if os.path.isfile(git_exclude):
            with open(git_exclude, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if ".vscode/" not in content and ".vscode" not in content:
                with open(git_exclude, "a", encoding="utf-8") as f:
                    f.write("\n.vscode/\n")

        print("已同步工作區專屬任務：%s -> %s (已排除於該專案 Git)" % (project_name, dest_tasks))


if __name__ == "__main__":
    main()
