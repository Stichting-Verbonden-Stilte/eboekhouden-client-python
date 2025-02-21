"""This is the main package file for the verbonden_stilte package."""

import logging

from rich.logging import RichHandler
from .eboekhouden import EBoekhoudenClient
from .enums import DateFilterOperator

# Version and author info for the package
__version__ = "2.0-beta"
__author__ = "Daan Damhuis"
__organization__ = "Verbonden Stilte"

# Add RichHandler to the root logger
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger(__name__)

log.info("Initializing %s version %s", __package__, __version__)

__all__ = ["EBoekhoudenClient", "DateFilterOperator"]
