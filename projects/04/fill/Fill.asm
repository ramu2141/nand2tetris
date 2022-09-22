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


// r0 = SCREEN
//
// LOOP:
//     if *KBD == 0 goto WHITE
//         // BLACK:
//             *r0 = !0
//             goto COMMON
//         WHITE:
//             *r0 = 0
//         COMMON:
//             r0 = r0 + 1
//             if r0 - SCREEN - 8192 < 0 goto LOOP
//                 r0 = SCREEN
//                 goto LOOP

// r0 = SCREEN
@SCREEN
D=A
@R0
M=D

(LOOP)
    // if *KBD = 0 goto WHITE
    @KBD
    D=M
    @WHITE
    D;JEQ

    // BLACK
        // *r0 = !0
        @R0
        A=M
        D=0
        M=!D
        // goto COMMON
        @COMMON
        0;JMP

    (WHITE)
        // *r0 = 0
        @R0
        A=M
        M=0
        
    (COMMON)
        // r0 = r0 + 1
        @R0
        MD=M+1
    
        // if r0 - SCREEN - 8192 < 0 goto (LOOP)
        @SCREEN
        D=D-A
        @8192
        D=D-A
        @LOOP
        D;JLT

        // r0 = SCREEN
        @SCREEN
        D=A
        @R0
        M=D
        
        // goto LOOP
        @LOOP
        0;JMP