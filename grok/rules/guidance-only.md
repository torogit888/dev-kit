# Guidance Only — Do Not Run Heavy Ops

## Default behavior
- Prefer **explaining how** over **doing it for me**.
- Give clear, copy-pasteable commands and steps I can run myself.
- Do **not** execute compile / build / Docker / test steps unless I explicitly ask in that turn.

## Do not run unless I explicitly ask
- **Compile / build**: do not run build scripts, packaging, image builds, or install/compile heavy deps.
- **Docker**: do not start/stop containers, `docker compose`, `runDocker.sh`, image builds, or similar.
- **Tests**: do not run unit tests, UAT, pytest, or `script/runUnitTest`.

When those are needed, **tell me the exact command(s)** and stop. Wait for me to run them (or to explicitly ask you to run them).

## Ask before long-running steps
Before any step that may take a long time (e.g. Docker bring-up, full test suites, large downloads, long builds, background servers), **ask me to choose** first. Present options (run myself / ask you to run / skip) and wait.

## Allowed without asking
- Reading, searching, and explaining code
- Small, reversible local edits I requested
- Short non-destructive inspect commands (e.g. `ls`, `git status`, reading a file)

## Conflict note
If a project `AGENTS.md` documents how to build/test with Docker, treat that as **documentation for me**, not as permission for you to run those commands automatically.
