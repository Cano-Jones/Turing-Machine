from typing import Literal
from collections.abc import Iterable
import argparse
import re
from itertools import combinations



type Movement = Literal['+', '-', '=']
type HeadStatus = str
type Symbol = str

INITIAL_HEAD_STATUS: HeadStatus = "@"
STOP_HEAD_STATUS: HeadStatus = "#"
EMPTY_SYMBOL: Symbol = "_"


def validate_instruction_line(instruction_line: str) -> None:

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


def validate_instruction_file(path: str) -> None:

    with open(path, "r", encoding="utf-8") as f:
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
                validate_instruction_line(line)
            else:
                raise SyntaxError(f"Invalid instruction line format at line {line_counter + 1}")
            line_counter += 1
            

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(prog = "Turing-Machine",
                                      description = "A Turing-Machine implementation in Python",
                                      epilog = "Author: Cano Jones, Alejandro",
                                      suggest_on_error = True)
    
    parser.add_argument("-i", "--instructions", type=str, help="Path to the instructions file", required=True)
    parser.add_argument("-t", "--input", type=str, help="Tape string state (if called, this will be used as the initial tape state)", required=False)
    parser.add_argument("-s", "--steps", type=int, help="Maximum number of steps to run the machine (default: 1000)", default=1000, required=False)

    args = parser.parse_args()
    validate_instruction_file(args.instructions)
    return args




class Head:
    def __init__(self) -> None:
        self.status: HeadStatus = INITIAL_HEAD_STATUS
        self.position: int = 0
    
    def UpdateStatus(self, new_status: HeadStatus) -> None:
        self.status = new_status

    def Move(self, movement: Movement) -> None:
        if movement == '+':
            self.position += 1
        elif movement == '-':
            self.position -= 1
        elif movement == '=':
            pass
        else:
            raise ValueError(f"Invalid movement {movement}, must be +, - or =")

def load_tape_from_file(path: str) -> str:

    with open(path, "r", encoding = "utf-8") as f:
        for line in f:
            if line.startswith(">>>"):
                tape_input = line[3:].strip()
                return tape_input

class Tape:
    def __init__(self) -> None:
        self.tape: dict[int, Symbol] = {}
    
    def load(self, tape_input: str | None = None, instructions_file: str = "") -> None: # From file or input
        if tape_input is not None:
            for i, symbol in enumerate(tape_input):
                self.tape[i] = symbol
        elif instructions_file:
            tape_input = load_tape_from_file(instructions_file)
            for i, symbol in enumerate(tape_input):
                self.tape[i] = symbol
        

    def Read(self, position: int) -> Symbol:
        return self.tape.get(position, EMPTY_SYMBOL)

    def Write(self, position: int, symbol: Symbol) -> None:
        self.tape[position] = symbol
    
    def __str__(self) -> str:
        if not self.tape:
            return '[' + EMPTY_SYMBOL + ']'
        
        min_pos = min(self.tape.keys())
        max_pos = max(self.tape.keys())

        tape_str = "["
        for pos in range(min_pos, max_pos + 1):
            tape_str += self.Read(pos)
        
        return tape_str + "]"
    
class Instruction:
    def __init__(self, current_status: HeadStatus, read: Symbol, write: Symbol, move: Movement, next_status: HeadStatus) -> None:
        self.current_status: HeadStatus = current_status
        self.read: Symbol = read
        self.write: Symbol = write
        self.move: Movement = move
        self.next_status: HeadStatus = next_status
    
    def __call__(self, head: Head, tape: Tape) -> None:

        if head.status != self.current_status:
            raise ValueError(f"Head status {head.status} does not match instruction's current status {self.current_status}")
        if tape.Read(head.position) != self.read:
            raise ValueError(f"Symbol at head position {head.position} does not match instruction's read symbol {self.read}")
        
        tape.Write(head.position, self.write)
        head.Move(self.move)
        head.UpdateStatus(self.next_status)
    
    def __str__(self) -> str:
        return f"<{self.current_status}, {self.read}, {self.write}, {self.move}, {self.next_status}>"


    
def load_instructions_from_file(path: str) -> set[Instruction]:
    instructions: set[Instruction] = set()

    pattern = re.compile(r'<(.*?)>')

    with open(path, "r", encoding="utf-8") as f:
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

                instructions.add(
                    Instruction(current_status, read, write, move, next_status)
                )

    return instructions



class InstructionSet:
    def __init__(self, instructions: Iterable[Instruction] | None | str = None) -> None:
        self.Instructions: set[Instruction] = set()

        if isinstance(instructions, str):
            self.load(instructions)
        elif instructions is not None:
            self.Instructions = set(instructions)
        
        self.validate()
    
    def load(self, instructions_file_path: str) -> None:
        self.Instructions = load_instructions_from_file(instructions_file_path)

    def validate(self) -> None:
        validate_instructions_set(self)
    
    def FindInstruction(self, head: Head, tape: Tape) -> Instruction | None:

        for instruction in self.Instructions:
            if instruction.current_status == head.status and instruction.read == tape.Read(head.position):
                return instruction

        return None

def validate_instructions_set(instruction_set: InstructionSet) -> None:

    if not any(instruction.current_status == INITIAL_HEAD_STATUS for instruction in instruction_set.Instructions):
        raise SyntaxError(f"Instruction set must have an instruction with current status {INITIAL_HEAD_STATUS} (reserved for initial head status)")
    if not any(instruction.next_status == STOP_HEAD_STATUS for instruction in instruction_set.Instructions):
        raise SyntaxError(f"Instruction set must have an instruction with next status {STOP_HEAD_STATUS} (reserved for halting)")
    if any(instruction.move not in ['-', '=', '+'] for instruction in instruction_set.Instructions):
        raise SyntaxError(f"Instruction set must have instructions with movement -, = or +")
    if any(instruction.current_status == STOP_HEAD_STATUS for instruction in instruction_set.Instructions):
        raise SyntaxError(f"Instruction set cannot have instructions with current status {STOP_HEAD_STATUS} (reserved for halting)")
    
    for pair in combinations(instruction_set.Instructions, 2):
        if pair[0].current_status == pair[1].current_status and pair[0].read == pair[1].read:
            raise SyntaxError(f"Instruction set has conflicting instructions: {pair[0]} and {pair[1]}")

    # Check for infinite loops

    for instruction in instruction_set.Instructions: # Only checks for 1-instruction loops...
        if (instruction.current_status == instruction.next_status
            and instruction.move == '='
            and instruction.read == instruction.write
            ):
            raise SyntaxError(f"Instruction set has potential infinite loop: {instruction}")


class TuringMachine:
    def __init__(self, instruction_set: InstructionSet) -> None:
        self.instruction_set: InstructionSet = instruction_set
    
    def Run_step(self, head: Head, tape: Tape) -> None:
        instruction = self.instruction_set.FindInstruction(head, tape)
        if instruction is not None:
            instruction(head, tape)
        else:
            raise RuntimeError(f"No instruction found for head status {head.status} and tape symbol {tape.Read(head.position)}")

    def Run(self, head: Head, tape: Tape, max_steps: int = 1000) -> None:
        for _ in range(max_steps):
            if head.status == STOP_HEAD_STATUS:
                break
            self.Run_step(head, tape)
        
        else:
            raise RuntimeError(f"Maximum number of steps {max_steps} reached without halting")


def main():
    args = parse_args()

    instruction_set = InstructionSet(args.instructions)
    instruction_set.validate()

    tape = Tape()
    tape.load(tape_input=args.input, instructions_file=args.instructions)

    head = Head()

    machine = TuringMachine(instruction_set)

    machine.Run(head, tape, max_steps=args.steps)

    """while head.status != STOP_HEAD_STATUS:
        try:
            machine.Run_step(head, tape)
        except RuntimeError as e:
            print(f"Runtime error: {e}")
            break
        print(f"Head status: {head.status}, Head position: {head.position}, Tape state: {tape}")"""

    print("Final tape state:", tape)

    


if __name__ == "__main__":
    main()