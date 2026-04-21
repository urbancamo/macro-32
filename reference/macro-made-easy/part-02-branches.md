
# MACRO Made Easy – Part II: Branches

## MACRO Made Easy

## Part II: Branches

### or

## How Do I Get There from Here?

#### by

### Hunter Goatley

### Western Kentucky University

------------------------------------------------------------------------

Last issue, I presented a MACRO program that, while very simple, demonstrated many of the important concepts of MACRO programming. Before getting into a discussion of how to manipulate data in MACRO, I thought we’d start this issue with a look at how you can control the flow of a program using branch instructions and various tests. Since most data manipulation is repetitive or conditional, I decided that future articles would be easier to follow if we discussed branches first so they can be used later without looking like “magic.” We’ll also look at a very simple macro to introduce the usage of MACRO macros.

Branch instructions are used to change the normal flow of execution in a program. Normally, a program executes the instructions in sequential order: fetch an instruction, execute it, fetch the next instruction, execute it, etc. You obviously wouldn’t be able to write a very useful program if you there wasn’t some way to change that flow and skip sections of code to execute other sections. The branch instructions allow you to control the flow of your program in a number of ways.

A branch is affected by changing the address of the next instruction to execute, which is maintained in the special register PC (Program Counter). When I use the term PC throughout this article, you should assume that I really mean the address that is stored in the PC, unless I refer specifically to the register itself. Since the PC is a register and registers are longwords (32 bits), the VAX can address 2^32 bytes (more than 4 gigabytes).

There are about 45 branch-related instructions in the MACRO instruction set. All of these instructions perform the branch by modifying the contents of the PC in one of three ways: by incrementing the value stored in the PC, by decrementing the value, and by replacing the value. In all three cases, the address stored in the PC is modified to point to a new instruction.

Though the number of instructions sounds intimidating, keep in mind that, as I mentioned last time, many of the instructions are simply variations of other instructions. For example, there are three instructions that unconditionally transfer control to another address: BRB, BRW, and JMP. The instruction used depends upon the context of the branch. The following code fragment shows how these instructions are normally used:

            MOVL    R0,R1                   ; Copy R0 to R1 for no reason
            BRB     10$                     ; Skip over the next section of code
            CLRL    R1                      ; Never executed in this example
     10$:   CLRL    R0                      ; Clear the contents of R0

In this example, the “CLRL R1” instruction would never be executed, unless some other instruction transferred control to that address. Obviously you wouldn’t normally write code like this; if the CLRL instruction is not needed, you’d simply leave it out. However, simple branches like this can be useful when debugging code to skip non-essential or incomplete portions of code.

### HOW A BRANCH INSTRUCTION WORKS

The “BRB” mnemonic stands for “branch with byte displacement,” which means that the byte following the instruction’s opcode is a value that should be added to the PC. For example, let’s look at the listing file created from the code above (with added headers to show what each column is):

                  Binary    Addr   Src
                   Code           Line
                  --------  ----  ----
                      0000  0000     1         .entry x,^m<>
                   02   11  0002     2         BRB     10$
                   51   D4  0004     3         CLRL    R1
                   50   D4  0006     4 10$:    CLRL    R0

The line for “BRB 10$” shows that the BRB opcode is “11” and the operand is “02”. This is the byte displacement that is added to the PC to affect the branch. Let’s say we’re ready to execute the BRB instruction; the PC contains “0002”, the address of the BRB. When the opcode and operand are fetched by the CPU, the PC is updated to “0004”, the address of the next instruction to execute. Now the “BRB” instruction is executed and the byte “02” is sign-extended to fill a longword and added to the PC (“0004”), changing the PC to contain address “0006”. Now the CPU is ready to fetch the next instruction to execute, which is now the instruction at address “0006”, the “CLRL R0”.

If the branch is a backwards branch (the target address precedes the current address), the byte displacement is a negative value. The value is sign-extended to fill a longword and then added to the PC, effectively subtracting an amount from the PC.

Before looking at an example, let’s look at address arithmetic for a moment. The high-bit of a number is the sign bit, indicating whether the number is positive or negative. If the high-bit is 0 (clear), the number is positive; if the high-bit is 1 (set), the number is negative. When a number is “sign-extended”, the high-bit is replicated to fill the preceding bytes out to the desired size. For example, when a byte is converted to a longword, the three high bytes in the longword are filled with the sign-bit to form a positive or negative longword number:

            Decimal         Byte    ->      Longword
            -------         ----            --------
             -1              FF     ->      FFFFFFFF
              2              02     ->      00000002

There are MACRO instructions to convert bytes to words to longwords and vice versa. We’ll look at those later.

Getting back to the backwards branch example, consider the following fragment from a listing file:

           50   01   D0  0002     2 05$:    MOVL    #1,R0
                FB   11  0005     3         BRB     05$

As you can see, the byte displacement for BRB is “FB” (-5). After the BRB instruction has been fetched, PC contains “0007”; 5 must be subtracted from the PC to point to “0002”.

VMS trivia—the code for the NULL process consists of one line resulting in an infinite loop:

            10$:    BRB     10$

### OTHER DISPLACEMENT SIZES

As should be obvious by now, the byte displacement for BRB limits how far away the target can be. Specifically, the target address must be within 127 bytes of the BRB instruction, since the largest positive value that can be stored in a byte is 127. The MACRO assembler will complain that an address is out of range if the positive offset is greater than 127:

            BRB     10$             ; Branch to 10$
            .BLKB   128             ; Put 128 bytes in between them
     10$:   RET                     ; Target instruction

When the program is assembled, the following error is generated:

%MACRO-E-BRDESTRANG, Branch destination out of range

You’ve now seen one of the most common (and most frustrating) errors encountered by MACRO programmers. The addition of a few instructions can cause change the offsets enough to affect lots of branches in a program. It’s not uncommon for dozens of lines to be flagged with the “out of range” error.

Note that the lower limit for negative byte displacements is -128. However, because the branch instruction itself requires 2 bytes, the effect is that the destination address must be within 126 bytes from the address of the branch instruction. So what does all this mean? Well, it means that most people don’t count the bytes since the assembler will complain if it’s too far away, so the easiest thing is to do is just remember that the limit is +/- 127 bytes. One MACRO textbook I’ve seen even stated that the difference between destination address and the branch instruction is “approximately 127 bytes”!

So what can you do about the problem? Well, if you are using BRB instructions, you can simply replace them with BRW instructions (BRanch with Word displacement). As the name implies, a word is used to hold the displacement offset instead of a byte, changing the offset limits from +/- 127 to +/- 32767. For example, modifying the code above generates:

                       0000  0000     1         .entry x,^m<>
                  0080   31  0002     2         BRW     10$
                   00000085  0005     3         .BLKB   128
                         04  0085     4 10$:    RET

Now the word displacement “0080” is sign-extended to a longword and added to the PC to point to address 0085. Note, too, that the number of bytes needed to store the instruction increased from 2 to 3, since the word displacement requires one additional byte of storage. Judicious use of BRB and BRW instructions can result in space savings, which isn’t normally critical but could be important in systems code.

The JMP instruction differs from the BRx instructions in that the target address is actually stored in a longword following the instruction opcode. Instead of storing a displacement that is added to the PC, the longword actually replaces the contents of the PC. Replacing the BRW above with a JMP instruction yields:

                       0000  0000     1         .entry x,^m<>
           00000088'EF   17  0002     2         JMP     10$
                   00000088  0008     3         .BLKB   128
                         04  0088     4 10$:    RET

Note that the JMP instruction requires 6 bytes of storage, not 5, because the byte “EF” is used to describe the longword that follows (it identifies the operand as being “longword relative”). I plan to cover the details of opcodes and operands in a future article; for now, it’s enough to know that the longword is preceded by a “description” byte.

As you can see, the JMP instruction is expensive in terms of storage required. The only time it should be used is when it is known that the destination is more than 32767 bytes away. Most programs never even approach that size, so it’s safe to say that, practically, the only time the JMP instruction would be used is when you are transferring control to an address in system space.

### A WARNING ABOUT CHOOSING INSTRUCTIONS

Frequently, assembly programmers who are new to MACRO will pepper their code with JMPs, since that’s the instruction many assembly languages use to transfer control. The differences between BRB, BRW, and JMP exemplify the advantages and disadvantages of the complex instruction set used by the VAX architecture. The advantages include the ability to control program size and execution speed with the proper use of a given instruction; the obvious disadvantage is that you must know that there are several instructions to choose from when writing MACRO code.

Intimate knowledge of the VAX instruction set is not something you can expect to achieve quickly. When I first started using MACRO-32 7 years ago, I had no idea what many of 350+ instructions did. I found one that did what I wanted and used it. Over time, I discovered more and more instructions and realized that my early programs were poor examples of MACRO programming (this is true even with some of the code accompanying some of my previous VAX PROFESSIONAL articles). My point is: if you’re new to MACRO programming, don’t worry about trying to master the entire instruction set; you’ll learn it, but it may take a little while.

One of my objectives for this column is to help you avoid common mistakes when writing MACRO programs. So here’s Programming Hint \#1:

Avoid the JMP instruction when BRB and BRW can be used to achieve the desired branch.

### CONDITIONAL BRANCHES

Most of the 45 branch-related instructions are conditional branches, meaning that they branch only if some condition is true. The large number of instructions allows you to write very sophisticated looping constructs, including those usually associated only with high-level languages. The displacement operand for all of the conditional branch instructions is stored in one byte. This section will present some of the more common conditional branch instructions, starting with BLBC and BLBS, which were briefly mentioned in the previous article.

The VAX calling standard specifies that R0 (and sometimes R1) is used by a subroutine to return a status value to its caller. By convention, odd values are treated as success and even values indicate an error occurred. This convention allows the use of the two branch instructions BLBC (Branch Low Bit Clear) and BLBS (Branch Low Bit Set) to allow for branching to handle error and success statuses. As shown before, BLBC is frequently used to branch to an error handler if a routine returns an error:

            CALLS   #0,DO_SOMETHING                 ; Call some routine
            BLBC    R0,ERROR                        ; Branch if an error occurred

There are more “generic” branch instructions that allow you to specify which bit should be tested to determine whether or not to branch. The BBC (Branch Bit Clear) and BBS (Branch Bit Set) instructions are frequently used when testing a bitmask for certain flags. If you wanted to perform a branch when bit 3 is set in R4, you could use the following instruction:

            BBS     #3,R4,10$               ; Branch if bit 3 is set

The first operand is the bit number to check (numbered from 0), the second operand is the source longword, and the third operand is the destination label. It should be clear now that you can use the BBC and BBS instructions to perform the same checks as BLBC and BLBS by simply specifying bit number 0:

            BBC     #0,R0,ERROR             ; Branch if low bit is clear

However, The BLBC and BLBS instructions are slightly faster because the bit that must be checked is fixed at bit 0, which is the bit addressed by the source operand; the BBS and BBC instructions must allow for the bit to be located at some additional offset from the base address.

The other BB instructions are:

- BBSS – Branch if bit is set and set the bit
- BBSC – Branch if bit is set and clear the bit
- BBCC – Branch if bit is clear and clear the bit
- BBCS – Branch if bit is clear and set it

These instructions are useful when you want to control a program’s flow based on the current setting of a flag and you want to leave the flag in a known state. For example, assume you want to use bit 3 in R0 to determine whether or not a variable should be zeroed out. The following infinite loop demonstrates how the BBSS instruction could be used:

            CLRL    R0              ; Clear R0 (start with bit 3 clear)
     10$:   BBSS    #3,R0,20$       ; Branch if bit 3 is set; in either
                                    ; ... case, go ahead and set it
            CLRL    R1              ; Clear contents of R1
     20$:   INCL    R1              ; Bump contents of R1 by 1
     30$:   BRB     10$             ; Infinite loop

The first time the BBSS is executed, R0 contains 0 (no bits set). The BBSS does not take the branch, but it does set bit 3 in R0. Execution drops through to the CLRL R1, then the INCL R1, and finally BRB 10$. Now the BBSS is executed again, but this time bit 3 in R0 is set, so the branch is taken, the bit is set (even though it’s already set), and the PC is updated to point to INCL R1. The CLRL R1 instruction will never be executed again in this infinite loop. Obviously, you wouldn’t really write a routine like this, but it does demonstrate how a bit flag can control execution flow and be manipulated with a single instruction.

### CONDITION CODE BRANCHES

The VAX has a special PSL (Processor Status Longword) that contains information relevant to the current state of the processor (fancy that!). Four of the bits in the PSL are known as the condition codes. These bits are named as follows:

- N-bit (Negative) — Set when an instruction stores a negative result, cleared when the result is positive or zero.
- Z-bit (Zero) — Set when a result is 0, cleared when the result is positive or negative.
- V-bit (oVerflow) — Set when an arithmetic instruction results in overflow (the result is too large for the destination).
- C-bit (Carry) — Set when an arithmetic instruction results in a carry to or borrow from the most significant bit.

Not all instructions affect the condition codes; the *VAX Architecture* books and the MACRO manual describe when and how the codes are affected by each instruction.

The condition-code branches are usually seen following CMPx (CoMPare) and TSTx (TeST) instructions. As with the MOVx instruction, there are variants of these instructions for different sizes: CMPB (compare byte), CMPW (compare word), CMPL (compare long), etc. There are 16 instructions that test the condition codes to determine whether or not to branch. The more commonly used are:

- BEQL — Branch if EQual
- BNEQ — Branch if Not EQual
- BGTR — Branch if GreaTeR than
- BGEQ — Branch if Greater than or EQual
- BLSS — Branch if LeSS than
- BLEQ — Branch if Less than or EQual

These instructions are signed instructions, meaning that the sign of the result is taken into account when the test is made. You can append ‘U’ to any of the instructions to force an unsigned test. The signed form is usually used when performing signed integer or floating-point arithmetic; the unsigned forms are used when comparing addresses, characters, and unsigned integers. The following code fragment demonstrates how these instructions are typically used:

            CMPL    #3,R0                   ; Compare the contents of R0 with 3
            BLSS    10$                     ; Branch if less than
            BGTR    20$                     ; branch if greater than
            ; Here, R0 is equal to 3

Programming Hint \#2: The branch instructions do \*not\* modify the condition codes, making it possible to sequentially test the codes without having to do the compare over and over again.

There are also instructions to test the carry and overflow bits, but they are rarely used.

### COMPARISON INSTRUCTIONS

While we’re on the subject of comparisons, this is probably a good time to mention the comparison instructions. The CMPx (CoMPare) instructions compare two “scalar quantities,” which is to say, two numbers. The comparison is accomplished by subtracting the second operand from the first operand and setting the condition codes according to the result (compared to 0). The TSTx (TeST) instructions are used to compare a value to 0. They are functionally equivalent to using the CMPx instructions with a value of 0 as the second operand. Finally, the BITx (BIt Test) instructions perform a logical AND of two bitmasks and set the condition codes according to the result (compared to 0).

            CMPL    R4,R3           ; Compare contents of R4 and R3
            BLSSU   10$             ; Branch if R4 is less than R3

            TSTL    R4              ; Does R4 contain a 0?
            BLEQ    20$             ; Branch if less than or equal to 0

            BITL    #^X0F,R4        ; Are any of the first four bits set?
            BEQL    30$             ; Branch if first four bits are all 0

These instructions will be covered in more detail in a future article; I wanted to go ahead and let you know they exist because the condition-code branches don’t mean much with the instructions that set the condition codes!

As I mentioned above, most instructions that store a result also set the condition codes. This includes the MOVx instructions; once the value has been stored, it is compared to 0 and the condition codes are set. You’ll often see MACRO code that looks like the following segment:

            MOVL    X,R0            ; Move value at X into R0
            TSTL    R0              ; Was anything there (is it 0)?
            BEQLU   NOTHING         ; Branch to do nothing

The “TSTL R0” instruction is redundant in this case because the MOVL did an implicit TSTL after moving the value at X into R0. The code could be rewritten as:

            MOVL    X,R0            ; Move value at X into R0
            BEQLU   NOTHING         ; Branch to do nothing

Programming Hint \#3: When comparing values, check the previous instruction(s) to see if the condition codes are already set, letting you eliminate redundant TSTx instructions.

Again, I plan to cover these and other instructions in more detail in future articles.

### THAT &@^%#$@ “OUT OF RANGE” ERROR

Remember the “Branch destination out of range” error discussed above? Well, it’ll haunt you even more when you start using the conditional branch instructions, because each of them accepts only a byte displacement for the branch. This means that, for all of the conditional branch instructions, the branch destination must be within 127 bytes in either direction. As you can imagine this is somewhat limiting and is probably the single largest source of frustration for new MACRO programmers.

Author’s note: when discussing the actual number of bytes that can appear between a branch instruction and the destination, the figure 127 is normally used, even though it’s not really true

As you’ve probably guessed, the way around this limitation is to change the nature of the conditional test and add a BRW instruction to reach the real destination. For example, suppose that the following code generates an error because the label ERROR: is located more than 127 bytes away:

            CMPL    R0,R1           ; Compare R0 and R1
            BNEQU   ERROR           ; Branch if not equal

To get rid of the error message, add a BRW ERROR instruction and use the opposite condition-code branch instruction to jump to a local label:

            CMPL    R0,R1           ; Compare R0 and R1
            BEQLU   10$             ; Continue if they're equal
            BRW     ERROR           ; Not equal, so branch to handle error
     10$:

When you’re using the BLSS, BLEQ, BGTR, and BGEQ instructions, you want to be sure you flip the test correctly. For example, the following code:

            CMPL    R0,R1           ; Compare R0 and R1
            BLSSU   ERROR           ; Branch if R0 is less than R1

would become:

            CMPL    R0,R1           ; Compare R0 and R1
            BGEQU   10$             ; Continue if R0 is >= R1
            BRW     ERROR           ; R0 < R1, so branch to handle error
     10$:

If you have multiple branch instructions all going to the same out-of-range destination, there is another solution to the problem. The method may or may not be cleaner than adding multiple BRW instructions; it all depends on personal preference and whether or not the size of the code is important.

This second method involves adding a BRW instruction and having your conditional branches transfer control to the BRW to reach the final destination. Let’s take the following code as an example, where label DO_IT is out-of-range:

            CMPL    #2341,R0                ; Does R0 contain 2341?
            BEQLU   DO_IT                   ; Branch if so
            CMPL    #1432,R1                ; Does R1 contain 1432?
            BEQLU   DO_IT                   ; Branch if so
            CMPL    #555,PHONE              ; Does PHONE contain 555?
            BEQLU   DO_IT                   ; Branch if so
            [...]                           ; Otherwise do this....

This can be rewritten with minimal changes by adding one BRW instruction and two local labels:

            CMPL    #2341,R0                ; Does R0 contain 2341?
            BEQLU   10$                     ; Branch if so
            CMPL    #1432,R1                ; Does R1 contain 1432?
            BEQLU   10$                     ; Branch if so
            CMPL    #555,PHONE              ; Does PHONE contain 555?
            BNEQU   20$                     ; Branch if not
     10$:   BRW     DO_IT                   ; Branch to go DO_IT
     20$:   [...]                           ; Otherwise do this....

Of course, there are other ways the code could have been arranged, but the point is that you can branch to a BRW instruction that is within the 127-byte range to affect a branch to the out-of-range label.

### A SIMPLE MACRO TO CHECK FOR ERRORS

Because BLBC is used so frequently to check for errors, I usually save myself some frustration (at the expense of a few bytes) by using a macro that checks for errors and branches (with a word offset) to an error handler. I’m going to show you the very simple macro that I use, but I won’t be going into a whole lot of detail about writing macros (that’s for—you guessed it—a future article).

The problem: I want to branch to a specified label on any error returned from a subroutine. This would normally be coded as:

            CALLS   #0,SOME_ROUTINE         ; Call some routine
            BLBC    R0,ERROR                ; Branch if an error occurred

Our goal is to eliminate any potential “branch destination out of range” errors, so we effectively want to change all such calls to:

            CALLS   #0,SOME_ROUTINE         ; Call some routine
            BLBS    R0,10$                  ; Branch if successful
            BRW     ERROR                   ; Branch to error handler
     10$:   [...]

The following macro, named ON_ERR, does this:

            .MACRO  ON_ERR  ERRHND,?HERE    ;* Define a macro
            BLBS    R0,HERE                 ; Branch if successful
            BRW     ERRHND                  ; Branch to error handler
     HERE:  .ENDM   ON_ERR                  ;* End of macro definition

ON_ERR takes one parameter, the address of the error handler. The code above could then be changed to:

            CALLS   #0,SOME_ROUTINE         ; Call some routine
            ON_ERR  ERROR                   ; Branch if an error occurred

When the macro is expanded by the assembler, ERRHND is replaced by the specified parameter (ERROR, in this case) and the following code is generated:

            CALLS   #0,SOME_ROUTINE         ; Call some routine
            BLBS    R0,30000$               ; Branch if successful
            BRW     ERROR                   ; Branch to error handler
    30000$: [...]

The only “tricky” piece of the macro is the local label. If I had hardcoded a label name in the macro, I could only use the macro once; if it appeared twice, the macro would be expanded twice, using the hardcoded label name, which would generate an error stating that the label has multiple definitions.

Of course, it looks like I did hardcode a label, but the ‘?’ that appears before the label HERE on the .MACRO line tells the assembler to automatically generate a unique local label each time the macro is expanded. The first time it is expanded, the local label is 30000$, the second time 30001$, etc. The following excerpt is from a listing file generated with the DCL command $ MACRO TEST/LIST/SHOW=EXPANSIONS:

                            0002     7         ON_ERR  ERROR
                03 50   E8  0002               BLBS    R0,30000$
                 0080   31  0005               BRW     ERROR
                            0008        30000$:

Note that the listing shows both the macro call and the expanded binary code that was generated by the macro.

### NEXT TIME….

This month we covered several methods for controlling the flow of execution in a program, and you’ve seen a very simple, but useful, macro in action. Next issue, we’ll look at the instructions you’d use to implement the high-level looping constructs like WHILE, UNTIL, FROM/TO, and CASE.

See you next time: same Bat-time, same Bat-journal.

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.\

