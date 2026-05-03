import logging

from ..config.constants import BLANK_SYMBOL

logger = logging.getLogger(__name__)

class Tape(dict[int, str]):
    """
    Represents the tape of the Turing Machine as a potentially infinite dictionary mapping integer positions to symbols.
    The tape is initialized from a file or a provided string, and any uninitialized position defaults to a blank symbol.

    Attributes
    ----------
    log : logging.Logger | None
        An optional logger for recording tape actions and changes.
    
    Methods
    -------
    __missing__(key: int) -> str
        Returns the blank symbol for any uninitialized position and initializes it in the tape.
    __str__() -> str
        Returns a string representation of the tape, showing only the non-blank portion for readability.
    """

    def __init__(self, filepath: str, arg_input: str | None = None, log = None) -> None:
        """Initializes the tape from a file or a provided string input.
        Parameters
        ----------
        filepath : str
            The path to the file containing the tape input.
        arg_input : str | None
            An optional string input for initializing the tape.
        log : logging.Logger | None
            An optional logger for recording tape actions and changes.
        Returns
        -------
        None
        """
        super().__init__()

        if arg_input is None:
            tape_str = _load_from_file(filepath)
        else:
            tape_str = arg_input

        for i, char in enumerate(tape_str):
            self[i] = char

        if log is not None:
            logger.info(f"Initialized tape with input: '{tape_str}'")

    def __missing__(self, key: int) -> str:
        """Returns the blank symbol for any uninitialized position and initializes it in the tape."""
        self[key] = BLANK_SYMBOL
        return BLANK_SYMBOL

    def __str__(self) -> str:
        if not self:
            return "[]"

        # Find leftmost and rightmost non-blank positions
        non_blank_positions = [pos for pos in self if self[pos] != BLANK_SYMBOL]
        
        if not non_blank_positions:
            return "[]"
        
        min_p = min(non_blank_positions)
        max_p = max(non_blank_positions)

        return "[" + "".join(self[i] for i in range(min_p, max_p + 1)) + "]"

def _load_from_file(path: str) -> str:
    """
    Loads the tape input from a specified file, looking for a line starting with '>>>' to extract the tape content.
    Parameters
    ----------
    path : str
        The path to the file containing the tape input.
    Returns
    -------
    str
        The extracted tape input.
    Raises
    ------
    ValueError
        If no tape input is found in the specified file.
    """
    
    with open(path, "r", encoding = "utf-8") as f:
        for line in f:
            if line.startswith(">>>"):
                tape_input = line[3:].strip()
                return tape_input
        else:
            raise ValueError(f"No tape input found in file: {path}")

if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")