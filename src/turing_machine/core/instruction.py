from dataclasses import dataclass

from ..config.types import HeadStatus, Movement, Symbol
from .head import Head
from .tape import Tape

@dataclass(frozen=True)
class Instruction:
    current_status: HeadStatus
    read: Symbol
    write: Symbol
    move: Movement
    next_status: HeadStatus

    def __call__(self, head: Head, tape: Tape) -> None:
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