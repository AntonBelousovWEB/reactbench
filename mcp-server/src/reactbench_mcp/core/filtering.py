"""TaskFilter — composable predicate over Task collections."""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from .models import Task


@dataclass(frozen=True)
class TaskFilter:
    difficulty: str | None = None
    category: str | None = None
    tags: tuple[str, ...] | None = None
    name_glob: str | None = None

    def apply(self, tasks: Iterable[Task]) -> list[Task]:
        result = list(tasks)
        if self.difficulty is not None:
            result = [t for t in result if t.metadata.difficulty == self.difficulty]
        if self.category is not None:
            result = [t for t in result if t.metadata.category == self.category]
        if self.tags is not None:
            result = [t for t in result if all(tag in t.metadata.tags for tag in self.tags)]
        if self.name_glob is not None:
            result = [t for t in result if fnmatch.fnmatch(t.id, self.name_glob)]
        return result
