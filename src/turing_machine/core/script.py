import re
from collections import defaultdict

from ..config.types import HeadStatus, Symbol
from ..config.constants import INITIAL_HEAD_STATUS, STOP_HEAD_STATUS
from .instruction import Instruction

class Script:
    def __init__(self, filepath: str, transitions: dict[tuple[HeadStatus, Symbol], Instruction] | None = None) -> None:
        
        self.transitions = (
            _load_from_file(filepath)
            if transitions is None
            else transitions
        )

        self._validate()
    
    def __call__(self, head_status: HeadStatus, symbol: Symbol) -> Instruction | None:
        return self.transitions.get((head_status, symbol))
    
    def _validate(self) -> None:
        _validate_script(self)

    def __setitem__(self, key, value):
        raise TypeError("Script is immutable")

def _load_from_file(filepath: str) -> dict[tuple[HeadStatus, Symbol], Instruction]:

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



def _build_graph(script: Script):
    graph = defaultdict(set)

    for instr in script.transitions.values():
        graph[instr.current_status].add(instr.next_status)

    return graph

def _has_cycle(graph: dict) -> bool:
    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return True
        if node in visited:
            return False

        visited.add(node)
        stack.add(node)

        for nxt in graph[node]:
            if dfs(nxt):
                return True

        stack.remove(node)
        return False

    return any(dfs(n) for n in graph)

def _validate_script(script: Script) -> None:

    if not any(instruction.current_status == INITIAL_HEAD_STATUS for instruction in script.transitions.values()):
        raise SyntaxError(f"Instruction set must have an instruction with current status {INITIAL_HEAD_STATUS} (reserved for initial head status)")
    if not any(instruction.next_status == STOP_HEAD_STATUS for instruction in script.transitions.values()):
        raise SyntaxError(f"Instruction set must have an instruction with next status {STOP_HEAD_STATUS} (reserved for halting)")
    if any(instruction.move not in ['-', '=', '+'] for instruction in script.transitions.values()):
        raise SyntaxError(f"Instruction set must have instructions with movement -, = or +")
    if any(instruction.current_status == STOP_HEAD_STATUS for instruction in script.transitions.values()):
        raise SyntaxError(f"Instruction set cannot have instructions with current status {STOP_HEAD_STATUS} (reserved for halting)")


    # Check for infinite loops



    for instruction in script.transitions.values(): # Only checks for 1-instruction loops...
        if (instruction.current_status == instruction.next_status
            and instruction.move == '='
            and instruction.read == instruction.write
            ):
            raise SyntaxError(f"Instruction {instruction} creates a trivial infinite loop")
        
    """graph = _build_graph(script) # Leave for future logging
    if _has_cycle(graph):
        print("Warning: potential infinite state cycle detected")"""

if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")