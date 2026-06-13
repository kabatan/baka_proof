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

try:
    from pyvis.network import Network

    def _show_without_browser(self: Network, name: str, local: bool = True, notebook: bool = True) -> Any:
        self.write_html(name, local=local, notebook=notebook, open_browser=False)
        return None

    Network.show = _show_without_browser  # type: ignore[method-assign]
except Exception:
    pass
