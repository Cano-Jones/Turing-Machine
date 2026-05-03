import logging

from ..config.types import HeadStatus, Movement
from ..config.constants import INITIAL_HEAD_STATUS, MOVEMENT_TABLE

logger = logging.getLogger(__name__)

class Head:
    """
    Represents the head of the Turing machine, which can read and write symbols on the tape and move left or right.

    Attributes
    ----------
    status : HeadStatus
        The current status of the head, which can be used to determine the next instruction to execute.
    position : int
        The current position of the head on the tape. Can be positive or negative, with 0 representing the initial position.
    log : logging.Logger | None
        An optional logger for recording head actions and movements.
    
    Methods
    -------
    move(direction: Movement) -> None
        Moves the head in the specified direction (left, right, or stay).
    __str__() -> str
        Returns a string representation of the head's current status and position.
    """
    def __init__(self, initial_status: HeadStatus = INITIAL_HEAD_STATUS, initial_position: int = 0, log = None) -> None:
        """
        Initializes the head with a given status and position.
        Parameters
        ----------
        initial_status : HeadStatus
            The initial status of the head.
        initial_position : int
            The initial position of the head on the tape.
        log : logging.Logger | None
            An optional logger for recording head actions and movements.
        """

        if log is not None:
            logger.info(f"Initializing head.")
            
        self.status: HeadStatus = initial_status
        self.position: int = initial_position
        self.log = log

    def move(self, direction: Movement):
        """Moves the head in the specified direction (left, right, or stay).
        Parameters
        ----------
        direction : Movement
            The direction in which to move the head.
        Returns
        -------
        None
        """

        if self.log is not None:
            logger.debug(f"Moving head from position {self.position} to position {self.position + MOVEMENT_TABLE[direction]} with movement '{direction}'.")

        self.position += MOVEMENT_TABLE[direction]
    def __str__(self) -> str:
        return f"Head(status={self.status}, position={self.position})"

if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")