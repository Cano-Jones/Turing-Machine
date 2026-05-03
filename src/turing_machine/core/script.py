import re
from collections import defaultdict
import logging

from ..config.types import HeadStatus, Symbol
from ..config.constants import INITIAL_HEAD_STATUS, STOP_HEAD_STATUS
from .instruction import Instruction

logger = logging.getLogger(__name__)

class Script:
    """
    Represents a script for the Turing machine, containing a set of instructions for each possible combination of head status and tape symbol.

    Attributes
    ----------
    transitions : dict[tuple[HeadStatus, Symbol], Instruction]
        A dictionary mapping pairs of head status and tape symbol to the corresponding instruction to execute.
    log : logging.Logger | None
        An optional logger for recording script loading and validation actions.
    
    Methods
    -------
    __call__(head_status: HeadStatus, symbol: Symbol) -> Instruction | None
        Fetches the instruction corresponding to the given head status and tape symbol, or returns None if no such instruction exists.
    _validate() -> None
        Validates the script to ensure it meets the necessary requirements for execution, such as having an instruction for the initial head status and a halting instruction.
    __str__() -> str
        Returns a string representation of the script, showing all instructions in a readable format.
    __repr__() -> str
        Returns a string representation of the script, showing all instructions in a more compact format.
    """
    def __init__(self, filepath: str, transitions: dict[tuple[HeadStatus, Symbol], Instruction] | None = None, log = None) -> None:
        """
        Initializes the script by loading instructions from a file or using a provided dictionary of transitions.
        
        Parameters
        ----------
        filepath : str
            The path to the file containing the script instructions.
        transitions : dict[tuple[HeadStatus, Symbol], Instruction] | None
            An optional dictionary of transitions to use instead of loading from a file.
        log : logging.Logger | None
            An optional logger for recording script loading and validation actions.
        
        Returns
        -------
        None
        """

        self.log = log

        self.transitions = (
            _load_from_file(filepath)
            if transitions is None
            else transitions
        )

        self._validate()

        if self.log is not None:
            logger.info(f"Script loaded successfully from {filepath} with instructions:\n{repr(self)}")
            
    
    def __call__(self, head_status: HeadStatus, symbol: Symbol) -> Instruction | None:
        """
        Fetches the instruction corresponding to the given head status and tape symbol, or returns None if no such instruction exists.
        Parameters
        ----------
        head_status : HeadStatus
            The current status of the head for which to fetch the instruction.
        symbol : Symbol
            The symbol currently under the head on the tape for which to fetch the instruction.
        Returns
        -------
        Instruction | None
            The instruction corresponding to the given head status and tape symbol, or None if no such instruction exists.
        """

        if self.log is not None:
            logger.debug(f"Fetching instruction for head status '{head_status}' and symbol '{symbol}'")

        return self.transitions.get((head_status, symbol))
    
    def _validate(self) -> None:
        """Validates the script to ensure it meets the necessary requirements for execution, such as having an instruction for the initial head status and a halting instruction."""
        _validate_script(self)

    def __setitem__(self, key, value):
        raise TypeError("Script is immutable")
    
    def __str__(self) -> str:
        rep = "{"
        for instr in self.transitions.values():
            rep += f" {instr} |"
        return rep + "}"
    def __repr__(self) -> str:
        return "\n".join(str(instr) for instr in self.transitions.values())

def _load_from_file(filepath: str) -> dict[tuple[HeadStatus, Symbol], Instruction]:
        """
        Loads the script instructions from a file and returns a dictionary of transitions.
        
        Parameters
        ----------
        filepath : str
            The path to the file containing the script instructions.

        Returns
        -------
        dict[tuple[HeadStatus, Symbol], Instruction]
            A dictionary of transitions representing the script instructions.
        Raises
        ------
        FileNotFoundError
            If the specified script file does not exist.
        SyntaxError
            If the script file does not conform to the expected format or contains invalid instructions.
        """

        transitions: dict[tuple[HeadStatus, Symbol], Instruction] = {}

        pattern = re.compile(r'<(.*?)>')
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    instruction_str = match.group(1)
                    parts = instruction_str.split(",")

                    current_status = parts[0].strip()
                    read = parts[1].strip()
                    write = parts[2].strip()
                    move = parts[3].strip()
                    next_status = parts[4].strip()

                    instruction = Instruction(current_status, read, write, move, next_status)
                    if (current_status, read) in transitions:
                        raise SyntaxError(f"Duplicate instruction for current status {current_status} and read symbol {read}")
                    transitions[(current_status, read)] = instruction

        return transitions



def _validate_script(script: Script) -> None:
    """
    Validates the script to ensure it meets the necessary requirements for execution, such as having an instruction for the initial head status and a halting instruction.
    
    Parameters
    ----------
    script : Script
        The script to be validated.
    
    Returns
    -------
    None
    
    Raises
    ------
    SyntaxError
        If the script does not meet the necessary requirements for execution, such as missing an instruction for the initial head status or a halting instruction, or if it contains invalid instructions.
    """

    if not any(instruction.current_status == INITIAL_HEAD_STATUS for instruction in script.transitions.values()):
        raise SyntaxError(f"Instruction set must have an instruction with current status {INITIAL_HEAD_STATUS} (reserved for initial head status)")
    if not any(instruction.next_status == STOP_HEAD_STATUS for instruction in script.transitions.values()):
        raise SyntaxError(f"Instruction set must have an instruction with next status {STOP_HEAD_STATUS} (reserved for halting)")
    if any(instruction.move not in ['-', '=', '+'] for instruction in script.transitions.values()):
        raise SyntaxError(f"Instruction set must have instructions with movement -, = or +")
    if any(instruction.current_status == STOP_HEAD_STATUS for instruction in script.transitions.values()):
        raise SyntaxError(f"Instruction set cannot have instructions with current status {STOP_HEAD_STATUS} (reserved for halting)")


    for instruction in script.transitions.values(): # Only checks for 1-instruction loops...
        if (instruction.current_status == instruction.next_status
            and instruction.move == '='
            and instruction.read == instruction.write
            ):
            raise SyntaxError(f"Instruction {instruction} creates a trivial infinite loop")

if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")