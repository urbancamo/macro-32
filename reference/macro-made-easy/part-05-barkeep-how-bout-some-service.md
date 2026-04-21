
# MACRO Made Easy – Part V: Barkeep! How ‘Bout Some Service?

## MACRO Made Easy

## Part V: Barkeep! How ‘Bout Some Service?

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

### Calling System Services

We’ve already seen that run-time library routines are usually called from MACRO using the CALLS and CALLG instructions. The VMS system services are also called with these instructions, but usually only indirectly. The default macro library, STARLET.MLB, contains macros for calling each of the system services. The macros make it very easy to specify the parameters to be passed to the services, in addition to helping with the program’s self-documentation.

There are three macros for each each system service; the suffix of each macro determines how it is to be used. Each macro is named for the system service it calls: the $ASSIGN macros relate to the SYS$ASSIGN system service, the $GETJPIW macros to SYS$GETJPIW, etc. The possible suffixes and examples of each are:

- “_S” — Uses CALLS to call the service, e.g., $ASSIGN_S
- “_G” — Uses CALLG to call the service, e.g., $ASSIGN_G
- None — Sets up the argument list for the “_G” form, e.g., $ASSIGN

The $ASSIGN system service assigns an I/O channel to a device. I’ll use that in the following examples because it nicely illustrates several points about calling the system services.

The SYS$ASSIGN system service accepts four parameters, as shown in this excerpt from the on-line help:

            $ASSIGN devnam, chan, [acmode], [mbxnam]

Of the four, only two are required: the devnam (device name) and the chan (channel). The access mode and the mailbox name are optional parameters. However, unlike the run-time library routines, the optional parameters cannot simply be omitted. The system services expect all of their arguments to be passed; optional parameters such as acmode and mbxnam are “omitted” by passing a value of 0. This is true for all the system services. Some high level languages, such as C, let you omit optional parameters; the compiler will generate the code to pass 0 for all omitted parameters. In the case of MACRO, the system service macros provide defaults for optional parameters.

### The $ASSIGN_S Example

The most common way to call system services is with the CALLS form. As I mentioned in the last issue, this isn’t necessarily the most efficient way because each parameter passed to the routine has to be pushed onto the stack before the routine is called. However, the CALLS form is often the simplest method in terms of writing the code:

    DEVICE:         .Ascid  /TXA2:/
    CHAN:           .Blkl   1
            .
            .
            .
            $ASSIGN_S -                     ; Assign a channel to the device
                    devnam = DEVICE,-       ; ...  The device name
                    chan   = CHAN           ; ...  Word to hold channel number
            BLBC    R0,ERROR                ; Branch on error

The code generated when the $ASSIGN_S macro is expanded looks like this fragment:

            CLRQ    -(SP)
            PUSHAW  CHAN
            PUSHAQ  DEVICE
            CALLS   #4,G^SYS$ASSIGN

The system service macros are keyword macros, which means that the parameters can be specified using keywords or by positional placement. The example above uses keywords; it could have been coded by specifying the parameters in their proper order:

            $ASSIGN_S -
                    DEVICE,CHAN

In both cases, acmode and mbxnam default to 0.

The Figure shows the actual definitions of all the SYS$ASSIGN macros. They were taken from STARLET.MLB, with comments that I supplied.

------------------------------------------------------------------------

    ;
    ;  Macros for SYS$ASSIGN system service.  All can be found in the default
    ;  system macro library, SYS$SYSTEM:STARLET.MLB.
    ;
    ;  $ASSIGN macro
    ;
    ;  Calls macro $ASSIGNDEF to define the parameter offset symbols and allocates
    ;  storage for the argument list.
    ;
    ;  Note that all parameters default to 0.
    ;
            .MACRO  $ASSIGN DEVNAM=0,CHAN=0,ACMODE=0,MBXNAM=0
                    $ASSIGNDEF
                    .LONG           4               ; Four arguments
                    .ADDRESS        DEVNAM          ; The device name
                    .ADDRESS        CHAN            ; Word to receive I/O channel
                    .ADDRESS        ACMODE          ; Access mode
                    .ADDRESS        MBXNAM          ; Mailbox name
            .ENDM   $ASSIGN
    ;
    ;  $ASSIGNDEF macro
    ;
    ;  Defines symbols for the offsets into the argument list for each argument
    ;  (ASSIGN$_DEVNAM = 4, ASSIGN$_CHAN = 8, etc.).  $OFFDEF is another macro.
    ;
            .MACRO  $ASSIGNDEF
                    $OFFDEF ASSIGN, <devnam,chan,acmode,mbxnam>
            .ENDM   $ASSIGNDEF
    ;
    ;  $ASSIGN_G macro
    ;
    ;  Expands to CALLG arglst,G^SYS$ASSIGN.  Note the .GLOBL, which declares
    ;  SYS$ASSIGN as a global (external) symbol.
    ;
            .MACRO  $ASSIGN_G       ARGPTR
                    .GLOBL  SYS$ASSIGN
                    CALLG   ARGPTR,G^SYS$ASSIGN
            .ENDM   $ASSIGN_G
    ;
    ;  $ASSIGN_S macro
    ;
    ;  Pushes arguments on stack and does CALLS to SYS$ASSIGN.  $ASNPUSH and
    ;  $PUSHADR are other STARLET macros that are called to push longwords and
    ;  addresses onto the stack.
    ;
            .MACRO  $ASSIGN_S DEVNAM,CHAN,ACMODE=#0,MBXNAM=0
                    .GLOBL  SYS$ASSIGN
                    $ASNPUSH MBXNAM,ACMODE
                    $PUSHADR CHAN,CONTEXT=W
                    $PUSHADR DEVNAM,CONTEXT=Q
                    CALLS   #4,G^SYS$ASSIGN
            .ENDM   $ASSIGN_S
    </devnam,chan,acmode,mbxnam>

------------------------------------------------------------------------

**Programmer’s Hint \#1:** Using the keyword method of specifying the system service parameters performs two useful functions. It helps document the program by specifying which parameter is which, and, more importantly, it shields you from any possible future changes in the parameter order.

### The $ASSIGN and $ASSIGN_G Example

The _G form of system service macro expands to call the service using a CALLG instruction. As I described last issue, the CALLG instruction accepts an argument list address as its first operand; the _G macros also expect the argument list address as a parameter.

The macro without an extension is normally used to build the argument list for a service called via CALLG. For example, the $ASSIGN_G macro calls the SYS$ASSIGN system service, while the $ASSIGN macro is used to create the argument list. The $ASSIGN macro (and similar macros for all the services) accepts all the same keyword parameters as the _S form. However, instead of generating instructions that push the arguments onto the stack, assembler directives are generated that build the argument list as data.

Continuing with examples, the following fragment should be located in a data area. It defines the argument list for a call to SYS$ASSIGN just like the $ASSIGN_S example above:

    DEVICE:         .Ascid  /TXA2:/
    CHAN:           .Blkl   1
    ;
    ;  Now build the argument list
    ;
    ASSIGN_ARGLST:  $ASSIGN -
                            devnam  = DEVICE,-
                            chan    = CHAN

Remember that an argument list consists of a longword containing the number of arguments that follow and then successive longwords for each argument. The directives created by the $ASSIGN macro above could have been coded as:

    ASSIGN_ARGLST:  .Long   4               ; 4 arguments
                    .Address DEVICE         ; The device name
                    .Address CHAN           ; Word to receive the channel number
                    .Quad   0               ; Next two default to 0

The actual call to SYS$ASSIGN could then be coded as:

            $ASSIGN_G -                     ; Assign an I/O channel to device
                    ASSIGN_ARGLST

which expands to something like:

            CALLG   ASSIGN_ARGLST,G^SYS$ASSIGN

Using the CALLG form can result in significantly faster code, because the arguments no longer have to be pushed onto the stack. This should be especially evident in loops that call something like $QIOW over and over. The SYS$QIOW system service expects twelve arguments—if $QIOW_S is used in a loop, all twelve arguments get pushed onto the stack each time. If the argument list is static, or mostly static, a tremendous savings can result from using CALLG.

**Programmer’s Hint \#2:** Use the CALLG form wherever possible to make the code more efficient and legible.

Note that the use of CALLG can result in non-recursive routines. Depending on the routines being called, argument lists may point to buffers that are to receive data from the called routine. Because CALLG argument lists are static, the same buffer would be used for each recursion through the routine. If you must write recursive (or AST-reentrant) routines, you must make sure that your argument lists point to static, read-only data areas. Otherwise, you should use CALLS and allocate storage from the stack.

Typically, the I/O channel returned by SYS$ASSIGN is used in calls to the SYS$QIO service (or to SYS$QIOW, which is synchronous—it waits for the I/O to complete before returning to the caller). A typical call using $QIOW_S to write 80 bytes starting at address BUFFER to the channel stored in CHAN would look like the following:

            $QIOW_S chan    = CHAN,-                ; Write to CHAN channel
                    func    = #IO$_WRITEVBLK,-      ; Want to write data
                    p1      = BUFFER,-              ; Starting address is BUFFER
                    p2      = #80                   ; Write out 80 bytes

Notice that IO$_WRITEVBLK and 80 are specified as literals—the ‘#’ was necessary to produce the desired effects, because those arguments are passed by value. When the $QIOW macro is used, the ‘#’ would be omitted from them because the $QIOW macro generates storage directives that assume the value specified is a literal. For example, the argument list above would be specified as:

            $QIOW   chan    = CHAN,-
                    func    = IO$_WRITEVBLK,-
                    p1      = BUFFER,-
                    p2      = 80

The directives produced for FUNC and P2 would look something like:

                    .Long   IO$_WRITEVBLK
                    ....
                    .Long   80

The SYS$QIOW system service brings up another feature of the argument list macros. The $QIOW argument CHAN is passed by value, not by reference. When using $QIOW_S, the push for the channel might look like:

            PUSHW   CHAN            ; Push the channel value

Because the CHAN value isn’t known until run-time, the value cannot be stored at assembly time by specifying CHAN to the $QIOW macro. Doing so would cause the value of the symbol CHAN to be stored as a word value:

            .WORD   CHAN            ; Not what was intended

Instead, the value must be copied to the argument list after the SYS$ASSIGN system service has assigned the channel. Initially, the $QIOW macro would probably be invoked either specifying 0 for the CHAN keyword or leaving it out so it defaults to 0. I like to include all parameters that will be used, just to make it more obvious that I will be supplying a value later. For example, the $QIOW macro would probably be invoked as:

    QIOW_ARGLST:    $QIOW   chan    = 0,-                   ; Fill in at run-time
                            func    = IO$_WRITEVBLK,-       ; Write data to channel
                            p1      = BUFFER,-
                            p2      = 80

Now, before the $QIOW_G macro can be used, the assigned channel must be copied to the argument list. Because the channel is actually the second argument to $QIOW (the event flag number is the first), the CHAN value is the third longword in the argument list:

    QIOW_ARGLST:    .Long   12              ; Number of arguments
                    .Long   0               ; Event flag number
                    .Long   0               ; Assigned I/O channel
                    ....

The channel could be stored by specifying an offset of 8 from the QIOW_ARGLST address:

            MOVZWL  CHAN,QIOW_ARGLST+8      ; Store the channel number in arglst

However, this method isn’t very readable—the ‘8’ looks like a magic number. There is a better way to specify the offset using an apparently little-known side effect of the argument list macros. In addition to generating the proper assembler directives to store the data, the macros create symbols that point to each of the arguments in the argument list. The symbol names are taken from the argument keywords, prefaced with the name of the macro, a dollar sign, and an underscore. For example, the symbolic offset for the channel is:

            QIOW$_CHAN

The channel can better be stored in the argument list by using this symbol:

            MOVZWL  CHAN,QIOW_ARGLST+QIOW$_CHAN     ; Store the channel in arglst

Now the “magic” aspects have gone away, the code is more legible, and you’ve been protected from any possible changes to the order of the arguments to the $QIOW system service. If you must fill in several arguments at run-time and you have a register to spare, you might want to place the argument list address in a register and use displacement addressing:

            MOVAL   QIOW_ARGLST,R1                  ; R1 <- arglst address
            MOVZWL  CHAN,QIOW$_CHAN(R1)             ; Store the channel
            MOVL    R0,QIOW$_P2(R1)                 ; Store length (in R0)

For large argument lists, using this form of addressing should prove to be slightly faster. The MOVAL instructions moves the address of QIOW_ARGLST into R1, while MOVZWL (MOVe Zero-extended Word to Longword) converts the channel (stored as a word) to a longword by filling the high-word with zeros (zero-extending the word).

**Programmer’s Hint \#3:** When setting up argument lists, take advantage of local labels where appropriate to help the legibility of your code. For example, many system services and run-time library routines accept an ASCII string descriptor as an argument. Many times, the string is only needed when building the argument list. For example, the $SETPRN system service changes the process name for the current process. Its sole parameter is the new process name. That string probably won’t be needed elsewhere in the program, so it could be addressed using a local label:

    SETPRN_ARGLST:  $SETPRN -
                            prcnam  = 10$
            10$:    .Ascid  /Goat Busters/

The same rules apply to local labels in data psects as in code psects. They can only be referenced between two non-local labels or within a local block. Because the MACRO assembler is a two-pass assembler, the fact that it doesn’t know about 10$ during the first pass doesn’t make any difference to the final data.

### Item Lists

Several system services expect the address of an item list. Because it is a very common data structure, let’s take a brief look at how an item list is constructed.

An item list is a series of words and longwords that describe various items of information that are to be passed to or returned from a system service. Each item descriptor in an item list consists of 12 bytes arranged as two words and two longwords:

            +-----------------------------------+ +0
            |    Item code    |      Size       |
            +-----------------------------------+ +4
            |      Address of item buffer       |
            +-----------------------------------+ +8
            |       Return length buffer        |
            +-----------------------------------+

An item list just consists of a series of item descriptors, terminated by a longword 0. The size and item code each consist of one word; the address of the item buffer can be a source or destination buffer, depending on the item code, and the return length buffer is the address of a longword which will receive the length of the data written to the destination buffer. If you don’t want to specify a return length address in an item list, just specify 0 in the longword.

One of the most commonly used services that requires an item list is $GETJPI (and its synchronous form, $GETJPIW). $GETJPI (GET Job and Process Information) returns information about processes on the system. It accepts a number of parameters, one of which is the address of the item list. Each piece of information that can be returned by $GETJPI is described by an item code that begins with JPI$_. For example, the username can be returned by specifying JPI$_USERNAME and the PID can be retrieved via the code JPI$_PID. These item codes are defined in the STARLET macro $JPIDEF.

There is no predefined macro to create item lists, but one can be easily constructed. The item list to retrieve only the username for a process would look like the following fragment:

    JPI_ITMLST:     .Word   12              ; Username buffer is 12 bytes long
                    .Word   JPI$_USERNAME   ; Want to retrieve the username
                    .Address USERNAME       ; The buffer to receive the username
                    .Address USERNAME_LEN   ; The buffer to receive the length
                    .Long   0               ; Terminating 0 longword---end of list
    USERNAME:       .Blkb   12              ; Buffer to receive the item list
    USERNAME_LEN:   .Blkl   1               ; Buffer to receive length of username

To retrieve the username of the current process, the argument list can be constructed using:

    JPI_ARGLST:     $GETJPIW -
                            itmlst  = JPI_ITMLST

Finally, the call to $GETJPIW would look like:

            $GETJPIW_G -                    ; Get the username of the current
                    JPI_ARGLST              ; ...  process

Item lists can be difficult to understand or construct when using high-level languages, but in MACRO, the item list is an almost-trivial data structure.

The macro .ITEM, shown below, can be used to build an item list. There are a number of ways such a macro could be constructed; I chose a very simple version:

            .Macro   .ITEM   buflen=4,itmcod,bufadr,retlen=0
            .Word    buflen
            .Word    itmcod
            .Address bufadr
            .Address retlen                 ; The return length defaults to 0
            .Endm   .ITEM

Note that I used a period (.) as the first character in the macro name to make it look like an assembler directive. Also, the bufsiz and retlen parameters have default values of 4 and 0, respectively. The item list above could then be built in one of two ways (positional or keyword):

    JPI_ITMLST:     .ITEM   12, JPI$_USERNAME, USERNAME, USERNAME_LEN
                    .Long   0                       ; End of list

or

    JPI_ITMLST      .ITEM   buflen  = 12,-
                            itmcod  = JPI$_USERNAME,-
                            bufadr  = USERNAME,-
                            retlen  = USERNAME_LEN
                    .Long   0                       ; End of list

Which version is better is solely dependent on the programmer; the first version is clearly easier to type, but the second provides additional information about each parameter.

Now that we have the .ITEM macro, we can write another macro that will let us create the entire item list, including the terminating longword 0. While there are a number of ways such a macro could be written, my item list macro, called ITMLST, will actually invoke .ITEM to store the data. In order to do that, ITMLST must accept a variable number of groups of .ITEM parameters and invoke .ITEM for each group. The angle brackets, \<\>, are used to create such groups in macro calls.

The actual definition of ITMLST is fairly trivial, because it uses a very powerful assembler directive, .IRP (Indefinite RePeat). The macro is shown below, followed by a discussion of how it’s invoked and how it works:

       .Macro  ITMLST  ITEMS       ;* Define the ITMLST macro
        .Irp    itmdsc,     ; Step through each group in ITEMS
        .ITEM   itmdsc          ; Pass the group to .ITEM
        .Endr               ; End of repeat group
        .Long   0           ; End of item list
        .Endm   ITMLST          ;* End of the ITMLST macro

The .IRP directive iteratively extracts items from a comma-separated list. The implication, then, is that ITEMS must be a list of .ITEM parameters separated by commas. But the .ITEM parameters must also be separated from each other by commas. To accomplish this, angle brackets, \<\>, can be used.

In MACRO statements, the angle brackets are used to show grouping, like parentheses do in high-level languages. They are frequently used to override operator precedence in arithmetic expressions, as demonstrated by the following directive:

       .Long   <3*<4+5>>       ; Multiply (4+5) by 3

Similarly, the brackets can force the .ITEM parameters into a single group:

       <12,JPI$_USERNAME,USERNAME,USERNAME_LEN>

A comma-separated list of these groups can be surrounded by an outer set of brackets to create the single parameter expected by ITMLST. The following line shows how two different item descriptors could be passed to ITMLST:

    JPI_ITMLST:
        ITMLST  <<12,JPI$USERNAME,USERNAME,USERNAME_LEN>,<4,JPI$_PID,PID>>

When ITMLST is expanded, ITEMS consists of a list of two items. The .IRP directive extracts the first item (\<12,…,USERNAME_LEN\>) and assigns it to the symbol ITMDSC. The .ITEM macro is then invoked, using ITMDSC as its argument, which really expands to the following line:

       .ITEM   12,JPI$_USERNAME,USERNAME,USERNAME_LEN

This process is repeated for each member of the ITEMS list, so the next line that is generated is:

       .ITEM   4,JPI$_PID,PID

Because there are no more list items, the assembler drops out of the .IRP-.ENDR loop and continues expanding ITMLST. The only thing left is the directive to store the longword 0 that terminates the item list.

Because .ITEM is itself a macro, the actual code generated by the expanded macros will look something like this:

    JPI_ITMLST:    .Word   12
            .Word   JPI$_USERNAME
            .Address USERNAME
            .Address USERNAME_LEN
            .Word   4
            .Word   JPI$_PID
            .Address PID
            .Address 0
            .Long   0

As I stated earlier, I like to specify the macro argument keywords when calling a macro to shield myself from possible changes in the argument order. Because each member of the ITMLST parameter gets passed to the .ITEM macro, we can specify the .ITEM parameter keywords. This macro call shows how the keywords would be given:

    JPI_ITMLST:    ITMLST  <-
                ,-
                -
                >

Note that I used the continuation character to spread the macro call over multiple lines to make it easier to read. Again, keyword usage is often a matter of taste, as it does require more typing. However, I find the results well worth the effort.

### Another Method for Calling Run-Time Library Routines

We saw last issue that the run-time library routines are called via CALLS or CALLG instructions. For efficiency, some routines can also be invoked via a second entry point using a JSB (Jump SuBroutine) instruction. The manual entry for each RTL routine will indicate whether or not the routine can be invoked with JSB. Note that the JSB interface is only available from MACRO and BLISS, because high-level languages don’t provide direct support for the JSB instruction.

Additional information about the JSB interface can be found in the VMS manuals entitled *Introduction to the VMS Run-Time Library* and *VMS RTL String Manipulation (STR$) Manual*.

Virtually all of the RTL routines that provide a JSB entry point deal with dynamic strings. The Table lists all of the STR$ routines that can be invoked with a JSB. The only OTS$ and LIB$ routines that support JSBs are the OTS$ and LIB$ versions of some of the STR$ routines. The MTH$ routines also provide a number of JSB entry points.

**STR$ Routines that Provide JSB Entry Points**

<table data-cellspacing="5">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr>
<th style="text-align: left;">STR$ RTL Routine</th>
<th style="text-align: left;">JSB Entry Point</th>
<th style="text-align: left;">Description</th>
</tr>
&#10;<tr>
<td colspan="3" style="text-align: left;"><hr /></td>
</tr>
<tr>
<td style="text-align: left;">STR$ANALYZE_SDESC</td>
<td style="text-align: left;">STR$ANALYZE_SDESC_R1</td>
<td style="text-align: left;">Analyze String Descriptor</td>
</tr>
<tr>
<td style="text-align: left;">STR$COPY_DX</td>
<td style="text-align: left;">STR$COPY_DX_R8</td>
<td style="text-align: left;">Copy a Source String Passed by Descriptor to a Destination String</td>
</tr>
<tr>
<td style="text-align: left;">STR$COPY_R</td>
<td style="text-align: left;">STR$COPY_R_R8</td>
<td style="text-align: left;">Copy a Source String Passed by Reference to a Destination String</td>
</tr>
<tr>
<td style="text-align: left;">STR$DUPL_CHAR</td>
<td style="text-align: left;">STR$DUPL_CHAR_R8</td>
<td style="text-align: left;">Duplicate Character n Times</td>
</tr>
<tr>
<td style="text-align: left;">STR$FREE1_DX</td>
<td style="text-align: left;">STR$FREE1_DX_R4</td>
<td style="text-align: left;">Deallocate One Dynamic String</td>
</tr>
<tr>
<td style="text-align: left;">STR$GET1_DX</td>
<td style="text-align: left;">STR$GET1_DX_R4</td>
<td style="text-align: left;">Allocate One Dynamic String</td>
</tr>
<tr>
<td style="text-align: left;">STR$LEFT</td>
<td style="text-align: left;">STR$LEFT_R8</td>
<td style="text-align: left;">Extract a Substring of a String</td>
</tr>
<tr>
<td style="text-align: left;">STR$LEN_EXTR</td>
<td style="text-align: left;">STR$LEN_EXTR_R8</td>
<td style="text-align: left;">Extract a Substring of a String</td>
</tr>
<tr>
<td style="text-align: left;">STR$POSITION</td>
<td style="text-align: left;">STR$POSITION_R6</td>
<td style="text-align: left;">Return Relative Position of Substring</td>
</tr>
<tr>
<td style="text-align: left;">STR$POS_EXTR</td>
<td style="text-align: left;">STR$POS_EXTR_R8</td>
<td style="text-align: left;">Extract a Substring of a String</td>
</tr>
<tr>
<td style="text-align: left;">STR$REPLACE</td>
<td style="text-align: left;">STR$REPLACE_R8</td>
<td style="text-align: left;">Replace a Substring</td>
</tr>
<tr>
<td style="text-align: left;">STR$RIGHT</td>
<td style="text-align: left;">STR$RIGHT_R8</td>
<td style="text-align: left;">Extract a Substring of a String</td>
</tr>
</tbody>
</table>

 

When the JSB entry point is used, input and output parameters are passed to the routine in registers instead of through an argument list. The JSB entry point name includes a suffix that denotes the highest register that will be accessed or modified. All registers from R0 to the register indicated in the routine name can be used by the RTL routine. As the VAX Calling Standard dictates, you should always assume that R0 and R1 are modified.

For example, the routine STR$ANALYZE_SDESC, which analyzes string descriptors, has a JSB entry point named STR$ANALYZE_SDESC_R1. The R1 suffix indicates that R1 is the highest register that will be modified. Similarly the JSB entry point STR$COPY_DX_R8 will modify R0 through R8.

Parameters are passed in the same order as they are specified with the CALL interface by placing the first parameter in R0, the second in R1, and so on. The manual entry for each routine should be consulted to ensure that the parameters are passed via the appropriate mechanism (by reference or by value). In general, the parameters are passed the same way for both interfaces.

Routines that return values in parameters are exceptions to the ordering of parameters. For example, STR$ANALYZE_SDESC normally accepts three parameters:

- The address of the input descriptor to analyze
- The address of a word to receive the integer length of the string
- The address of a longword to receive the address of the string

When a JSB is used to invoke STR$ANALYZE_SDESC_R1, only one parameter is passed in a register: R0 holds the address of the input descriptor. The output parameters are returned in R0 and R1, as indicated by the suffix R1. The output parameters are always returned in their respective order, starting with either R0, R1, or R2, depending on whether or not the routine returns a condition value in R0.

The following example shows a sample call to STR$ANALYZE_SDESC_R1:

    BUFFER:         .Ascid  /This is a sample descriptor to analyze./
    [...]
            MOVAQ   BUFFER,R0               ; Move descriptor addr to R0
            JSB     G^STR$ANALYZE_SDESC_R1  ; Call STR$ routine to analyze it
    ;
    ; After JSB, R0 has the string's length and R1 has its address
    ;

Whichever method is used for calling RTL routines, general addressing (G^) should always be used so that the linker and the image activator can find the routine in the shareable image.

### NEXT TIME….

Next issue, we’ll take a closer look at the differences between the synchronous and asynchronous system services and how you can use them to your advantage. Also, now that we’ve covered the basics of looping and calling other routines and system services, it’s time to look at some of the benefits of the powerful VAX instruction set. We’ll start by taking a look at the extensive support for character manipulations and examining the best ways for moving data around.

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

