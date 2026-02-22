# Troubleshooting

Use this page when the screenshot command fails to find windows or fails to capture output.

## Import error for ScreenCaptureKit
- Symptom: `ImportError` requesting `pyobjc-framework-ScreenCaptureKit`.
- Cause: runtime dependency is missing.
- Fix: run `/opt/homebrew/opt/python@3.12/bin/python3.12 -m pip install -r pip_requirements.txt`.

## No matching window found
- Symptom: error says the window with the selected parent and title was not found.
- Cause: app name or title filter does not match an active window.
- Fix: retry with only the app name first, then add `--title` after confirming matches.

## Command runs but no screenshot is saved
- Symptom: tool exits with a `screencapture` output error.
- Cause: invalid output format flag or denied macOS screen capture permission.
- Fix: use one of `png`, `pdf`, `jpg`, `tiff` for `--output` and verify Screen Recording permission for your terminal app.

## Help and baseline checks
- Run `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture --help`.
- Run `source source_me.sh && /opt/homebrew/opt/python@3.12/bin/python3.12 -m pytest tests -q` to confirm repo health.

## Known gaps
- Add a section for CI or headless environments after those workflows are validated in this repo.
