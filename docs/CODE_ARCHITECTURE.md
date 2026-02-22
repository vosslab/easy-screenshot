# Code architecture

This repository provides a small Python CLI package for targeted macOS window screenshots.

## Components
- `screenshot/screencapture.py`: CLI entry logic, option parsing, and screenshot execution.
- `screenshot/get_window_id.py`: Quartz integration for window listing and filtering by app/title.
- `tests/`: policy and quality gates for lint, imports, ASCII compliance, indentation, and security checks.
- `devel/commit_changelog.py`: development helper script for changelog-related workflow.

## Runtime flow
- CLI receives `APPLICATION_NAME` and options.
- Window selection options are translated to a Quartz bitmask.
- Matching window ids are generated from window metadata.
- The command calls macOS `screencapture` with selected window ids and output options.

## Error handling
- Domain errors are wrapped as `ScreencaptureEx`.
- CLI exits with status `0` on success and `1` on command or lookup failure.

## Known gaps
- Add a call graph section if additional modules are introduced.
