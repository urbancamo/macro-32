
# MACRO Made Easy – Part VI: Character Witness

## MACRO Made Easy

## Part VI: Character Witness

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

### A Brief Word about Asynchronous System Services

Before moving on to the MACRO-32 character instructions, let’s take a brief look at the asynchronous system services. As the label implies, asynchronous system services complete asynchronously, which means that the calling program need not wait for the service to complete execution before continuing on. The system service can do one of two things (or both) to signal its completion: it can set an event flag that the program waits for and it can queue an Asynchronous System Trap (AST) to the process.

For event flags, a program calls the asynchronous system service, specifying the event flag to wait for and an I/O status block (IOSB). After the call returns, the program can continue on until it must check that the system service completed, at which point it calls the $SYNCH system service, again specifying the event flag number and the I/O status block. If the service has already completed, the event flag will already be set; the status is copied to the IOSB and control returns immediately to the calling program. If the service has not completed yet, the $SYNCH service places the process into an event flag wait state (LEF (Local Event Flag) or CEF (Common Event Flag), depending on the event flag number) until the event flag is set. At that time, the status is copied to the IOSB and the process is removed from the xEF wait state.

Some asynchronous system services have synchronous counterparts that automatically call $SYNCH on behalf of the caller. The synchronous versions have the same name, with a ‘W’ (for ‘W’ait) appended to the end. For example, the synchronous version of $QIO is $QIOW. Table 1 lists the asynchronous system services and their synchronous equivalents. Note that even when calling the synchronous versions, you should always specify an IOSB to ensure proper operation. Without it, multiple uses of an event flag within the same program could result in inaccurate waits. For example, if you use event flag \#0 for more than one system service call, without the IOSB there’s no way to tell which system service set the event flag.

**Table 1 — Ansynchronous System Services**

<table data-cellspacing="5">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<th style="text-align: left;">Asnychronous</th>
<th style="text-align: left;">Synchronous</th>
<th style="text-align: left;">Description</th>
</tr>
&#10;<tr>
<td colspan="3" style="text-align: left;"><hr /></td>
</tr>
<tr>
<td style="text-align: left;">$ABORT_TRANS</td>
<td style="text-align: left;">$ABORT_TRANSW</td>
<td style="text-align: left;">Aborts a transaction</td>
</tr>
<tr>
<td style="text-align: left;">$BRKTHRU</td>
<td style="text-align: left;">$BRKTHRUW</td>
<td style="text-align: left;">Sends a message to terminals</td>
</tr>
<tr>
<td style="text-align: left;">$DNS</td>
<td style="text-align: left;">$DNSW</td>
<td style="text-align: left;">Distributed Name Service interface</td>
</tr>
<tr>
<td style="text-align: left;">$END_TRANS</td>
<td style="text-align: left;">$END_TRANSW</td>
<td style="text-align: left;">Ends a transaction</td>
</tr>
<tr>
<td style="text-align: left;">$ENQ</td>
<td style="text-align: left;">$ENQW</td>
<td style="text-align: left;">Queues a new lock or lock conversion</td>
</tr>
<tr>
<td style="text-align: left;">$GETDVI</td>
<td style="text-align: left;">$GETDVIW</td>
<td style="text-align: left;">Get device information</td>
</tr>
<tr>
<td style="text-align: left;">$GETJPI</td>
<td style="text-align: left;">$GETJPIW</td>
<td style="text-align: left;">Get job/process information</td>
</tr>
<tr>
<td style="text-align: left;">$GETLKI</td>
<td style="text-align: left;">$GETLKIW</td>
<td style="text-align: left;">Get lock information</td>
</tr>
<tr>
<td style="text-align: left;">$GETQUI</td>
<td style="text-align: left;">$GETQUIW</td>
<td style="text-align: left;">Get queue information</td>
</tr>
<tr>
<td style="text-align: left;">$GETSYI</td>
<td style="text-align: left;">$GETSYIW</td>
<td style="text-align: left;">Get system information</td>
</tr>
<tr>
<td style="text-align: left;">$QIO</td>
<td style="text-align: left;">$QIOW</td>
<td style="text-align: left;">Queues an I/O request to a device</td>
</tr>
<tr>
<td style="text-align: left;">$SNDJBC</td>
<td style="text-align: left;">$SNDJBCW</td>
<td style="text-align: left;">Sends message to job controller</td>
</tr>
<tr>
<td style="text-align: left;">$START_TRANS</td>
<td style="text-align: left;">$START_TRANSW</td>
<td style="text-align: left;">Starts a transaction</td>
</tr>
<tr>
<td style="text-align: left;">$UPDSEC</td>
<td style="text-align: left;">$UPDSECW</td>
<td style="text-align: left;">Updates section file on disk</td>
</tr>
</tbody>
</table>

The Asynchronous System Trap (AST) is a routine in your program that is called whenever the system service completes. The AST routine may set a flag in your program, or it could call other routines that must be called after the system service has completed. The choice between using event flags and ASTs depends wholly on your application. Direct AST usage with system services is fairly rare for most applications.

So when would you want to use an asynchronous service? One example is when calling $GETJPI to get information about a process. My LOGIN program (described in a *VAX Professional* article in April 1989) calls $GETJPI to retrieve the mode of the process and the terminal name. Because there are other things the program can do before that information is needed, I called the asynchronous routine and proceeded to define logicals and symbols. When I was ready to use the terminal name and the mode, I simply called the $WAITFR system service to wait for the proper event flag, then continued on with the information returned by $GETJPI.

Proper use of the asynchronous system services can greatly increase program speed, because the program doesn’t necessarily spend much time waiting for events to complete.

### THE CHARACTER INSTRUCTIONS

The VAX architecture features rich support for character string manipulations. There are instructions to move characters, compare characters, locate characters, skip characters, and translate characters. These powerful instructions make it very easy to work with strings in assembly language. Unfortunately, the price paid for the instructions can be significant in code that is to be optimized for speed because the micro-code for the instructions perform several complex tasks.

Unlike most instructions, the character instructions actually use registers as work registers while working with the data. Depending on the instruction, registers R0–R5 may be used for temporary values. However, the values left in the work registers at the end of the instruction’s execution can be quite useful. These values will be discussed in more detail below.

The character instructions also set the condition codes depending on the last operation performed. Again, these will be discussed in some detail below.

While the character instructions were designed to work with character strings, they can be used for any sequence of bytes. For example, the MOVCx (MOVe Character) instructions are the preferred way to copy large blocks of data.

### Moving Characters

There are two instructions used to copy character strings: MOVC3 and MOVC5 (MOVe Character). The number following MOVC indicates the number of operands that each instruction requires. Both registers use R0–R5 as work registers, so care must be taken to either avoid using those registers or to save and restore their contents before and after the instruction. The length operands for the instructions are words, so programs using MOVCx can copy as many as 65,535 bytes with one instruction.

MOVC3 accepts a length, a source address, and a destination address; it is used to copy a certain number of bytes from one buffer to another. For example, the following instruction copies 100 bytes from the buffer pointed to by DATA1 to DATA2:

            MOVC3   #100,DATA1,DATA2                ; Copy 100 bytes

After the instruction executes, R0, R2, R4, and R5 all contain 0; R1 contains the address of one byte past the source string (DATA1+100, in this example), and R3 contains the address of the byte beyond the destination string (DATA2+100). The Z condition code is always set to 1 and the N, V, and C bits are always cleared (set to 0).

MOVC5 accepts a source length, a source address, a fill byte, a destination length, and a destination address; it is frequently used to copy a string of bytes into between buffers of different lengths. If the destination length is larger than the source length, the fill byte is copied into the destination bytes beyond the source length. For example, the following instruction copies 100 bytes from DATA1 into the 512-byte buffer DATA2; the remaining 412 bytes of DATA2 are filled with zeros:

            MOVC5   #100,DATA1,#0,#512,DATA2        ; Copy and fill to DATA2

If you are working with strings, you can use ASCII literals for the fill byte to pad a string with blanks, for example:

            MOVC5   #20,NAME,#^A" ",#32,OUTPUT

Twenty bytes are copied from NAME to OUTPUT, and the remaining 12 bytes of output are filled in with an ASCII blank (#A^” “, which is 32 decimal).

If the destination buffer is smaller than the source buffer, the high-end bytes of the source buffer are not copied. For example, the following instruction would only copy 20 bytes from NAME to OUTPUT—the last 12-bytes of NAME and the fill byte will be ignored:

            MOVC5   #32,NAME,#^A" ",#20,OUTPUT

After the MOVC5 executes, R2, R4, and R5 all contain 0. R0 contains a 0 if all the source bytes were moved, or the number of remaining source bytes not copied if the source string is larger than the destination. Like MOVC3, register R1 points to one byte beyond the last byte of the source string that was moved and R3 points one byte beyond the last byte of the destination. After the example above is executed, R0 would contain 12, R1 would point to NAME+20, and R3 would point to OUTPUT+20. The V condition code is always cleared; the others are set according to the difference between the source and destination lengths. Using the branch instruction notations, N is set if srclen LSS destlen, Z is set if they are equal, and C is set if srclen LSSU destlen.

The operation of the MOVCx instructions is such that the buffers can overlap without affecting the result. For example, the following instruction will essentially shift the bytes in DATA1 right by one byte:

            MOVC3   #100,DATA1,DATA1+1              ; Move all bytes right one byte

As mentioned above, MOVC3 is the preferred method for copying one block of memory to another. MOVC5 is the preferred method for fill a block of memory with a particular byte. For example, the following instruction will effectively zero out a buffer:

            MOVC5   #0,#0,#0,#512,BUFFER            ; Zero out 512-byte buffer

The use of \#0 for the source length tells MOVC5 that it isn’t to move any bytes from the source address, so the source address \#0 (which is an invalid address for most other instructions) is acceptable here because it is never used by MOVC5. (If a nonzero source length had been specified, an access violation would have resulted because address 0 is an invalid data address.)

While it is sometimes frustrating that R0–R5 are used as scratch registers, the values left in R1 and R3 can be quite useful when copying multiple strings to a buffer. For example, suppose you want to copy several ASCIC strings to an output buffer (recall that an ASCIC string is a counted ASCII string, whose first byte specifies the length of the string). The most efficient way to perform the copy is to remember that R3 always holds the address of the byte beyond the last destination byte after MOVC3. By loading the output buffer address in R3, you can copy multiple strings to the destination without ever having to reinitialize the pointer:

    STR1:           .ASCIC  /Hunter/
    STR2:           .ASCIC  /Goatley/
    OUTBUF:         .BLKB   32
    ....
            MOVAB   OUTBUF,R3               ; Move OUTBUF address to R3
            MOVZBL  STR1,R0                 ; Get length of STR1 (it's a word)
            MOVC3   R0,STR1+1,(R3)          ; Copy STR1 to OUTBUF (leaving addr
                                            ; ... of next byte in R3!!!)
            MOVB    #^A" ",(R3)+            ; Now copy a space in after it and
                                            ; ... bump R3 to point to next byte
            MOVZBL  STR2,R0                 ; Now get length of STR2
            MOVC3   R0,STR2+1,(R3)          ; And copy it in after space
            MOVAB   OUTBUF,R0               ; Get length of OUTBUF again
            SUBL2   R0,R3                   ; Now R3 holds the length of OUTBUF!

After the execution of the first MOVC3, R3 points to OUTBUF+6. The blank is copied using MOVB with auto-increment mode, leaving R3 pointing to OUTBUF+7. The second MOVC3 leaves R3 pointing to OUTBUF+14. By subtracting the starting address from the last value in R3, we can easily calculate the length of the data stored at OUTBUF (14 in this case). It should be obvious that this is much faster than using multiple registers and ADDx instructions to keep track of the destination addresses and lengths.

While the example above is a bit contrived, the method that it demonstrates is actually quite useful, especially when dealing with string descriptors and output buffers. Whenever I use MOVCx in this fashion, I usually add a comment explaining that R3 is used by MOVCx so that it doesn’t confuse someone who doesn’t understand exactly what the MOVCx instructions do.

If you need to save and restore the work registers, the easiest way is to use PUSHR and POPR to push and pop the selected registers; for example:

            PUSHR   #^M<R0,R1,R2,R3,R4,R5>          ; Save registers from MOVC3
            MOVC3   #100,DATA1,DATA2                ; Copy data
            POPR    $^M<R0,R1,R2,R3,R4,R5>          ; Restore all registers

However, remember that PUSHR and POPR are *very* costly instructions. It would be much more efficient to individually PUSHL and POPL the necessary registers (you can also use the PUSHR and POPR macros that were presented in the fourth part of this series, [“MACRO Made Easy, Part IV: Calling All Code,”](https://hunter.goatley.com/macro-made-easy/part-iv-calling-all-code/) February 1992).

Also, I mentioned earlier that MOVC3 and MOVC5 are time-consuming instructions. For short strings like STR1 and STR2 in the example above, a loop copying the strings a byte at a time will be significantly faster. If the data to be copied consists of a static number of bytes, words, longwords, or quadwords, multiple MOVx instructions would also be faster. For example, to copy the following 14-byte string:

STR1: .ASCII /Hunter Goatley/

either of the following pieces of code could be used:

            MOVAB   OUTBUF,R1                       ; Point to OUTBUF
            MOVQ    STR1,(R1)+                      ; Copy string to OUTBUF
            MOVL    STR1+8,(R1)+                    ; ...
            MOVW    STR1+12,(R1)+                   ; ...

or

            MOVAB   OUTBUF,R1                       ; Point to OUTBUF
            MOVAB   STR1,R0                         ; Point to source
            MOVQ    (R0)+,(R1)+                     ; Move 8 bytes
            MOVL    (R0)+,(R1)+                     ; Move 4 bytes
            MOVW    (R0)+,(R1)+                     ; Move 2 bytes

I use the following rules of thumb when trying to decide whether or not to use MOVCx:

- Is the string less than about 20 characters? If so, I usually use multiple MOVx instructions to move it.
- Do I know the length of the string at assembly-time? If not, I always use MOVCx, just because it’s a lot simpler than trying to set up loops to handle the lengths at run-time.
- Will I need to pad the destination buffer? If so, I usually use MOVC5, unless I know at assembly-time that the strings are short.
- Are the contents of R0–R5 important? If so, I’ll sometimes not use MOVCx just so I don’t have to save and restore them.
- Am I feeling lazy and don’t care about efficiency? If so, I almost always use MOVCx.

### Comparing Characters

Like MOVCx, the VAX architecture includes two flavors of string comparison instructions: CMPC3 (CoMPare Character) and CMPC5. Like the MOVCx instructions, the number indicates the number of operands for each. The operands themselves are identical to the MOVCx instructions. Also, up to 65,535 bytes can be compared with a single instruction. However, the CMPCx instructions use only registers R0–R3 as work registers; R4 and R5 are not used.

The CMPCx instructions compare two strings, stopping when an inequality has been found or all the bytes have been examined. The condition codes are set according the results of the last bytes compared. Again using the branch notation, the N-bit is set if the first byte is LSS the second byte, the Z-bit is set if they are equal, and the C-bit is set if the first byte is LSSU the second byte. The setting of the condition codes allows you to follow a CMPCx instruction with a branch that checks the codes (for example, BEQL, BLSS, BGTR, etc.).

The CMPCx instructions work as expected with ASCII text because the ASCII codes for letters and numbers are arranged in numerical order. For example, the ASCII code for ‘a’ is 97 (decimal) and the code for ‘b’ is 98. A comparison between the strings “apple” and “ball” would determine that “apple” is “less than” “ball” because the code for ‘a’ is less than the code for ‘b’. Similarly, the string “bare” is less than “bear” because ‘a’ is less than ‘e’. Thinking in these terms should make it easier to determine the logical flow of a program based on the comparisons.

CMPC3, like MOVC3, accepts as operands a length, a source address, and a destination address:

            CMPC3   #100,DATA1,DATA2                ; Compare 100 bytes
            BNEQU   10$                             ; Branch if not equal

After the instruction executes, R0 and R2 both contain the number of bytes remaining in the source string, including the byte that stopped the comparison; if the strings are equal, both registers will contain 0. If the strings are equal, R1 and R3 will point one byte beyond the source and destination strings, respectively. Otherwise, R1 and R3 contain the addresses of the bytes in the source and destination, respectively, that terminated the comparison.

Like MOVC5, CMPC5 accepts a source length, a source address, a fill byte, a destination length, and a destination address. With CMPC5, the fill byte is used to logically extend the shorter string (either the source or the destination) for comparison, which again continues until an inequality is detected or all bytes have been compared. For example, in the following segment, CMPC5 will pad STR1 with blanks and find that STR1 and STR2 are equal:

    STR1:   .ASCII  /Hunter Goatley/                ; String
    STR1_L = .-STR1
    STR2:   .ASCII  /Hunter Goatley              /  ; Same thing with blanks
    STR2_L = .-STR2
    .....
            CMPC5   #STR1_L,STR1,#^A/ /,#STR2_L,STR2
            BEQLU   10$                             ; Branch if equal
    .....

Determining the contents of R0–R3 after CMPC5 is a little more complicated than with CMPC3. R0 contains the number of bytes remaining in the source string (include the unequal byte); it contains 0 only if the strings are of equal length and are equal, or all bytes of the source were compared before the comparison terminated. In the same manner, R2 will contain the number of bytes remaining in the *destination* string, or 0 if the strings are equal and of equal length or all of the bytes in the destination string were compared before termination. R1 and R3 will point to either the bytes that terminated the comparison (in the source and destination strings, respectively) or one-byte beyond the strings if either or both are exhausted.

If both strings have a length of 0, the strings are treated as equal strings (the Z condition code is set and N, V, and C are cleared).

In the following segment, let’s assume that you have two usernames you wish to arrange in alphabetical order. The following data and code segment shows how you might set up the test:

    USER1:          .ASCII  /GOATHUNTER/
    USER2:          .ASCII  /GOATBUSTER/
    USER_L = .-USER1
    ....
            CMPC3   #USER_L,USER1,USER2             ; Compare the usernames
            BLSSU   LESS_THAN                       ; Branch if USER1 < USER2
            BGTRU   GREATER_THAN                    ; Branch if USER1 > USER2
            ; Here they're equal

In this example, the branch that would be taken is GREATER_THAN, since the ‘H’ in “GOATHUNTER” is greater than the ‘B’ in “GOATBUSTER”.

### Locating and Skipping Characters

The LOCC (LOCate Character) and SKPC (SKiP Character) instructions are used to find or skip a particular character in a string. Both instructions take the same operands: the byte to locate or skip, the length of the string, and the address of the string. Both instructions use R0 and R1 as work registers.

LOCC compares the specified character with the bytes in the string, stopping when a matching character is found or the string is exhausted. SKPC also compares each byte of the string with the given byte, stopping when an *unequal*byte is found or the string is exhausted. If a match is found, the Z-bit is cleared, R0 contains the number of characters remaining in string (including the located or unequal byte), and R1 contains the address of the byte that terminated the search. If a match or unequal byte is not found, the Z-bit is set, R0 contains 0, and R1 points one byte beyond the string.

Notice that the setting of the Z condition code seems to be backwards from the expected value. For example, to take a branch after LOCC if the character is not found, a BEQLU instruction should be used:

            LOCC    #^A/ /,#100,DATA        ; Find the first blank
            BEQLU   10$                     ; Branch if it is *not* found!
                                            ; Drop through if it is found....

The following example shows one way to parse two words in a buffer with an arbitrary number of blanks appearing anywhere in the string. At the end of its execution, R2 points to the first word, R3 contains the length of the first word, R4 points to the second word, and R5 contains the length of the second word:

    STRING:         .ASCII  /     First     Second    /
    STRING_LEN = . - STRING

BLANK = ^A/ / …. MOVAB STRING,R1 ; R1 -\> STRING MOVL \#STRING_LEN,R0 ; R0 = length of STRING SKPC \#BLANK,R0,(R1) ; Skip any blanks at beginning MOVL R1,R2 ; Save beginning addr of first word LOCC \#BLANK,R0,(R1) ; Find first blank BEQLU BIG_ERROR ; Branch if not found SUBL3 R2,R1,R3 ; R3 has length of first word! SKPC \#BLANK,R0,(R1) ; Skip over any blanks in the middle MOVL R1,R4 ; Save beginning address of second word LOCC \#BLANK,R0,(R1) ; Find blank at end or end of string SUBL3 R4,R1,R5 ; R5 has length of second word! ….

The only assumption this code makes is that there are two words separated by at least one blank in STRING. Notice that careful use of R0 and R1 kept the code compact and efficient.

### Locating a Substring

The MATCHC (MATCH Characters) instruction locates a substring in a character string. This powerful instruction provides MACRO programmers with the same functionality as the INDEX() function in high-level languages. MATCHC accepts four operands: the length of the substring to find, the address of the substring, the length of the source string, and the address of the source string.

If the substring is found, the Z-bit is set; otherwise, it is cleared. Registers R0–R3 are used as work registers. If a match is found, at the end of execution, R0 contains 0, R1 points one byte beyond the substring, R2 contains the number of bytes remaining in the source string after the match, and R3 points one byte beyond the matched substring in the source. If no match is made, R0 contains the length of the substring, R1 contains the address of the substring, R2 contains 0, and R3 points one byte beyond the source string.

    SUB:            .ASCII  /danger/
    SUB_LEN = .-SUB
    STRING:         .ASCII  /Asps!  Very dangerous; you go first!/
    STRING_LEN = .-STRING
    ....
            MATCHC  #SUB_LEN,SUB,#STRING_LEN,STRING         ; Find "danger"
            BNEQU   NOT_FOUND                               ; Branch if not found
            ; R3 points to "ous; you...."

### NEXT TIME….

The instructions covered above are by far the most commonly used character instructions. The support for manipulating character strings at the instruction-level is just one of the things that makes the VAX assembly language so pleasant to use when programming. Next issue, we’ll conclude our examination of the character instructions. We’ll also work through a step-by-step example of writing a complex macro that can help with character manipulations.

------------------------------------------------------------------------

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

------------------------------------------------------------------------

**Addendum \#1**

Here’s a short MACRO program that demonstrates the use of several character instructions to locate a substring and find the beginnings and lengths of two words in a string.

    SUB:       .ASCII  /Sec/
    SUB_LEN = .-SUB
    STRING:     .ASCII  /First Second/
    STRING_LEN = . - STRING

    BLANK = ^A/ /
        .ENTRY  TEST,^M<>
        MATCHC  #SUB_LEN,SUB,#STRING_LEN,STRING
        MOVAB   STRING,R1       ; R1 -> STRING
        MOVL    #STRING_LEN,R0      ; R0 = length of STRING
        SKPC    #BLANK,R0,(R1)      ; Skip any blanks at beginning
        MOVL    R1,R2           ; Save beginning addr of first word
        LOCC    #BLANK,R0,(R1)      ; Find first blank
        BEQLU   BIG_ERROR       ; Branch if not found
        SUBL3   R2,R1,R3        ; R3 has length of first word!
        SKPC    #BLANK,R0,(R1)      ; Skip over any blanks in the middle
        MOVL    R1,R4           ; Save beginning address of second word
        LOCC    #BLANK,R0,(R1)      ; Find blank at end or end of string
        SUBL3   R4,R1,R5        ; R5 has length of second word!

    BIG_ERROR:
        RET
        .END    TEST

 

