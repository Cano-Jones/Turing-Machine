# Turing-Machine
Program that simulates the functionality of a Turing Machine.

The Turing Machine consists on an infinite tape divided on 'cells' that where a ASCII character can be written, and a 'Reader' that can move through the tape and change the character on the cell in which it stands and can be on different 'states'. The dynamics of the reader are determined by a set of commands (Code); each command have the next arguments:
>
>-Initial state of the reader. (Is)
>
>-ASCII character readed by the reader. (Vr)
>
>-ASCII character written by the reader. (Vw)
>
>-Movement of the reader. (Mr)
>
>-Final state of the reader. (Fs)

The algorithm goes as follows: If the reader (at some position) is at state 'Is' and read a character 'Vr', then, it changes that character to character 'Vw', then, the reader moves acording to 'Mr' (one position to the right, to the left or it stays put) and changes its state to 'Fs' before repeting the process. If no command is aplicable or if the reader arives to a stopping state, the loop ends, and the result is whatever is left written on the tape.

This program recives a file containing the characters written on a tape and a set of commands. This file mus follow the next format:
> _%Comment_
> 
> _>INPUT:_
> 
> _TapeCharacters_
> 
> _>CODE:_
> 
> _<@,Vr,Vw,Mr,Fs>_
> 
> _<Is,Vr,Vw,Mr,Fs>_
> 
> _<Is,Vr,Vw,Mr,Fs>_
> 
> ...
> 
> _<Is,Vr,Vw,Mr,#>_

%Comment, >INPUT: and >CODE: headers are mandatory. The first reader state must be '@' and there muct be at least one stopping state '#'.

An example of execution is shown (the file Addition.tm can be found on the CodeExamples folder), using a UNIX terminal:
 
`$ python3 Turing.py<Addition.tm`

`<< 011001+00111`

`>> 100000`

`$`

After executing the Turing.py program using the Addition.tm file, the initial tape is printed after '>>' and the final tape is printes after '>>'. This example takes two binary numbers as initial tape and ads them.

If there is any error on the file format, an error message stating the issue will be printed before exiting the program. Possible ERROR messages are:

- `>ERROR: No inital comment header \'%\'`

- `>ERROR: No INPUT header`

- `>ERROR: No CODE header`

- `>ERROR: Command syntax, \'<\' or \'>\' missing`

- `>ERROR: Command syntax, incorrect number of arguments`

- `>ERROR: No initial command \'@\`

- `>ERROR: Command syntax, incorrect movement argument`

- `>ERROR: No stopping command \'#\`

- `>ERROR: Two commands with equal coditions`

- `>ERROR: Infinite loop comand <A,B,B,X,A>`

- `>ERROR: Different sets of initial and final states`

Needed libraries:
- sys
- copy
- colorama
