import time
from typing import Iterator

try:
	import CoreFoundation
	import ScreenCaptureKit
except ImportError as ex:
	raise ImportError(
		"Please install pyobjc-framework-ScreenCaptureKit via pip and then try again."
	) from ex


WindowInfo = dict[str, str | int | bool]

WINDOW_OPTIONS = {
	"exclude_desktop": "Exclude desktop windows from the shareable content query.",
	"on_screen_only": "Include only windows currently on screen.",
}

USER_OPTS_STR = "exclude_desktop on_screen_only"


class WindowLookupEx(Exception):
	pass


def parse_window_options(options: str) -> tuple[bool, bool]:
	"""
	Convert option tokens into ScreenCaptureKit shareable-content flags.
	"""
	option_names = [token for token in options.split() if token]
	unknown = [token for token in option_names if token not in WINDOW_OPTIONS]
	if unknown:
		unknown_text = ", ".join(sorted(set(unknown)))
		raise WindowLookupEx(f"Unknown window selection options: {unknown_text}")
	exclude_desktop = "exclude_desktop" in option_names
	on_screen_only = "on_screen_only" in option_names
	return exclude_desktop, on_screen_only


def get_window_info(options: str = USER_OPTS_STR, timeout_seconds: float = 5.0) -> list[WindowInfo]:
	"""
	Query shareable windows via ScreenCaptureKit.
	"""
	exclude_desktop, on_screen_only = parse_window_options(options)
	content_state: dict[str, object] = {"content": None, "error": None, "done": False}

	def completion_handler(content, error):
		content_state["content"] = content
		content_state["error"] = error
		content_state["done"] = True

	ScreenCaptureKit.SCShareableContent.getShareableContentExcludingDesktopWindows_onScreenWindowsOnly_completionHandler_(
		exclude_desktop,
		on_screen_only,
		completion_handler,
	)

	deadline = time.monotonic() + timeout_seconds
	while not content_state["done"] and time.monotonic() < deadline:
		CoreFoundation.CFRunLoopRunInMode(CoreFoundation.kCFRunLoopDefaultMode, 0.05, False)

	if not content_state["done"]:
		raise WindowLookupEx("Timed out waiting for ScreenCaptureKit shareable content.")

	if content_state["error"] is not None:
		raise WindowLookupEx(str(content_state["error"]))

	content = content_state["content"]
	if content is None:
		return []

	windows = []
	for window in content.windows():
		owner_app = window.owningApplication()
		owner = ""
		if owner_app is not None:
			owner_name = owner_app.applicationName()
			owner = str(owner_name) if owner_name else ""
		title_value = window.title()
		title = str(title_value) if title_value else ""
		window_id = int(window.windowID())
		on_screen = bool(window.isOnScreen())
		active = bool(window.isActive())
		windows.append(
			{
				"window_id": window_id,
				"owner_name": owner,
				"title": title,
				"is_on_screen": on_screen,
				"is_active": active,
			}
		)
	return windows


def gen_ids_from_info(windows: list[WindowInfo]) -> Iterator[tuple[int, str, str]]:
	for win_dict in windows:
		owner = str(win_dict.get("owner_name", ""))
		name = str(win_dict.get("title", ""))
		num = int(win_dict.get("window_id", 0))
		yield num, owner, name


def print_window_ids(windows):
	for info in windows:
		print(*info)


def gen_window_ids(parent: str, title: str = "", options: str = USER_OPTS_STR) -> Iterator[int]:
	windows = get_window_info(options)
	parent, title = parent.lower(), title.lower()

	for num, owner, name in gen_ids_from_info(windows):
		if parent in owner.lower():
			if title:
				if title in name.lower():
					yield num
			else:
				yield num
