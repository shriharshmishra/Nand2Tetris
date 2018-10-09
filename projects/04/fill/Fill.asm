// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//Psuedocode 
//screen_end=SCREEN + 8192
//
//(LOOP)
//    if KBD = 0 goto COLOR_WHITE
//    else goto COLOR_BLACK
//
//(COLOR_BLACK)
//    color=0
//    goto FILL
//
//(COLOR_WHITE)
//    color=-1
//    got FILL
//
//    i=SCREEN
//(FILL)
//    if (screen_end-i = 0) goto LOOP
//    else 
//       M[i]=color
//       i=i+1
//       goto FILL


    //Initialize screen_end
    @8192
    D=A
    @SCREEN
    D=D+A
    @screen_end
    M=D


(LOOP)
    //Read Keyboard memory 
    @KBD
    D=M

    //If KBD=0 goto COLOR_WHITE
    @COLOR_WHITE
    D;JEQ
    
    //Set color to black (-1)
    @color
    M=-1
    @FILL
    0;JMP

    //Set color to white (0)
(COLOR_WHITE)
    @color
    M=0

    //Fill the screen memory with value of 'color'
(FILL)
    //Initialize i=SCREEN
    @SCREEN
    D=A 
    @i
    M=D

(FILL_LOOP)
    //Calculate screen_end - i 
    @screen_end
    D=M
    @i
    D=D-M

    //Goto LOOP if screen_end - i = 0
    @LOOP
    D;JEQ

    //Set screen memory with color value
    @color
    D=M
    @i
    A=M
    M=D

    //Increment i 
    @i
    M=M+1

    @FILL_LOOP
    0;JMP
