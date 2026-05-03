import logging

from turing_machine import *

logger = logging.getLogger(__name__)

def main():

    args = parse_arguments()
    if args.log is not None:
        logging_setup("INFO", args.log)

    if args.log is not None:
        logger.info(f"Logging enabled. Log file: {args.log}")
        logger.info(f"Validating script file: {args.script}")
    validate_script(args.script)

    head = Head(log=args.log)
    tape = Tape(filepath = args.script, arg_input = args.tape, log=args.log)

    print(f"<<< {tape}")
    script = Script(filepath = args.script, log=args.log)
    machine = TuringMachine(head, tape, script, log=args.log)

    machine.run(max_steps=args.max_steps, spinner = not args.no_spinner)

    print(f">>> {tape}")

    if args.log is not None:
        logger.info("Turing machine execution completed.")

if __name__ == "__main__":
    main()
