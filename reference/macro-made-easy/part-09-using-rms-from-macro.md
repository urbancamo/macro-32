
# MACRO Made Easy – Part IX: Readin’, Writin’, and MACRO: Using RMS from MACRO

## MACRO Made Easy

Part IX: Readin’, Writin’, and MACRO:\
Using RMS from MACRO
--------------------------------------

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

In the October issue, MACRO macros were discussed. One thing that I should have mentioned but forgot to was to be careful when using macros that accept parameters. Most of these macros are case-sensitive with regard to the parameters. For example, the BUG_CHECK macro accepts a parameter TYPE that tells whether or not a fatal bugcheck is to be generated. The TYPE allowed is “FATAL”, which must be specified as all uppercase letters because the routine uses .IF to determine the type:

            .IF IDN ,

If “fatal” were specified, the check would fail because “fatal” is not identical to “FATAL”. The MACRO-32 assembler (and compiler under OpenVMS AXP) is not case-sensitive, but some of the system macros are. (Thanks to Brian Schenkenberger for pointing out this omission from the previous article in this series).

### File I/O & MACRO

Unlike most high-level languages, MACRO-32 does not provide any built-in file I/O functions. Instead, the MACRO-32 programmer must use RMS (Record Management Services) to create, read from, and write to files. High-level languages usually provide the ability to manipulate files using built-in functions like OPEN, CLOSE, READ, etc. All of the VMS high-level languages actually do the work by calling RMS, which in turn issues the proper $QIO calls to actually read and write the disk files.

Most beginning MACRO programmers are intimidated by the thought of using RMS—indeed, it is more cumbersome to use than most high-level file functions are. However, RMS is actually pretty trivial to use, especially from MACRO. As more and more programs are written in C for VMS, programmers are discovering that they must also use RMS instead of C’s built-in file functions if they want to create files with special RMS attributes, such as indexed files. Calling RMS from C is quite a bit more cumbersome than it is from MACRO.

There are a number of RMS routines that are called just like VMS system services are called. In fact, there are macros defined to call the RMS routines just like the system services. The most common RMS routines are $OPEN, $CLOSE, $CONNECT, $PUT, and $GET. Table 1 shows all of the RMS routines and the major RMS macros used in conjunction with RMS calls. All of the RMS macros can be found in the default system macro library, SYS$LIBRARY:LIB.MLB.

**Record Management Services**

|              |                                             |
|--------------|---------------------------------------------|
| $CLOSE      | Close a file                                |
| $CONNECT    | Connect a RAB to a file                     |
| $CREATE     | Create a file                               |
| $DELETE     | Delete a record in a file                   |
| $DISCONNECT | Disconnect a RAB from a file                |
| $DISPLAY    | Get file attribute information              |
| $ENTER      | Enter a file name into a directory          |
| $ERASE      | Delete a file and its directory entry       |
| $EXTEND     | Extend a file’s size (allocate more blocks) |
| $FIND       | Find a particular record in a file          |
| $FLUSH      | Flush all RMS buffers to disk               |
| $FREE       | Unlock all locked records                   |
| $GET        | Get a record from a file                    |
| $NXTVOL     | Process next tape volume                    |
| $OPEN       | Open a file                                 |
| $PARSE      | Parse a filename                            |
| $PUT        | Write a record to a file                    |
| $READ       | Read a block from a file (block I/O)        |
| $RELEASE    | Unlock the current record                   |
| $REMOVE     | Remove a file’s directory entry             |
| $RENAME     | Rename a file                               |
| $REWIND     | Position file pointer to first record       |
| $SEARCH     | Search for one or more files                |
| $SPACE      | Move forward or backward X blocks           |
| $TRUNCATE   | Remove records from the end of a file       |
| $UPDATE     | Update a record in an indexed file          |
| $WAIT       | Wait for asynchronous RMS I/O               |
| $WRITE      | Write a block to a file (block I/O)         |

**Storage macros**

|          |                                        |
|----------|----------------------------------------|
| $FAB    | Define a File Access Block             |
| $RAB    | Define a Record Access Block           |
| $NAM    | Define a NAM block for name processing |
| $XABALL | Controls disk space allocation         |
| $XABDAT | Provides file date information         |
| $XABFHC | Provides file header information       |
| $XABJNL | Provides journaling information        |
| $XABKEY | Provides additional key information    |
| $XABPRO | Provides control over file protection  |
| $XABRDT | Provides revision-date information     |
| $XABSUM | Provides summary information           |
| $XABTRM | Controls RMS terminal I/O              |

 

The RMS routines use several data structures to describe files and I/O streams for those files. The primary structures are the FAB (File Access Block) and the RAB (Record Access Block). The FAB describes the file—the attributes, the organization (sequential, indexed, relative), the file name, etc. The RAB describes the various record options that are in effect when the file is read or written. The programmer is responsible for initializing the FAB and RAB; when the RMS routines are called, the addresses of the FABs and RABs are passed appropriately. The RMS routines then update the structures to reflect such things as the position in the file, whether or not it’s open, etc.

Additional structures that won’t be discussed in this issue are the NAM block, used for name processing, and the XABs (eXtended Attribute Blocks). These structures will be covered in the next issue.

[Program 1](#Program1) shows a full MACRO program that implements a no-frills TYPE program. It will be referenced in the sections below. The rest of this article will describe how the RMS routines are called from MACRO, but it is not designed to be a full-fledged tutorial on using RMS. For more information on RMS, please consult the RMS reference manual in the VMS documentation set. Most of the examples in that manual are written in MACRO-32.

### The RMS Macros

There are three macros defined for each type of RMS data structure:

- $xxx — allocates storage for and initializes the structure
- $xxxDEF — defines the symbolic offsets into the structure
- $xxx_STORE — produces instructions to store values in the structure

For example, the macros $FAB, $FABDEF, and $FAB_STORE are defined for FABs. The $xxxDEF macros should be specified at the top of a program to define all the symbolic offsets that are to be used. The $xxx (like $FAB) macro is used in a data psect to allocate and initialize storage for the structure. The $xxx_STORE macros can be used in code psects to produce the necessary instructions to initialize fields in the structure. The programmer can also use the symbolic offsets to initialize those fields. This is discussed in more detail below. The symbolic offsets are named following normal VMS conventions; for example, FAB$L_FNA is the offset to the address of the file name in a FAB.

Another macro that should be included in programs calling RMS is $RMSDEF, which defines all the symbols for status conditions returned by the RMS routines. Such symbols include RMS$_NORMAL (normal success status from RMS), RMS$_EOF (end-of-file detected), RMS$_FNF (file not found), etc.

The following lines were taken from TYPE.MAR (Program 1):

            $DSCDEF                                 ; Descriptor symbols
            $SSDEF                                  ; System service status symbols
            $FABDEF                                 ; Define FAB symbols
            $RABDEF                                 ; Define RAB symbols
            $RMSDEF                                 ; RMS status symbols

The MACRO-32 assembler (and compiler) will automatically find the FAB and RAB symbols when it searches the default system macro library, but it’s still a good idea to specifically reference the definition macros.

### Building a FAB to Open a File for Reading

Before a file can be opened using the $OPEN RMS routine, a FAB must be constructed that describes that file. In MACRO, this FAB is created using the $FAB macro. The $FAB macro actually reserves space for the FAB structure; it only produces storage directives that contain specified values. As such, it should be placed in a writable data psect in your program. The psect must be writable because RMS will update certain fields in the FAB when the file is opened.

The $FAB accepts a large number of parameters, each of which is used to provide initial values for the FAB fields. The parameters are usually named by keywords instead of just given as positional parameters. For example, the TYPE program includes the following FAB:

            .PSECT  _TYPE_DATA,NOEXE,WRT,LONG,SHR

    INPUT_FAB:      $FAB    DNM=<SYS$DISK:[].LIS>,- ; The default name
                            FAC=GET,-               ; Want to GET from file
                            SHR=<GET,PUT>           ; Let others access it

NOTE: FABs and RABs *must* be aligned on longword boundaries. The PSECT that contains them should specify LONG as one of its attributes, though it is not absolutely necessary if all FABs and RABs are grouped together at the beginning of a psect. It never hurts to include .ALIGN LONG directives to ensure that the structures are properly aligned (if they’re not, the MACRO-32 assembler/compiler will complain).

The $FAB definition above specifies three parameters:

- DFN — Default File Name
- FAC — File ACcess
- SHR — Share options to allow others to access file

In this particular program, a default file spec of SYS$DISK:\[\].LIS is supplied. The file name is read using LIB$GET_FOREIGN; by supplying a default file name, the running user can omit some of the fields in the file specification.

The name of the file could be hardcoded in the FAB using the FNM parameter:

            $FAB    FNM=<WKU$ROOT:[DATA]THE_FILE.LOG>

Both DNM and FNM are recognized by the $FAB macro, even though there are no such fields in the FAB structure. The actual fields in the FAB are FAB$L_FNA (File Name Address), FAB$B_FNS (File Name Size), FAB$L_DNA (Default Name Address), and FAB$B_DNS (Default Name Size). The $FAB macro stores the specified DNM and FNM strings outside the FAB itself and initializes the appropriate FNA and FNS fields.

The FAC parameter specifies the types of access that are to be allowed on the file. By specifying FAC=GET, we’re telling RMS that the file is being opened for read-only access; the program will not be allowed to write to the file. Other options that can be specified include PUT (write access), DEL (delete access), UPD (update access), and BIO (block I/O). Each option corresponds to a bit in the FAB field FAB$B_FAC. The symbolic names are FAB$V_GET, FAB$V_PUT, etc. As you can see, using the $FAB macro eliminates having to specify the full names for the bits.

Similarly, the SHR option describes other simultaneous access that is allowed while this program has the file open. The names given set bits in the FAB$B_SHR field; those given above allow other programs to read and write to the file while TYPE has it open. Because a list of options was specified, they had to be included between angle brackets (\<\>) so that the MACRO-32 assembler/compiler would treat them as a value to SHR and not as separate positional parameters to the $FAB macro.

There are, of course, many other options that could be specified in the FAB. For example, we could specify the organization (the default is ORG=SEQ, for sequential file), record format (default is RFM=VAR, for varying length records, the record attributes, etc. When creating a FAB for an output file, more $FAB parameters should be specified; since TYPE will be opening an existing file, there’s no need to specify them.

### Modifying a FAB

Not all FAB fields are necessarily known at assembly-time; for example, in the TYPE program, the filename is not known until run-time, when the user specifies the file to be typed. In cases like this, the fields must be initialized on-the-fly. This can be done by using the $xxx_STORE macro and by using the symbolic offsets.

The $xxx_STORE macro lets you specify the fields and values much as they’re specified when the $FAB macro is given. For example, the following $FAB_STORE invocation performs some of the same initializations as the $FAB macro above:

    INPUT_FAB:      $FAB    DNM=<SYS$DISK:[].LIS>
            .
            .
            .
            .ENTRY  CODE,^M<>
            .
            .
            .
            $FAB_STORE -                            ; Modify the FAB
                    FAB = INPUT_FAB,-               ; ... The FAB address
                    FAC = GET,-                     ; ... The FAC bits
                    SHR = <get,put>                 ; ... The SHR bits

The $FAB_STORE macro produces instructions that reference the FAB using the symbolic offsets. The programmer can choose not to use $FAB_STORE and just write the instructions. The following code shows how the symbolic offsets would be used; the code generated by $FAB_STORE would look almost identical to this code:

            MOVAL   INPUT_FAB,R2                    ; R2 -> FAB for efficiency
            MOVB    #FAB$M_GET,FAB$B_FAC(R2)        ; FAC = GET
            MOVB    #<FAB$M_SHRGET!FAB$M_SHRPUT>,-  ; SHR = <GET,PUT>
                    FAB$B_SHR(R2)                   ; ...

In TYPE, the name of the file is read using LIB$GET_FOREIGN. The address of the name string and its length are then copied to the FAB using $FAB_STORE:

            MOVAQ   FILENAME,R1                     ; R1 -> filename descriptor
            MOVAL   INPUT_FAB,R2                    ; Move FAB address to R2

            $FAB_STORE -                            ; Store the necessary FAB info
                    FAB     = (R2),-                ; ...  The FAB address
                    FNA     = @DSC$A_POINTER(R1),-  ; ...  The filename address
                    FNS     = DSC$W_LENGTH(R1)      ; ...  The filename length

Similarly, the $FAB_STORE could have been replaced by lines like the following:

            MOVL    DSC$A_POINTER(R1),FAB$L_FNA(R2) ; Let FAB point to filename
            MOVB    DSC$W_LENGTH(R1),FAB$B_FNS(R2)  ; Store the size in FAB

While using registers to point to the FAB structure is more efficient, the symbolic offsets can also be added to the address. For example:

            MOVL    DSC$A_POINTER(R1),INPUT_FAB+FAB$L_FNA
            MOVB    DSC$W_LENGTH(R1),INPUT_FAB+FAB$B_FNS

### Opening the File

A file is actually opened by calling the $OPEN service, passing it the address of the FAB:

            $OPEN   FAB=INPUT_FAB                   ; Try to open the file

The $OPEN system service returns a status in R0 indicating whether or not the open was successful. If the file was opened, the value returned is RMS$_NORMAL. If the specified file did not exist, the value RMS$_FNF (file not found) would be returned in R0. (There is actually additional status information that is returned. The additional information will be discussed in the next issue.)

All of the RMS routines accept two other parameters, ERR and SUC. These optional parameters are the addresses of routines that are called in the event of an error or success, respectively. Though rarely used, they do provide the programmer with the ability to call a special routine based on the status of the call. The routine is specified like any other parameter:

            $OPEN   FAB=INPUT_FAB,ERR=OPEN_ERROR_HANDLER

### Building the RAB to Read a File

Now that the file has been opened, a RAB (Record Access Block) must be “connected” to a FAB to establish a record stream. This stream determines how the records in the file are actually accessed. The RAB is associated with the FAB by calling the $CONNECT service.

The RAB includes a pointer to the FAB, the type of access that is to be performed (sequential or indexed), the addresses and sizes of user buffers that hold the records read and written, the address, size, and position of keys in indexed reads and writes, and more. The following $RAB definition is from TYPE:

    INPUT_RAB:      $RAB    FAB=INPUT_FAB,-         ; Point to FAB
                            RAC=SEQ,-               ; Sequential access
                            UBF=BUFFER,-            ; Input buffer addr
                            USZ=512                 ; Size of input buffer

When a RAB is used for input, the RAB fields RAB$L_UBF and RAB$W_USZ must describe the user buffer into which a record is read. The buffer must be large enough to hold the largest record in the file.

The $CONNECT service expects the address of the RAB to be passed in. Note that the $CONNECT can only be called *after* a successful call to $OPEN. If the file is not already open, the connect will fail.

            MOVAL   INPUT_RAB,R3                    ; Move RAB address to R3
            $CONNECT -                              ; Connect the RAB to the file
                    RAB=(R3)                        ; ...
            BLBC    R0,20$                          ; Branch on error

As with the FAB, the RAB can be modified using either the $RAB_STORE macro or by using the symbolic offsets directly. For example, a user buffer could be allocated dynamically by calling LIB$GET_VM; the address and size of the allocated buffer could then be stored in the RAB:

            PUSHAL  RAB_ADDRESS                     ; Allocate 512 bytes
            PUSHAL  RAB_SIZE                        ; ...
            CALLS   #2,G^LIB$GET_VM                 ; ...
            BLBC    R0,40$                          ; Branch on error
            MOVW    RAB_SIZE,RAB$W_USZ(R3)          ; Store the size
            MOVL    RAB_ADDRESS,RAB$L_UBF(R3)       ; Store the address

Once $CONNECTed, the RAB address is passed as a parameter to the record I/O routines like $GET, $PUT, $FIND, and $DELETE.

If the FAB for a file specifies the MSE (Multi-Stream Environment) bit in the SHR field, more than one RAB can be connected to a single FAB. This lets a program maintain multiple pointers into a file and read and write from the file in multiple ways. For example, a RAB for sequential access and a RAB for indexed access can both be $CONNECTed to the FAB. The program can then call $GET with one RAB to read sequentially and call $GET with the other RAB to perform an indexed read.

In fact, a program can also use the same RAB for both sequential and indexed reads by simply changing the RAB$B_RAC field at run-time. Of course, for indexed reads, the key fields (RAB$L_KBF, RAB$B_KSZ) must be properly initialized. Indexed files will be discussed in the next issue.

### Reading From a File

Once the file has been opened and a RAB successfully connected, the program can read records from the file by calling the $GET service. The address of the RAB is passed to it:

            $GET    RAB=(R3)                        ; Read a record from the file

Usually, records are read and processed until there are no more records in the file. The TYPE program demonstrates the loop that is used to read records until end-of-file is returned:

            PUSHL   #SS$_NORMAL                     ; Push "normal" status on stack

     10$:   $GET    RAB=(R3)                        ; Read a record from the file
            CMPL    #RMS$_EOF,R0                    ; Was EOF returned?
            BEQLU   30$                             ; Branch if so
            BLBC    R0,20$                          ; Branch on any other error
            MOVW    RAB$W_RSZ(R3),DSC$W_LENGTH(R4)  ; Copy length to descriptor
            MOVL    RAB$L_RBF(R3),DSC$A_POINTER(R4) ; Copy address to descriptor
            PUSHAQ  (R4)                            ; Print the buffer to SYS$OUTPUT
            CALLS   #1,G^LIB$PUT_OUTPUT             ; ...
            BRB     10$                             ; Loop until EOF

     20$:   MOVL    R0,(SP)                         ; Replace "normal" with error
     30$:   $CLOSE  FAB=(R2)                        ; Close the file
            POPL    R0                              ; Restore saved status

Notice that R0 is compared with the RMS status RMS$_EOF to determine whether or not end-of-file has been reached. If so, the program branches to close the file and exit. If R0 does not contain RMS$_EOF, a standard BLBC is used to branch in case any other error occurred. If the read was successful, the record read is written to SYS$OUTPUT by calling LIB$PUT_OUTPUT.

When $GET is called, the record read is copied into the specified user buffer, whose address is stored in RAB$L_UBF. $GET then copies the address of that buffer to RAB$L_RBF and the length of the record read into RAB$W_RSZ. TYPE copies the length and address to a static string descriptor that is passed to LIB$PUT_OUTPUT.

### Closing the File

The $CLOSE service is called to close the open file. The RABs can be disconnected by calling the $DISCONNECT service; if they’re not disconnected, $CLOSE will automatically disconnect them before closing the file. In this program, even the $CLOSE is not explicitly needed, because the file will be closed by the VMS image rundown routines. Still, it’s good practice to include the call. For completeness, the call to $DISCONNECT would look like:

            $DISCONNECT -                   ; Disconnect the RAB from the file
                    RAB=INPUT_RAB           ; ...

Note that a status of SS$_NORMAL is pushed onto the stack before the loop above is entered. The status is used as the final exit status when EOF is detected on the file. If some other error occurs, the error branch to 20$ is taken and the status is copied from R0 to the stack, replacing the SS$_NORMAL that was placed there. The $CLOSE service is called, and then the saved status is moved back into R0. This trick lets the program call $CLOSE without obliterating an error status that caused the abnormal termination. If the program runs until EOF is encountered, the code branches to 30$, skipping the save of R0; when the final code is popped back into R0, it’ll be SS$_NORMAL value, not RMS$_EOF.

### Writing to a File

The $PUT service is called to write a record to a file. Like $GET, it expects the address of a RAB to be passed to it. The record that is written to the file is accessed via the RAB$L_RBF and RAB$W_RSZ fields. If the $PUT is to an indexed file, the appropriate key buffer will also have be initialized properly. Once again, indexed files will be discussed in the next issue.

### RMS Block I/O

The $READ and $WRITE services are called to perform block I/O on a file. In block I/O, the file is read a block at a time instead of a record at a time. Block I/O can be much faster when copying the contents of one file to another file. [Program 2](#Program2) shows a callable routine called COPY_FILE that can be used to copy a file. It demonstrates block I/O using $READ and $WRITE, as well as how the FABs and RABs are initialized on-the-fly. Each call to $READ causes as many as 127 blocks of the source file to be read into the buffer; the contents of that buffer are then written to the new file using $WRITE. If COPY_FILE had been written using record I/O, the routine would have been much more complex. And by reading multiple blocks with each $READ, the file is copied more quickly.

COPY_FILE can be called from any language; the input and output files are passed as parameters. The new file is created by calling the $CREATE service, passing in the address of the FAB that fully describes the file to be created.

[Program 3](https://hunter.goatley.com/macro-made-easy/part-ix-readin-writin-and-macro-using-rms-from-macro/Program3) shows a very simple C program that calls COPY_FILE.

### NEXT TIME….

Next issue, we’ll continue our look at RMS file I/O from MACRO.

------------------------------------------------------------------------

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

------------------------------------------------------------------------

**<span id="Program1"></span>Program 1**

            .TITLE  TYPE
            .IDENT  /01-000/
    ;++
    ;
    ;  Facility:    TYPE
    ;
    ;  Author:      Hunter Goatley
    ;               goathunter@WKUVX1.BITNET
    ;
    ;  Date:        November 15, 1992
    ;
    ;  Abstract:
    ;
    ;       This program is a no-frills version of TYPE that shows
    ;       some simple RMS calls to read a file.
    ;
    ;  Modified by:
    ;
    ;       01-000          Hunter Goatley          15-NOV-1992 12:12
    ;               Original version.
    ;
    ;--

            .DSABL  GLOBAL                          ; Declare external references
            .ENABL  SUPPRESSION                     ; Don't list unreference symbols
            .NOSHOW BINARY                          ; Include binary in listings
    ;
    ;  External routines:
    ;
            .EXTRN  LIB$GET_FOREIGN                 ; Get foreign command line
            .EXTRN  LIB$PUT_OUTPUT                  ; Write to SYS$OUTPUT

            $DSCDEF                                 ; Descriptor symbols
            $SSDEF                                  ; System service status symbols
            $FABDEF                                 ; Define FAB symbols
            $RABDEF                                 ; Define RAB symbols
            $RMSDEF                                 ; RMS status symbols

            .SHOW   BINARY                          ; Include binary in listings
    
            .PSECT  _TYPE_DATA,NOEXE,WRT,LONG,SHR

    INPUT_FAB:      $FAB    DNM=<SYS$DISK:[].LIS>,- ; The default name
                            FAC=GET,-               ; Want to GET from file
                            SHR=<GET,PUT>           ; Let others access it

    INPUT_RAB:      $RAB    FAB=INPUT_FAB,-         ; Point to FAB
                            RAC=SEQ,-               ; Sequential access
                            UBF=BUFFER,-            ; Input buffer addr
                            USZ=512                 ; Size of input buffer

    BUFFER:         .BLKB   512                     ; Decent-sized buffer

                    .ALIGN  LONG                    ; Align on longword boundary
    GET_FOREIGN_ARGS:                               ; LIB$GET_FOREIGN arglst
                    .LONG   3                       ; ... 3 arguments
                    .ADDRESS FILENAME               ; ... The input buffer
                    .ADDRESS 10$                    ; ... The prompt
                    .ADDRESS FILENAME               ; ... Word to receive length
            10$:    .ASCID  /_File: /               ; Foreign command prompt

    FILENAME:       .WORD   0                       ; Dynamic descriptor for string
                    .BYTE   DSC$K_DTYPE_T           ; ... Text string
                    .BYTE   DSC$K_CLASS_D           ; ... Dynamic string
                    .LONG   0                       ; ... Address filled in later

    OUTBUFF_D:      .WORD   0                       ; Static descriptor for string
                    .BYTE   DSC$K_DTYPE_T           ; ... Text string
                    .BYTE   DSC$K_CLASS_S           ; ... Static string
                    .LONG   0                       ; ... Address filled in later

    
            .PSECT  _TYPE_CODE,EXE,NOWRT,LONG,PIC,SHR
            .ENTRY  TYPE,^M<R2,R3,R4,R5,R6,R7,R8,R9,R10,R11>
    ;
    ;  Call LIB$GET_FOREIGN to get the filename
    ;
            CALLG   GET_FOREIGN_ARGS,-              ; Get the filename to TYPE
                    G^LIB$GET_FOREIGN               ; ...
            BLBC    R0,40$                          ; Branch on error

    ;
    ;  See if a filename was even given.
    ;
            MOVAQ   FILENAME,R1                     ; R1 -> filename descriptor

            MOVL    #SS$_NORMAL,R0                  ; Assume normal status
            TSTW    DSC$W_LENGTH(R1)                ; Was there a length?
            BEQLU   40$                             ; If no filename, just exit

    ;
    ;  Now make the FAB point to the filename using $FAB_STORE.  The FAB and
    ;  RAB addresses are copied to registers for efficiency.
    ;
            MOVAL   INPUT_FAB,R2                    ; Move FAB address to R2
            MOVAL   INPUT_RAB,R3                    ; Move RAB address to R3

            $FAB_STORE -                            ; Store the necessary FAB info
                    FAB     = (R2),-                ; ...  The FAB address
                    FNA     = @DSC$A_POINTER(R1),-  ; ...  The filename address
                    FNS     = DSC$W_LENGTH(R1)      ; ...  The filename length
    ;
    ;  Now open the file using $OPEN
    ;
            $OPEN   FAB=(R2)                        ; Try to open the file
            BLBC    R0,40$                          ; Branch on error
    ;
    ;  Now connect the RAB to the open file
    ;
            $CONNECT -                              ; Connect the RAB to the file
                    RAB=(R3)                        ; ...
            BLBC    R0,20$                          ; Branch on error

            MOVAQ   OUTBUFF_D,R4                    ; R4 -> output descriptor
            PUSHL   #SS$_NORMAL                     ; Push "normal" status on stack

     10$:   $GET    RAB=(R3)                        ; Read a record from the file
            CMPL    #RMS$_EOF,R0                    ; Was EOF returned?
            BEQLU   30$                             ; Branch if so
            BLBC    R0,20$                          ; Branch on any other error
            MOVW    RAB$W_RSZ(R3),DSC$W_LENGTH(R4)  ; Copy length to descriptor
            MOVL    RAB$L_RBF(R3),DSC$A_POINTER(R4) ; Copy address to descriptor
            PUSHAQ  (R4)                            ; Print the buffer to SYS$OUTPUT
            CALLS   #1,G^LIB$PUT_OUTPUT             ; ...
            BRB     10$                             ; Loop until EOF

     20$:   MOVL    R0,(SP)                         ; Replace "normal" with error
     30$:   $CLOSE  FAB=(R2)                        ; Close the file
            POPL    R0                              ; Restore saved status

     40$:   RET                                     ; Return to caller

            .END    TYPE

------------------------------------------------------------------------

**<span id="Program2"></span>Program 2**

            .TITLE  COPY_FILE
            .IDENT  /01-000/
    ;++
    ;
    ;  Facility:    COPY_FILE
    ;
    ;  Author:      Hunter Goatley
    ;               goathunter@WKUVX1.BITNET
    ;               Western Kentucky University
    ;
    ;  Date:        November 15, 1992
    ;
    ;  Abstract:
    ;
    ;       This MACRO-32 module contains the routine COPY_FILE.  It is
    ;       provided as an example of calling RMS routines from MACRO-32
    ;       for the "MACRO Made Easy" series in _Digital Systems Journal_.
    ;
    ;  Modified by:
    ;
    ;       01-000          Hunter Goatley          15-NOV-1992 15:48
    ;               Original version.
    ;
    ;--
            .DSABL  GLOBAL                          ; Declare external references
            .ENABL  SUPPRESSION                     ; Don't list unreference symbols
            .NOSHOW BINARY                          ; Include binary in listings

            .MACRO  ON_ERR  THERE,?HERE
            BLBS    R0,HERE                         ; Branch on success
            BRW     THERE                           ; Branch to THERE on error
     HERE:  .ENDM   ON_ERR

            $DSCDEF                                 ; Descriptor symbols
            $RMSDEF                                 ; RMS status symbols
            $FABDEF                                 ; Define FAB symbols
            $RABDEF                                 ; Define RAB symbols
            $SSDEF                                  ; System service status symbols

    MAX_REC_SIZE = 127*512                          ; Read up to 127 blocks at once

            .SHOW   BINARY                          ; Include binary in listings

    
            .PSECT  _COPY_FILE_DATA,NOEXE,WRT,LONG
    ;
    ;***  File Access Block for input
    ;
    INFAB:          $FAB    FAC=<BIO,GET>,-         ; File Access (Block I/O & GET)
                            SHR=<GET>               ; Allow others to read also
    ;
    ;***  Record Access Block for input
    ;
    INRAB:          $RAB    FAB=INFAB, -            ; The File Access Block
                            RAC=SEQ, -              ; Record Access is sequential
                            UBF=INREC, -            ; Input buffer address
                            USZ=MAX_REC_SIZE        ; The max size of record
    ;
    ;***  File Access Block for output
    ;
    OUTFAB:         $FAB    FAC=<BIO,PUT>           ; File Access (Block I/O & PUT)
    ;
    ;***  Record Access Block for output
    ;
    OUTRAB:         $RAB    FAB=OUTFAB, -           ; The File Access Block
                            RAC=SEQ, -              ; Record Access is sequential
                            RBF=INREC               ; The record buffer address

                    .ALIGN  LONG
    INREC:          .BLKB   MAX_REC_SIZE            ; Input buffer

    
            .SBTTL  COPY_FILE
    ;+
    ;
    ;  Routine:     COPY_FILE
    ;
    ;  Functional Description:
    ;
    ;       This routine copies one file to another using RMS block I/O.
    ;       The data in the file is copied intact, though not all file
    ;       attributes are preserved; specifically, such things as creation
    ;       date, backup date, protection, etc., are not maintained.
    ;
    ;       NOTE: THIS ROUTINE MAKES SOME ASSUMPTIONS ABOUT THE PARAMETERS
    ;       PASSED IN.  IT ASSUMES THAT STRING DESCRIPTOR ADDRESSES ARE
    ;       PASSED BY REFERENCE.
    ;
    ;       Also, note that the source file name is used as the default
    ;       file name of the copy.  The new file will be created in the
    ;       same directory as the existing file.
    ;
    ;  Formal parameters:
    ;
    ;       4(AP)   - Address of descriptor for the source file
    ;       8(AP)   - Address of descriptor for the new file
    ;
    ;  Returns:
    ;
    ;       R0      - Status
    ;
    ;-

    OLD_FILE        = 1*4                           ; The original file name
    NEW_FILE        = 2*4                           ; The filename of the copy

            .PSECT  _COPY_FILE_CODE,EXE,NOWRT,LONG,SHR
            .ENTRY  COPY_FILE,^M<R2,R3,R4,R5,R6,R7>

            MOVAB   INFAB,R2                        ; Move addresses to registers
            MOVAB   OUTFAB,R3                       ; ... for efficiency
            MOVAB   INRAB,R4                        ; ...
            MOVAB   OUTRAB,R5                       ; ...
    ;
    ;  Initialize the file name in the original file's FAB.
    ;
            MOVQ    @OLD_FILE(AP),R6                ; Get descriptor of file names
            MOVZBL  R6,R6                           ; Get the length as a byte
            $FAB_STORE -                            ; Store the filename in the FAB
                    FAB=(R2), -                     ; ...
                    FNA=(R7), -                     ; ...
                    FNS=R6                          ; ...
    ;
    ;  Copy the name to the new file's FAB as the default name to allow
    ;  default fields to be applied,
    ;
            $FAB_STORE -                            ; Store the filename in the FAB
                    FAB=(R3), -                     ; ...  Use for the default
                    DNA=(R7), -                     ; ...  file spec for the target
                    DNS=R6                          ; ...  (for wildcarding)
    ;
    ;  Now store the new filename in the FAB.
    ;
            MOVQ    @NEW_FILE(AP),R6                ; Get descriptor for new name
            MOVZBL  R6,R6                           ; Get the length as a byte
            $FAB_STORE -                            ; Store the filename in the FAB
                    FAB=(R3), -                     ; ...
                    FNA=(R7), -                     ; ...
                    FNS=R6                          ; ...
    ;
    ;  Open the original file for reading.
    ;
            $OPEN   FAB=(R2)                        ; Open the input file
            ON_ERR  50$                             ; Branch on error
            $CONNECT RAB=(R4)                       ; Connect the RAB to it
            ON_ERR  50$                             ; Branch on error
    ;
    ;  The file is open, so copy the fields related to organization, type,
    ;  size, etc., to the FAB for the new file.
    ;
            MOVL    FAB$L_ALQ(R2),FAB$L_ALQ(R3)     ; Copy the Allocation size
            MOVW    FAB$B_BKS(R2),FAB$B_BKS(R3)     ; Copy the bucket size
            MOVL    FAB$L_MRN(R2),FAB$L_MRN(R3)     ; Copy the maximum record #
            MOVW    FAB$W_MRS(R2),FAB$W_MRS(R3)     ; Copy the Maximum Record Size
            MOVB    FAB$B_ORG(R2),FAB$B_ORG(R3)     ; Copy the file ORGanization
            MOVB    FAB$B_RAT(R2),FAB$B_RAT(R3)     ; Copy the Record ATtributes
            MOVB    FAB$B_RFM(R2),FAB$B_RFM(R3)     ; Copy the Record ForMat
    ;
    ;  Now create the new file using the $CREATE service.
    ;
            $CREATE FAB=(R3)                        ; Open the same file for output
            ON_ERR  50$                             ; Branch on error

            PUSHL   #SS$_NORMAL                     ; Save "normal" status on stack

            $CONNECT RAB=(R5)                       ; Connect
            ON_ERR  30$                             ; Branch on error
    ;
    ;  The SS$_NORMAL is still on top of the stack to be used when EOF is reached.
    ;
    ;  Multiple blocks are read with each $READ and written with each $WRITE.
    ;
    ;
     10$:   $READ   RAB=(R4)                        ; Read a block of the file
            CMPL    #RMS$_EOF,R0                    ; End of file?
            BEQLU   40$                             ; Branch if so
            BLBC    R0,30$                          ; Success?  Go on
     20$:   MOVW    RAB$W_RSZ(R4),RAB$W_RSZ(R5)     ; Move the size to the OUTRAB
            $WRITE  RAB=(R5)                        ; Write the modified record out
            BLBC    R0,30$                          ; Error?  Return it
            BRB     10$                             ; Go get next record and process it
                                                    ;
     30$:   MOVL    R0,(SP)                         ; Save the error status
     40$:   $CLOSE  FAB=(R3)                        ; Close the file
            POPL    R0                              ; Restore the status
     50$:   PUSHL   R0                              ; Save the status
            $CLOSE  FAB=(R2)                        ; Close the input file
            POPL    R0                              ; Restore the status
            RET                                     ; Return to the caller

            .END

------------------------------------------------------------------------

**<span id="Program3"></span>Program 3**

    /*
     *  File:       COPY.C
     *
     *  Author:     Hunter Goatley, goathunter@WKUVX1.BITNET
     *
     *  Date:       November 15, 1992
     *
     *  Abstract:
     *
     *      Incredibly simplistic C program that copies one file to another
     *      by calling the MACRO-32 routine COPY_FILE.
     *
     */
    #include <descrip.h>
    #include <stdio.h>
    #include <string.h>

    extern COPY_FILE();

    int main(int argc, char *argv[])
    {
       struct dsc$descriptor_s infile  = {0, DSC$K_DTYPE_T, DSC$K_CLASS_S, 0};
       struct dsc$descriptor_s outfile = {0, DSC$K_DTYPE_T, DSC$K_CLASS_S, 0};

       if (argc != 3) {                     /* Simple error check */
          printf("Usage: copy old-file new-file\n");
          return(1);
       }

       /*  Initialize the string descriptors using the (expected) arguments  */
       infile.dsc$w_length = strlen(argv[1]);
       infile.dsc$a_pointer = argv[1];

       outfile.dsc$w_length = strlen(argv[2]);
       outfile.dsc$a_pointer = argv[2];

       /*  Now copy the file  */
       return (COPY_FILE (&infile, &outfile));
    }

