from __future__ import annotations

import re


class ProofRegionGuard:
    start_pattern = re.compile(r"--\s*PROOF-REGION-START:[A-Za-z0-9_.:-]+")
    end_pattern = re.compile(r"--\s*PROOF-REGION-END:[A-Za-z0-9_.:-]+")

    def outside_regions(self, text: str) -> str:
        kept: list[str] = []
        in_region = False
        for line in text.splitlines():
            if self.start_pattern.match(line.strip()):
                in_region = True
                continue
            if self.end_pattern.match(line.strip()):
                in_region = False
                continue
            if not in_region:
                kept.append(line)
        return "\n".join(kept)

    def permits(self, original: str, candidate: str) -> bool:
        return self.outside_regions(original) == self.outside_regions(candidate)
