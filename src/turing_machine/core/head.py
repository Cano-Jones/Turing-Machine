from ..config.types import HeadStatus, Movement
from ..config.constants import INITIAL_HEAD_STATUS, MOVEMENT_TABLE

class Head:
    def __init__(self, initial_status: HeadStatus = INITIAL_HEAD_STATUS, initial_position: int = 0) -> None:
        self.status: HeadStatus = initial_status
        self.position: int = initial_position
    def move(self, direction: Movement):
        self.position += MOVEMENT_TABLE[direction]
    def __str__(self) -> str:
        return f"Head(status={self.status}, position={self.position})"

if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")