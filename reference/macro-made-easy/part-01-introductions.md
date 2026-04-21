
# MACRO Made Easy – Part 1: The Introductions

## MACRO Made Easy

## Part I: The Introductions

#### by

### Hunter Goatley

### Western Kentucky University

------------------------------------------------------------------------

Over the past few years, I’m sure you’ve noticed that I like to write programs in MACRO-32, the VAX assembly language. During that time, a number of you have told me that you wish you knew MACRO better (or knew it, period). Well, pull your pants legs up—’cause here’s your chance to get down and dirty with MACRO-32, the language your mother never warned you about.

Before we get started, I want to point out that I’m assuming that you already know the differences between binary, decimal, and hexadecimal, and that you have probably had some exposure to some assembly language at some point. I’m going to try to maintain a balance that will let assembler-illiterates and MACRO-illiterates both benefit from this series, but I’m sure I’ll tend to leave out a lot of the nitty-gritty details about assembly languages in general.

As you try to learn MACRO, you should have a copy of the MACRO manual, which is part of the VMS extended documentation set (the “gray wall”). The full title is *VAX MACRO and Instruction Set Reference Manual*. In addition to the manual, the on-line help under MACRO has been expanded in recent versions of VMS to include much of the documentation for the assembly directives and instructions. Also, if you can find one, the 1981 *VAX Architecture* handbook is an invaluable programming aid (and it’s smaller than the manual).

MACRO-11 was the assembly language for the PDP-11 series of computers. When the VAX systems were designed, DEC apparently used MACRO-11 as its starting point for MACRO-32, because MACRO-32 is, fundamentally, a superset of MACRO-11; the basic instruction sets are very similar.

MACRO-32, from this point referred to as MACRO, consists of more than 350 instructions. These instructions are represented by mnemonics, which describe the function of the instruction. For example, the RET instruction is, in hex, 04. Instead of forcing programmers to write 04 every time they want to return from a subroutine, the programmer uses RET and the assembler translates this to 04.

Of the large number of instructions, many of them are variations on a single instruction. For example, the MOVQ, MOVL, MOVW, and MOVB instructions all copy data from one location to another; the number of bytes copied is specified by the last letter of each mnemonic: Q for quadword (8 bytes), L for longword (4 bytes), W for word (2 bytes), and B for byte.

The VAX is a 32-bit machine, so the size of all data addresses is 32 bits, or 4 bytes (a longword). Though a VAX can address any byte, it is more efficient to fetch instructions and data that begin on longword boundaries.

Like most assembly languages, MACRO statements consist of an optional label, a mnemonic representing a binary op-code, any operands, and an optional comment. Briefly, these are the separators required for each field:

1.  **Label**: optional, terminates in a colon. For example, LABEL:
2.  **Mnemonic opcode**: separated from any operands by whitespace
3.  **Operands**: only if instruction has operands. Multiple operands are separated by commas
4.  **Comment**: optional, begins with a semi-colon. For example, ;Comment

By convention, tabs are usually used to separate the various fields. For example, if a line has no label, the opcode starts in column 9 (the first tab position):

    LABEL:  MOVL    R0,R1                   ; Copy status to R1
            MOVL    R0,R2                   ; Copy it to R2, too

The listing file that MACRO can produce contains 132-column text; it is recommended that MACRO statements not exceed 80 characters, so the lines in the listing file do not exceed 132 characters.

Labels and comments may appear on lines by themselves, but opcodes and operands can only be separated using the ‘-‘ continuation character. For example, the first line above could have been coded:

    ; This is an ugly way to format an instruction
    LABEL:
            MOVL    -                       ; Copy status to R1
                    R0,-                    ; ...
                    R1                      ; ...

Obviously, you’d only want to use the continuation character in places where the statement’s readability suffers. For example, the following instruction benefits tremendously from the continuation characters:

            BISL2   #<-                     ; Set WRAP, MECHTAB, and
                    TT$M_WRAP!-             ; ... SCOPE bits in mask
                    TT$M_MECHTAB!-          ; ...
                    TT$M_SCOPE>,-           ; ...
                    TTCHARS+4               ; ...

When statements are continued on multiple lines, the continuation character ‘-‘ must be the last non-whitespace character preceding the comment field. While it is possible to split symbolic names across lines, it’s better to break a line only after a “natural break,” for example, after a symbolic name or between operands.

### LABELS

A label identifies a location in a program; when a label is defined, the value of the label is the address of the statement following the label. MACRO labels may be 1 to 31 characters long, and can consist of the letters A–Z, the numbers 0–9, the dollar sign ($), the underscore (_), and a period (.). Normal labels must begin with an alphabetic character.

There are two kinds of labels in MACRO statements: global and local. Global labels can be referenced from anywhere in a program or module; in fact, a label can be made visible to an external module by specifying two colons after the label name:

    GLOBAL_LABEL::
            MOVL    R0,R1                   ; Copy the status to R1

The term global is somewhat misleading, since it refers to both a symbol global to one module and a symbol known to external modules. In the discussion below, “global” refers to a symbol known to the module in which it is defined.

Local labels, on the other hand, are defined only for a particular block of code or data. Specifically, they can be only be used between two global labels, or within a defined local block (described below). Local labels are composed of numeric strings followed by a dollar sign and a colon:

    10$:    MOVL    R0,R1                   ; The label 10$ is a local label

Programmers may use any numbers in labels up to “35299$”; the MACRO assembler generates higher-numbered local labels when expanding macros that generate their own local labels (all of which will be explained in due time).

Any reference to a local label outside the local block results in an error. For example, the following code will generate an error when it is assembled:

    LOOP:   MOVL    (R6)+,R0
            DECL    (R6)
            BEQL    10$
            SOBGTR  R1,LOOP
    10$:    BRB     20$
    LOOP2:  MOVL    (R5)+,R0
    20$:    ADDL2   R1,R0
            SOBGTR  R0,LOOP2

The instruction “BEQL 10$” is valid because 10$ appears in the local block between labels “LOOP” and “LOOP2.” The instruction “BRB 20$” will generate an “undefined label” error because “20$” is not defined in the same local block as the “BRB” instruction.

### OPCODES, ETC.

The opcode field can actually consist of one of three items: a mnemonic opcode, such as MOVL or RET; a macro name; or an assembler directive.

An assembler directive is a statement that gives some instruction to the MACRO assembler. There are directives to control the printing of the listing file (.PAGE, .SUBTITLE), to declare external and global variables (.EXTERNAL, .GLOBAL), to reserve and declare space for data (.BLKL, .LONG), and to specify assembly- and linkage-time libraries (.LIBRARY, .LINK). There are also directives to define macros (.MACRO, .ENDM) and control the expansion of macros (.IF). Many of these directives will be covered in future articles; they are all documented in the MACRO manual.

As you probably noticed, the assembler directives all begin with a period. This helps distinguish them from the mnemonic opcodes and user macros (though macros can be named with a period to make them look like directives). Like the mnemonic opcodes, most of the directives take one or more operands.

### OPERANDS

The operands for an opcode or directive are separated from the previous field by whitespace (usually a tab). Multiple operands are separated by commas and, as has been shown above, can be continued on multiple lines to ease readability of the code.

The order of the operands in MACRO differs from the order in some other assembly languages, most notably IBM 370 assembly and 8088 assembly. In MACRO, the operands are in a natural source-to-destination, left-to-right order. For example, the following instruction moves a literal value to a register:

            MOVL    #1,R0                           ; Place a 1 in R0

The operands are evaluated left-to-right, just as you’d read them. The source, \#1, is copied to the destination, R0.

### COMMENTS

It is very good programming practice to liberally comment your MACRO code. I comment every line of MACRO, with block comments to explain what’s about to happen or provide any additional notes that might be useful in deciphering the code later.

As described above, a MACRO comment is preceded by a semi-colon. A comment can appear anywhere on a line; all text after the semi-colon is treated as part of the comment. For example, the following code fragment shows the use of block and line comments.

    ;
    ;  Get the address of the input record buffer and clear the first 4 bytes
    ;  of the buffer.
    ;
            MOVAL   INBUFF,R0               ; R0 -> input buffer
            CLRL    (R0)                    ; Clear first longword

### A COUPLE OF OTHER THINGS

You probably already know that the VAX is a “little endian” when it comes to memory storage. That is, the bits in a byte are numbered from right to left instead of left to right, as with many other (“big endian”) systems. While seemingly awkward to many VAX newcomers, the little endian approach seems very natural to me. Graphically, a longword (4 bytes) would look like the following:

            +--------------------------------------------+
            |  |  |                                | | | |
            +--------------------------------------------+
             31 30          ......                  2 1 0

In VMS documentation, data structures are typically displayed as groups of longwords. For example, the following illustration shows a string descriptor, which is 8 bytes:

             31                                         0
            +--------------------------------------------+
            |Type (b) | Class (b) |    Length (word)     | +0
            +--------------------------------------------+
            |                  Pointer                   | +4
            +--------------------------------------------+

If the label DESCRIPTOR points to the beginning of the structure, the length field would be addressed as DESCRIPTOR, the class byte would be addressed as DESCRIPTOR+2, the type byte would be addressed as DESCRIPTOR+3, and the pointer would be addressed as DESCRIPTOR+4.

If this is confusing now, bear with me. I plan to explain more as we go along.

### ASSEMBLING A PROGRAM

MACRO programs are assembled using the DCL command MACRO. Like all compilers, the MACRO assembler generates an object file (.OBJ). A listing file can be generated by specifying /LIST on the MACRO command:

            $ MACRO/LIST REVERSE

Many of the qualifiers that control the format of listing file can also be specified in the MACRO program using assembler directives. For example, the .SHOW directive corresponds to the /SHOW qualifier.

### A DISSECTION OF A PROGRAM

I think the easiest way to gain an understanding of MACRO is to examine a sample program in detail. Program 1 is REVERSE.MAR, a simple program that covers a lot of valuable MACRO topics. Functionally, all it does is read a string from SYS$INPUT, reverse the order of the characters of the string, and write it back out to SYS$OUTPUT.

One of the first things most beginning MACRO programmers want to do is write a program that does terminal I/O. Unlike high-level languages, MACRO doesn’t have any built-in mechanism for doing I/O (under RT-11 on the PDPs, there were assembler directives that performed character I/O, but VAX MACRO doesn’t have that feature). Instead, the programmer must make use of system services, in one form or another. In future articles, we’ll look at doing I/O using the $QIO system service and RMS; this time, we’ll look at two run-time library routines to do I/O using SYS$INPUT and SYS$OUTPUT. Though they don’t do anything but bare minimum input and output, they provide the easiest way to do I/O from MACRO.

            .TITLE  REVERSE - A program to demo simple I/O from MACRO
            .IDENT  /01-000/
    ;++
    ;
    ;  Facility:    REVERSE
    ;
    ;  Author:      Hunter Goatley
    ;
    ;  Date:        May 31, 1991
    ;
    ;  Functional Description:
    ;
    ;       Simple program to read a string from SYS$INPUT and print it in
    ;       reverse order to SYS$OUTPUT.
    ;
    ;  Modified by:
    ;
    ;       01-000          Hunter Goatley          31-MAY-1991 08:02
    ;               Original version.
    ;
    ;--
            .DSABL  GLOBAL                          ; Declare external references
            .ENABL  SUPPRESSION                     ; Don't list unreference symbols
            .NOSHOW BINARY                          ; Don't include binary listings
    ;
    ;  External routines:
    ;
            .EXTRN  LIB$GET_INPUT                   ; Read from SYS$INPUT
            .EXTRN  LIB$PUT_OUTPUT                  ; Print to SYS$OUTPUT
    ;
    ;  Declare symbols used here (the following macros are stored in the default
    ;  MACRO library SYS$LIBRARY:STARLET.MLB).
    ;
            $DSCDEF                                 ; Descriptor symbols
            $SSDEF                                  ; System service status symbols

            .SHOW   BINARY                          ; Include binary in listings

            .PAGE
            .SBTTL  Data storage
            .PSECT  _REVERSE_DATA,NOEXE,WRT,LONG

    PROMPT:         .ASCID  /Enter a string: /      ; Prompt for input
                    .ALIGN  LONG                    ; Align on longword boundary
    ;
    ;  Descriptor for input buffer
    ;
    INBUFF_L = 256                                  ; Length of the buffer
    INBUFF_D:       .WORD   INBUFF_L                ; Length of the buffer
                    .BYTE   DSC$K_DTYPE_T           ; Text string
                    .BYTE   DSC$K_CLASS_S           ; Static string
                    .ADDRESS INBUFF                 ; Address of the buffer

    INBUFF:         .BLKB   INBUFF_L                ; Reserve space for the buffer
    ;
    ;  Descriptor for the output buffer
    ;
    OUTBUFF_D:      .WORD   0                       ; Length filled in at run-time
                    .BYTE   DSC$K_DTYPE_T           ; Text string
                    .BYTE   DSC$K_CLASS_S           ; Static string
                    .ADDRESS .+4                    ; Address of the buffer
                    .BLKB   INBUFF_L                ; Reserve space for buffer

            .PAGE
            .SBTTL  The Program

            .PSECT  _REVERSE_CODE,EXE,NOWRT,LONG
            .ENTRY  REVERSE,^M<R2>
    ;
    ;  Call run-time library routine to read input from SYS$INPUT
    ;
            PUSHAW  INBUFF_D                        ; Address of word to receive
                                                    ; ... the length of the input
            PUSHAQ  PROMPT                          ; Address of the prompt
            PUSHAQ  INBUFF_D                        ; Address of the input buffer
                                                    ; ... descriptor
            CALLS   #3,G^LIB$GET_INPUT              ; Read input from SYS$INPUT
            BLBC    R0,100$                         ; Branch on an error
    ;
    ;  Now set up some registers to contain the values needed to copy the string
    ;  in reverse order from the input buffer to the output buffer.
    ;
    ;  First, make R2 point to the end of the input buffer
    ;
            MOVAB   INBUFF,R2                       ; R2 -> input buffer
            MOVZWL  INBUFF_D,R0                     ; R0 = length of the input
                                                    ; ... (converted to longword)
            ADDL2   R0,R2                           ; R2 -> byte past end of buffer
    ;
    ;  Since the output string will the the same length as the input string, go
    ;  ahead and copy the length of the string the output buffer descriptor.
    ;
            MOVW    R0,OUTBUFF_D                    ; Store length in descriptor
            MOVAB   @OUTBUFF_D+4,R1                 ; R1 -> output buffer
    ;
    ;  The following loop copies the input string to the output buffer a byte
    ;  at a time, moving backwards through the input buffer and forward through
    ;  the output buffer.
    ;
    ;  At this point, the following registers contain the following values:
    ;
    ;       R0      = Number of character to copy
    ;       R1      = Pointer to beginning of output buffer
    ;       R2      = Pointer to end of input buffer
    ;
     10$:   MOVB    -(R2),(R1)+                     ; Copy byte from input buffer
                                                    ; ... to the output buffer
            SOBGTR  R0,10$                          ; Loop until all copied

            PUSHAQ  OUTBUFF_D                       ; Print the output buffer
            CALLS   #1,G^LIB$PUT_OUTPUT             ; ... to SYS$OUTPUT

     100$:  RET                                     ; Return to caller

            .END    REVERSE

### THE SETUP

Starting at the top of REVERSE.MAR, we find the following lines:

            .TITLE  REVERSE - A program to demo simple I/O from MACRO
            .IDENT  /01-000/

Both of these lines are assembler directives used for the identification of the program, in both the listing file and the final executable image. The first word following .TITLE is used as the program’s name. This name is displayed at the top of each page in the listing file and is stored in the generated object module. In the case of a single-module program, the .TITLE string is stored in the image header and can be displayed using ANALYZE/IMAGE. The rest of the line (up to 40 characters) is also displayed in the listing file headers.

The .IDENT line accepts a delimited string of 1 to 31 characters, which is also used to identify the module. Like the .TITLE string, this string is displayed in the listing file and stored in the object module. Typically, the .IDENT string consists of some numeric representation of the module’s version, like 01-000 above.

If the object module is added to an object library, the .TITLE string is used to name the module; the .IDENT string is displayed with the LIBRARY/LIST/FULL command to identify the version of the module.

Next comes the comment block that introduces the program. I opted for the DEC convention of starting this block with “;++” and ending it with “;–“. This is, of course, completely optional, but it does delimit the header comment block in an obvious fashion.

The following three lines are more assembler directives:

            .DSABL  GLOBAL                          ;Declare external references
            .ENABL  SUPPRESSION                     ;Don't list unreferenced symbols
            .NOSHOW BINARY                          ;Don't include binary listings

The first one, .DSABL GLOBAL, forces the programmer to declare all external references. Normally, MACRO will assume that all unresolved variables are external; the final resolution of the variables is not done until the linker is executed. By using the .DSABL directive, you can trap a lot of typographical errors in your program at assembly-time—the assembler will complain that a symbol is undefined. (.DSABL is short for .DISABLE; either form can be used. You’ll notice that I usually use the short version because it fits within the normal tab stops.)

The .ENABL and .NOSHOW both control the amount of material included in the listing file, if one is generated. .ENABL SUPPRESSION tells the assembler not to list any symbols that were defined but not referenced. When you use the default definition macros, you can generate literally hundreds of symbols that are never used; this directive keeps them out of the listing file.

The .NOSHOW BINARY line is actually not needed here, because it is the default. .SHOW BINARY, found later in the program, tells the assembler to show the binary code generated by macro calls. This information can be useful when you are trying to find the exact instructions produced by an expanded macro. I used the .NOSHOW here because I don’t want any binary code generated for the $\*DEF macros to follow—by specifying it here, the showing is temporarily suspended even if the user specified /SHOW=BINARY on the MACRO command. .SHOW/.NOSHOW BINARY will be covered in more detail in a future article about writing macros.

Now that the assembler will force the declaration of all external symbols, we need to declare the two run-time library routines the program will use:

    ;
    ;  External routines:
    ;
            .EXTRN  LIB$GET_INPUT                   ; Read from SYS$INPUT
            .EXTRN  LIB$PUT_OUTPUT                  ; Print to SYS$OUTPUT

The full name of .EXTRN is .EXTERNAL. These lines just inform the assembler that the symbols are external references that will be resolved at link-time.

All of the DEC-defined symbols and constants are found in macro libraries in SYS$LIBRARY. (Macro libraries have a file extension of .MLB.) The STARLET library contains many of the average definitions used by user-mode programs. This library is automatically searched by the MACRO assembler to resolve any undefined macro references.

Typically, the macros used from STARLET are named $???DEF, where ??? corresponds to the first few characters of the symbol name. For example, the constant SS$_NORMAL represents a success status; it is defined by the macro $SSDEF, found in STARLET. With that in mind, the following two lines declare the symbols we need for REVERSE:

    ;
    ;  Declare symbols used here (the following macros are stored in the default
    ;  MACRO library SYS$LIBRARY:STARLET.MLB).
    ;
            $DSCDEF                                 ; Descriptor symbols
            $SSDEF                                  ; System service status symbols

$DSCDEF defines all the symbols used to build string descriptors, briefly mentioned earlier. (Actually, REVERSE doesn’t use any of the symbols defined in $SSDEF, but most programs will, so I usually include it.)

The next line re-enables the inclusion of binary output from macro expansions:

            .SHOW   BINARY                          ; Include binary in listings

### PROGRAM SECTIONS

Our program’s actual data storage begins with the following lines:

            .PAGE
            .SBTTL  Data storage
            .PSECT  _REVERSE_DATA,NOEXE,WRT,LONG

The .PAGE forces a page break in the listing file; .SBTTL (.SUBTITLE) provides a subtitle for the heading on each page in the listing.

Programs can be divided into different program sections, each of which can have different attributes. The assembler creates two program sections automatically: the unnamed section (named .BLANK.) and an absolute program section (named .ABS.). All symbols defined before a .PSECT directive, data, or an instruction, are automatically placed in the absolute program section.

Judicious use of program sections can increase program efficiency and readability. Program sections can be used to, among other things, write-protect data, allow multiple modules to share the same data, and specify the order in which the object modules are linked together. Like labels, the PSECT name can be 1 to 31 alphanumeric characters, plus the dollar sign, period, and underscore; the first character cannot be a number.

REVERSE.MAR only has two program sections: _REVERSE_DATA and _REVERSE_CODE. Frequently, I will divide my data section into two sections, one that’s write protected and one that’s not. Because the data area is so small in REVERSE, I didn’t make the division. The following list describes each of the attributes specified for the data area:

- NOEXE — section is not executable (not implemented yet in the assembler, but included in case it ever is)
- WRT — section is writeable (data can be written to the section)
- LONG — specifies that the section is longword-aligned (the starting address is on a longword boundary)

More information about program sections can be found in the MACRO manual, under the description of the .PSECT directive.

### THE DATA

Strings on the VAX are described by string descriptors. These descriptors are 8 bytes in length and specify the length of the string (2 bytes), the type of descriptor (one byte; DSC$K_DTYPE_T for text strings), the class of the descriptor (one byte; DSC$K_CLASS_S for static buffers), and a pointer to the actual string data (4 bytes). (Eight-byte structures are usually called quadwords in MACRO.) Strings are, generally, passed to and from run-time library routines by passing the address of the string descriptor.

There are directives for storing ASCII data in a number for formats in a MACRO program. One of these is .ASCID, which stores the string and also creates a static string descriptor for the string. REVERSE.MAR uses the .ASCID directive to create a descriptor for the prompt to write to SYS$OUTPUT:

    PROMPT:         .ASCID  /Enter a string: /      ; Prompt for input

This directive actually creates a quadword descriptor and the bytes containing the ASCII values of the string delimited by the slashes. The string is actually delimited by the first character and the next occurrence of that character:

                    .ASCID  "This is valid, too."

The ASCID string can be continued on multiple lines by using the continuation character to break the string into multiple pieces:

                    .ASCID  /This line has been /-
                            /broken up into 3/-
                            /pieces/

The other .ASCIx directives are .ASCII (stored literally, with no descriptor), .ASCIC (counted ascii string, whose first byte specifies the length of the string), and .ASCIZ (the string is terminated by a null byte, like strings in C).

The next line makes sure the following data is aligned on a longword boundary:

                    .ALIGN  LONG                    ; Align on longword boundary

Note that the alignment size specified in a .PSECT line determines the maximum boundary alignment that can be given to the .ALIGN directive—since LONG was specified, we can align to a longword boundary.

Next, we need to reserve storage for our input buffer and build a descriptor for it. Instead of using the .ASCID, we’ll use other directives to build the descriptor. First, I defined a symbol, INBUFF_L, to specify the length of the buffer:

    INBUFF_L = 256                                  ; Length of the buffer

By using a symbol, I can change the value in only one place, without worrying about identifying all the locations that might be affected by the change. Now, we’ll use assembler directives to store the values in the proper sizes to build a descriptor:

    INBUFF_D:       .WORD   INBUFF_L                ; Length of the buffer
                    .BYTE   DSC$K_DTYPE_T           ; Text string
                    .BYTE   DSC$K_CLASS_S           ; Static string
                    .ADDRESS INBUFF                 ; Address of the buffer

The .WORD and .BYTE directives allocate a word and byte, respectively, storing the specified value at that address. (Similarly, there are .LONG and .QUAD directives for storing longword and quadword values.) The two .BYTE lines could have been combined into one line, because you can specify multiple values, separated by commas. Doing so, though, would have hampered readability. The DSC$K_ symbols are defined in $DSCDEF, which we referenced earlier. The descriptor type, DSC$K_DTYPE_T, specifies that the descriptor is for a text string; the class, DSC$K_CLASS_S, specifies that the string is static, not dynamic. The use of static and dynamic strings will be covered in more detail in a future article.

The .ADDRESS directive stores the address of the specified symbol in a longword—in this case, the address of INBUFF is stored in the longword, completing the string descriptor.

Now that the descriptor has been created, we need to reserve the space for the buffer itself. Since we defined INBUFF_L to be 256, we need to reserve INBUFF_L bytes for storage:

    INBUFF:         .BLKB   INBUFF_L                ; Reserve space for the buffer

.BLKB reserves a certain number of bytes, but doesn’t initialize them. Once again, you can reserve words, longwords, and quadwords, using .BLKW, .BLKL, and .BLKQ, respectively. There are ten .BLKx directives in all.

The last piece of data we need is an output buffer and its descriptor. This descriptor is a little different from the first one:

    OUTBUFF_D:      .WORD   0                       ; Length filled in at run-time
                    .BYTE   DSC$K_DTYPE_T           ; Text string
                    .BYTE   DSC$K_CLASS_S           ; Static string
                    .ADDRESS .+4                    ; Address of the buffer
                    .BLKB   INBUFF_L                ; Reserve space for buffer

I didn’t specify a length for this one, because we won’t know the length of the output string until run-time, when the user has entered a string. Also, you’ll notice that I specified the buffer address differently. The MACRO assembler uses the period (.) to denote the current address during the assembly; specifying “.+4” says to take the current address and add 4 to it. Since we know the .ADDRESS stores a longword value, “.+4” refers the first byte after the .ADDRESS longword. This “trick” lets us not define another symbol that points to the output buffer. Normally, I don’t recommend using this method because it’s harder to see what it really does. However, many programs use it, and its use here will help demonstrate a technique for getting the address of the buffer itself.

### THE ENTRY POINT

The actual executable code for the program is started in REVERSE.MAR by defining a new program section, _REVERSE_CODE. Note that I specified NOWRT, making the section non-writeable:

            .PSECT  _REVERSE_CODE,EXE,NOWRT,LONG

It’s a good idea to make your code sections protected from writes to help debugging—should you accidentally try to write to the memory occupied by the program’s code, an access violation will be signalled. Note that if you were breaking all the rules by writing self-modifying code, you wouldn’t want to protect the section from write access.

The beginning of the program is heralded by the following .ENTRY statement:

            .ENTRY  REVERSE,^M<R2>

.ENTRY defines an entry point into the code. It takes two parameters: the label for the entry point, and a register bitmask. The label follows the normal label-naming conventions. The register bitmask specifies all the registers that should be saved automatically before the flow of execution enters this code.

The VAX has 16 general purpose registers, some of which are reserved: R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, AP, FP, SP, and PC. Each register holds a longword (4 bytes). The registers and their uses are described by the following list:

- R0–R5: generally available to the software for temporary storage of values. R0 and R1 are typically used to hold status values. Some instructions actually use these registers as scratch registers, notably the character instructions.
- R6–R11: available to the program for the storage of data.
- AP: points to the argument list.
- FP: points to the call frame.
- SP: stack pointer; contains the address of the stack, which is used for temporary data storage.
- PC: program counter; contains the address of the next instruction to execute.

As you’d probably expect, there is a lot that could be said about the registers. The AP, FP, and SP will be discussed in some detail in a future article.

Getting back to the entry mask, any of the registers R2 through R11 can be specified in the mask. The mask is actually stored as a word at the address equated with the label. The label is defined globally and is known to external modules. Multiple registers are separated by commas:

            .ENTRY  REVERSE,^M<r2,r3,r4,r5,r6,r7,r8,r9,r10,r11>
    </r2,r3,r4,r5,r6,r7,r8,r9,r10,r11>

When a program is executed, VMS calls it using a CALLS instruction. The CALLS instruction automatically saves the AP, FP, SP, and PC, and any registers specified in the word bitmask. Since R0 and R1 are used to pass status codes between routines, they cannot be specified in the list. Again, the CALLx instructions will be discussed in more detail in a future article.

### THE PROGRAM ITSELF

Remember that REVERSE.MAR reads a string from SYS$INPUT, reverses the order of the bytes, and prints it out to SYS$OUTPUT. The I/O is accomplished using the run-time library routines LIB$GET_INPUT and LIB$PUT_OUTPUT. These routines provide a very simple but useful interface to RMS (Record Management Services) to do simple I/O to a terminal. Both routines are documented in the *VMS RTL Library (LIB$) Manual*.

LIB$GET_INPUT accepts three parameters, only one of which is required. The parameters are the address of the string descriptor for the buffer to receive the input, an optional address of a string descriptor for a prompt to be printed, and an optional address of a word to receive the length of the input string. From a high-level language, the call might look something like:

            status = LIB$GET_INPUT (buffer, prompt, buffer);

In MACRO, such routines are called using the CALLS and CALLG instructions. For this example, only CALLS will be discussed. The ‘S’ refers to the stack; parameters are passed to a routine by pushing the values onto the stack, and then specifying the number of parameters as the first operand of the CALLS instruction:

            PUSHAW  INBUFF_D                        ; Address of word to receive
                                                    ; ... the length of the input
            PUSHAQ  PROMPT                          ; Address of the prompt
            PUSHAQ  INBUFF_D                        ; Address of the input buffer
                                                    ; ... descriptor
            CALLS   #3,G^LIB$GET_INPUT              ; Read input from SYS$INPUT

The PUSHAx instructions push an address on the stack. PUSHAW pushes the address of a word and PUSHAQ pushes the address of a quadword (again, there are also PUSHAB, PUSHAL, etc.). In the example above, any of these instructions could have been used, because they all push an address on the stack. The type specified by the final letter only performs a function when auto-increment and auto-decrement modes are used in an instruction (discussed some below). However, I decided to let the instructions help describe the data that is actually passed to the routine.

Because the stack is used in a last-in, first-out (LIFO) method, the first address passed must be the last specified parameter. Hence, the address of the word to receive the length of the input string is actually specified first, followed by the address of the prompt’s descriptor, and finally by the address of the descriptor for the actual input buffer.

The CALLS instruction takes two parameters: the number of parameters pushed on the stack, and the address of the entry mask of the routine to which control should be transferred. The operand “#3” is treated by the assembler as a literal value; a 3 is stored as the operand. The addresses of the run-time library routines are always specified using the general addressing mode (G^). This mode causes the linker to convert the address to a relative offset if the routine is relocatable (can be located anywhere in memory) and an absolute address if the routine is not relocatable. All this starts getting deep, so, for now, let’s just remember to always use “G^” when calling a run-time library routine.

The next instruction is used to check for any error that may have been returned by LIB$GET_INPUT. The VAX calling standard defines all success status values as odd numbers, while all error status values are even numbers. This design allows you to check for errors simply be checking the low bit of the value. If it is set, the value is an odd number, which is a successful status; if the low bit is clear, the value is even, which indicates an error occurred.

            BLBC    R0,100$                         ; Branch on an error

BLBC stand for “Branch Low Bit Clear”; routines that follow the VAX calling standard return status values in R0, so this instruction checks the low bit of R0. If the bit is clear, an error occurred, so control branches to the instruction at the address associated with the local label 100$. BLBC has a counterpart, BLBS, which takes the branch if the low bit is set.

At this point in the program’s execution, the user at the terminal has been prompted to enter a string, and that string has been copied to the buffer described by the INBUFF_D descriptor. We’re now ready to copy the string to the output buffer in reverse order. This will be accomplished by loading the proper addresses into registers and using auto-increment and auto-decrement modes to copy the bytes.

To copy the bytes in reverse order, we need to start copying from the end of the input string. The following instructions load the address of the end of the string into R2:

            MOVAB   INBUFF,R2                       ; R2 -> input buffer
            MOVZWL  INBUFF_D,R0                     ; R0 = length of the input
                                                    ; ... (converted to longword)
            ADDL2   R0,R2                           ; R2 -> byte past end of buffer

The MOVAB moves the address of the byte at the label INBUFF into R2. The MOVAx instructions work just like the PUSHAx instructions, except that you can specify the destination for the address. In fact, the PUSHAB instruction can be emulated using the following MOVAL instruction:

            MOVAL   PROMPT,-(SP)                    ; Push the address on the stack

“(SP)” means to use the value stored in SP as an address (in this case, the address of the top of the stack). The operand “-(SP)” specifies auto-decrement mode, using the stack pointer. What this means is that the value of the stack pointer is automatically decremented by a certain amount before the resulting address is used. The amount by which the stack pointer is decremented is determined by the last letter of the MOVAx instruction. In this example, MOVAL was used to move a longword (the address is a longword), so the stack pointer is decremented by 4 before the address is copied to the stack. Had MOVAB been used, the address in SP would have been decremented by only one byte; when the address was copied, it would have written over 3 bytes of some data already on the stack.

Getting back to RESERVE.MAR, the MOVAB instruction loads the address of the input buffer, equated with the label INBUFF, into R2. The next instruction loads the first word of the string descriptor INBUFF_D into R0. The instruction MOVZWL is a variation of the MOVx instructions mentioned at the beginning of this article. It stands for “MOVe Zero-extended Word to Longword,” which means the word is copied into bits 0–15 of R0 and the value is zero-extended—bits 16–31 are cleared. Since our goal is to make R2 point to the end of the input string, we need to perform some address arithmetic; by using MOVZWL instead of MOVW, we’ve ensured that the high-word of the previous contents of R0 don’t get added to the high-word of R2.

The address arithmetic is accomplished using the ADDL2 instruction. As we mentioned earlier, the order of MACRO operands is left-to-right source-to-destination. With that in mind, the instruction

            ADDL2   R0,R2                           ; R2 -> byte past end of buffer

adds the value in R0 to that in R2, leaving the sum in R2. At this point, R2 contains the address of the byte just past the end of the input string:

    INBUFF:         Some sample input string.
                                             ^
                                             R2 points here

Moving on, we still have the length of the input string in R0. Since we’re just reversing the bytes, we know that the length of the string to be written to SYS$OUTPUT is equal to the length of the input string, so let’s just copy the word length to our output buffer’s descriptor:

            MOVW    R0,OUTBUFF_D                    ; Store length in descriptor

Now we need to get the address of our output buffer in a register. Remember that the output descriptor was set up using “.+4” and that there is no label associated with the buffer itself. Now, because we know the buffer immediately follows the descriptor, we could get its address by adding 8 to the address of the descriptor:

            MOVAB   OUTBUFF_D+8,R1                  ; R1 -> output buffer

But what happens if we want to separate the buffer from the descriptor, or if we’re not really sure where the buffer actually is? Well, we have the address of the buffer in the descriptor, so we can retrieve it safely using the following instruction:

            MOVAB   @OUTBUFF_D+4,R1                 ; R1 -> output buffer

The “@OUTBUFF_D+4” is, officially, “longword relative deferred” addressing. In layman’s terms, it means treat the value located at OUTBUFF_D+4 as an address. In this case, the same thing could have been accomplished using MOVL:

            MOVL    OUTBUFF_D+4,R1                  ; R1 -> output buffer

See how your choices are practically endless? That’s what makes programming in MACRO so much fun!

Now that we have the address of the output buffer in R1 and the address of the byte past the input buffer in R2, we’re ready to begin copying the string from one to the other. This can very easily be accomplished using auto-decrement mode (described earlier) and auto-increment mode. The following two instruction loop is all that’s needed to copy the string in reverse order:

     10$:   MOVB    -(R2),(R1)+                     ; Copy byte from input buffer
                                                    ; ... to the output buffer
            SOBGTR  R0,10$                          ; Loop until all copied

Here’s how it works: the address in R2 is decremented by 1 (because the instruction is MOVB), the byte at that address is copied to the address stored in R1, and R1 is incremented by 1. Auto-increment mode, specified by “(R1)+”, works opposite from auto-decrement in that the value in the register is not incremented until after the address is referenced.

The SOBGTR instruction is “Subtract One and Branch if GreaTeR.” Since the value in R0 is the length of the string, we can use it to control the number of times the MOVB instruction is executed. Each time a byte is copied, one is subtracted from the length and the result is compared to 0; if the value is greater than 0, there are still bytes to be copied, so the branch to 10$ is taken. Once the value hits zero, we have copied all the bytes of the string, and control simply drops through to the next instruction.

As you’ve probably guessed by now, SOBGTR is only one of several looping instructions; naturally, a future article will cover these instructions in more depth.

We’ve now copied the input string, in reverse order, to the output buffer. The length of the string has already been stored in the string descriptor for the output buffer, OUTBUFF_D, so we’re ready to print the string to SYS$OUTPUT. The following instructions call LIB$PUT_OUTPUT, passing the address of the descriptor as the only parameter:

            PUSHAQ  OUTBUFF_D                       ; Print the output buffer
            CALLS   #1,G^LIB$PUT_OUTPUT             ; ... to SYS$OUTPUT

Finally, the program ends with the following line:

     100$:  RET                                     ; Return to caller

The RET instruction (RETurn) returns control to the caller of the routine, VMS in this case. Note that the local label 100$ was referenced earlier by the BLBC instruction. Had there been an error from LIB$GET_INPUT, control would have been transferred to the RET, effectively passing the error status back to the calling routine. One of the functions of the RET instruction is to restore the contents of all registers specified in the entry mask.

The module ends using the .END directive:

            .END    REVERSE

The .END directive takes a transfer label as an optional operand. Since REVERSE.MAR is a complete program, we must tell the linker which entry point is to be called when the program is activated. Specifying REVERSE ensures that, at image activation time, VMS transfers control to the address labelled REVERSE. Had this program consisted only of routines to be called from other programs, the label would not have been specified.

As a final note, when the assembler sees the .END directive, it stops processing the file. This makes it possible to put additional comments or programming notes at the end of a program, without prefixing each line with a semi-colon to make them comments.

The following figure shows a sample run of REVERSE.MAR:

            $ MACRO REVERSE
            $ LINK REVERSE
            $ RUN REVERSE
            Enter a string: This is a sample run of REVERSE
            ESREVER fo nur elpmas a si sihT
            $

Well, congratulations! That wasn’t so bad, was it? You’ve just successfully made it through a complete MACRO program, in a journey probably more detailed than you hoped, but bereft of many, many other details. In the months to come, I’ll be looking at programming methods for MACRO, including how to implement the control loops offered by high-level languages, how to write subroutines in MACRO, how to write macros in MACRO, and lots, lots more. I hope you’ll stayed tuned ’til next time: same Bat-time, same Bat-journal.

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

