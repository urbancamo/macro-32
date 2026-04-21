
# MACRO Made Easy – Part IV: Calling All Code

## MACRO Made Easy

## Part IV: Calling All Code

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

One of the nicest features of the VAX architecture is the VAX Calling Standard. This standard makes it possible for routines written in different languages to call each other, as long as the language compilers adhere to the standard. For example, a routine written in MACRO can call a routine written in COBOL or BASIC just like it would call another routine written in MACRO. The reverse is also true, in that a program written in COBOL can call routines written in BASIC or MACRO, for example, as easily as calling another COBOL routine. If you’ve ever tried linking multiple-language programs under IBM’s MVS system, you’ll really gain an appreciation for the VAX Calling Standard.

So what is the VAX Calling Standard and how does it work? Well, without going into all of the specifics, it defines the rules for passing arguments from one routine to another and back, how registers are to be saved and restored, and how the stack will be used. I’ll cover bits of the calling standard as we look at the various ways of calling routines from MACRO. For a complete description of the VAX Calling Standard, consult the _VAX Architecture_ book or the _Introduction to VMS System Routines_ manual.

There are two types of routines that can be written in MACRO: subroutines and procedures. Subroutines are MACRO routines that can only be called from other MACRO routines (or BLISS routines), while procedures can be called from any high-level language. Essentially, the difference between the two types is determined by which instructions are used to transfer control to the routine. The instructions we’ll examine here are the BSBx, JSB, and CALLx.

Author’s note: I’ll be using the word “call” loosely throughout the article to mean “transfer control to”. References to callable routines should be interpreted as references to procedures, not subroutines. The terms should make sense, based on the context.

### THE SUBROUTINE

Control is transferred to a subroutine using one of the following instructions:

- BSBB — Branch SuBroutine with Byte offset
- BSBW — Branch SuBroutine with Word offset
- JSB — Jump SuBroutine

All three instructions accept one operand, which is the address of the target subroutine. As with the branch instructions, the differences among these instructions lie solely with how the target address is determined. For BSBB and BSBW, the operand is a displacement that is added to the PC (Program Counter), while the JSB operand is an address that replaces the contents of the PC. Again, as with the BRx and JMP instructions, the BSBW instruction will most often be used to call subroutines; JSB is typically only needed when calling system routines that lie outside of the range addressable with word displacements.

Subroutines generally begin with a label, just like any other section of code to which you wish to branch or jump. Subroutines return control using the RSB (Return from SuBroutine) instruction. The following code fragment shows a sample subroutine that doesn’t do much:

    TEST:   CLRL    R0              ; Clear contents of R0
            RSB                     ; Return to caller

The following line shows the instruction that would be used to branch to this subroutine:

            BSBW    TEST            ; Or BSBB, if it fits

The BSBx and JSB instructions push the contents of the PC, which points to the next instruction, onto the stack before modifying the PC. The RSB simply pops the return address of the stack and stores it back in the PC, causing the instruction after the BSBx or JSB instruction to become the next instruction to execute.

The following list points out some of the things to keep in mind when using subroutines. Each of these will be examined in more detail:

- There is no defined mechanism for passing parameters to and from a subroutine.
- Register contents are not automatically saved and restored.
- The position of the stack pointer must be maintained.

Because there is no defined method for passing parameters, any method may be used. Parameters are usually passed to the subroutine by placing their contents in certain registers; the subroutine can then expect to find the values in those registers. For example, a subroutine may expect an address to be passed in R1; it may return a value in any register, though R0 is usually used to return status values.

Similarly, the subroutine must ensure that it does not modify the contents of any registers not used to pass information back to the calling routine. Since the registers are not automatically saved, the subroutine must save and restore the contents of all registers that it uses to perform its function. The register contents are usually temporarily copied to the stack until the registers are no longer needed.

The PUSHL (PUSH Longword) and POPL (POP Longword) instructions can be used to copy register contents to and from the stack. They each take one operand: the source and destination, respectively, for the longword copied to and from the stack. The POPL instruction isn’t a real instruction; the MACRO assembler generates a “MOVL (SP)+,dest” instruction for POPL. For example, the following instruction

            POPL    R0

really generates

            MOVL    (SP)+,R0

However, the POPL mnemonic is easier to read when matching PUSHL/POPL pairs. The following code fragment shows how a register’s contents could be saved in a subroutine:

    TEST:   PUSHL   R1              ; Save the contents of R1
            ....                    ; Code that can freely use R1
            POPL    R1              ; Restore the contents of R1
            RSB                     ; Return to the caller

The PUSHR (PUSH Register) and POPR (POP Register) instructions can be used to copy several registers to and from the stack. They accept a register bitmask as an operand; for each bit that is set (bit 0 through bit 14), the corresponding register contents are pushed, in order. Register bit masks are specified using the “^M\<\>” notation. For example, the following instructions will push and pop the contents for registers R0, R1, R4, and R5:

            PUSHR   #^M<R0,R1,R4,R5>        ; Save R0, R1, R4, and R5
            POPR    #^M<R0,R1,R4,R5>        ; Restore the registers

The assembler generates a literal for the register mask, so the “#” is necessary. When the PUSHR above executes, the contents of R5 are pushed onto the stack, followed by R4, R1, and R0. POPR restores the contents in the opposite order, popping R0’s contents off the top first. The registers are processed in this order regardless of the order in which they were specified in the register mask. Consequently, the following two lines have the same effect as the two above:

            PUSHR   #^M<R4,R0,R5,R1>        ; Save R0, R1, R4, and R5
            POPR    #^M<R5,R4,R1,R0>        ; Restore the registers

Because of all the work that PUSHR and POPR must perform (scanning the bit mask for bits that are set and then saving or restoring the register contents), multiple PUSHLs and POPLs are generally more efficient (and faster).

Programming Hint \#1: PUSHR and POPR do \*not\* affect the condition codes, while PUSHL and POPL do. POPR is very useful in situations where a value must be popped off the stack and the current setting of the condition codes should be maintained.

If you use the stack to save register contents, it is vitally important that you restore the stack pointer to its original contents. Normally, this is done by matching PUSHx/POPx pairs, but direct manipulation of the SP (Stack Pointer) register is sometimes used. When the subroutine first receives control, the return address is at the top of the stack:

            +-------------------------+  <- (SP)
            |      Return Address     |
            +-------------------------+  <- 4(SP)
            |                         |
            +-------------------------+

If the stack is not properly maintained, the RSB will not return to the proper location. In fact, improper stack maintenance is one of the most common problems programmers have working in MACRO. It’s very easy to forget to pop a value off the stack, as this example shows:

            PUSHL   R5                      ; Save the contents of R5
            [...]                           ; Omitted code
            BSBW    SOME_ROUTINE            ; Call some other subroutine
            BLBC    R0,100$                 ; Branch on errors
            [...]                           ; Omitted code
            POPL    R5                      ; Restore the contents of R5
            [...]                           ; Omitted code
     100$:  RSB                             ; Return to caller

While this is an exaggerated example, it is all too easy to write code like this, especially when you are modifying existing code.

### THE PROCEDURE

Callable procedures are routines that adhere to the VAX Calling Standard. MACRO routines written as procedures can be called from other languages, while subroutines cannot. For callable procedures, the method used for passing parameters and saving and restoring registers is clearly defined.

Procedures begin with a label and an entry mask, which is a bit mask containing registers that are to be automatically saved at entry and restored upon exiting the procedure. The VAX Calling Standard declares that R0 and R1 are to be used for returning status values to the calling procedure; they cannot be specified in the entry register mask. R2 through R11 can be specified, in addition the mnemonics IV (Integer oVerflow) and DV (Decimal string oVerflow), which enable arithmetic overflow traps. I’ll pass on discussing those for now.

The following line shows the format of an entry mask, which is usually defined using the .ENTRY directive:

            .ENTRY  TEST,^M<R2,R3,R4,R5>

The symbol TEST is the name of the callable routine; it is a global symbol, which means that its value is known outside of the module it is located in. The register mask is stored as a word value (two bytes); it isn’t a literal when specified with .ENTRY, so there is no “#” as when specifying a register mask for PUSHR/POPR. The following lines are equivalent to the line above:

    TEST::          .WORD   ^M<R2,R3,R4,R5>
    TEST::          .WORD   ^X3C
    TEST::          .WORD   ^B00111100      ; Set bits 2, 3, 4, and 5

If you wanted a non-global procedure, you could specify the label “TEST:”, with only one colon. Such a routine would then be unknown outside of its module.

When the procedure TEST is called, registers R2 through R5 are automatically pushed onto the stack, along with the AP, FP, SP, and PC. I’ll defer discussion of the actual data structures involved until a future article; for now, let’s concentrate on how you can write simple callable routines and call other routines.

Procedures return control to their callers with the RET (RETurn from procedure) instruction. This instruction restores the contents of the registers specified in the entry mask, resets the stack pointer, and sets the PC to point to the return address.

Skipping the details, it should be noted that RET automatically resets the stack pointer to its initial value. This means that stack maintenance isn’t as critical within callable routines as it was in subroutines. Obviously care must be taken within the routine to ensure that the pushes and pops match properly, but there isn’t any need to make sure that all pushed values are popped off at the procedure’s end. This makes it easy to use the stack for temporary storage space in segments larger than 1 to 4 bytes.

Callable procedures are called using either CALLS (CALL with argument list on Stack) or CALLG (CALL with General argument list). Both instructions are responsible for setting up the argument list that is passed to the procedure, as well as saving the registers specified in the entry mask.

### The CALLS Instruction

CALLS is the most frequently used call instruction. It accepts two operands: a byte containing the number of arguments passed and the address of the procedure to call. The arguments are passed to the procedure by pushing them onto the stack. It is assumed that the arguments have already been pushed onto the stack before the CALLS is executed.

If you will recall from Part 1 of this series, the sample program made calls to the run-time library routines LIB$GET_INPUT and LIB$PUT_OUTPUT. The following code shows the call to LIB$GET_INPUT:

            PUSHAW  INBUFF_D                        ; Address of word to receive
                                                    ; ... the length of the input
            PUSHAQ  PROMPT                          ; Address of the prompt
            PUSHAQ  INBUFF_D                        ; Address of the input buffer
                                                    ; ... descriptor
            CALLS   #3,G^LIB$GET_INPUT              ; Read input from SYS$INPUT

Once again, the parameters are pushed onto the stack in reverse order, because the stack is used in a last-in, first-out (LIFO) method. General addressing mode (G^) is used when calling all run-time library routines, but isn’t normally used when calling procedures that are not included in shareable images.

If you were calling a routine without any parameters, you would simply specify “#0” as the argument count:

            CALLS   #0,SOME_PROC            ; Call some procedure without args

The RET instruction is responsible for cleaning up the stack; when control returns to the calling procedure, all of the arguments pushed on the stack have been removed (actually, the SP gets reset, effectively popping the arguments off the stack). There is no need to pop any of the values after the CALLS.

### THE CALLG INSTRUCTION

CALLG seems to be one of the more under-used instructions. CALLG performs all of the functions that CALLS does: it calls a procedure, automatically saving the necessary registers. It differs from CALLS only in the method of passing arguments to the procedure.

CALLG accepts two operands: the address of the argument list and the address of the procedure to call. While CALLS expected the argument list to have been pushed on the stack, CALLG expects that the entire argument list has already been set up somewhere in memory (which means that the list could be on the stack). CALLG doesn’t accept the number of arguments as an operand; instead, the first longword of the argument list is assumed to be the argument count.

To best illustrate how CALLG is used, let’s re-code the call to LIB$GET_INPUT above. The argument list is expected to reside in memory somewhere, so it is typically created in the program’s data area:

    ARGLIST:
            .LONG    3                      ; Number of arguments to follow
            .ADDRESS INBUFF_D               ; Address of the input buffer
            .ADDRESS PROMPT                 ; The address of the prompt
            .ADDRESS INBUFF_D               ; Address of word to get length

The procedure is then called with the following line:

            CALLG   ARGLIST,G^LIB$GET_INPUT      ; Read input from SYS$INPUT

As you can see, this can significantly reduce the amount of code needed to call procedures, because there is no need to PUSH all the values onto the stack. In programs that repeatedly call procedures in a loop, using CALLG instead of CALLS (assuming that arguments are to be passed) can significantly increase performance.

Judicious use of CALLG can also make the program’s code more readable. Consider the following examples, which read a string from SYS$INPUT and write it back to SYS$OUTPUT:

            PUSHAW  INBUFF_D                        ; Address of word to receive
                                                    ; ... the length of the input
            PUSHAQ  PROMPT                          ; Address of the prompt
            PUSHAQ  INBUFF_D                        ; Address of the input buffer
                                                    ; ... descriptor
            CALLS   #3,G^LIB$GET_INPUT              ; Read input from SYS$INPUT
            BLBC    R0,ERROR                        ; Branch on error

            PUSHAQ  INBUFF_D                        ; Now write it to SYS$OUTPUT
            CALLS   #1,G^LIB$PUT_OUTPUT             ; ...
            BLBC    R0,ERROR                        ; Branch on error

Recoding with CALLG, the actual instructions executed at run-time become:

            CALLG   IN_ARGLST,G^LIB$GET_INPUT       ; Read from SYS$INPUT
            BLBC    R0,ERROR                        ; Branch on error
            CALLG   OUT_ARGLST,G^LIB$PUT_OUTPUT     ; Write to SYS$OUTPUT
            BLBC    R0,ERROR                        ; Branch on error

Programming Hint \#2: Whether using CALLS or CALLG, make sure the argument count is accurate. It’s all too easy to push 3 values on the stack and specify either CALLS \#4 or CALLS \#2; in either case, the results probably won’t be what you were expecting.

### USING THE ARGUMENTS IN A PROCEDURE

When writing your own callable procedure, the arguments passed in are accessible using the AP register (Argument Pointer). Upon entry to the procedure, the AP is set to point to the argument list, which has the same format as the argument list built for CALLG:

            +-------------------------------------------+
            |           0                  | Arg Count  |   (AP)
            +-------------------------------------------+
            |           argument 1                      |  4(AP)
            +-------------------------------------------+
            |           ....                            |  8(AP)
            +-------------------------------------------+
            |           argument n                      | 12(AP)
            +-------------------------------------------+

As is probably evident at this point, CALLG just moves the address of the argument list into AP. The CALLS instruction simply pushes the argument count onto the stack and sets AP to point to that address on the stack; the other PUSHes have set up the arguments in the proper order as shown above.

The argument count is stored as an unsigned integer in the low byte of the longword addressed by (AP). The VAX calling standard reserves the remaining bits in the longword and declares that they must be zero. To get the number of arguments, simply reference (AP):

            MOVZBL  (AP),R0                 ; R0 gets the argument count

The arguments are then referenced as 4(AP), 8(AP), and so on. Remember that each argument is a longword (four bytes), so the offsets are in increments of four.

Arguments can be passed by value or by reference; the only difference this makes to a procedure is whether the value located in the argument list is an address or an actual value. The following example shows how an integer would be passed by value:

            PUSHL   #32                     ; Push a number (passed by value)
            CALLS   #1,SOME_ROUTINE         ; Call the routine

The routine would then pick up the number with an instruction like the following:

            MOVL    4(AP),R0                ; R0 gets the number

If the number had been passed by reference, R0 would now contain the address of the location holding the number. The number could then be retrieved using an instruction like this one:

            MOVL    @4(AP),R0               ; R0 gets the number

This says, “4(AP) holds an address; move the longword stored at that address into R0.”

As you’ve probably noticed, virtually all of the run-time library routines have optional parameters. The routines themselves can determine how many arguments were passed by getting the argument count and processing the arguments appropriately. For example, the following code determines how many arguments were passed and branches to handle them:

            MOVZBL  (AP),R0                 ; Were any arguments passed?
            BEQL    NONE                    ; Branch if not (R0 contains 0)
            CMPL    #2,R0                   ; Were there two arguments?
            BGTR    10$                     ; No---branch to handle only first one
            [...]                           ; Omitted code to process 8(AP)
     10$:   [...]                           ; Omitted code to process 4(AP)

When writing procedures, it’s a good idea to make sure that only the expected number of parameters were passed. Some of the LIB$ routines return the fatal value LIB$_WRONUMARG (“wrong number of arguments”) when an incorrect number of parameters are passed. Your procedures can also return this value; it’s defined in the STARLET macro $LIBDEF.

            $LIBDEF

            [....]

            .ENTRY  TEST,^M<>
            CMPW    #4,(AP)                 ; Were there at most 4 arguments?
            BGEQ    OK                      ; 4 or fewer are OK....
            MOVL    #LIB$_WRONUMARG,R0      ; Return "wrong number"
            RET                             ; ...
     OK:    [...]

Keep in mind that status values are returned in R0. Ideally, you should use symbolic error codes such as LIB$_WRONUMARG and SS$_NORMAL, instead of hardcoding error values.

To make your code more readable and to minimize the chance of introducing bugs through typos, it’s a good idea to set up symbols equal to the offsets of each argument from AP. For example, suppose you have a routine that accepts two parameters: the address of a descriptor for a username and the address of a UIC, in that order. These correspond to 4(AP) and 8(AP), respectively. Through the use of symbols, your code can be more self-documenting:

    USERNAME = 4                                    ; First argument -- 4(AP)
    UIC      = 8                                    ; Second argument -- 8(AP)

            MOVQ    @USERNAME(AP),R0                ; Move descriptor to R0/R1
            MOVL    @UIC(AP),R2                     ; Move UIC to R2

Just to make the code even more readable, I usually take advantage of the assembler’s built-in multiplication operator and specify the symbols in terms of their order times 4 bytes (a longword):

    USERNAME = 1 * 4                    ; Argument 1 -- the username
    UIC      = 2 * 4                    ; Argument 2 -- the UIC

With definitions like these, it’s very obvious which list position each argument holds. I’ve written routines that take as many as 10 parameters; it’s a lot easier to determine the order using “8\*4”, “9\*4”, and “10\*4” than it is to use “32”, “36”, and “40”. It is also easier to change the order of arguments because you just have to change the first number to match the new order.

### AN EXAMPLE

Program 1 is a trivial MACRO program that will demonstrate many of the topics discussed above. For the purposes of demonstration, it uses BSBW to branch to a subroutine that uses CALLS to call a procedure that uses CALLG to call an external procedure written in C (Program 2). The C procedure accepts an argument and then calls the MACRO routine DO_MATH to perform simple math functions. This is an obviously exaggerated example, but it does demonstrate the principles. I’d recommend compiling and linking the programs /DEBUG so you can step through each of the calls (remember to use the DEBUG command STEP/INTO).

The following shows a sample run:

            $ macro caller
            $ cc callee
            $ link caller,callee,sys$input/options
            sys$share:vaxcrtl.exe/share
            ^Z
            $ run caller
            The first number passed to START_C_RTN is 98765
            The second number passed to START_C_RTN is 1234
            98765 + 1234 = 99999
            98765 - 1234 = 97531
            98765 * 1234 = 121876010
            98765 / 1234 = 80
            $

NEXT TIME….

This month we covered the basics of setting up and calling internal subroutines and procedures. You should now be able to write MACRO programs that can call procedures written in other languages and vice versa. Next issue, we’ll look at the methods for calling the VMS system services, along with additional methods for calling run-time library routines.

------------------------------------------------------------------------

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

------------------------------------------------------------------------

### PROGRAM 1

            .TITLE  CALLER
            .IDENT  /01-000/
    ;++
    ;
    ;  Facility:    CALLER
    ;
    ;  Author:      Hunter Goatley
    ;
    ;  Date:        November 27, 1991
    ;
    ;  Abstract:
    ;
    ;       This program demonstrates calls to subroutines, procedures, and
    ;       external procedures written in C.
    ;
    ;       To build:
    ;
    ;               $ MACRO CALLER
    ;               $ CC CALLEE
    ;               $ LINK CALLER,CALLEE,SYS$INPUT/OPTIONS
    ;               SYS$SHARE:VAXCRTL.EXE/SHARE
    ;               ^Z
    ;               $ RUN CALLER
    ;
    ;  Modified by:
    ;
    ;       01-000          Hunter Goatley          27-NOV-1991 09:09
    ;               Original version.
    ;
    ;--

            .LIBRARY        /SYS$LIBRARY:LIB.MLB/

            .DSABL  GLOBAL                          ; Declare external references
            .ENABL  SUPPRESSION                     ; Don't list unreferenced symbol
            .NOSHOW BINARY                          ; Include binary in listings
    ;
    ;  External routines:
    ;
            .EXTRN  START_C_RTN                     ; External C procedure

            $LIBDEF                                 ; Include LIB$_ symbols
            $SSDEF                                  ; System service status symbols

            .SHOW   BINARY                          ; Include binary in listings

            .PSECT  _CALLER_DATA,NOEXE,WRT,LONG,SHR

    NUMBER1:        .LONG   98765                   ; Store the numbers
    NUMBER2:        .LONG   1234                    ; ...

    ;
    ;  Pass by reference just for the fun of it.
    ;
    ARGLIST:        .LONG   2                       ; Only one argument
                    .ADDRESS NUMBER1                ; Address of the first number
                    .ADDRESS NUMBER2                ; Address of the second number

            .PSECT  _CALLER_CODE,EXE,NOWRT,LONG,PIC,SHR
            .ENTRY  CALLER,^M<R2,R3,R4,R5,R6,R7,R8,R9,R10,R11>

            BSBW    GET_STARTED                     ; Branch to GET_STARTED subrtn
                                                    ; Status is returned in R0
            RET                                     ; Return to caller

    ;------------------------------
    GET_STARTED:
            PUSHL   R1                              ; Save contents of R1
            CLRL    R1                              ; Clear it for no good reason

            CALLS   #0,CALLS_START                  ; Now call

            POPL    R1                              ; Restore contents of R1
            RSB                                     ; Return to caller

    ;------------------------------
            .ENTRY  CALLS_START,^M<R2,R3,R4,R5,R6>

            CALLG   ARGLIST,START_C_RTN             ; Use CALLG to call next proc.

            RET                                     ; Return to caller

    ;------------------------------
    ;+
    ;
    ;  Routine:     DO_MATH
    ;
    ;  Functional Description:
    ;
    ;       Perform stupid math tricks.
    ;
    ;  Formal parameters:
    ;
    ;        4(AP)  - The type of math to do.  Longword passed by value.
    ;        8(AP)  - The first number.  Longword passed by value.
    ;       12(AP)  - The second number.  Longword passed by value.
    ;       16(AP)  - Address of longword to receive the result.  By reference.
    ;
    ;  Returns:
    ;
    ;       R0      - Status
    ;
    ;-
    TYPE    = 1 * 4                                 ; Type of math
    NUM1    = 2 * 4                                 ; First number
    NUM2    = 3 * 4                                 ; Second number
    RESULT  = 4 * 4                                 ; The result

            .ENTRY  DO_MATH,^M<R2,R3>
            MOVL    #LIB$_WRONUMARG,R0              ; Assume wrong number of args
            CMPB    #4,(AP)                         ; Are there four arguments?
            BNEQ    BYE                             ; Branch if not OK

     10$:   MOVL    #SS$_NORMAL,R0                  ; Set up R0 to assume error
            CASE    TYPE    = B,-                   ; Type is byte
                    SRC     = TYPE(AP),-            ; Source is type argument
                    LIMIT   = #1,-                  ; Limit starts at one
                    DISPLIST= <-                    ; The displacements
                            ADD,-
                            SUBTRACT,-
                            MULTIPLY,-
                            DIVIDE>
            MOVL    #SS$_ABORT,R0                   ; Return abort status
            BRB     BYE

    ADD:    ADDL3   NUM1(AP),NUM2(AP),@RESULT(AP)   ; Add the values and store them
            BRB     BYE

    SUBTRACT:
            SUBL3   NUM2(AP),NUM1(AP),@RESULT(AP)   ; Subtract NUM2 from NUM1
            BRB     BYE

    MULTIPLY:
            MULL3   NUM1(AP),NUM2(AP),@RESULT(AP)   ; Multiply NUM1 and NUM2
            BRB     BYE

    DIVIDE: DIVL3   NUM2(AP),NUM1(AP),@RESULT(AP)   ; Divide NUM1 by NUM2

    BYE:    RET                                     ; Return to caller

            .END    CALLER

------------------------------------------------------------------------

### Program 2

    /*
     *  Trivial little C program to demonstrate calling a trivial MACRO routine
     *  to perform simple math.
     *
     *  START_C_RTN is called from a MACRO procedure.  It then calls the MACRO
     *  procedure DO_MATH to do the real work.
     *
     *  Trivial, but it does show how arguments can be passed to and from routines.
     *
     */

    #define ADD 1
    #define SUB 2
    #define MUL 3
    #define DIV 4

    extern long int DO_MATH (long int, long int, long int, long int *);

    long int
    start_c_rtn (long int *number1, long int *number2)
    {
       long int results;
       long int status;

       printf("The first number passed to START_C_RTN is %d\n", *number1);
       printf("The second number passed to START_C_RTN is %d\n", *number2);

       status = DO_MATH (ADD, *number1, *number2, &results);
       if (status)
            printf("%d + %d = %d\n", *number1, *number2, results);
       else
            printf("Error doing addition\n");

       status = DO_MATH (SUB, *number1, *number2, &results);
       if (status)
            printf("%d - %d = %d\n", *number1, *number2, results);
       else
            printf("Error doing subtraction\n");

       status = DO_MATH (MUL, *number1, *number2, &results);
       if (status)
            printf("%d * %d = %d\n", *number1, *number2, results);
       else
            printf("Error doing multiplication\n");

       status = DO_MATH (DIV, *number1, *number2, &results);
       if (status)
            printf("%d / %d = %d\n", *number1, *number2, results);
       else
            printf("Error doing division\n");

       return(status);
    }

