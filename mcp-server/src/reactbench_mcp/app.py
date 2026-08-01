"""Composition root — builds production dependency graph."""
import logging
from .adapters import FilesystemJobStore, FilesystemTaskStore, SubprocessHarborClient
from .config import AppConfig
from .tools.contracts import AppContext

_log = logging.getLogger("reactbench-mcp")


def wire() -> AppContext:
    config = AppConfig()
    _log.info("ReactBench root: %s", config.repo_root)
    return AppContext(
        config=config,
        tasks=FilesystemTaskStore(config),
        jobs=FilesystemJobStore(config),
        harbor=SubprocessHarborClient(config),
    )
