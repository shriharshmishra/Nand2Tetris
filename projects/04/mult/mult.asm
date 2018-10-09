// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

//initialize 
//r0, r1, i=r0,r2=0
//
//loop
//    if i = 0 goto @END
//    r2=r2+r1
//    i=i-1
//    @LOOP
//    (END)

    //Initialize i=R0-1
    @R0 
    D=M
    @i
    M=D

    //Initialize R2=0
    @R2
    M=0

(LOOP)
    //Set Loop Condition
    @i
    D=M
    @END
    D;JEQ 

    //Loop Body
    // Update R2
    @R1
    D=M
    @R2
    M=D+M
    
    //Update i
    @i
    M=M-1
    
    //End Loop
    @LOOP
    0; JMP
    
(END)
    @END
    0;JMP


