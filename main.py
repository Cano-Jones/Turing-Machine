from turing_machine import *

def main():

    head = Head()
    tape = Tape("test.tm")
    script = Script("test.tm")
    machine = TuringMachine(head, tape, script)

    machine.run()

    print(f"\nFinal tape state: {tape}")

if __name__ == "__main__":
    main()