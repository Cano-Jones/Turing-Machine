from dataclasses import dataclass

from ..config.types import HeadStatus, Movement, Symbol
from .head import Head
from .tape import Tape

@dataclass(frozen=True)
class Instruction:
    """
    Represents a single instruction in the Turing machine's script, defining how the head should move and what symbol to write based on the current head status and tape symbol.
    
    Attributes
    ----------
    current_status : HeadStatus
        The current status of the head that this instruction applies to.
    read : Symbol
        The symbol that must be read from the tape for this instruction to be executed.
    write : Symbol
        The symbol that will be written to the tape when this instruction is executed.
    move : Movement
        The direction in which the head will move after executing this instruction (left, right, or stay).
    next_status : HeadStatus
        The new status of the head after executing this instruction.

    Methods
    -------
    __call__(head: Head, tape: Tape) -> None
        Executes the instruction by modifying the head and tape according to the instruction's parameters.
    __str__() -> str
        Returns a string representation of the instruction in the format:
        <current_status, read, write, move, next_status>
    """
    current_status: HeadStatus
    read: Symbol
    write: Symbol
    move: Movement
    next_status: HeadStatus

    def __call__(self, head: Head, tape: Tape) -> None:
        """
        Executes the instruction by modifying the head and tape according to the instruction's parameters.

        Parameters
        ----------
        head : Head
            The head of the Turing machine.
        tape : Tape
            The tape of the Turing machine.

        Returns
        -------
        None
        
        Raises
        --------
        ValueError
            If the head status or tape symbol does not match the instruction's requirements.
        """
        if head.status != self.current_status:
            raise ValueError(f"Head status {head.status} does not match instruction's current status {self.current_status}")
        if tape[head.position] != self.read:
            raise ValueError(f"Symbol at head position {head.position} does not match instruction's read symbol {self.read}")
        
        tape[head.position] = self.write
        head.move(self.move)
        head.status = self.next_status

    def __str__(self) -> str:
        return f"<{self.current_status}, {self.read}, {self.write}, {self.move}, {self.next_status}>"


if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")