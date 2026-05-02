
import sys
from time import sleep

from .head import Head
from .tape import Tape
from .script import Script
from ..config.constants import STOP_HEAD_STATUS, SPINNER

class TuringMachine:
    def __init__(self, head: Head, tape: Tape, script: Script) -> None:
        self.head: Head = head
        self.tape: Tape = tape
        self.script: Script = script
    
    def step(self) -> None:
        status = self.head.status
        symbol = self.tape[self.head.position]
        instruction = self.script(status, symbol)
        if instruction is None:
            raise RuntimeError(f"No instruction for head status {status} and tape symbol {symbol}")
        instruction(self.head, self.tape)
    
    def run(self, max_steps: int = 1000, show_spinner: bool = True) -> None:
        for i in range(max_steps):
            sleep(1)
            try:
                self.step()

                if show_spinner:
                    sys.stdout.write(
                        f"\rRunning {SPINNER[i % len(SPINNER)]}"
                    )
                    sys.stdout.flush()

                if self.head.status == STOP_HEAD_STATUS:
                    break

            except RuntimeError:
                break

if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")