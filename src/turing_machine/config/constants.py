
from .types import HeadStatus

INITIAL_HEAD_STATUS: HeadStatus = "@"
STOP_HEAD_STATUS: HeadStatus = "#"
BLANK_SYMBOL: str = "_"

SPINNER = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

MOVEMENT_TABLE: dict[str, int] = {
    "+": 1,
    "-": -1,
    "=": 0
}