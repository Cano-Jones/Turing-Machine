import sys
import logging

from .head import Head
from .tape import Tape
from .script import Script
from ..config.constants import STOP_HEAD_STATUS, SPINNER

logger = logging.getLogger(__name__)

class TuringMachine:
    def __init__(self, head: Head, tape: Tape, script: Script, log = None) -> None:
        self.head: Head = head
        self.tape: Tape = tape
        self.script: Script = script
        self.log = log

        if self.log is not None:
            logger.info(f"Turing machine correctly initialized with head {head}, tape {tape} and script {script}")

    def step(self) -> None:
        status = self.head.status
        symbol = self.tape[self.head.position]
        instruction = self.script(status, symbol)
        if instruction is None:
            raise RuntimeError(f"No instruction for head status {status} and tape symbol {symbol}")
        instruction(self.head, self.tape)
    
    def run(self, max_steps: int = 1000, spinner: bool = True) -> None:
        
        if self.log is not None:
            logger.info("Starting Turing machine execution")
            logger.info(f"Step {0}: Head status: {self.head.status}, Tape: {self.tape}")
        for i in range(max_steps):
            try:
                self.step()

                if self.log is not None:
                    logger.info(f"Step {i + 1}: Head status: {self.head.status}, Tape: {self.tape}")

                if spinner:
                    sys.stdout.write(f"\rRunning {SPINNER[i % len(SPINNER)]}")
                    sys.stdout.flush()

                if self.head.status == STOP_HEAD_STATUS:
                    break

            except RuntimeError:
                break

        # Clean up spinner line
        if spinner:
            sys.stdout.write("\r\033[K")
            sys.stdout.flush()

if __name__ == "__main__":
    raise ImportError("This module is not meant to be run directly.")