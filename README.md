# Turing Machine

A Python implementation of a Turing Machine that executes computational tasks defined in custom script files.

## Overview

A Turing Machine is a theoretical computing device consisting of:

- **Tape**: An infinite memory with cells containing symbols
- **Head**: A pointer that reads, writes, and moves across the tape
- **Rules**: Instructions that determine behavior based on current state and symbol

This implementation allows you to define and run Turing Machine algorithms via script files.

## Installation & Usage

To install the requiered libraries
```bash
uv sync
```

Run a Turing Machine script with:

```bash
uv run turing -s <script_file> [options]
```

### Options

- `-s, --script` (required): Path to the `.tm` script file
- `-t, --tape`: Initial tape content (optional)
- `-l, --log`: Enable logging with optional file path
- `-m, --max-steps`: Maximum execution steps (default: 1000)
- `--no-spinner`: Disable spinner animation
- `-v, --version`: Show version

### Examples

```bash
uv run turing -s script_examples/hello_world.tm
uv run turing -s script_examples/addition.tm -t "5,3"
uv run turing -s script_examples/addition.tm -l output.log -m 5000
```

## Project Structure

```
src/turing_machine/
├── core/              # Core Turing Machine components
│   ├── head.py       # Tape head
│   ├── tape.py       # Tape management
│   ├── instruction.py # Instruction parsing
│   ├── script.py     # Script loading
│   └── turing_machine.py  # Main logic
├── config/            # Configuration
│   ├── constants.py   # Constants
│   └── types.py       # Type definitions
├── utilities/         # Utility functions
│   ├── cli.py        # CLI argument parsing
│   ├── validation.py # Input validation
│   └── logging.py    # Logging setup
└── main.py           # Entry point

script_examples/      # Example scripts
```

## Writing Script Files

Script files use the `.tm` format to define Turing Machine behavior:

```
% Comment line
>>>initial,tape,content
~${
    <state, read_symbol, write_symbol, movement, next_state>
    <state, read_symbol, write_symbol, movement, next_state>
}
```

### Script Components

- **`%`**: Comment (ignored)
- **`>>>`**: Marks the start of initial tape definition (no space after `>>>`)
- **`~${ ... }`**: Instruction block
- **Instruction format**: `<state, read_symbol, write_symbol, movement, next_state>`
  - `state`: Current state (number or identifier)
  - `read_symbol`: Symbol to read (`_` for blank)
  - `write_symbol`: Symbol to write (`_` for blank)
  - `movement`: `+` (move right), `-` (move left), `=` (no movement)
  - `next_state`: Next state (`#` to halt/stop)

[![CanoJones](https://img.shields.io/badge/author-CanoJones-blue?logo=github&logoColor=white)](https://github.com/Cano-Jones)

<!-- START OF LICENSE -->
<p xmlns:dct="http://purl.org/dc/terms/" xmlns:cc="http://creativecommons.org/ns#" class="license-text">
  <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">
    <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" />
  </a><br />
  This work is licensed under a
  <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.
</p>
<!-- END OF LICENSE -->
