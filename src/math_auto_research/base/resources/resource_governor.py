from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import Iterator

from math_auto_research.base.resources.resource_budget import ResourceRejected, ResourceRequest


class ResourceGovernor:
    def __init__(self) -> None:
        self._semaphores = {
            "lean": threading.Semaphore(1),
            "proof_worker": threading.Semaphore(1),
            "symbolic_closure": threading.Semaphore(1),
            "construction_proposer": threading.Semaphore(1),
            "heavy_search": threading.Semaphore(1),
            "none": threading.Semaphore(8),
        }

    @contextmanager
    def admit(self, request: ResourceRequest) -> Iterator[ResourceRequest]:
        request.validate()
        semaphore = self._semaphores.get(request.engine_role, self._semaphores["none"])
        acquired = semaphore.acquire(timeout=0)
        if not acquired:
            raise ResourceRejected(f"resource role busy: {request.engine_role}")
        try:
            yield request
        finally:
            semaphore.release()
