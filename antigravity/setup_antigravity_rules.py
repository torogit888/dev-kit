#!/usr/bin/env python3
"""Install Antigravity (Gemini) global guidance-only instructions into ~/.gemini.

Targets:
1. Global GEMINI.md:
   - ~/.gemini/GEMINI.md
2. Global Antigravity Config Rules:
   - ~/.gemini/config/rules/guidance-only.md
   - ~/.gemini/antigravity/rules/guidance-only.md
"""
from __future__ import print_function

import os
import shutil
import sys


def kit_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)


def gemini_home_dir():
    override = os.environ.get("GEMINI_HOME") or os.environ.get("ANTIGRAVITY_HOME")
    if override:
        return override
    home = os.path.expanduser("~")
    return os.path.join(home, ".gemini")


def main():
    root = kit_root()
    src = os.path.join(root, "antigravity", "rules", "guidance-only.md")
    if not os.path.isfile(src):
        raise SystemExit("missing source rule: %s" % src)

    gemini_home = gemini_home_dir()
    if not os.path.isdir(gemini_home):
        os.makedirs(gemini_home)

    # 1. ~/.gemini/GEMINI.md
    dest_gemini_md = os.path.join(gemini_home, "GEMINI.md")
    shutil.copy2(src, dest_gemini_md)
    print("wrote Antigravity global rule: %s" % dest_gemini_md)

    # 2. ~/.gemini/config/rules/guidance-only.md
    config_rules_dir = os.path.join(gemini_home, "config", "rules")
    if not os.path.isdir(config_rules_dir):
        os.makedirs(config_rules_dir)
    dest_config_rule = os.path.join(config_rules_dir, "guidance-only.md")
    shutil.copy2(src, dest_config_rule)
    print("wrote Antigravity config rule: %s" % dest_config_rule)

    # 3. ~/.gemini/antigravity/rules/guidance-only.md (if antigravity dir exists or create it)
    antigravity_rules_dir = os.path.join(gemini_home, "antigravity", "rules")
    if not os.path.isdir(antigravity_rules_dir):
        os.makedirs(antigravity_rules_dir)
    dest_antigravity_rule = os.path.join(antigravity_rules_dir, "guidance-only.md")
    shutil.copy2(src, dest_antigravity_rule)
    print("wrote Antigravity rules dir: %s" % dest_antigravity_rule)


if __name__ == "__main__":
    main()

