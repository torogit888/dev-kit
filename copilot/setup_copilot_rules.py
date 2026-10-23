#!/usr/bin/env python3
"""Install Copilot global guidance-only instructions into VS Code User prompts and ~/.copilot.

Targets:
1. VS Code User prompts folder:
   - Windows: %APPDATA%/Code/User/prompts/guidance-only.instructions.md
   - macOS: ~/Library/Application Support/Code/User/prompts/guidance-only.instructions.md
   - Linux: ~/.config/Code/User/prompts/guidance-only.instructions.md
2. Copilot CLI / Agent home:
   - ~/.copilot/copilot-instructions.md
"""
from __future__ import print_function

import os
import re
import shutil
import sys


def kit_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)


def vscode_user_dir():
    override = os.environ.get("VSCODE_USER_SETTINGS")
    if override:
        return os.path.dirname(override)
    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise SystemExit("APPDATA is not set")
        return os.path.join(appdata, "Code", "User")
    home = os.path.expanduser("~")
    if sys.platform == "darwin":
        return os.path.join(home, "Library", "Application Support", "Code", "User")
    return os.path.join(home, ".config", "Code", "User")


def strip_frontmatter(text):
    return re.sub(r"^---\r?\n.*?\r?\n---\r?\n*", "", text, count=1, flags=re.DOTALL)


def main():
    root = kit_root()
    src = os.path.join(root, "copilot", "rules", "guidance-only.instructions.md")
    if not os.path.isfile(src):
        raise SystemExit("missing source rule: %s" % src)

    # 1. Copy to VS Code User prompts folder (*.instructions.md)
    user_dir = vscode_user_dir()
    prompts_dir = os.path.join(user_dir, "prompts")
    if not os.path.isdir(prompts_dir):
        os.makedirs(prompts_dir)
    dest_vscode = os.path.join(prompts_dir, "guidance-only.instructions.md")
    shutil.copy2(src, dest_vscode)
    print("wrote VS Code user instruction: %s" % dest_vscode)

    # 2. Copy body to ~/.copilot/copilot-instructions.md for Copilot CLI / SDK
    copilot_home = os.environ.get("COPILOT_HOME") or os.path.join(os.path.expanduser("~"), ".copilot")
    if not os.path.isdir(copilot_home):
        os.makedirs(copilot_home)
    dest_copilot_cli = os.path.join(copilot_home, "copilot-instructions.md")
    with open(src, "r", encoding="utf-8") as f:
        raw_content = f.read()
    body_content = strip_frontmatter(raw_content)
    with open(dest_copilot_cli, "w", encoding="utf-8") as f:
        f.write(body_content)
    print("wrote Copilot CLI instruction: %s" % dest_copilot_cli)


if __name__ == "__main__":
    main()
