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

(LOOP)
// R0=16384
@SCREEN
D=A
@R0
M=D

@KBD
D=M
@FILLBK
D;JNE
@FILLWT
0;JMP

(FILLBK)
    // if R0-24575>0: goto LOOP2
    @R0
    D=M
    @24575
    D=D-A
    @LOOP
    D;JGT

    // MEM[R0]=0b1111111111111111
    D=0
    @R0
    A=M
    M=!D

    // R0 = R0+1
    @R0
    M=M+1

@FILLBK
0;JMP


(FILLWT)
    // if R0-24575>0: goto LOOP2
    @R0
    D=M
    @24575
    D=D-A
    @LOOP
    D;JGT

    // MEM[R0]=0b0000000000000000
    @R0
    A=M
    M=0

    // R0 = R0+1
    @R0
    M=M+1

@FILLWT
0;JMP