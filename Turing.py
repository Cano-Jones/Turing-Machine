#!/usr/bin/env python
"""
Turing.py

This program simulates the functionality of a Turing Machine.
Given a input and a set of commands (Code) it returns the value of the computation.
Commands have 5 arguments:
-Initial state (Is): char
-Value readed (Vr): char
-Value writen (Vw): char
-Reader movement (Rm): '+', '-', 'X'
-Final state (Fs): char
The syntax of a command is as follows: <Is,Vr,Vw,Rm,Fs> 
The program works after a input file is given ($ python3 Turing.py<Inputfile.extension), this input file must follow the next sintax:

% Comment
>INPUT:
Input
>CODE:
<@,Vr,Vw,Rm,Fs> 
<Is,Vr,Vw,Rm,Fs> 
<Is,Vr,Vw,Rm,Fs> 
.
.
.
<Is,Vr,Vw,Rm,#> 

Comment, INPUT and CODE headers are needed, first Initial state must be '@' and there must be at least one stopping final state '#'. 
Input cannot be left empty, if no Input is wanted, this section must be 'NULL'.

Different ERROR messages cand be printed if code syntax or code rules are broken, in that case program exits.

:Author: Cano Jones, Alejandro
:Date: March 2023
:LinkedIn: https://www.linkedin.com/in/alejandro-cano-jones-5b20a7136/
:GitHub: https://github.com/Cano-Jones
"""

#Used libraries
from sys import stdin as std
from copy import copy

class Reader:
    """
    Reader Class
    Describes the nature of the Turings Reader, it can move through the tape, read de value on its position and change it into another.

    Attributes
    ----------
    state: Current command state of the reader.
    position: Current position of the reader over the tape.
    """
    def __init__(self, state, position):
        """
        Definition of Reader Class
        """
        self.state=state #Current command state of the reader.
        self.position=position #Current position of the reader over the tape.

    def Move(self, step, array):
        """
        Reader.Move(step, array)
        Moves the reader to another position of the tape. It can move one position to the right (+), one position to the left (-) or
        it can stay put (X). If the position of the reader is not on the lenth of the array describing the tape, the array expands its lenth,
        adding an empty (_) value on that new position.
        """
        if step=='+': #If the movement command is '+'
            self.position+=1 #Moves the reader a position to the right
            if self.position>len(array)-1: #If the reader position surpasses the array describing the tape lenth
                array.extend('_') #An extension with an empty value is added at the end of the array
        elif step=='-': #If the movement command is '-'
            self.position-=1 #Moves the reader a position to the left
            if self.position<0: #If the reader position is below 0
                array[:0]=['_'] #An extension with an empty value is added at the beggining of the array
                self.position=0 #And the reader is positioned at that cell defined now as position 0

def PrepareCode():
    """
    PrepareCode()

    Reads input file, checks if input is valid (if not, prints ERROR message stating reason before stopping program) and returns the Tape initial state
    and the code. 
    """
    Text=std.read() #sys.stdin.read() reads input file and saves it into 'Text' variable
    #If last line of input file is empty, it is deleted
    if Text[-1]=='\n': 
        Text=list(Text)
        del Text[-1]
        Text=''.join([str(elem) for elem in Text])

    Text=Text.split("\n") #Input file is devided into lines
    Check=CodeCheck(Text) #Checks if code is valid
    if Check[0]==False: exit(Check[1]) #If not valid, ERROR message stating reason is printed before stopping program
    tape = ['_'] if Text[2] == 'NULL' else list(Text[2]) #If the INPUT is 'NULL' tape is defined as a single empty '_' cell
    for i in range(4): del Text[0] #Command, Headers and INPUT lines are deleted
    code=[] #Code array is deifned
    for i in Text: #Loop for each surviving line of Text, where code is
        i=i.replace('<','') #Opening syntax is deleted
        i=i.replace('>','') #Closing syntax is deleted
        code.append(i.split(',')) #Individual arguments of command is stored in new array element
    return [tape, code] #Initial tape state and code are returned


def CodeCheck(Text):
    """
    CodeCheck(Text)

    Checks if the input file (saved in the 'Text' variable) is valid. It returns a boolean variable (True if no errors are found, False otherwise) and a string
    (The returned string indicates the error if there ise one, if there is no error, a 'no errors' message is returned)
    """
    if Text[0][0]!='%': return [False, '>ERROR: No inital comment header \'%\''] #If there is no Comment header, there is an ERROR
    if Text[1]!='>INPUT:': return [False, '>ERROR: No INPUT header'] #If there is no INPUT header, there is an ERROR
    if Text[3]!='>CODE:': return [False, '>ERROR: No CODE header'] #If there is no CODE header, there is an ERROR
    #Check if the command syntaxt of opener '<' and '>' are present
    for i in range(4,len(Text)): 
        if Text[i][0]!='<' or Text[i][-1]!='>': return [False,'>ERROR: Command syntax, \'<\' or \'>\' missing'] #If they are not present, there is an ERROR
    #Check if the number of arguments in each command (separated by ',') is correct (5)
    for i in range(4,len(Text)):
        if len(Text[i].split(','))!=5: return [False,'>ERROR: Command syntax, incorrect number of arguments'] #If not, there is an ERROR
    #Check if the initial state of the first command is the initial state ''@'
    if Text[4][1]!='@': return [False,'>ERROR: No initial command'] #If not, there is an ERROR
    #Chek if the values of the movement argument are correct (possible values are '+', '-' & 'X')
    for i in range(4,len(Text)):
        if Text[i].split(',')[3] not in ['+', '-', 'X']: return [False,'>ERROR: Command syntax, incorrect movement argument'] #If not, there is an ERROR
    #Check if there is a stopping command '#'
    aux=False
    for command in Text[4:]: #Loop over all command lines
        if command.split(',')[4]=='#>': #If a stopping comand '#' is found, there is no ERROR
            aux=True
            break
    if aux==False: return [False,'>ERROR: No stopping command'] #If no stopping command is found, there is an ERROR
    #Check if there are two commands with equal conditions
    for i in range(4,len(Text)): #Loop over all commands
        for j in range(i+1,len(Text)): #Loop over the commands different than the upper loop
            if Text[i].split(',')[:3]==Text[j].split(',')[:3]: return [False,'>ERROR: Two commands with equal coditions'] #If there are two commands with equal 
                                                                                                                            #conditions there is an ERROR
    #Check if there is an 'Infinite loop command'
    for command in Text[4:]: #Loop over all commands
        #Command is formated for simpler analysis
        aux=command.replace('<','')
        aux=aux.replace('>', '')
        aux=aux.split(',')
        if aux[0]==aux[-1] and aux[1]==aux[2] and aux[3]=='X': return [False, '>ERROR: Infinite loop comand <A,B,B,X,A>'] #If there is an infinite command,
                                                                                                                            #there is an ERROR
    #Check if there is a initial state for each final state (no final states without initial states and viceversa)
    Ini_States=set() #Set of initial states is defined
    Fin_States=set() #Set of final states is defined
    #Complete sets are calculated below
    for command in Text[4:]: #Loop over all comanda
        #command is formated for simpler analysis
        aux=command.replace('<','')
        aux=aux.replace('>','')
        Ini_States.add(aux.split(',')[0]) #Initial state is added
        Fin_States.add(aux.split(',')[-1]) #Final state is added
    
    #Initial '@' and stopping '#' states are mandatory, only states different than those are needed 
    Ini_States.remove('@') #Initial state '@' is deleted 
    Fin_States.remove('#') #Stopping state '#' is deleted
    if '@' in Fin_States:  Fin_States.remove('@') #If initial state '@' is used as final state it is deleted
    if Ini_States!=Fin_States: return [False,'>ERROR: Different sets of initial and final states'] #If the set of initial and final states are different, there 
                                                                                                        # is an ERROR
    
    return [True,'No errors found'] #If no error are found, no ERROR is returned

def Compute(Tape, Code):
    """
    Compute(Tape, Code)

    Computes the result of applying the code rules to the Tape state.    
    """
    r=Reader('@',0) #Defines the initial conditions of the reader: State '@' and position 0
    aux=True
    while r.state!='#' and aux==True: #The code rules are followed until stop state '#' is achived or if no command aplies
        #PrintTape('/> ',Tape) #If uncommented prints '/>' followed with the curret tape state
        for command in Code: #Loop for each command
            if r.state==command[0] and Tape[r.position]==command[1]: #If the command aplies
                Tape[r.position]=command[2] #The tape value at reader position is changed
                r.Move(command[3], Tape) #The reader moves to new position
                r.state=command[4] #The reader state is changed
                aux=True
                break #Command has been aplied, new loop must take place
            else: aux=False #If no command aplies, the computation stops

def PrintTape(Text, Tape):
    """
    PrintTape(Text, Tape)
    Prints the state of the tape, with a text indicator. The indicator is used by the Main() funtion to print '<<' before the initial state and
    print '>>' before the final state. It can be used in the Compute() funtion to print the state of the Tape at each computational step, it prints '/>' before
    the current tape state.
    """
    aux=copy(Tape) #Creates a copy of the Tape to handle without changing the original array
    if aux==[]: 
        print(Text+'NULL') #If the tape is empty, it prints the 'NULL' state
        return 
    else: #If the tape is not empty
        #Empty values at the beggining of the tape are not shown
        while aux[0]=='_': #If the first value is empty
            del aux[0] #That cell is deleted
            if aux==[]: #If that causes the Tape to be empty
                print(Text+'NULL') #The 'Null' state is printed
                return 
        #Empty values at the ending of the tape are not shown
        while aux[-1]=='_' and aux!=[]: del aux[-1] #If the las cell is empty, it is deleted
        print(Text+''.join([str(elem) for elem in aux]).replace('_',' ')) #The tape state is printed as a string, the inner empy values are remplaced by spaces

def Main():
    """
    Main function of the program. It obtains the Tape state ad the code to follow, after that, prints the state of the tape. Then, computes the final state of 
    the tape, printing its value.
    """
    Tape, Code = PrepareCode() #Gets the Tape initial state and the code
    PrintTape('<< ', Tape) #Prints the initial state of the code
    Compute(Tape, Code) #Computes the final state of the tape
    PrintTape('>> ', Tape) #Prints the final state of the tape

if __name__ == "__main__":
    Main()

    

