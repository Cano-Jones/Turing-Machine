import re
from ..config import STOP_HEAD_STATUS

def validate_script(filepath: str) -> None:
    """
    Validates the Turing-Machine script file for correct format and potential issues.

    Parameters
    ----------
    filepath : str
        The path to the Turing-Machine script file to be validated.
    
    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        If the specified script file does not exist.
    SyntaxError
        If the script file does not conform to the expected format or contains invalid instructions.
    """

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            line_counter = 0
            last_line = len(f.readlines()) - 1
            for line in f:
                if line_counter == 0 and not line.startswith("%"):
                    raise SyntaxError("Instruction file must start with a comment header (line starting with %)")
                if line_counter == 1 and not line.startswith(">>>"):
                    raise SyntaxError("Instruction file must have a input line (starting with '>>>') after the comment header")
                if line_counter == 2 and not line == "~${\n":
                    raise SyntaxError("Instruction file must have a line with '~${' after the input line")
                if line_counter == last_line and not line == "@}\n":
                    raise SyntaxError("Instruction file must have a line with '}' at the end of the file")
                if line.startswith("\t<") and line.endswith(">\n"):
                    _validate_instruction_line(line)
                else:
                    raise SyntaxError(f"Invalid instruction line format at line {line_counter + 1}")
                line_counter += 1

    except FileNotFoundError:
        raise FileNotFoundError(f"Script file not found: {filepath}")

def _validate_instruction_line(instruction_line: str):
    """
    Validates a single instruction line from the Turing-Machine script.
    
    Parameters
    ----------
    instruction_line : str
        A line from the script file that is expected to contain an instruction in the format:
        <current_status, read_symbol, write_symbol, move_direction, next_status>
    
    Returns
    -------
    None
    
    Raises
    ------
    SyntaxError
        If the instruction line does not conform to the expected format or contains invalid components.
    """

    pattern = re.compile(r'<(.*?)>')
    match = pattern.search(instruction_line)
    instruction_str = match.group(1)
    parts = instruction_str.split(",")

    if len(parts) != 5:
        raise SyntaxError(f"Instruction line must have 5 parts separated by commas, found {len(parts)}: {instruction_line}")
    if parts[3].strip() not in ['-', '=', '+']:
        raise SyntaxError(f"Instruction line movement must be -, = or +, found {parts[3].strip()}: {instruction_line}")
    if parts[0].strip() == STOP_HEAD_STATUS:
        raise SyntaxError(f"Instruction line cannot have current status {STOP_HEAD_STATUS} (reserved for halting), found {parts[0].strip()}: {instruction_line}")
    if any (part.strip() == "" for part in parts):
        raise SyntaxError(f"Instruction line cannot have empty parts, please use '_' for empty symbols, found empty part in: {instruction_line}")
    if len(parts[1].strip()) != 1 or len(parts[2].strip()) != 1:
        raise SyntaxError(f"Read and write symbols must be single characters, multi-character symbols found in: {instruction_line}")


if __name__ == "__main__":
    raise NotImplementedError("This module is not intended to be run as a standalone script.")