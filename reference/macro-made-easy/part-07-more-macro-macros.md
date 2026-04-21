
# MACRO Made Easy – Part VII: More MACRO Macros

## MACRO Made Easy

## Part VII: More MACRO Macros

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

A note before beginning: this article talks a lot about the efficiencies of certain VAX instructions. Note that these conversations don’t necessarily apply to the MACRO-32 compilers on Alpha and Itanium. The methods described still work, but they may or may not be more efficient than what the compilers choose to do on those platforms.

### Finishing with the Character Instructions

Last issue, we covered a number of the very powerful instructions for manipulating characters on the VAX. There are five more character instructions that are not used very often, so we’ll give them a cursory glance this time. The first one is the Calculate Cyclic Redundancy Check (CRC) instruction. It is used to provide checks during communications and to provide support for software that performs checksums. Since I’ve never had any reason to use the instruction, I’ll skip any further discussion; for more information, see the VMS manual *VAX MACRO and Instruction Set Reference Manual* or the *VAX Architecture Handbook*.

The other four instructions all use a 256-byte table of characters to perform their work. The instructions are:

- MOVTC — MOVe Translated Characters
- MOVTUC — MOVe Translated Until Character
- SPANC — SPAN Characters
- SCANC — SCAN Characters

As their names imply, MOVTC and MOVTUC are very useful for translating characters as they are being copied. Perhaps the most common usage is to convert lowercase characters to uppercase as they are copied.

The format of the instruction usage is:

            MOVTC srclen,srcaddr,fill,tbladdr,dstlen,dstaddr

The operands are identical to those accepted by MOVC5, except that the fill byte is followed by the address of a 256-byte table. Each character being moved is used as an index into this table and the byte at that table index is copied to the destination buffer. The MOVTC and MOVTUC are not used very often, mostly because the building of the table can be cumbersome, unless you employ some assembler directives. For example, the code below, which only converts lowercase to uppercase, uses a work symbol (SEED) and the .REPEAT directive to store successive bytes representing each character in the ASCII character set.

    SEED = 0
    UPCASE:
            .REPEAT <^A/a/>                 ;*Repeat up to 97 times
            .BYTE   SEED                    ;*Store the byte in the table
            SEED = SEED + 1                 ;*Bump the seed
            .ENDR                           ;*Loop until done
            ;
            ;  Now put the uppercase letters in instead of the lowercase letters.
            ;
            .ASCII  /ABCDEFGHIJKLMNOPQRSTUVWXYZ/
            SEED = <^A/z/+1>                ;*Reset seed at "z" + 1
            .REPEAT <256-SEED>              ;*Fill out rest of table
            .BYTE   SEED                    ;*...
            SEED = SEED + 1                 ;*...
            .ENDR                           ;*...

    STRING: .ASCII  /this is a lowercase string/
    STRING_LEN = .-STRING
    OUTBUF: .ASCII  /                          /

            .ENTRY  UPCASE_IT,^M<>
            MOVTC   #STRING_LEN,STRING,#0,UPCASE,#STRING_LEN,OUTBUF
            RET
            .END    UPCASE_IT

The table could also have been built using successive .BYTE directives:

    UPCASE:         .BYTE   0,1,2,3,4,5,6,7,8,9,10,11,....
                    .BYTE   20,21,22,23,24,...
                    .....
                    .BYTE   ...,251,252,253,254,256

But you can see how tedious that would have been if all we wanted to do is convert lowercase to uppercase. It should also be obvious that MOVTC could be extremely effective if you were implementing some cipher algorithm, since each character in a string could be replaced within a single VAX instruction.

The difference between MOVTC and MOVTUC is that MOVTUC will stop either when the strings are exhausted *or* an escape character is reached in the source string. The escape character replaces the fill character in the MOVTC instruction:

            MOVTUC  srclen,srcaddr,esc,tbladdr,dstlen,dstaddr

If the escape character is reached, the V-bit condition code is set (which can be checked using a BVS instruction (Branch V-bit Set). MOVTUC is most useful when you want to translate everything up to a particular character. For example, suppose your program contained a buffer consisting of lines of terminal input, where each line is terminated by a carriage return (\<CR\>) in the buffer. You could copy (and/or translate) each line of input using the following instruction:

            MOVTUC  #INBUFF_LEN,INBUFF,#13,COPY,#STRING_LEN,DESTINATION
            BVS     ESCAPE_FOUND                    ; Branch if escape found

The string INBUFF would be copied until either a \<CR\> was found or the whole string was copied. To suppress any translation on the string, the following sequence could be used to build the table:

    SEED = 0
    COPY:   .REPEAT 256
            .BYTE   SEED
            SEED = SEED + 1
            .ENDR

SCANC and SPANC also use a 256-byte table, but the usage is a little different. The format of these instructions is as follows:

            SxANC   len,addr,tbladdr,mask

Each byte in the string is again used as an index into the 256-byte table. The byte selected is then ANDed with the MASK operand. The operation continues until the result is zero for SPANC or non-zero for SCANC. The values left in R0 and R1 are the number of remaining bytes, including the “offending” character, and the address of that character. In it’s simplest case, you could use SCANC to locate any control characters (ASCII values 0–31) in a string:

    TABLE:          .REPEAT 32
                    .BYTE   1
                    .ENDR
                    .REPEAT <256-32>
                    .BYTE   0
                    .ENDR
    INBUFF:         .ASCII  /Hello, /
                    .BYTE   13
                    .ASCII  /Goodbye/
    INBUFF_LEN = .-INBUFF
            ....
            SCANC   #INBUFF_LEN,INBUFF,TABLE,#1
            ;
            ;  Here, R1 points to the 13 (<CR>) and R0 contains 8

As I said above, these character instructions are not used very often, but they can be extremely useful in the proper program.

### Writing Character Macros

Now that we’ve seen most of the VAX character instructions, let’s turn our attention to writing some rather complex macros that can be helpful when working with the character instructions. You may recall that we’ve written a couple of short macros before, most notably the .ITMLST macros in [“MACRO Made Easy, Part 5”](https://hunter.goatley.com/macro-made-easy/part-v-barkeep-how-bout-some-service/) (April 1992).

First, let’s look at the MOVS macro, which is pictured in [Program 1](https://hunter.goatley.com/macro_07.html#Program1). MOVS was designed to let you copy short strings to buffers without having to create storage space in the data program section (psect). MOVS will generate a series of MOVL, MOVW, and MOVB instructions with the string broken up into longword, word, and byte ASCII literals. The length of the string can also be copied to an optional DESTLEN parameter. For example, the following invocation:

            MOVS    <Table addresses: >,OUTBUFF,OUTBUFF_LEN

would produce the following instructions:

            PUSHL   R0
            MOVAB   OUTBUFF,R0
            MOVL    #^A/Tabl/,(R0)+
            MOVL    #^A/e ad/,(R0)+
            MOVL    #^A/dres/,(R0)+
            MOVL    #^A/ses:/,(R0)+
            MOVB    #^A/ /,(R0)+
            POPL    R0
            MOVL    #17,OUTBUFF_LEN

Such sequences can be useful when writing MACRO. The alternative would’ve have been to create the string in the data psect:

    STRING:         .ASCII  /Table addresses: /
    STRING_LEN = .-STRING
            ....
            MOVC3   #STRING_LEN,STRING,OUTBUFF

Let’s start with the concepts used by the macro. The first thing it should do is determine the number of longwords, words, and bytes in the string so it knows how many, and which, MOVx instructions should be generated. This can be determined using the %LENGTH assembler string operator, which returns the length of a string. The following lines show the .MACRO statement and the initializing of some work symbols:

            .MACRO  MOVS    STRING,DEST,DESTLEN
            ;
            ;  Initialize the work symbols.
            ;
            ..MOVS_LENGTH = %LENGTH(STRING)         ;Get the string length
            ..MOVS_POS = 0                          ;Offset into string starts at 0

Using the example above (), the assembler symbol ..MOVS_LENGTH is equated with value 17. ..MOVS_POS is used as a pointer into the STRING when we actually produce the MOVx instructions.

Now that we’ve got the length, we need to calculate the number of longwords, words, and bytes that the string can be broken into. For efficiency, the string should be broken up into as many large pieces as possible. The following lines create the symbols ..MOVS_L_CNT, ..MOVS_W_CNT, ..MOVS_B_CNT:

            ;
            ;  Count the number of longwords, words, and bytes in the string.
            ;
            ..MOVS_L_CNT    = <..MOVS_LENGTH / 4>
            ..MOVS_W_CNT    = <..MOVS_LENGTH / 2> & 1
            ..MOVS_B_CNT    =  ..MOVS_LENGTH & 1

For our examples, the values are 4, 0, and 1, respectively. Next, the macro saves the contents of R0 on the stack and initializes R0 to point to the destination address:

            PUSHL   R0                              ;Save R0 for work
            MOVAB   DEST,R0                         ;Destination address -> R0

Now we’re ready to generate the MOVx instructions. We already know how many of each should be generated, but how can the string be broken up into the desired ASCII literals? The method used in MOVS is the %EXTRACT string operator. It works just like the SUBSTR() in high-level languages, except that it produces no code—it is strictly an assembler operator, like the unary and binary operators (+, -, \*, /, etc.). The %EXTRACT is embedded in the appropriate MOVx instruction like so:

            MOVL    #^A/%EXTRACT(..MOVS_POS,4,<STRING>)/,(R0)+

The instruction above would extract 4 bytes from STRING, starting at the offset equated with ..MOVS_POS (0, initially). The \<\> are needed around STRING to keep the assembler from complaining that there are too many operands. If ..MOVS_POS is 0, the resulting instruction would be:

            MOVL    #^A/Tabl/,(R0)+

Once again, the .REPEAT and .ENDR assembler directives are used to generate the appropriate number of MOVx instructions. Since we have the appropriate values defined as ..MOVS_x_CNT, we can use those as .REPEAT operands:

            .REPEAT ..MOVS_L_CNT
            MOVL    #^A/%EXTRACT(..MOVS_POS,4,<STRING>)/,(R0)+
            ..MOVS_POS = ..MOVS_POS + 4             ;Point to next bytes
            .ENDR

In this example, the value of MOVS_L_CNT is 4, so the instructions between the .REPEAT and the .ENDR will be executed four times. Each time a MOVL is generated, the value of ..MOVS_POS is incremented by 4 to point to the next byte after the longword just used. The other three generated instructions would look like these:

            MOVL    #^A/e ad/,(R0)+
            MOVL    #^A/dres/,(R0)+
            MOVL    #^A/ses:/,(R0)+

Once the MOVLs have been processed, the same thing is done for the words and bytes:

            .REPEAT ..MOVS_W_CNT
            MOVW    #^A/%EXTRACT(..MOVS_POS,2,<STRING>)/,(R0)+
            ..MOVS_POS = ..MOVS_POS + 2             ;Point to next bytes
            .ENDR
            ;
            ;  Now do the byte, if there is one.
            ;
            .REPEAT ..MOVS_B_CNT
            MOVB    #^A/%EXTRACT(..MOVS_POS,1,<STRING>)/,(R0)+
            .ENDR

Note that there will be at most only one MOVW and only one MOVB instruction. However, the .REPEAT-.ENDR combination was used for consistency and flexibility, and because I believe I found a bug in the assembler. If a .IF conditional was used, the %EXTRACT failed to produce the proper character. Using .REPEAT generated the proper MOVB instruction.

Now we need to restore the contents of our work register (R0):

            POPL    R0                              ;Restore contents of R0

Finally, we’re ready to copy the string length to the DESTLEN parameter, if it was specified on the macro call. This is accomplished using the .IIF directive, which is an immediate conditional. That is, it can be used to produce a single line of code.

            ;
            ;  Leave length in DESTLEN, if specified.
            ;
            .IIF    NOT_BLANK, DESTLEN,     MOVL    #..MOVS_LENGTH,DESTLEN

This line says that if DESTLEN is “not blank” (it has a value), then generate the MOVL instruction. Otherwise, move on to the next line, which is the .ENDM line:

            .ENDM   MOVS                            ;*End of MOVS macro

Make sense? You might want to study it a little more before moving on, because the next macro (macros) is considerably more involved. Also, the .IF conditional will be examined in more detail.

### The MOVCX Macro

As I mentioned last issue, the MOVC3 instruction can be rather costly, depending on the VAX platform (since the instruction is emulated in software on many VAXes today). This is especially true when MOVC3 is used to copy short strings of no more than, say, 20 bytes. In those cases, a series of MOVQ, MOVL, MOVW, and MOVB instructions will be more efficient. Additionally, many programs use registers R0–R5 and must save and restore them before and after the MOVC3 instruction is executed. To gain maximum efficiency and minimal programmer headache, I wrote a macro called MOVCX that will automatically save and restore any work registers, and, more importantly, will determine whether the length is a literal and, if so, will generate the appropriate MOVx instructions for short strings.

[Program 2](https://hunter.goatley.com/macro_07.html#Program2) depicts the MOVCX macro and its supporting macros PUSHREG and POPREG.

The first three parameters to MOVCX are the same as for MOVC3: the length, the source address, and the destination address. It also takes two more parameters: a flag, PRESERVE, that determines whether or not the registers should be saved, and LIMIT, which determines the maximum size of a “short” string that will be copied with MOVx instructions. The defaults are PRESERVE=YES and LIMIT=32, as can be seen on the .MACRO line:

            .MACRO  MOVCX   LENGTH,SRC,DEST,PRESERVE=YES,LIMIT=32

Before looking at the macro, let’s look again at the algorithm used. The first thing it does is determine whether or not the LENGTH parameters is a short literal or immediate value (preceded by \#, S^#, or I^#). For example, the following are all literals:

            MOVCX   #3,SRC,DEST
            MOVCX   #STRING_LEN,STRING,OUTBUFF
            MOVCX   S^#STRING_LEN,STRING,OUTBUFF
            MOVCX   I^#STRING_LEN,STRING,OUTBUFF    ;Immediate

Immediate mode would not normally be used, but it is handled by the macro.

If the length is not a literal, a normal MOVC3 is generated, with R0–R5 preserved if desired. If the length *is* a literal, it is compared with the LIMIT (32, by default). If it exceeds the limit, once again, a normal MOVC3 is generated, since it is probably more efficient than multiple MOVx instructions.

Finally, if the length does *ot* exceed the limit, the proper number of MOVQ, MOVL, MOVW, and MOVB instructions are generated to copy quadwords, longwords, words, and bytes. Notice that there will be at most one longword, one word, and one byte to copy. For example, if the length is twenty bytes, it can be copied as two quadwords (16 bytes) and a longword (4 bytes). If the length were 22, it would be two quadwords, one longword, and one word, etc.

The MOVCX macro uses the assembler directives .NTYPE, .IF, and .REPEAT. .NTYPE returns the addressing mode of the given symbol; it is used to determine whether or not the given length is a literal. .IF lets us implement conditional assembly, and we’ve already seen .REPEAT used in MOVS.

Before looking at MOVCX itself, let’s look at its two supporting macros, PUSHREG and POPREG. MOVCX will need to save and restore registers in several places. Because the PUSHR and POPR instructions are rather costly, I wanted to use PUSHLs and POPLs, but I didn’t want them cluttering up the MOVCX macro. The solution I chose was create PUSHREG and POPREG macros and nest calls to them inside MOVCX.

In the .ITMLST macros presented in Part 5, I used the .IRP (Indefinite RePeat) assembler directive. I also used it in PUSHREG and POPREG to process each of the registers that are to be saved and restored. The call to PUSHREG and POPREG should include a comma-separated list of registers, surrounded by angle brackets:

            PUSHREG <R0,R1,R2,R3,R4,R5>

The actual macro definition is as follows:

            .MACRO  PUSHREG REGS                    ;*Push registers on stack;
            .IRP    REG,<REGS>                      ;*For each register given;
            PUSHL   REG                             ; Save contents of REG;
            .ENDR                                   ;*Loop until no more;
            .ENDM   PUSHREG                         ;*End of PUSHREG macro;

The .IRP REG,\<REGS\> directive processes each register in the comma-separated list; the generated code consists of PUSHL R0, PUSHL R1, etc. Because POPREG is implemented the same way, it is important to make sure that the registers are specified in exactly the opposite order as their order for PUSHREG to maintain the LIFO stack order (last in, first out):

            POPREG  <R5,R4,R3,R2,R1>

This is not very flexible from a programmer’s view, but since these macros were written primarily to support MOVCX, I decided that it was OK.

Now let’s take a look at the MOVCX macro. The .MACRO line and a symbol initialization come first:

            .MACRO  MOVCX   LENGTH,SRC,DEST,PRESERVE=YES,LIMIT=32
            ..MOVCX_X = 0                           ;Initialize the work variable

..MOVCX_X will be used later in the macro to hold an offset into a string. It should be initialized here so that it’s use later won’t result in the assembler complaining that the symbol is undefined or not absolute.

The first thing MOVCX should do is check to see if the specified length is a literal. As mentioned above, this is accomplished using the .NTYPE directive, which returns the addressing mode of the specified operand. The addressing mode is normally an 8-bit value, though it can be 16 bits. Bits 0–3 represent the register used in the addressing mode; bits 4–7 represent the mode itself. Normally, literals are determined by bits 4–7 having a value in the range 0–3. However, a literal causes .NTYPE to return with bits 4–7 as all zeros. Immediate mode is indicated by the value 1. The following line shows the .NTYPE call:

            .NTYPE  ..MOVCX_LEN_TYPE,LENGTH         ;Get the addressing mode

The addressing mode of LENGTH is equated with the symbol ..MOVCX_LEN_TYPE. Since we’re only interested in bits 4–7, out of a possible 16, we need to mask out the rest. This is accomplished by shifting the value right 4 bits and ANDing the result with ^XF to mask out the upper nibble(s):

            ..MOVCX_LEN_TYPE = <..MOVCX_LEN_TYPE@-4> & ^XF

The ‘@’ is the shift operator; “-4” says, “Shift right 4 bits.”

We can now check to see if the type is a literal or an immediate (0 or 1). This is done using the .IF assembler directive. The general format of the .IF directive is:

            .IF condition parameter(s)
            ...
            ...  statements
            ...
            .ENDC

The condition is one of the following:

 

<table data-cellspacing="5">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<tbody>
<tr>
<th style="text-align: left;">Condition</th>
<th style="text-align: left;">Abbrev.</th>
<th style="text-align: left;">Complement</th>
<th style="text-align: left;">Abbrev.</th>
<th style="text-align: left;"># of params</th>
</tr>
&#10;<tr>
<td colspan="5" style="text-align: left;"><hr /></td>
</tr>
<tr>
<td style="text-align: left;">EQUAL</td>
<td style="text-align: left;">EQ</td>
<td style="text-align: left;">NOT_EQUAL</td>
<td style="text-align: left;">NE</td>
<td style="text-align: left;">1 expression</td>
</tr>
<tr>
<td style="text-align: left;">GREATER</td>
<td style="text-align: left;">GT</td>
<td style="text-align: left;">LESS_EQUAL</td>
<td style="text-align: left;">LE</td>
<td style="text-align: left;">1 expression</td>
</tr>
<tr>
<td style="text-align: left;">LESS_THAN</td>
<td style="text-align: left;">LT</td>
<td style="text-align: left;">GREATER_EQUAL</td>
<td style="text-align: left;">GE</td>
<td style="text-align: left;">1 expression</td>
</tr>
<tr>
<td style="text-align: left;">DEFINED</td>
<td style="text-align: left;">DF</td>
<td style="text-align: left;">NOT_DEFINED</td>
<td style="text-align: left;">NDF</td>
<td style="text-align: left;">1 symbol</td>
</tr>
<tr>
<td style="text-align: left;">BLANK</td>
<td style="text-align: left;">B</td>
<td style="text-align: left;">NOT_BLANK</td>
<td style="text-align: left;">NB</td>
<td style="text-align: left;">1 (only in macros)</td>
</tr>
<tr>
<td style="text-align: left;">IDENTICAL</td>
<td style="text-align: left;">IDN</td>
<td style="text-align: left;">DIFFERENT</td>
<td style="text-align: left;">DIF</td>
<td style="text-align: left;">2 (only in macros)</td>
</tr>
</tbody>
</table>

When an expression is given, it is evaluated and compared with 0. If the evaluation results in a true statement, the lines following the .IF are expanded. For example, if symbol TRUE has a value of 1, the following lines would produce CLRL R0:

            .IF EQ TRUE
            CLRL    R0
            .ENDC

There are also directives for handling other cases: .IF_FALSE, .IF_TRUE, .IF_TRUE_FALSE. These are most frequently used in cases like the following:

            .IF condition parameter(s)
            ...
            ...  statements if true
            ...
            .IF_FALSE
            ...
            ...  statements if false
            ...
            .ENDC

The DEFINED and NOT_DEFINED conditionals let you write VMS version-specific code and easily assemble debug instructions or leave them out. They take one operand: a symbol. If the symbol is defined (or not defined), the lines between are included. For example, if you have code that depends on a certain value being defined, you could use the .IF conditionals to avoid undefined symbol errors when compiling on a machine running without that value. The following code would assemble properly on all systems, even on a version of VMS before VT400-series terminals were defined:

            .IF DEFINED TT$_VT400_Series            ;If the VT400 is known,
            MOVL    #TT$_VT400_Series,R0            ;... set it to that
            .IF_FALSE                               ;Otherwise, set it to
            MOVL    #TT$_VT100,R0                   ;... VT100
            .ENDC                                   ;*End of conditional

As you can see, this is functionally equivalent to \#ifdef and \#ifndef in the C programming language.

The BLANK, NOT_BLANK, IDENTICAL, and DIFFERENT conditionals can only be used with macros. BLANK and NOT_BLANK can be used to see if the named macro parameter was given or not. We used NOT_BLANK with the .IIF in MOVS:

            .IIF    NOT_BLANK, DESTLEN,     MOVL    #..MOVS_LENGTH,DESTLEN

The .IIF works the same way as .IF, except that it can only produce a single instruction. The line above could also have been written as:

            .IF NOT_BLANK DESTLEN
            MOVL    #..MOVS_LENGTH,DESTLEN
            .ENDC

Finally, DIFFERENT and IDENTICAL can be used to check the value that was passed as a macro parameter. We’ll see an example of that momentarily.

Getting back to the MOVCX macro, we can check to see if the operand type is literal or immediate with the following conditional:

            .IF LE <..MOVCX_LEN_TYPE-1>

The expression, \<..MOVCX_LEN_TYPE-1\>, is evaluated and compared with 0. If MOVCX_LEN_TYPE is either 0 or 1, subtracting 1 from it will leave 0 or -1, which is LE 0. So the statements following the .IF up to either .IF_FALSE or .ENDC will be expanded.

Assuming the value is a literal, we need to see if it falls within the specified limit for character strings. The parameter LENGTH is equated to the original literal string, which includes the ‘#’ (or “S^#” or “I^#”). We need to remove the ‘#’ before we can use LENGTH as a number for the limit test. This is accomplished with the following lines:

                    .IF IDN <#>,<%EXTRACT(0,1,LENGTH)>
                            ..MOVCX_X = %LENGTH(LENGTH)
                            ..MOVCX_LENGTH = <%EXTRACT(1,..MOVCX_X,LENGTH)>
                    .ENDC

The first line extracts the first character of LENGTH and compares that with the string \<#\>. If it’s equal, it gets the length of the LENGTH string, then equates a new symbol, ..MOVCX_LENGTH, with the remaining number using the %EXTRACT string operator. For example, assume MOVCX was invoked with the following line:

            MOVCX   #10,STRING,BUFFER

After evaluation, ..MOVCX_LENGTH would be equated to 10. If a symbol is passed in:

            MOVCX   #STRING_LEN,STRING,BUFFER

..MOVCX_LENGTH would receive the value of the symbol STRING_LEN. Additional checks are made to handle \<S^#\> and \<I^#\>.

                    ;
                    ;  If "S^" is present (short literal), remove it.
                    ;
                    .IF IDN <S^#>,<%EXTRACT(0,3,LENGTH)>
                            ..MOVCX_X = %LENGTH(LENGTH)
                            ..MOVCX_LENGTH = <%EXTRACT(3,..MOVCX_X,LENGTH)>
                    .ENDC
                    ;
                    ;  If "I^" is present (immediate mode), remove it.
                    ;
                    .IF IDN <I^#>,<%EXTRACT(0,3,LENGTH)>
                            ..MOVCX_X = %LENGTH(LENGTH)
                            ..MOVCX_LENGTH = <%EXTRACT(3,..MOVCX_X,LENGTH)>
                    .ENDC

Now that the string length is equated with ..MOVCX_LENGTH, we can compare that with the LIMIT parameter. Notice that LIMIT has a default value, we don’t need to check to see if it’s there; however, we could have with a line like the following:

                    .IF NOT_BLANK LIMIT

The limit check is performed with the following conditional:

                    .IF GT <..MOVCX_LENGTH - LIMIT>

At this point, if the length is greater than the specified limit, a normal MOVC3 is generated. The registers are saved and restored if the PRESERVE parameter value is identical to YES:

                            .IIF IDENTICAL PRESERVE,<YES>, -
                                    PUSHREG <R5,R4,R3,R2,R1,R0>
                            MOVC3   LENGTH,SRC,DEST
                            .IIF IDENTICAL PRESERVE,<YES>, -
                                    POPREG  <R0,R1,R2,R3,R4,R5>

If the value didn’t exceed the limit, the following code is expanded:

                    .IF_FALSE                       ;Didn't exceed LIMIT
                            ;
                            ;  Now count the number of quadwords, longwords, words,
                            ;  and bytes in the string.
                            ;
                            ..MOVCX_Q_LEN = <..MOVCX_LENGTH / 8>
                            ..MOVCX_L_LEN = <..MOVCX_LENGTH / 4> & 1
                            ..MOVCX_W_LEN = <..MOVCX_LENGTH / 2> & 1
                            ..MOVCX_B_LEN = <..MOVCX_LENGTH> & 1

As in MOVS, the lines above calculate the number of quadwords in the string, followed by whether or not there is a longword, word, or byte left over. Next the registers are saved (if desired) and the SRC and DEST addresses are copied to to R0 and R1:

                            ;
                            ;  Save registers, if necessary.
                            ;
                            .IIF IDENTICAL PRESERVE,<YES>,  PUSHREG <R0,R1>

                            MOVAB   SRC,R0          ;Move SRC address to R0
                            MOVAB   DEST,R1         ;Move DEST address to R1

Now we’re ready to generate the actual MOVQ, MOVL, MOVW, and MOVB instructions. Again, this code is almost identical to that generated by MOVS, except the string is not an ASCII literal string:

                            .IF NE ..MOVCX_Q_LEN    ;*If there are any of this type
                            .REPEAT ..MOVCX_Q_LEN   ;... generate that number of
                            MOVQ    (R0)+,(R1)+     ;... MOVQ instructions
                            .ENDR                   ;*Loop until no more MOVQs
                            .ENDC                   ;*End of .IF

                            .IIF NE, ..MOVCX_L_CNT, MOVL    (R0)+,(R1)+
                            .IIF NE, ..MOVCX_W_CNT, MOVW    (R0)+,(R1)+
                            .IIF NE, ..MOVCX_B_CNT, MOVB    (R0)+,(R1)+

Finally, if the operand type was not a literal, a normal MOVC3 is generated. This is the .IF_FALSE part of the original .IF that checked to see if the operand type was a literal or immediate:

            .IF_FALSE

                    .IIF IDENTICAL PRESERVE,<YES>,  PUSHREG <R5,R4,R3,R2,R1,R0>

                    MOVC3   LENGTH,SRC,DEST         ;Just use a MOVC3

                    .IIF IDENTICAL PRESERVE,<YES>,  POPREG  <R0,R1,R2,R3,R4,R5>

            .ENDC

            .ENDM   MOVCX                           ;*End of MOVCX macro

### Some Samples

The following lines show some invocations of the MOVS and MOVCX macros:

            MOVCX   STR_D,@STR_D+4,OUTBUF           ;Generates a MOVC3
            MOVAB   OUTBUF,(R1)
            MOVCX   S^#STR_LEN,STR,(R1)
            MOVCX   I^#STR1_LEN,STR1,(R1)
            MOVCX   #STR1_LEN,STR1,(R1),PRESERVE=NO
            MOVS    <This is a test! @>,(R1)

            MOVAB   OUTBUF,R4
            MOVS    <SYSTEM>,JIB$T_USERNAME(R4),R0  ;Leave length in R0

As you can see, you can write some pretty complex macros. Even if you don’t find a use for MOVS and MOVCX, you should be ready to try to write your own macros to generate the code you want.

### NEXT TIME….

Next issue, we’ll look at some macros provided with VMS and also look at doing file I/O from MACRO using RMS.

------------------------------------------------------------------------

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

------------------------------------------------------------------------

<span id="Program1"></span>

## Program 1

    ;+
    ;
    ;  Macro:       MOVS
    ;
    ;  Author:      Hunter Goatley, goathunter@WKUVX1.BITNET
    ;               May 25, 1992
    ;
    ;  Functional description:
    ;
    ;       The MOVS macro copies a given string to a given destination
    ;       address.  The length of the string can be optionally copied
    ;       to the DESTLEN parameter.
    ;
    ;       This macro is useful when you want to copy small ASCII strings
    ;       to a buffer, without creating the string in a data area.  For
    ;       example:
    ;
    ;               MOVS    <SYSTEM>,JIB$T_USERNAME+1(R3),R0
    ;               MOVB    R0,JIB$T_USERNAME(R3)
    ;
    ;       The sequence above would generate the following instructions:
    ;
    ;               PUSHL   R0
    ;               MOVAB   JIB$T_USERNAME+1(R3),R0
    ;               MOVL    #^A/SYST/,(R0)+
    ;               MOVW    #^A/EM/,(R0)+
    ;               POPL    R0
    ;               MOVL    #6,R0
    ;               MOVB    R0,JIB$T_USERNAME(R3)
    ;
    ;-
            .MACRO  MOVS    STRING,DEST,DESTLEN

            ;
            ;  Initialize the work symbols.
            ;
            ..MOVS_LENGTH = %LENGTH(STRING)         ;Get the string length
            ..MOVS_POS = 0                          ;Offset into string starts at 0

            ;
            ;  Count the number of longwords, words, and bytes in the string.
            ;
            ..MOVS_L_CNT    = <..MOVS_LENGTH / 4>
            ..MOVS_W_CNT    = <..MOVS_LENGTH / 2> & 1
            ..MOVS_B_CNT    = <..MOVS_LENGTH> & 1

            PUSHL   R0                              ;Save R0 for work
            MOVAB   DEST,R0                         ;Destination address -> R0
            ;
            ;  For each longword that can be moved, generate an instruction
            ;  like the following:
            ;               MOVL    #^A/TEXT/,(R0)+
            ;
            .REPEAT ..MOVS_L_CNT
            MOVL    #^A/%EXTRACT(..MOVS_POS,4,<STRING>)/,(R0)+
            ..MOVS_POS = ..MOVS_POS + 4             ;Point to next bytes
            .ENDR

            ;
            ;  Now do any words that can be done.
            ;
            .REPEAT ..MOVS_W_CNT
            MOVW    #^A/%EXTRACT(..MOVS_POS,2,<STRING>)/,(R0)+
            ..MOVS_POS = ..MOVS_POS + 2             ;Point to next bytes
            .ENDR

            ;
            ;  Now do the byte, if there is one.
            ;
            .REPEAT ..MOVS_B_CNT
            MOVB    #^A/%EXTRACT(..MOVS_POS,1,<STRING>)/,(R0)+
            .ENDR

            POPL    R0                              ;Restore contents of R0

            ;
            ;  Leave length in DESTLEN, if specified.
            ;
            .IIF    NOT_BLANK, DESTLEN,     MOVL    #..MOVS_LENGTH,DESTLEN

            .ENDM   MOVS                            ;*End of MOVS macro

------------------------------------------------------------------------

<span id="Program2"></span>

## Program 2

    ;+
    ;
    ;  Macro:       PUSHREG & POPREG
    ;
    ;  Author:      Hunter Goatley, goathunter@WKUVX1.BITNET
    ;               May 25, 1992
    ;
    ;  Functional description:
    ;
    ;       PUSHREG and POPREG accept as inputs a list of registers whose
    ;       contents are pushed onto and popped off of the stack using
    ;       PUSHL and POPL instructions.  This is faster than using
    ;       the PUSHR and POPR instructions.
    ;
    ;  WARNING: the list of registers passed to POPREG must be in the exact
    ;           opposite order from the list passed to PUSHREG.  For example:
    ;
    ;               PUSHREG <R0,R1,R2>
    ;               POPREG  <R2,R1,R0>
    ;
    ;-
            .MACRO  PUSHREG REGS                    ;*Push registers on stack;
            .IRP    REG,<REGS>                      ;*For each register given;
            PUSHL   REG                             ; Save contents of REG;
            .ENDR                                   ;*Loop until no more;
            .ENDM   PUSHREG                         ;*End of PUSHREG macro;

            .MACRO  POPREG  REGS                    ;*Pop registers off stack;
            .IRP    REG,<REGS>                      ;*For each register given;
            POPL    REG                             ; Restore contents of REG;
            .ENDR                                   ;*Loop until no more;
            .ENDM   POPREG                          ;*End of POPREG macro;

    ;+
    ;
    ;  Macro:       MOVCX
    ;
    ;  Author:      Hunter Goatley, goathunter@WKUVX1.BITNET
    ;               May 25, 1992
    ;
    ;  Functional description:
    ;
    ;       MOVCX is designed to serve as a functional replacement for MOVC3.
    ;       Because MOVC3 is a relatively expensive instruction on most VAX
    ;       processors, it is desirable to use a combination of MOVQ, MOVL,
    ;       MOVW, and MOVB instructions when copying small strings.  MOVCX
    ;       will automatically determine if the given length parameter is
    ;       a literal value (known at assembly-time) and, if so, will generate
    ;       the appropriate MOVx instructions to copy the string.  If the
    ;       string length is not a literal, or is greater than 32 bytes, a
    ;       MOVC3 is generated.  In both cases, the macro will, by default,
    ;       preserve the registers used as scratch registers.
    ;
    ;       NOTE: this macro also calls the PUSHREG, POPREG, and MOVCX_GEN_MOVX
    ;       macros.  It also defines a number of symbols, all prefixed by the
    ;       string "..MOVCX_".
    ;
    ;  Formal parameters:
    ;
    ;       LENGTH          The length of the string
    ;       SRC             The address of the first byte of the source
    ;       DEST            The address of the first byte of the destination
    ;       PRESERVE        If YES (the default), all registers are preserved
    ;       LIMIT           MOVC3 size limit (default 32)
    ;
    ;       If PRESERVE=NO and the length is a literal, R0 and R1 are used as
    ;       work registers.
    ;
    ;  Calling sequence:
    ;
    ;       MOVCX   #STRING_LEN,SOURCE,DESTINATION
    ;       MOVCX   (R3),(R4),(R5)
    ;       MOVCX   #STRING_LEN,SOURCE,DESTINATION,PRESERVE=NO      ;Don't save regs
    ;
    ;-
            .MACRO  MOVCX   LENGTH,SRC,DEST,PRESERVE=YES,LIMIT=32
            ..MOVCX_X = 0                           ;Initialize the work variable

            ; Get the type of the length parameter.  The type returned is
            ; either an 8-bit or 16-bit value.  Bits 0--3 represent the
            ; register used; bits 4--7 represent the addressing mode.  The
            ; addressing mode returned by .NTYPE isn't exactly the same as
            ; the normal addressing mode encoding. Specifically, a literal
            ; is specified by bits 4--7 being all zero (instead of holding
            ; one of the values 0--3).
            ;
            .NTYPE  ..MOVCX_LEN_TYPE,LENGTH         ;Get the addressing mode

            ; Since we're only interested in bits 4--7, shift the type
            ; returned right 4 bits, then AND it with hexadecimal F to
            ; clear out the high byte in case a 16-bit value was returned.
            ;
            ..MOVCX_LEN_TYPE = <..MOVCX_LEN_TYPE@-4>&^XF

            ; Now check to see if the addressing mode is short literal
            ; (value is 0) or immediate (value is 1).

            .IF LE <..MOVCX_LEN_TYPE-1>
                    ;
                    ;  Because it's a literal, the "#" should be present.
                    ;  Let's be safe, though, and check for it before using
                    ;  the length as a number (in symbol ..MOVCX_LENGTH).
                    ;
                    .IF IDN <#>,<%EXTRACT(0,1,LENGTH)>
                            ..MOVCX_X = %LENGTH(LENGTH)
                            ..MOVCX_LENGTH = <%EXTRACT(1,..MOVCX_X,LENGTH)>
                    .ENDC
                    ;
                    ;  If "S^" is present (short literal), remove it.
                    ;
                    .IF IDN <S^#>,<%EXTRACT(0,3,LENGTH)>
                            ..MOVCX_X = %LENGTH(LENGTH)
                            ..MOVCX_LENGTH = <%EXTRACT(3,..MOVCX_X,LENGTH)>
                    .ENDC
                    ;
                    ;  If "I^" is present (immediate mode), remove it.
                    ;
                    .IF IDN <I^#>,<%EXTRACT(0,3,LENGTH)>
                            ..MOVCX_X = %LENGTH(LENGTH)
                            ..MOVCX_LENGTH = <%EXTRACT(3,..MOVCX_X,LENGTH)>
                    .ENDC

                    ;
                    ;  At this point, ..MOVCX_LENGTH holds the length of the
                    ;  string to copy.
                    ;
                    ;  If we exceed the length limit (32, by default), just
                    ;  generate a MOVC3 instruction (and save regs if desired).
                    ;
                    .IF GT <..MOVCX_LENGTH - LIMIT>

                            .IIF IDENTICAL PRESERVE,<YES>, -
                                    PUSHREG <R5,R4,R3,R2,R1,R0>
                            MOVC3   LENGTH,SRC,DEST
                            .IIF IDENTICAL PRESERVE,<YES>, -
                                    POPREG  <R0,R1,R2,R3,R4,R5>

                    .IF_FALSE                       ;Didn't exceed LIMIT
                            ;
                            ;  Now count the number of quadwords, longwords, words,
                            ;  and bytes in the string.
                            ;
                            ..MOVCX_Q_LEN = <..MOVCX_LENGTH / 8>
                            ..MOVCX_L_CNT = <..MOVCX_LENGTH / 4> & 1
                            ..MOVCX_W_CNT = <..MOVCX_LENGTH / 2> & 1
                            ..MOVCX_B_CNT = <..MOVCX_LENGTH> & 1

                            ;
                            ;  Save registers, if necessary.
                            ;
                            .IIF IDENTICAL PRESERVE,<YES>,  PUSHREG <R0,R1>

                            MOVAB   SRC,R0          ;Move SRC address to R0
                            MOVAB   DEST,R1         ;Move DEST address to R1

                            .IF NE ..MOVCX_Q_LEN    ;*If there are any of this type
                            .REPEAT ..MOVCX_Q_LEN   ;... generate that number of
                            MOVQ    (R0)+,(R1)+     ;... MOVQ instructions
                            .ENDR                   ;*Loop until no more MOVQs
                            .ENDC                   ;*End of .IF

                            .IIF NE, ..MOVCX_L_CNT, MOVL    (R0)+,(R1)+
                            .IIF NE, ..MOVCX_W_CNT, MOVW    (R0)+,(R1)+
                            .IIF NE, ..MOVCX_B_CNT, MOVB    (R0)+,(R1)+

                            ;
                            ;  Restore the registers, if they were saved.
                            ;
                            .IIF IDENTICAL PRESERVE,<YES>,  POPREG  <R1,R0>
                    .ENDC
            ;
            ;  Here, the length was not a literal, so just generate a MOVC3
            ;  instruction, preserving registers if necessary.
            ;
            .IF_FALSE

                    .IIF IDENTICAL PRESERVE,<YES>,  PUSHREG <R5,R4,R3,R2,R1,R0>

                    MOVC3   LENGTH,SRC,DEST         ;Just use a MOVC3

                    .IIF IDENTICAL PRESERVE,<YES>,  POPREG  <R0,R1,R2,R3,R4,R5>

            .ENDC

            .ENDM   MOVCX                           ;*End of MOVCX macro

