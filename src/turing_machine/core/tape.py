
from ..config.constants import BLANK_SYMBOL

class Tape(dict[int, str]):

    def __init__(self, filepath: str, arg_input: str | None = None) -> None:
        super().__init__()

        if arg_input is None:
            tape_str = _load_from_file(filepath)
        else:
            tape_str = arg_input

        for i, char in enumerate(tape_str):
            self[i] = char

    def __missing__(self, key: int) -> str:
        self[key] = BLANK_SYMBOL
        return BLANK_SYMBOL

    def __str__(self) -> str:
        if not self:
            return "[]"

        min_p = min(self)
        max_p = max(self)

        return "[" + "".join(self[i] for i in range(min_p, max_p + 1)) + "]"

def _load_from_file(path: str) -> str:
    
    with open(path, "r", encoding = "utf-8") as f:
        for line in f:
            if line.startswith(">>>"):
                tape_input = line[3:].strip()
                return tape_input
        else:
            raise ValueError(f"No tape input found in file: {path}")

if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")