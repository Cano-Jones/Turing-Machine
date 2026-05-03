import logging

from ..config.types import HeadStatus, Movement
from ..config.constants import INITIAL_HEAD_STATUS, MOVEMENT_TABLE

logger = logging.getLogger(__name__)

class Head:
    def __init__(self, initial_status: HeadStatus = INITIAL_HEAD_STATUS, initial_position: int = 0, log = None) -> None:

        if log is not None:
            logger.info(f"Initializing head.")
            
        self.status: HeadStatus = initial_status
        self.position: int = initial_position
        self.log = log

    def move(self, direction: Movement):

        if self.log is not None:
            logger.debug(f"Moving head from position {self.position} to position {self.position + MOVEMENT_TABLE[direction]} with movement '{direction}'.")

        self.position += MOVEMENT_TABLE[direction]
    def __str__(self) -> str:
        return f"Head(status={self.status}, position={self.position})"

if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")