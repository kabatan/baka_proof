from __future__ import annotations

import sys
from pathlib import Path

import newclid.api
import newclid.webapp
from newclid.__main__ import main


def _pull_to_server_no_browser(*_args: object, server_path: Path, **_kwargs: object) -> None:
    server_path.mkdir(parents=True, exist_ok=True)


newclid.api.pull_to_server = _pull_to_server_no_browser
newclid.webapp.pull_to_server = _pull_to_server_no_browser


if __name__ == "__main__":
    main()
