import json
import sys
from typing import List

from loguru import logger


def dump_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)


def enable_logging() -> List[int]:
    """Set up the structuregraph_helpers logging with sane defaults."""
    logger.enable("structuregraph_helpers")

    config = dict(
        handlers=[
            dict(
                sink=sys.stderr,
                format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS Z UTC}</>"
                " <red>|</> <lvl>{level}</> <red>|</> <cyan>{name}:{function}:{line}</>"
                " <red>|</> <lvl>{message}</>",
                level="INFO",
            ),
            dict(
                sink=sys.stderr,
                format="<red>{time:YYYY-MM-DD HH:mm:ss.SSS Z UTC} | {level} | {name}:{function}:{line} | {message}</>",
                level="WARNING",
            ),
        ]
    )
    return logger.configure(**config)
