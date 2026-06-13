from __future__ import annotations

import os
import webbrowser
from typing import Any


def _blocked_open(*_args: Any, **_kwargs: Any) -> bool:
    return False


webbrowser.open = _blocked_open
webbrowser.open_new = _blocked_open
webbrowser.open_new_tab = _blocked_open

if hasattr(os, "startfile"):
    os.startfile = _blocked_open  # type: ignore[attr-defined]
