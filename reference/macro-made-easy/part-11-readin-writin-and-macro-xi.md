
# MACRO Made Easy – Part XI: Readin’, Writin’, and MACRO

## MACRO Made Easy

## Part XI: Readin’, Writin’, and MACRO

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

One of the most tedious things about writing in MACRO is trying to format output. If all you want to print are text strings, things are easy—you can just call LIB$PUT_OUTPUT or some other routine to print the string. But what happens when you have some number in a register that you’d like to print out as a decimal ASCII string? Or as a hexadecimal string? One way, though not the recommended way, is to use MACRO instructions to convert the number from one format to another.

Fortunately, there is a system service, $FAO, that can quickly become the MACRO-32 programmer’s best friend. This article walks the MACRO-32 border, because the service is certainly applicable to other languages besides MACRO-32.

### Some Historical Perspective

When I first started learning MACRO, I wrote a program called WKUMON that displayed job and process information for all the processes on the system. It was initially written so that the currently running images could be checked and has since become one of my most valued programs. Having already learned MACRO-11 but being new to MACRO-32, I was flabbergasted by the number and variety of instructions in the MACRO-32 instruction set. As I was writing WKUMON, I found that I needed to print out numbers like login dates and times, working set sizes, and priorities. Being the trouper I was, I set about figuring out how to do it.

What I found was a wealth of instructions that would convert a number from, say, hexadecimal to packed decimal. This packed decimal form could then be processed by the EDITPC instruction to produce an ASCII string. (Yes, it’s true—I’m one of the proud, the few, the ones foolish enough to try to use the EDITPC instruction. If you’ve never used it, consider yourself lucky!) WKUMON has several subroutines that look like the following fragment:

    PGFLT_OUT:
            PUSHR   #^M<r0,r1,r2,r3,r4,r5,r6,r7>
                                            ; Save R0-R7
            CVTLP   @#PAGE_FAULTS,#6,PAGE_FAULTS
                                            ; Convert to packed for EDITPC
            EDITPC  #6,PAGE_FAULTS,PGFLT_PAT,(R11)
                                            ; Edit the string to suppress Leading 0
            ADDL2   #8,R11                  ; Bump OUTBUF pointer
                                            ;
            POPR    #^M<r0,r1,r2,r3,r4,r5,r6,r7> ; Save R0-R7
            RSB                             ; Return to calling routine

At label PGFLT_PAT are the following macros:

    PGFLT_PAT:                              ; EDITPC editing pattern for page faults
            EO$ADJUST_INPUT 6               ; 6 digits
            EO$MOVE         5               ; Move 5 digits
            EO$SET_SIGNIF                   ; Set significance (if all 0s, print 1)
            EO$MOVE         1               ; Move one
            EO$BLANK_ZERO   6               ; Suppress leading zeros
            EO$END                          ; End of editing pattern

On one hand, it’s pretty amazing that you can do this type of thing with a single instruction. On the other, you’re a glutton for punishment if you try to use it in normal user-mode programs. I won’t show you how I dealt with displaying the CPU time, though I will say it involved several CVTLF (long to float), DIVF2 (divide float), CVTFL (float to longword), CVTLP (long to packed), and CVTPS (packed decimal to numeric string). From looking at other MACRO programs, I’ve long felt that I’m really about the only person in the world who has used these instructions.

There is, of course, a good reason why most people haven’t used these instructions outside of some MACRO-32 banking application. That reason is the $FAO system service, which stands for Formatted ASCII Output. I was pretty slow—it wasn’t until a couple of months after I finished WKUMON that I discovered I took the really *long* way around….

(If you want to know more about these instructions, please see the *VAX MACRO And Instruction Set Reference* manual.)

### Formatted ASCII Output ($FAO)

The $FAO and $FAOL services do just what their names imply—they format ASCII output strings based on a control string passed to them. The difference between the two services lies in the method used to pass parameters to them. This difference will be discussed below.

The $FAO system service provides similar functionality to sprintf() in C, PUT EDIT in PL/1, and PRINT USING in BASIC. Once again, as with the RMS services, $FAO appears to have been designed specifically for MACRO and BLISS programmers, though it can of course be called from any language.

$FAO requires at least two parameters: a control string and an output buffer, both passed by descriptor address. Other parameters are the address of a word to receive the length of the formatted string and additional parameters needed by the control string. The control string is just an ASCID string with $FAO format directives embedded in it. These directives consist of an exclamation (!) followed by some two-character sequence. For example, the $FAO directive to convert a hexadecimal longword to its ASCII hexadecimal notation would be “!XL”; to convert it to octal notation would be “!OL”. Table 1 shows a list of all of the $FAO format directives.

As you can see from the table, $FAO is a very versatile system service that makes formatting output quite trivial from MACRO. $FAO control strings are usually stored as .ASCID strings in a MACRO data psect:

    FAOCTR:         .ASCID  /The system date and time is: !%D/
    FAOOUT:         .WORD   256
                    .BYTE   DSC$K_DTYPE_T
                    .BYTE   DSC$K_CLASS_S
                    .ADDRESS .+4
                    .BLKB   256

The call to $FAO might then look something like this:

            $FAO_S  CTRSTR  = FAOCTR,-      ; Format the output using FAOCTR
                    OUTBUF  = FAOOUT,-      ; The output buffer is FAOOUT
                    OUTLEN  = FAOOUT,-      ; Write the final length to FAOOUT
                    P1      = #0            ; Use the current system date/time

As with all the other system services, there are three macros provided for use with the $FAO system service: $FAO (create an argument list), $FAO_S (call SYS$FAO using CALLS), and $FAO_G (call SYS$FAO using CALLG). The $FAO macro could have been used to build the argument list:

    FAO_ARGLST:     $FAO    CTRSTR  = 10$,-         ; $FAO argument list
                            OUTBUF  = FAOOUT,-      ; The output buffer is FAOOUT
                            OUTLEN  = FAOOUT,-      ; Write final length to FAOOUT
                            P1      = 0             ; Use current system date/time
            10$:    .ASCID  /The system date and time is: !%D/

The actual call would then look like:

            $FAO_G  FAO_ARGLST                      ; Format the output

A specific date and time could have been provided by specifying the address of the quadword value as P1. This address could be stored at runtime using an instruction like the following:

            MOVAQ   BINARY_TIME,FAO_ARGLST+FAO$_P1  ; Move address to arglst
            $FAO_G  FAO_ARGLST                      ; Format the string

For each $FAO directive that expects a parameter, that value is passed as one of P1 through P20. The directives are evaluated in the string left to right; each argument passed to $FAO is used as needed by directives in the order in which they’re specified. For example, the following control list would expect 3 parameters: the length of the first string, the address of the string, and the address of a longword containing the UIC to be displayed.

            .ASCID  /Username: !AD    UIC: !%U/

If fewer than 3 parameters are given, an access violation occurs. If more than 3 are given, the extra parameters are ignored. A parameter can be re-used by using the “!-” directive, as in the following example:

            .ASCID  /Username: !AC    UIC: !%U  (!-!%I)/

This control string prints a username, the numeric UIC, and the named UIC.

    UIC_CTRSTR:     .ASCID  /Username: !AC  UIC: !%U  (!-!%I)/
    [...]
            $FAO_S  CTRSTR  = UIC_CTRSTR,-  ; The $FAO control string
                    OUTBUF  = FAOOUT,-      ; The output buffer is FAOOUT
                    OUTLEN  = FAOOUT,-      ; Write final length to FAOOUT
                    P1      = USER,-        ; ASCIC address for username
                    P2      = UIC           ; Longword holding the UIC

This call would result in the following formatted string (assuming USER and UIC have been filled in):

    Username: GOATHUNTER  UIC: [2,1]  ([GOATHUNTER])

The “!Zx”, “!Ux”, “!Ox”, “!Xx”, and “!Sx” codes let you format numeric data in a variety of formats. As indicated in [Table 1](#Table1), the “!Zx”, “!Ox”, and “!Xx” codes leave leading zeros, while “!Ux” and “!Sx” do not. The ‘x’ portion of the code indicates the size of the number to be displayed—byte, word, or long. You can use $FAO to display data like the DCL command SHOW SYMBOL does:

    $ sho sym x
      X = 29345   Hex = 000072A1  Octal = 00000071241$
    $

The macro data and code fragments needed to produce equivalent output are:

    FAOSTUFF:       $FAO    CTRSTR=10$,-            ; The control string
                            OUTLEN=FAOOUT,-         ; The output length
                            OUTBUF=FAOOUT,-         ; The buffer address
                            P1=29345                ; The number to display
            10$:    .ASCID  /  X = !SL   Hex = !-!XL  Octal = !-!OL/

    [..Code..]
            $FAO_G  FAOSTUFF                        ; Format it
            PUSHAQ  FAO_OUT                         ; And print it
            CALLS   #1,G^LIB$PUT_OUTPUT             ; ...

The “!%S” directive can be very handy for those polishing touches that make your program look nice. All too often you’ll run across a program that prints something like:

        You have 1 new messages to read.

Using “!%S”, you can let $FAO worry about whether the ‘s’ in “messages” should be printed:

    MSG:    .ASCID  /You have !UL new message!%S to read./

If the value of the parameter is 1, no ‘s’ is inserted, otherwise it is inserted.

The $FAOL system service is used when you have more than 20 directive parameters to pass to $FAO, because $FAO accepts only P1 through P20. Instead of passing the parameters in the call itself, $FAOL accepts the address of a parameter list. The list is actually an array of addresses, one for each $FAO directive. For example, the following data fragment shows how you might set up a parameter list for the given $FAO string:

    FAOCTR:         .ASCID  /Hello, !AS.  This is !AS.  What do you want?/

    FAO_PRMLST:     .ADDRESS REAL_NAME              ;$FAOL parameter list for
                    .ADDRESS ME                     ;... FAOCTR

    REAL_NAME:      .ASCID  /Gene Simmons/
    ME:             .ASCID  /The Boogeyman/

The $FAOL call would then look like:

            $FAOL_S CTRSTR = FAOCTR,-               ; Call $FAO to format the
                    OUTBUF = FAOOUT,-               ; ... string
                    OUTLEN = FAOOUT,-
                    PRMLST = FAO_PRMLST

## The MESSAGE Facility

VMS includes a utility called MESSAGE that you can use to create your own VMS-style error messages. I bring this up here because the message strings are formatted using $FAO, which means you can specify $FAO directives in your error messages. This feature lets you provide specific information in an otherwise generic error message by supplying the appropriate values for the $FAO directives.

There’s a lot more to error messages and the MESSAGE facility than I will be covering here. For more information, consult the *Message Utility* manual in the VMS programming documentation set.

### Creating the Messages

Error messages are defined in a text file that is compiled by invoking the MESSAGE compiler from DCL. This text file includes MESSAGE directives that describe the severity of the error (SUCCESS, INFORMATIONAL, WARNING, ERROR, and FATAL) and other information. The file produced by the MESSAGE compiler is an object file (.OBJ) that can be linked with a program written in any VMS language. You can also produce a separate .EXE file that actually contains the message texts, while the .OBJ file contains a pointer to the .EXE message file itself. When the program is executed, any referenced messages are found in the .EXE file instead of in memory. You can think of them as working something like shareable images in that the .EXE file can be replaced without having to relink applications linked against it. For more information about the .EXE files, please see the *Message Utility* manual.

A sample MESSAGE file can be seen in [Program 1](#Program1). This file, though quite short, does show how easy it is to create your VMS-style error messages.

The MESSAGE file starts just like a MACRO-32 program with the optional directives .TITLE and .IDENT:

            .TITLE  ACCT_MSG
            .IDENT  /01-000/

Following those, the .FACILITY directive identifies the name of the facility (the program name), the facility number to be associated with error messages, and the prefix that the codes should have:

            .FACILITY       ACCT,1/PREFIX=ACCT_

If you’re only including one message file in your program, the facility number can be any arbitrary value, though there are rules for the values outlined in the *Message Utility* manual. The prefix is the prefix for the error symbol, like “SS$” in “SS$_NORMAL”. In this case, the prefix is “ACCT_”, which will produce messages like “ACCT__ADDACCT”. The ‘_’ is used instead of ‘$’ following DEC programming guidelines, which helps separate user-defined symbols from DEC-defined symbols.

The .SEVERITY directive specifies the severity of all the messages following the directive up to the next .SEVERITY directive in the file. For example, all of the messages between the INFORMATIONAL and WARNING .SEVERITY directives are informational messages. These are identified by the “-I-” in a full message text displayed by an application, along with the facility name (ACCT):

    %ACCT-I-ADDACCT, attempting to create account ADAM, SS#: 126272727

The .SEVERITY directive accepts a keyword indicating the severity level:

            .SEVERITY       INFORMATIONAL

The error messages themselves are defined with lines like the following:

    ADDACCT         /FAO_COUNT=2

The string ADDACCT makes up the second part of the error message’s symbolic name (ACCT__ADDACCT). The string between “\<\>” is an $FAO control string that is used to format the actual text of the error message. The qualifier /FAO_COUNT=2 specifies that there are 2 $FAO parameters accepted by this string. /FAO_COUNT is optional, but specifying does allow your program to determine the number of parameters expected by calling the $GETMSG system service.

### Using the Error Messages

Once your message file has been created, you compile it with the MESSAGE compiler. The default extension for message files is .MSG. If the file above was called ACCT_MSG.MSG, the following command would produce the .OBJ file:

            $ MESSAGE ACCT_MSG

The .OBJ file is just linked with the application like any other module:

            $ LINK ACCT,ACCT_MSG

So how do you reference the error symbols from a MACRO program? The symbolic names themselves are global symbols that can be referenced as .EXTERNAL symbols from MACRO:

            .EXTERNAL ACCT__ADDACCT

You can then use them just as you would symbolic error codes like SS$_NORMAL and RMS$_FNF:

            MOVL    #ACCT__ADDACCT,R0               ;Move add account "error" to R0

Of course, if you just RETurn the value to VMS, you’ll get the error text as is: VMS doesn’t know about the parameters that should have been specified. For INFORMATIONAL and SUCCESS messages, as well as others that require $FAO parameters, you must call LIB$SIGNAL, which we discussed some last month. For example, to signal the informational message for ACCT__ADDACCT, you’d write:

            PUSHAQ  SS_NUMBER               ; Print informational message with
            PUSHAQ  USERNAME                ; ... info filled in
            PUSHL   #2                      ; 2 parameters
            PUSHL   #ACCT__ADDACCT          ; The error code
            CALLS   #4,G^LIB$SIGNAL         ; Now signal it to print it

As shown above, the resulting message printed would look like:

    %ACCT-I-ADDACCT, attempting to create account ADAM, SS#: 126272727

For more information about LIB$SIGNAL, please see the LIB$ Run-time Library manual.

Note that the .SEVERITY of an error message does affect what happens when you call LIB$SIGNAL. When a FATAL error is signalled, the program will exit to VMS unless a condition handler has been established to catch that condition. Condition handlers will be covered in a future article.

### $FAO and MESSAGE Summary

The $FAO system services and the VMS Message Utility make it very easy for MACRO-32 programmers to produce the same kind of output supported by high-level languages. In many cases, it’s even easier to call $FAO from MACRO than it is to use the built-in language constructs in other languages. Used in conjunction with the MESSAGE facility, the MACRO-32 programmer can easily produce error messages just like native VMS applications, giving your MACRO-32 a polished look.

------------------------------------------------------------------------

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

------------------------------------------------------------------------

**<span id="Table1"></span>Table 1**

    Directive  Description

    Character string insertion:

    !AC        Inserts an ASCIC string.
    !AD        Inserts a string whose length and address are passed as parameters.
    !AF        Like !AD, except all nonprintable ASCII codes are replaced with ".".
    !AS        Inserts an ASCID character string.
    !AZ        Inserts an ASCIZ character string.

    Zero-filled numeric conversion:

    !OB        Converts a byte to octal notation.
    !OW        Converts a word to octal notation.
    !OL        Converts a longword to octal notation.
    !XB        Converts a byte to hexadecimal notation.
    !XW        Converts a word to hexadecimal notation.
    !XL        Converts a longword to hexadecimal notation.
    !ZB        Converts a byte to decimal notation.
    !ZW        Converts a word to decimal notation.
    !ZL        Converts a longword to decimal notation.

    Blank-filled numeric conversion:

    !UB        Converts an unsigned byte to decimal notation.
    !UW        Converts an unsigned word to decimal notation.
    !UL        Converts an unsigned longword to decimal notation.
    !SB        Converts a signed byte to decimal notation.
    !SW        Converts a signed word to decimal notation.
    !SL        Converts a signed longword to decimal notation.

    Special formatting:

    !/         Inserts a carriage return and a line feed.
    !_         Inserts a tab.
    !^         Inserts a form feed.
    !!         Inserts an exclamation point (!).
    !%T        Converts a quadword binary time to an ASCII time.  If 0 is passed
                    in, the current system time is inserted.
    !%D        Converts a quadword binary time to an ASCII date and time string.
                    If 0 is passed in, the current system date and time is
                    inserted.
    !%I        Converts a longword integer to a named UIC in the format
                    [group-identifier,member-identifier].
    !%U        Converts a longword integer to a numeric UIC.
    !%S        Inserts an "s" if the most recently converted number is not 1.
    !n<...!>   Left-justifies and blank-fills in an n-wide field.
    !n*c       Repeats the character (c) n times.
    !n%C       Inserts a character string when the most recently evaluated
                    argument has the value n. (Multilingual)
    !%E        Inserts a character string when the value of the most recently
                    evaluated argument does not match any preceding n%C
                    directives. (Multilingual)
    !%F        Marks the end of a plurals statement.

    Argument interpretation:

    !-         Reuses the last argument.
    !+         Skips the next argument.

------------------------------------------------------------------------

**<span id="Program1"></span>Program 1**

            .TITLE  ACCT_MSG
            .IDENT  /01-000/
    !++
    !
    !  File:        ACCT_MSG.MSG
    !
    !  Author:      Hunter Goatley
    !
    !  Description:
    !
    !       Sample message file.
    !
    !  Modification history:
    !
    !       01-000          Hunter Goatley            5-MAR-1993 15:35
    !               Genesis.
    !
    !--
            .FACILITY       ACCT,1/PREFIX=ACCT_

            .SEVERITY       INFORMATIONAL
    UICFOUND        <UIC !%U located for user !AS>/FAO_COUNT=2
    ADDACCT         <attempting to create account !AS, SS#: !AS>/FAO_COUNT=2
    ACCTEXISTS      <account already exists for !AS: !AS>/FAO_COUNT=2
    RDBADDMSGU      <identifier !AS value: !%U added to rights database>

            .SEVERITY       WARNING

    PWDERR          <error hashing password for user !AS>/FAO_COUNT=1

            .SEVERITY       ERROR
    INVMAJOR        <error finding UIC for user !AS, major !AS>/FAO_COUNT=2
    GROUPLOW        <group number too low>
    DIRERR          <error creating directory !AS for user !%U>/FAO_COUNT=2
    UICIDERR        <error adding identifier !AS value: !%U to rights database>-
                    /FAO_COUNT=2

            .SEVERITY       FATAL
    NOTEMPLATE      <error reading template record !AS from UAF>/FAO_COUNT=1

            .END

