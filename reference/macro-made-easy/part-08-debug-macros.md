
# MACRO Made Easy – Part VIII: Still More MACRO Macros, or, Rolling Your Own Debug Macros

## MACRO Made Easy

## Part VIII: Still More MACRO Macros, or, Rolling Your Own Debug Macros

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

Last issue, we looked at a couple of macros that can make the character instructions easier to use. Before looking at VMS-supplied macros, let’s examine another very useful macro that employs a couple of “neat tricks”.

One quick-and-dirty way to debug programs is by printing informational output during the program run: things like “Inside loop” and “Past initialization.” When writing in MACRO, the simplest way to print strings like these is to call the run-time library routine LIB$PUT_OUTPUT, which you may recall seeing in the first article in this series. If you’re in a real hurry, you could include the string in-line with your code and jump over it with a sequence like the following:

            BRW     20$                     ;Jump over the string
     10$:   .ASCID  /Here we are!/          ;Here's the debug string
     20$:   PUSHAQ  10$                     ;Print it using the
            CALLS   #1,G^LIB$PUT_OUTPUT     ;... RTL routine

This leads to lots of potential problems, not the least of which is readability concerns. You would also run into problems if another section of code accidentally branched to 10$.

Another, more conventional approach would be to store the message string with the rest of your program’s data and refer to it as needed:

    DATA1:          .LONG   21
    DEBUG1:         .ASCID  /There we were!/
    DATA2:          .BLKB   20
    ....
            PUSHAQ  DEBUG1                  ;Now print the string we
            CALLS   #1,G^LIB$PUT_OUTPUT     ;... stored in data area

The biggest problems with this approach are that you can’t tell what the debug message is by reading the code, you have to come up with unique labels for each of your debug messages, and removing them for production code becomes much more time-consuming. Fortunately, all of these issues can be resolved through the use of an elegant, but fairly simple, macro.

The trick to the macro lies in switching from a code psect to a data psect and back to the code psect. Remember that psects are program sections: logical divisions of your program into segments that group items sharing certain characteristics. By default, all data up to the first .ENTRY is placed in the .BLANK. psect and code is placed in the .MAIN. psect. You can specify your own psects, and specify their attributes, using the .PSECT assembler directive:

            .PSECT  CODE,EXE,NOWRT,LONG             ;Read-only code section
            .PSECT  RO_DATA,NOEXE,NOWRT,LONG        ;Read-only data section
            .PSECT  RW_DATA,NOEXE,WRT,LONG          ;Read-write data section

I won’t go into the details of all the .PSECT options, but you can specify the read-write attributes, whether or not the section is to be overlayed with other sections, and the alignment size for the section, among other attributes. Unless a .PSECT directive specifies that the section is be overlayed, multiple occurrences of a named psect are appended together when the program is assembled. For example, assume you have a macro source file TEST.MAR that contains the following psects:

            .PSECT  DATA,NOEXE,WRT,LONG
    DATA1:  .ASCID  /This is the first one./

            .PSECT  CODE,EXE,NOWRT,LONG
            .ENTRY  TEST,^M<>
            RET

            .PSECT  DATA,NOEXE,WRT,LONG
    DATA2:  .ASCID  /This is the second one./

            .END

When the program is assembled, the two DATA psects will be combined, with the effect being that the same as if they had been specified together:

            .PSECT  DATA,NOEXE,WRT,LONG
    DATA1:  .ASCID  /This is the first one./
    DATA2:  .ASCID  /This is the second one./

The MACRO-32 assembler provides two directives to assist in the temporary switching of psects: .SAVE_PSECT and .RESTORE_PSECT. .SAVE_PSECT saves the current psect context on the top of an internal psect stack used by the assembler; up to 31 psects can be saved at any time. .RESTORE_PSECT will restore the psect that is on the top of that internal stack. The usual way these directives are used is as follows:

            .PSECT  CODE,EXE,NOWRT          ;In CODE psect....
            [...]
            .SAVE_PSECT                     ;Save this psect context
            .PSECT  DATA,NOEXE,WRT          ;Switch to another psect
            [...]                           ;Include statements
            .RESTORE_PSECT                  ;Restore to CODE psect
            [...]

The directives don’t have much practical use except in the context of a macro; it’s just that type of macro that we’ll look at now. Before we do, though, I want to point out that switching psects as shown above would disrupt any local block that was in effect (the local block would be a block using local symbols such as 10$ and 20$). To prevent such disruptions when switching you can specify an optional parameter, LOCAL_BLOCK, to .SAVE_PSECT:

            .SAVE_PSECT     LOCAL_BLOCK     ;Save psect context with local

### The OUTPUT Macro

[Program 1](https://hunter.goatley.com/macro_08.html#Program1) shows the macro OUTPUT, which accepts a string to be displayed at run-time as a parameter. The macro performs the exact functions we’ve been describing: the current psect context is saved, it switches to a data psect, an ASCID string is stored in the data psect, the code psect is restored, and the address of the ASCID string is pushed on the stack and LIB$PUT_OUTPUT is called. Typical usage for the macro would look like the following line:

            OUTPUT   <Here we are!>         ;Print debug message

The first line of the macro contains the .MACRO directive:

            .MACRO  OUTPUT  STRING,?TEXT

Remember that STRING is the formal parameter, and “?TEXT” means that the assembler is to create a unique label to replace any occurrence of “TEXT” in the macro each time the macro is expanded.

The first thing the macro does is save the current psect:

            .SAVE_PSECT LOCAL_BLOCK                         ;* Save this PSECT;

It then switches to a read-only data psect named RO_DEBUG_DATA. You can change the name to match an existing psect, if you wish.

            .PSECT  RO_DEBUG_DATA,NOEXE,WRT,LONG,SHR    ;* Change to data PSECT;

Now that we’ve changed to the data psect, we are ready to create the ASCID string. The .ASCID directive is used, with the string STRING being replaced by the formal parameter when the macro is expanded. To enhance performance, the macro also makes sure that the data is aligned on a longword boundary:

            .ALIGN  LONG                    ;* Align on longword;
     TEXT:  .ASCID  ~STRING~                ;* Create .ASCID string;

TEXT: will be replaced with a local symbol generated by the assembler (something like 30000$:), and STRING will be replaced with the parameter passed to the macro. For example, given the following macro call:

            OUTPUT   <Here we are!>         ;Print debug message

the generated lines would look something like:

            .ALIGN  LONG
    30000$: .ASCID  ~Here we are!~

Remember that the angle brackets \<\> are needed on the macro call so that the string “Here we are!” gets passed as a single parameter. If you need to print a string that includes an angle bracket, you can use specify another delimiter by prefixing the first one with a carat (^). For example, the following line shows how you could use the double-quote character to delimit the string:

            OUTPUT  ^"Here we are!"

For the .ASCID string delimiters in the expanded macro, I used the tilde (~), simply because it’s a pretty rare character. You must pick some character to use for the delimiters, so try to pick a character that probably won’t be used in your output.

There is one drawback to telling the assembler to generate a label for TEXT: the label it generates is a local label. If we just restored the original code psect, we would not be able to reference TEXT because the local label would not be defined for that block. To get around this, we simply need to define a normal symbol that is equated to the value of the local label. This is accomplished with the following line:

            ..OUTPUT_TEXT = TEXT                            ;* Save the address;

If the label generated to replace text points to address 200 in the program, the symbol ..OUTPUT_TEXT will receive the value 200. The dots that appear in ..OUTPUT_TEXT were used just to try to avoid a potential conflict with another label OUTPUT_TEXT elsewhere in the program. Since we only care about the value of ..OUTPUT_TEXT once when we return to the original program, we can re-use it over and over again.

Finally, the macro returns to the code psect and generates the two instructions to print the string:

            .RESTORE_PSECT                                  ;* Go back to code;
            PUSHAQ  ..OUTPUT_TEXT                           ; Write the string;
            CALLS   #1,G^LIB$PUT_OUTPUT                     ; ... to SYS$OUTPUT;

### Additional Macro Tricks

Now that you can pepper your source code with OUTPUT macros, if you’re using them for debug output, you’ll probably want to disable them for the final production version of the program. You could go through and remove all of the OUTPUT lines from the source, but that’s an unnecessary hassle. By adding the appropriate .IF directive to the OUTPUT macro, you can easily include or exclude all of the output.

The simplest way is to just check to see if a symbol is defined or not at assembly time. You could do this by adding two lines to the OUTPUT macro:

            .MACRO  OUTPUT....
            .IF DEFINED DEBUG_OUTPUT        ;* Should we expand this macro?;
            .....
            .ENDC                           ;* End of .IF DEFINED;
            .ENDM   OUTPUT

To enable the output, you could just add the following line near the top of your MACRO source file:

    DEBUG_OUTPUT = 1                        ; Enable debug output

Once you were ready to produce the final version, just comment out or delete the line defining DEBUG_OUTPUT and the OUTPUT macros will never be expanded.

Another useful feature to add to the OUTPUT macro, especially if you’re using it for debug output, is the .PRINT directive. .PRINT accepts an expression and an optional comment; the value of the expression and the comment are displayed at assembly-time. A sample line that would print “Hello, world!” is:

            .PRINT  ;Hello, world!

When the program is assembled, the line would be printed to SYS$OUTPUT:

            $ MACRO TEST
            Hello, world!
            $

The expression can be any valid MACRO expression. For example, you can use symbols and the arithmetic operators:

            .PRINT  NUMBER_OF_CHARS*8       ;is the number of bytes

If you add the .IF DEFINED DEBUG_OUTPUT line to the OUTPUT macro, you might want to print a message to indicate that debug output has been enabled. Because you’d probably only want that message to be displayed once per assembly (instead of once each time the macro is used), you could use the .IIF directive to see if ..OUTPUT_TEXT has been defined yet:

            .IIF NDF, ..OUTPUT_TEXT, .PRINT ;Debug output has been enabled

If ..OUTPUT_TEXT is not defined the first time the macro is expanded, the message will be printed. For each time after that, the symbol will be defined and the message will not be printed. (Obviously, this line would be placed after the .IF DEFINED DEBUG_OUTPUT line.)

Other similarly useful directives are .WARN and .ERROR, which work the same way .PRINT does, except that they generate a warning and error, respectively. The warning and error are treated like any other MACRO warning or error generated during assembly.

### MACRO libraries

During this series, we’ve looked at a number of useful macros (ON_ERR, MOVS, MOVCX, and OUTPUT). The best way to use them (it would be rather tedious to type them in for every program that uses them) is to place them in one or more macro libraries. We’ve already discussed the two system macro libraries, STARLET.MLB and LIB.MLB, both located in SYS$LIBRARY. STARLET is automatically searched to resolve undefined macro references.

Like text, help, and object libraries, macro libraries are created with the DCL command LIBRARY. The following command would define a macro library called HGMACROS:

            $ LIBRARY/MACRO/CREATE HGMACROS

When /MACRO is specified, the default file type is .MLB, so a library HGMACROS.MLB would be created in the current default directory. To insert modules in the library, the LIBRARY/INSERT (or LIBRARY/REPLACE) command would be used:

            $ LIBRARY/MACRO/INSERT HGMACROS MACROS.MAR

The librarian will search the source .MAR file for any .MACRO directives. Any macros that are defined in the source file will be added to the macro library. If the .MAR file contains no .MACRO directives, an error message will be displayed stating so.

You’ll notice that each of the comments in the OUTPUT macro contains a semi-colon at the end of the comment, as well as the beginning:

     TEXT:  .ASCID  ~STRING~                ;* Create .ASCID string;

When the librarian inserts a macro into a library, it removes all the comments. By adding a semi-colon to the end of every comment, the librarian retains the comments (it strips everything from the last semi-colon to the end of the line, so terminating comments with the semi-colon causes it to leave everything from the first semi-colon to the second one). This is especially important when using .PRINT, .WARN, and .ERROR; if the comment is stripped from the directive, the message won’t be printed.

You can list the contents of a macro library using LIBRARY/LIST and you can delete modules using LIBRARY/DELETE=module.

There are two ways you can reference a macro library when assembling a program. The first is by specifying the library file name on the MACRO command line, using the /LIBRARY qualifier to identify it as being a library:

            $ MACRO HGMACROS/LIBRARY+TEST

Note the use of the ‘+’ concatenator instead of a comma. The ‘+’ tells the assembler to process the files as a single file; the /LIBRARY tells it that the first one is not a .MAR source file, but is a library to search.

Another, probably better, way to specify the library to search is to use the .LIBRARY directive, which should be included near the top of your .MAR source file:

            .LIBRARY        /HGMACROS.MLB/

If you want the assembler to search the LIB system library, you’d include a line like the following:

            .LIBRARY        /SYS$LIBRARY:LIB.MLB/

Up to 16 macro libraries can be specified. Libraries are searched in the reverse order in which they are specified, with STARLET being automatically searched last. Libraries specified on .LIBRARY lines are searched before libraries specified on the command line, again in reverse order.

### VMS-supplied Macros

As we’ve already covered in previous articles, the STARLET library contains macros for all the system services and error message symbols. The LIB library contains macros that are primarily of interest to systems programmers, including macros for to define symbolic offsets for data structures and macros for synchronizing access to those structures. There are a number of macros supplied in these libraries that are of interest to all MACRO programmers, whether you’re writing systems code or not.

Two STARLET macros that were added with some v5.x release of VMS that make life a lot easier for MACRO programmers are $LIB$ROUTINESDEF and $SMG$ROUTINESDEF. These macros define all of the macros for calling the LIB$ and SMG$ run-time library routines. The macros work just like the ones defined for system services, which was covered in the [April 1992 “MACRO Made Easy” article](https://hunter.goatley.com/macro-made-easy/part-v-barkeep-how-bout-some-service/). These macros let you call the run-time library routines using either CALLS or CALLG, and you can specify keywords for the arguments. For example, the following segment shows a call to LIB$SET_SYMBOL, which defines a local or global DCL symbol:

            $LIB_SET_SYMBOL_S -
                    SYMBOL  = symbol_name, -
                    VALUE_STRING = value_name, -
                    TABLE_TYPE_INDICATOR = #LIB$K_CLI_GLOBAL_SYM

Unfortunately, these macros are not documented, so the only way to determine the keywords for the parameters is by extracting the $LIB$ROUTINESDEF macro and searching for the desired macro definition inside that. The following DCL command shows how to extract that module:

            $ LIBRARY/MACRO/EXTRACT=$LIB$ROUTINESDEF-
                    /OUT=LIB_ROUTINES.MAR -
                    SYS$LIBRARY:STARLET.MLB

The system service and RTL macros call other macros to perform certain functions. Two of the most common are $PUSHADR and $PUSHTWO. $PUSHADR will push the address of a given argument, generating the correct PUSHAx instruction, and $PUSHTWO will push two longwords onto the stack. The macros make checks to determine if, for example, the two longwords to $PUSHTWO are both zero (#0) and, if so, will generate a CLRQ -(SP) instead of two PUSHL \#0 instructions.

The ASSUME macro, also defined in STARLET, accepts three parameters: an expression, a relation, and another expression. The expressions are evaluated and compared using the relation; if the result is not true, an error is generating (using .ERROR) stating that the relation is not true. For example, a very common usage of the ASSUME macro is to ensure that a certain amount of data fits on one page. If the data starts at label DATA and ends at DATA_END, the following ASSUME would verify that there are no more than 512 bytes between the two labels:

            ASSUME <DATA_END - DATA>  LE 512

If the assumption is not true, the following message is generated:

            Generated ERROR:  ***** DATA_END - DATA MUST BE LE 512 ;

The relations are the same as those for the .IF directive (GT, LE, EQ, etc.). The ASSUME macro is very useful, and it is very short—only six lines of assembler directives—no code is produced by the macro.

In the December 1991 issue, we looked at the CASE macro, which is defined in LIB.MLB. The CASE macro produces a CASEx instruction and generates the offsets automatically, based on a list that is passed in:

            CASE    R0,<zero,one,two>       ;CASEW with a base of #0

Other short, but useful, LIB macros include PUSHQ and POPQ, which produce the appropriate MOVQ instructions to push and pop a quadword to and from the stack. SETBIT will generate either a BBSS or BISB instruction to set a particular bit in a flag:

            SETBIT  #2,FLAGS                ;Set bit 2 in flags

CLRBIT will clear the bit using either BBCC or BICB, depending on the addressing mode of the value.

### NEXT TIME….

The easiest way to learn more about macros is by examining some of the macros supplied with VMS in STARLET and LIB. In particular, you can learn a lot from such macros as $LIB_KEY_TABLE and $$LIB_KEY_ENTRY.

Next issue, we’ll look at doing file I/O from MACRO using RMS.

------------------------------------------------------------------------

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

------------------------------------------------------------------------

**<span id="Program1"></span>Program 1**

    ;++
    ;
    ;  Macro:       OUTPUT
    ;
    ;  Author:      Hunter Goatley, goathunter@WKUVX1.BITNET
    ;
    ;  Functional description:
    ;
    ;       This macro will cause a string to be printed to SYS$OUTPUT by
    ;       storing the string as an ASCID string and generating a CALLS
    ;       to LIB$PUT_OUTPUT.  The ASCID strings are stored in a psect
    ;       named RO_DEBUG_DATA.
    ;
    ;  Formal parameters:
    ;
    ;       STRING          - The string to be written to SYS$OUTPUT
    ;
    ;  Sample call:
    ;
    ;       OUTPUT  <This is a debug message>
    ;
    ;--
            .MACRO  OUTPUT  STRING,?TEXT                    ;* Macro to print text;
            ;;
            ; Save the current code psect context;
            ;;
            .SAVE_PSECT LOCAL_BLOCK                         ;* Save this PSECT;
            ;;
            ;  Now switch to the data psect;
            ;;
            .PSECT  _RO_DEBUG_DATA,NOEXE,WRT,LONG,SHR       ;* Change to data PSECT;
            ;;
            ;  Align the string on a longword boundary and create it as an
            ;  ASCID string.;
            ;;
            .ALIGN  LONG                                    ;* Align on longword;
     TEXT:  .ASCID  ~STRING~                                ;* Create .ASCID string;
            ;;
            ;  Because TEXT is a local label, save the current pointer;
            ;;
            ..OUTPUT_TEXT = TEXT                            ;* Save the address;
            ;;
            ;  Now move back to the code psect and generate the CALLS to;
            ;  LIB$PUT_OUTPUT;
            ;;
            .RESTORE_PSECT                                  ;* Go back to code;
            PUSHAQ  ..OUTPUT_TEXT                           ; Write the string;
            CALLS   #1,G^LIB$PUT_OUTPUT                     ; ... to SYS$OUTPUT;
            .ENDM   OUTPUT                                  ;* End of OUTPUT macro;

