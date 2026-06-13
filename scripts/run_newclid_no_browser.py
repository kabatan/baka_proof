from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parent / "no_browser_sitecustomize").resolve()))
import sitecustomize  # noqa: F401,E402

import newclid.api
import newclid.webapp
from newclid.__main__ import main
from pyvis.network import Network


def _pull_to_server_no_browser(*_args: object, server_path: Path, **_kwargs: object) -> None:
    server_path.mkdir(parents=True, exist_ok=True)


newclid.api.pull_to_server = _pull_to_server_no_browser
newclid.webapp.pull_to_server = _pull_to_server_no_browser


def _show_without_browser(self: Network, name: str, local: bool = True, notebook: bool = True) -> object:
    self.write_html(name, local=local, notebook=notebook, open_browser=False)
    return None


Network.show = _show_without_browser  # type: ignore[method-assign]


if __name__ == "__main__":
    main()
