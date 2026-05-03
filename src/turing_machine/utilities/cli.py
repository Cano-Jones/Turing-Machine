import argparse
from datetime import datetime


def parse_arguments():

    parser = argparse.ArgumentParser(prog = "Turing-Machine",
                                      description = "A Turing-Machine implementation in Python",
                                      epilog = "Author: Cano Jones, Alejandro",
                                      suggest_on_error = True)
    
    parser.add_argument("-v", "--version", action = "version", version = "%(prog)s 2.0.0")
    parser.add_argument("-s", "--script", type = str, help = "Path to the Turing-Machine script file", required = True)
    parser.add_argument("-t", "--tape", type = str, help = "Initial tape content. If omitted, the script’s defined initial tape is used.", required = False)
    parser.add_argument("-l", "--log", nargs="?", type=str, default=None, const=datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"), help="Enable logging. Optionally provide a file path; otherwise a timestamped filename is used.")
    parser.add_argument("-m", "--max-steps", type=int, default=1000, help="Maximum number of steps to execute (default: 1000)")
    parser.add_argument("--no-spinner", action="store_true", help="Disable the spinner animation during executions")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    raise NotImplementedError("This module is not intended to be run as a standalone script.")