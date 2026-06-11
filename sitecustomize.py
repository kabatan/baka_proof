from __future__ import annotations

import sys
from pathlib import Path

src = Path(__file__).resolve().parent / "src"
if src.is_dir():
    src_text = str(src)
    if src_text not in sys.path:
        sys.path.insert(0, src_text)
