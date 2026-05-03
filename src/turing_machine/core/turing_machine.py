import sys
import logging

from .head import Head
from .tape import Tape
from .script import Script
from ..config.constants import STOP_HEAD_STATUS, SPINNER

logger = logging.getLogger(__name__)

class TuringMachine:
    """
    Represents a Turing machine, which consists of a head, a tape, and a script of instructions. The machine can execute instructions based on the current status of the head and the symbol under the head on the tape.
    
    Attributes
    ----------
    head : Head
        The head of the Turing machine, which can read and write symbols on the tape and move left or right.
    tape : Tape
        The tape of the Turing machine, which is an infinite array of cells that can hold symbols.
    script : Script
        The script of the Turing machine, which contains the instructions that dictate how the head should move and what symbols to write based on the current head status and tape symbol.
    log : logging.Logger | None
        An optional logger for recording machine execution steps and actions.
    
    Methods
    -------
    step() -> None
        Executes a single step of the Turing machine by fetching and executing the appropriate instruction based on the current head status and tape symbol.
    run(max_steps: int = 1000, spinner: bool = True) -> None
        Runs the Turing machine for a specified number of steps or until it reaches a halting state, optionally displaying a spinner to indicate progress.
    """
    def __init__(self, head: Head, tape: Tape, script: Script, log = None) -> None:
        """
        Initializes the Turing machine with a head, tape, and script.
        Parameters
        ----------
        head : Head
            The head of the Turing machine.
        tape : Tape
            The tape of the Turing machine.
        script : Script
            The script of the Turing machine.
        log : logging.Logger | None
            An optional logger for recording machine execution steps and actions.
        Returns
        -------
        None
        """
        self.head: Head = head
        self.tape: Tape = tape
        self.script: Script = script
        self.log = log

        if self.log is not None:
            logger.info(f"Turing machine correctly initialized with head {head}, tape {tape} and script {script}")

    def step(self) -> None:
        """
        Executes a single step of the Turing machine by fetching and executing the appropriate instruction based on the current head status and tape symbol.
        Parameters
        ----------
        None
        Returns
        -------
        None
        Raises
        ------
        RuntimeError
            If no instruction is found for the current head status and tape symbol.
        """
        status = self.head.status
        symbol = self.tape[self.head.position]
        instruction = self.script(status, symbol)
        if instruction is None:
            raise RuntimeError(f"No instruction for head status {status} and tape symbol {symbol}")
        instruction(self.head, self.tape)
    
    def run(self, max_steps: int = 1000, spinner: bool = True) -> None:
        """
        Runs the Turing machine for a specified number of steps or until it reaches a halting state, optionally displaying a spinner to indicate progress.
        Parameters
        ----------
        max_steps : int
            The maximum number of steps to execute before stopping the machine.
        spinner : bool
            Whether to display a spinner in the console to indicate that the machine is running.
        Returns
        -------
        None
        """
        
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