
# MACRO Made Easy – Part III: A CASE for Looping

## MACRO Made Easy

## Part III: A CASE for Looping

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

Continuing with our discussion of branch instructions, let’s examine the powerful tested-loop instructions that are part of the VAX instruction set. These instructions let high-level constructs such as WHILE and FOR loops execute quickly and efficiently on a VAX. Their existence also makes the transition from high-level-language programmer to MACRO programmer easier, since you don’t have to change how you normally think of programming.

There are essentially three groups of controlled branch instructions: those that subtract and compare, those that add and compare, and the CASEx instructions. Before getting into these groups, let’s look at how loops could be implemented using the instructions covered last issue.

### SIMPLE CONTROLLED LOOPS

A controlled loop consists of a branch instruction with a negative displacement and a comparison that determines when the loop should be terminated. Of course, a loop may never terminate (an infinite loop), depending on the application.

Using that definition as a guide, a very simple loop might look like the following pseudo-code:

    LOOP:   Compare two values
            Are they equal?
            No, branch back to LOOP
            Yes, drop through

The following fragment shows one method for implementing a loop like this:

            CLRL    R0              ; Clear R0
     10$:   INCL    R0              ; Bump R0
            CMPL    #100,R0         ; Is R0 = 100?
            BNEQU   10$             ; Loop if not

As you can tell from the comments, the contents of R0 start at 0 and are incremented until the value reaches 100. Alternatively, the test could have been performed first:

            CLRL    R0              ; Clear R0
     10$:   CMPL    #100,R0         ; Is R0 = 100?
            BEQLU   20$             ; Exit loop if so
            INCL    R0              ; Bump R0
            BRB     10$             ; Loop back

This type of loop is frequently used when an action must be repeated until a certain condition is detected. For example, assume you need to call a routine GET_LINE that reads a line from the terminal until the status RMS$_EOF (end of file, which means the user typed CTRL-Z) is returned. One way to code this loop is:

     10$:   CALLS   #0,GET_LINE     ; Read a line
            CMPL    #RMS$_EOF,R0    ; Was EOF returned?
            BNEQ    10$             ; Loop if not
            [...]

This loop is functionally equivalent to the following two fragments of pseudo-code:

            DO status = GET_LINE (buffer)           !An UNTIL loop
            UNTIL status EQL RMS$_EOF;

status = GET_LINE (buffer); !A WHILE loop WHILE (status NEQ RMS$_EOF) status = GET_LINE (buffer);

One of the problems with this loop is that other conditions are not handled—if some other error is returned that would prevent the EOF status from ever appearing, we’d end up in an infinite loop. A better way to code such a loop is

     10$:   CALLS   #0,GET_LINE     ; Read a line
            BLBS    R0,10$          ; Loop until error
    ;
    ;  Here an error occurred.  See if it's RMS$_EOF.
    ;  If it's not, branch to an error handler.
    ;
            CMPL    #RMS$_EOF,R0    ; Is it EOF?
            BNEQ    ERROR_HANDLER   ; No---branch to error handler
            [...]                   ; Normal code resumes....

Another very common example of this type of loop is when locating a character in a buffer. For example, assume you have the following buffer defined in a MACRO program:

            TEXT:    .ASCID  /This is a test; let's see how it works!/

One way to find the semi-colon (;) in the string is to use a loop like the following:

            MOVW    TEST,R0         ; Get the length of the string
            MOVL    TEST+4,R1       ; Get the address of the string
     10$:   CMPB    #^A/;/,(R1)+    ; Is this the semi-colon?
            BEQLU   20$             ; Branch if so
            DECL    R0              ; Decrement remaining length
            BNEQU   10$             ; Loop if not zero
            ; Here it wasn't found
            [...]
     20$:   ; Here it was found

Notice that this loop takes advantage of the fact the DECL (DECrement Longword) instruction sets the condition codes based on the final value in R0; if the value in R0 is zero, the Z condition code is set and the BNEQU fails. (There is a special instruction, LOCC, that is normally used to locate characters. The character instructions will be covered in a future article.)

### A BRIEF ASIDE TO DISCUSS LITERALS

This fragment also demonstrates an alternative way to specifying literals within instructions. If you’ll recall from Part 1 (August 1991), specifying a pound sign (#) before a number stores the literal value of that number in the instruction. For example, to move the value 100 to a register, you’d write:

            MOVL    #100,R0         ; Store 100 in R0

By default, all numbers in MACRO are assumed to be decimal values. If you wanted to store a hexadecimal 100 in R0, you’d write:

            MOVL    #^X100,R0       ; Store hexadecimal 100 in R0

The notation “^X” temporarily places the assembler in hexadecimal mode and the 100 is treated as hexadecimal 100. Other modes that may be specified are octal (^O), decimal (^D), and ASCII (^A). Just like with the ASCII directives like .ASCID, the value of an ASCII literal must be enclosed in a matching pair of characters. The example above used slashes to delimit the ASCII character:

            CMPB    #^A/;/,(R1)+

The value generated by “#^A/;/” is equivalent to “59”, “^X3B”, and “^O73”. The maximum length of an ASCII literal is four bytes (a longword), because the maximum size of an immediate operand is 4 bytes. The use of “^A” makes the source code easier to read when multiple characters are specified, because the ASCII characters are specified in their normal order. For example, assume you want to store the string “GOAT” in R0. Using “^A”, the instruction would be:

            MOVL    #^A"GOAT",R0    ; Note that " was used to delimit GOAT

Because the VAX is “little-endian,” the literal is actually stored as “TAOG” (in hexadecimal, the bytes are 54, 41, 4F, and 47). If you wanted to specify the hex value, you’d have to write the instruction as:

            MOVL    #^X<54414F47>,R0        ; Note <> to make it easier to read

Obviously, the “^A” form makes it easier to see what’s being stored.

### THE SOB INSTRUCTIONS

Getting back to our discussion of the looping instructions, you may recall that the program described in Part 1 used a SOBGTR instruction to implement the loop above. The SOBGxx instruction actually comes in two flavors: SOBGTR (Subtract One and Branch if GreaTeR) and SOBGEQ (Subtract One and Branch if Greater than or EQual). The use of one instruction over the other is determined simply by the needs of the application.

The example above could be rewritten to use the SOBGTR instruction:

            MOVW    TEST,R0         ; Get the length of the string
            MOVL    TEST+4,R1       ; Get the address of the string
     10$:   CMPB    #^A/;/,(R1)+    ; Is this the semi-colon?
            BEQLU   20$             ; Branch if so
            SOBGTR  R0,10$          ; Loop until no more string
            ; Here it wasn't found
            [...]
     20$:   ; Here it was found

The SOBGxx instructions take two parameters: the operand to be decremented and the address of the instruction to which control should be transferred if the test is true. Both instructions decrement the loop counter and then compare the result to zero. SOBGTR will take the specified branch if the result is greater than zero, while SOBGEQ will take the branch if the result is greater than or equal to zero. The SOBGxx instructions are usually used to implement controlled loops that must be iterated some known number of times.

If you look in the MACRO manual or in the on-line help, you’ll find the index operand (the loop counter) is listed as “index.ml”, which means that it must be a modifiable longword; the index operand cannot be a byte or word. SOBGxx loops are usually constructed using a register as the index operand. Also note that, like all of the branch instructions, the target address for the branch must be within approximately 127 bytes of the SOBGxx instruction.

Some compilers will use the SOBGxx instructions to implement certain instances of FOR loops. For example, the assembly code produced by the VAX C and GNU C compilers when the following code is compiled includes a SOBGTR instruction:

            main()
            {
              int i;
              for (i=100; i > 0; i--)
                printf("%d",i);
              exit(1);
            }

The BLISS compiler implements some instances of its FROM/TO construct using the SOBGxx instruction.

### THE AxB INSTRUCTIONS

The other instructions used to implement loops such as those described above are those that add a value to the loop counter and branch depending on the result. This family of instructions includes AOBLSS (Add One and Branch if LeSS than), AOBLEQ (Add One and Branch if Less than or EQual), and ACBx (Add, Compare, and Branch). As indicated by the names of the instructions, the AOBLxx instructions add one to the index operand, while the ACBx instruction adds an arbitrary amount.

The AOBLxx instructions take three operands: the limit, the index, and the displacement for the branch. As with the SOBGxx instructions, the index is a modifiable longword; again, registers are frequently used for the index, although memory addresses can be used too.

The limit operand specifies the value that the index is compared to when determining whether or not to take the branch. In the SOBGxx instructions, the limit was always 0. With the AOBLxx instructions, any longword value may be specified. These instructions are useful for implementing loops like the FOR/NEXT construct in BASIC. For example, the following code fragment loops one hundred times:

            MOVL    #1,R0           ; Start with 1
     10$:   MOVB    R0,(R1)+        ; Move it to some buffer
            AOBLEQ  #100,R0,10$     ; Loop 100 times

This is roughly equivalent to the following BASIC loop:

            FOR I = 1 TO 100
            [...]
            NEXT I

Using C as an example, again, the following null loop generates two lines of assembly code:

              for (i=1; i <= 100; i++);

The equivalent MACRO code would be something like the following:

            MOVL    #1,R0           ; Start at 1
     10$:   AOBLEQ  #100,R0,10$     ; Loop until R0 = 100

Programming Hint \#1: As you can see, it is possible to implement the same kinds of loops using either the SOBGxx or the AOBLxx instructions. However, because they compare the index to zero, the SOBGxx instructions are more efficient and should be used wherever possible.

The micro-code for the instructions (the low-level machine code that implements the VAX instructions) makes it very efficient to compare values to 0. Because AOBLxx must compare the index to a fixed value, the comparison takes longer. Also, it is more efficient to use two registers as the index and limit than it is to use a literal for the limit or memory for the index (because accessing the contents of the registers is much faster than accessing memory).

Granted, the differences in CPU time are almost negligible in the overall execution time of a program, but I’m a firm believer in writing programs as efficiently as possible. Of course, readability should not be sacrificed for efficiency unless you carefully document the reasons for selecting one method over another or you are writing certain kinds of system code.

As mentioned above, the ACBx instructions add an arbitrary value to the index and then compare the index to the limit. Like many other VAX instructions, the ACBx comes in several variants, depending on the size of the operands. For example, ACBW (Add, Compare, and Branch Word) compares words, ACBL compares longwords, and ACBB compares bytes. There are also floating-point ACBx instructions that won’t be discussed here.

The ACBx instructions differ from AOBLxx in several respects; the ACBx are much more flexible than their AOBLxx counterparts. First, ACBx instructions have four operands: the limit, the add amount, the index, and the displacement. The add amount can be positive or negative; its sign determines how the branch will be determined. If the add is greater than or equal to 0 and the index is less than or equal to the limit, the branch is taken. If the add is negative, the branch is taken only while the index is greater than or equal to the limit. This difference allows the ACBx instructions to perform as addition and subtraction commands, eliminating the need for SCBx instructions.

Second, the sizes of the limit, index, and add are all determined by the type of instruction used. For ACBB, all three operands are treated as bytes; for ACBW, they are all treated as words. Remember that the AOBLxx instructions always treat the index and limit as longwords.

Finally, the displacement operand for ACBx is a word displacement, not the byte displacement accepted by AOBLxx, which means that the branch destination must be within approximately 32767 bytes of the ACBx. This means that a AOBLEQ with a word displacement can be fashioned via a line similar to the following:

            ACBL    #LIMIT,#1,R0,10$        ; Add one, branch LEQ

As an example of the power of the ACBx, look at this FOR/NEXT loop in BASIC:

            J = 0
            FOR I = 0 TO 100 STEP 2
              J = J + 1
            NEXT I

Assuming R0 is I and R1 is J, the following MACRO code produces equivalent results:

            CLRL    R1              ; J = 0
            CLRL    R0              ; FOR I = 0
     10$:   INCL    R1              ; J = J + 1
            ACBL    #100,#2,R0,10$  ; FOR I = 0 TO 100 STEP 2

The code isn’t exactly the same, because the value left in R0 at the end of the loop will be 102. To produce exactly the same results, the following instruction would have to follow the ACBL:

            SUBL2   #2,R0           ; Bring I back down 2

Such subtle differences are automatically taken care of by high-level language compilers.

### THE CASEx INSTRUCTIONS

We’ve seen how the SOBGxx, AOBLxx, and ACBx instructions can be used to implement the looping constructs offered by high-level languages. One construct that was not covered, though, is the CASE. The general format of a CASE construct is:

            CASE object
               WHEN case1 : DO this;
               WHEN case2 : DO this;
               WHEN case3 : DO this;
               OTHERWISE:   Do this;

The VAX architecture includes a CASE in its instruction set. There are three CASE instructions: CASEB, CASEW, and CASEL. You should recognize by now that the last letter of each mnemonic determines how the operands are treated. The CASEx operands are: selector, base, limit, and a variable number of word displacements. The selector is the object that is being tested; the base and limit determine the lower and upper values that the selector can have. The sizes of the selector, base, and limit are determined by the CASEx variant.

The CASEx instruction is pretty unique among the VAX set. It accepts a variable number of operands that consist solely of branch offsets. Before explaining more, let’s look at a very simple example.

            CASEL   R0,#0,#2
     10$:   .WORD   ZERO-10$        ; CASE R0 = 0
            .WORD   ONE-10$         ; CASE R0 = 1
            .WORD   TWO-10$         ; CASE R0 = 2
            ; Otherwise
            RET

ZERO: \[…\] RET ONE: \[…\] RET TWO: \[…\] RET

Notice that the word offsets are constructed by subtracting the label 10$ from the target label. All displacements are from the address following the CASEx instruction; using a local symbol like 10$ makes it easy to calculate the offsets. You must remember to always use a label for the first displacement, not the address of the CASEx itself.

When the CASEL executes, the base is subtracted from the selector and stored in a temporary location. This temporary is then compared (unsigned) to the limit and, if the temporary is less than or equal to the limit, a branch displacement is selected and added to the PC. Because the displacements are word values, the selection is made by multiplying the temporary by 2. If the temporary is not LEQU to the limit, a displacement of (2\*(limit+1)) is added to the PC.

So what does all of that mean? Basically, that your base should be the lowest possible value of your selector, and the limit should be the number of possible sequential values, minus 1. The number of displacements that should be specified is equal to the specified limit, plus one. This is kind of tricky to figure out when you first start using CASEx. For example, in the code above, there are three possible values that can be in R0: 0, 1, and 2. The base is 0 and the limit is 2 (3 possibilities minus 1). The number of displacements actually specified is, therefore, 3, one for each possible value in R0.

Now, assume that R0 holds the value 1. Once the CASEL is fetched, the PC (Program Counter) points to 10$, the address following the CASEL. The base, 0, is subtracted from the 1 in R0, resulting in a temporary value 1. This temporary is then compared with the limit, 2, and is found to be less than or equal to the limit. Therefore, the temporary is multiplied by 2 to determine the offset for the proper displacement. In this example, that yields 2, so the second word displacement is selected and added to the PC, causing it to point to the label ONE:.

If R0 held 3, the subtraction would have resulted in a temporary value of 3, which is greater than the limit. In this case, 2\*(limit+1) is added to the PC, causing it to point to the instruction following the displacement table. This effectively implements the OTHERWISE clause provided by high-level languages.

Note that you must have a displacement for all possible values that fall sequentially between the base and the limit. If you want to skip a case, you can simply point the offset for that value to the instruction just past the displacement table. For example, suppose in the example above that you wanted only 0 and 2 to be valid for the CASE. You could change the displacement table so that it looks like the following fragment:

            CASEL   R0,#0,#2
     10$:   .WORD   ZERO-10$        ; CASE R0 = 0
            .WORD   OTHER-10$       ; CASE R0 = 1 (do nothing)
            .WORD   TWO-10$         ; CASE R0 = 2
     OTHER: ; Otherwise
            RET

ZERO: \[…\] RET TWO: \[…\] RET

### THE CASE MACRO

The CASEx is one of the instructions that makes the VAX architecture so powerful and helps make MACRO programs easier to maintain. Unfortunately, it is a little cumbersome, requiring extra attention to the values of the limit and the number of displacements. In order to make it easier to setup a CASEx statement, DEC has provided a CASE macro that can be used in its place.

In Part 1, you read that DEC-supplied macros are stored in macro libraries in SYS$LIBRARY; the STARLET.MLB was described then. DEC also provides a second macro library, called LIB.MLB, that primarily contains macros used by systems programmers. The LIB library contains, among others, macros that define most of the data structures used internally by VMS, macros that raise IPL and acquire spinlocks, and a few general-purpose macros. The CASE macro is an example of a general-purpose macro that is in LIB instead of STARLET, though the reason is unclear.

To use the CASE macro, you have to tell the MACRO assembler to search the LIB library. You can do this a couple of ways: via the command line or a .LIBRARY directive. The simplest way is to use the directive, so that you don’t have to remember any special qualifiers for the MACRO command line. The .LIBRARY directive should look like:

            .LIBRARY  /SYS$LIBRARY:LIB.MLB/         ; Search LIB.MLB

As with other directives, the slashes can be replaced by quotes or any other pair of matching characters. (If you want to use the command line, see the MACRO manual and on-line help for information on the /LIBRARY qualifier.)

The CASE macro is a rather short macro, actually, that demonstrates how powerful the macro capability of the MACRO assembler is. We’ll defer looking at the macro until a future article. For now, let’s just look at how the macro would be used.

The CASE macro accepts several named parameters: SRC, which is the selector; LIMIT, which in this case refers to the base value and defaults to \#0; TYPE, which defaults to “W”; NMODE, which determines how the limit value is stored and defaults to “S^#” so that the limit is stored as a short literal; and DISPLIST, which is the list of target addresses. The macro automatically figures out the upper limit based on the number of displacement addresses that are provided.

The CASEL example above could be re-coded using the CASE macro:

            CASE    TYPE    = L,-           ; Type is CASEL
                    SRC     = R0,-          ; Source is R0
                    LIMIT   = #0,-          ; Lower limit is 0 (default)
                    DISPLIST= <-            ; There are three displacements
                            ZERO,-          ; ... Notice how the <> are used
                            ONE,-           ; ... to delimit the DISPLIST
                            TWO>            ; ... value

While it still looks pretty cumbersome, it does eliminate the need to set up all of the .WORD displacements. SRC and DISPLIST are positional parameters, too; if you wish to accept all of the defaults, you can shorten the CASE call to:

            CASE    R0,<zero,one,two>       ; CASEW with base of #0
    </zero,one,two>

### NEXT TIME….

This month we covered most of the instructions that are used to implement the various controlled-loops offered by high-level languages. You’ve also seen how literals may be specified in instructions, and how you can use macros stored in the LIB macro library. Next issue, we’ll look at the methods for setting up and calling subroutines and routines written in MACRO or high-level languages.

------------------------------------------------------------------------

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.\

