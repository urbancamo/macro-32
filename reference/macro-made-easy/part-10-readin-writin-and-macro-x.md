
# MACRO Made Easy – Part X: Readin’, Writin’, and MACRO

## MACRO Made Easy

Part X: Readin’, Writin’, and MACRO:\
Using RMS from MACRO
-------------------------------------

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

Continuing with our discussion of calling RMS to perform file I/O from MACRO, let’s take a look at the NAM and XAB blocks. The NAM blocks are used in processing file names, while the XABs (eXtended Attribute Blocks) are used for additional file information.

### NAM Blocks

NAM blocks are used by RMS to return additional filename information to a user. The FAB points to a NAM block, which points to a buffer that will receive an expanded file name—that is, a filename that has had all defaults applied and all logicals translated. The NAM block is written by the $OPEN, $CREATE, $DISPLAY, and $PARSE services.

The $OPEN and $CREATE services open and create a file, respectively, as seen in the last issue. The $DISPLAY service retrieves file information, while the $PARSE service analyzes a file specification and fills in missing fields. The resultant file spec returned by $PARSE can be easily shown using the DCL lexical function F$PARSE:

            $ write sys$output f$parse("LOGIN.COM", "SYS$LOGIN")
            WKU$USER:[HUNTER]LOGIN.COM;
            $

The $PARSE service, which is called by F$PARSE(), parses the file spec “LOGIN.COM”, supplying the defaults from the file spec “SYS$LOGIN:;”. The translation of SYS$LOGIN: was WKU$USER:\[HUNTER\], which $PARSE used as the device and directory, since they were omitted from the original specification.

To demonstrate how the $PARSE service is called, please see [Program 1](#Program1). This routine, FPARSE, mimics the basic functionality of the F$PARSE() lexical function. It is designed to be used by programs that need the functionality, but don’t want to worry about setting up the needed FAB and NAM blocks. FPARSE accepts a file spec and a default file spec, along with a bitmask specifying which fields of the file name are to be returned to the specified string descriptor. (Note that the “related” file specification is not supported by FPARSE because the related NAM must itself have been used in a call to $OPEN, $CREATE, or $DISPLAY.)

The following extract shows the allocation and initialization of the FAB and NAM blocks:

    PARSE_FAB:      $FAB    FOP=NAM, -              ; Options: NAM block
                            NAM=PARSE_NAM           ; NAM block address
    PARSE_NAM:      $NAM    ESA=PARSE_RESULT, -     ; Resultant string address
                            ESS=NAM$C_MAXRSS        ; Buffer size
    PARSE_RESULT:   .BLKB   NAM$C_MAXRSS            ; Buffer for resultant name

When a NAM block is to be filled in by a service, the NAM bit must be set in the FAB field FAB$L_FOP (file options). The $FAB macro parameter FOP=NAM sets this bit. The FAB must also include the address of the NAM block that is to be written; the NAM=PARSE_NAM parameter stores the address of the NAM block in the FAB$L_NAM field. The symbol NAM$C_MAXRSS defines the maximum size of an RMS file specification (255 bytes).

The $NAM macro defines the NAM block. In this example, the only fields initialized are the address (ESA) and size (ESS) of the buffer that is to receive the expanded file specification. The NAM block is used primarily for output from $PARSE. Once the file spec has been parsed and the expanded string has been written to the ESA buffer, a number of fields in the NAM are set to indicate where in the buffer the various fields begin and what their lengths are. For example, the field NAM$L_DIR points to the beginning of the directory name the ESA, while NAM$B_DIR contains the size of the directory portion of the file spec. The FPARSE function uses that information to select the specific portions of the expanded name that are to be returned to the caller.

The routine begins by checking the number of arguments passed in to make sure they’re all present. Next, the procedure initializes the FAB and NAM blocks:

    ;
    ;  Initialize structures
    ;
            CLRB    FAB$B_FNS(R6)                   ; Clear file spec size
            CLRL    FAB$L_FNA(R6)                   ; Clear file spec address
            MOVB    #DEFAULT_SPEC_L,FAB$B_DNS(R6)   ; Set default file spec size
            MOVAB   DEFAULT_SPEC,FAB$L_DNA(R6)      ; Set default file spec addr

The FNA and FNS fields are cleared in case the file spec is not passed to FPARSE. A default file specification of “SYS$DISK:\[\].;” is used as a default, even if the called caller does not pass a default name. This FAB initialization is done at run-time because the FAB and NAM blocks will be re-used if the calling program calls FPARSE more than once. If the initialization was done at assembly-time, the initial values would be lost after the first call.

Next, FPARSE initializes the appropriate fields based on the arguments passed in. If a non-zero address is specified for an argument, the routine LIB$ANALYZE_SDESC_R2 is called to get the length and address of the string from the descriptor. This routine is used so that all string descriptors are handled correctly, including PL/1 VARYING strings. Once all the FAB fields have been set, the $PARSE service is called to actually parse the names:

            $PARSE  FAB=(R6)                        ; Go parse it

If the call is not successful, the error is returned to the caller. If $PARSE returns success, the options bitmask is checked and each of the desired fields is copied to a work buffer:

            BBC     #FP_V_NODE,R9,80$               ; Branch if node is not returned
            MOVZBL  NAM$B_NODE(R7),R0               ; Get length of node name
            MOVC3   R0,@NAM$L_NODE(R7),(R3)         ; Copy node to work buffer

When all of the fields have been copied to the work buffer, the routine calls STR$COPY_DX to copy the resulting string to the caller’s buffer. The caller should specify a dynamic string descriptor for the result.

The following code shows a C program that calls FPARSE.

    #include 

    int main(void)
    {
       struct dsc$descriptor_d result = {0, DSC$K_DTYPE_T, DSC$K_CLASS_D, 0};
       $DESCRIPTOR(file, "LOGIN");
       $DESCRIPTOR(def, "SYS$LOGIN:.COM");
       int status;
       int name_type = 0x6;

       status = FPARSE(&result, &file, &def, 0);    /* Return everything */
       if (status&1) LIB$PUT_OUTPUT(&result);

       status = FPARSE(&result, &file, &def, &name_type);   /* Name & Type only */
       if (status&1) LIB$PUT_OUTPUT(&result);

       return(status);
    }

As was mentioned above, the $OPEN service will also fill in a NAM block, if one is present in the FAB. The COPY_FILE routine presented in the last issue could be easily modified to return the resulting file name to the caller by just modifying the FAB and including the NAM.

### XABs

XABs are eXtended Attribute Blocks, which are used to retrieve and specify file information that is not available in the FAB, RAB, and NAM blocks. There are currently 11 different XABs that provide file date/time stamps, file header information, etc. To use an XAB, the address of the XAB is specified in the FAB field FAB$L_XAB. Multiple XABs can be used by chaining them together; each XAB includes a field called XAB$L_NXT that is the address of the next XAB in the chain. The last XAB in the chain contains a zero in XAB$L_NXT.

Like the other RMS data structures, there are macros to both declare storage space for the XAB (like $XABDAT) and to store information at run-time ($XABDAT_STORE).

The $OPEN and $DISPLAY services return information to XAB, while $CREATE, $CLOSE, and $EXTEND use them as input. For example, if you wanted the creation date for a file, you could simply specify an XABDAT as the XAB when you call $OPEN to open the file. The following MACRO data fragment shows how the XABDAT would be initialized:

    INFAB:          $FAB    FNM=<LOGIN.COM>,-
                            XAB=INXABDAT
    INXABDAT:       $XABDAT                         ; Date XAB for INFAB

When the $OPEN service is called, the creation date of the file, along with the revision and backup dates, will be written to the INXABDAT structure. The quadword creation date is stored in the XAB$Q_CDT field in INXABDAT, the backup date is stored in XAB$Q_BDT, and the revision date is stored in XAB$Q_RDT. These fields are used as input by the $CREATE service, allowing you to specify the creation date of a file other than the default, which is the current date and time. The following brief MACRO program shows how to specify a creation date and an owner UIC using a chain of XABs:

    INFAB:  $FAB    FNM=<HUNTER.TMP>,-              ; The FAB to create temp file
                    XAB=INXAB                       ; Point to the XABDAT
    INXAB:  $XABDAT NXT=INXAB2                      ; The date XAB
    INXAB2: $XABPRO UIC=<5,32>                      ; Owner is [5,32]

    ASCTIM: .ASCID  /7-MAY-1964 09:29:00.00/        ; My birthday
    BINTIM: .QUAD   0                               ; Quadword to hold binary time

            .ENTRY  TMP,^M<>
            $BINTIM_S -                             ; Convert the ASCII time to
                    TIMBUF=ASCTIM,-                 ; ... a quadword (64-bit)
                    TIMADR=BINTIM                   ; ... internal time value
            MOVQ    BINTIM,INXAB+XAB$Q_CDT          ; Move the date to the XABDAT
            $CREATE FAB=INFAB                       ; And create the file
            RET                                     ; Just exit, since this is only
            .END    TMP                             ; ... a short example

Once the program is assembled, linked, and run, the DCL command DIR shows:

    $ MACRO TEMP
    $ LINK TEMP
    $ RUN TEMP
    $ DIR/DATE/OWNER HUNTER.TMP

    Directory DKA200:[HUNTER]

    HUNTER.TMP;1          7-MAY-1964 09:29:00.00  [5,32]

    Total of 1 file.

### Indexed files

An indexed file allows records to be read or written in a random sequence based on some key. For example, the SYSUAF file (SYS$SYSTEM:SYSUAF.DAT) contains all of the information for all accounts on a system. The SYSUAF file is an indexed file with two keys: the username and the UIC. Particular records can be retrieved and modified by specifying either the username or the UIC of the desired account. Indexed files can also be read sequentially, just as with normal text files. The type of access (indexed or sequential) is determined by the RAC (Record Access Code) in the RAB. (Note that this value can be changed at run-time to toggle between keyed reads and sequential reads.)

Digital recommends that all access to the SYSUAF file be done through the system services $GETUAI and $SETUAI. Unfortunately, these system services cannot be used to read sequentially through all records in the SYSUAF file. Many applications must use RMS to read and write the SYSUAF file. With proper programming techniques such as always using symbolic offsets, programs that read and write the SYSUAF directly will probably always work.

[Program 2](#Program2) is a short MACRO-32 program called WHO.MAR that will display the owner name for a specified username. This example can actually be coded using the $GETUAI system service, but it serves as a convenient example because every system has a SYSUAF file (though it probably is protected from non-privileged access).

WHO works by reading a username from the foreign command line using LIB$GET_FOREIGN and then opening the SYSUAF file to read the record for that username. The owner name is then pulled from the buffer into which the record was copied.

The appropriate record is retrieved by specifying the given username as the key for the $GET service. A key is described by its length, its address, and the index number of the key (primary key, first alternate, etc.). As was mentioned above, the username is the primary key for the SYSUAF file; it is referred to as key 0. The key of reference (KRF) is specified in the RAB field RAB$B_KRF. Key 0 is the primary key, key 1 is the first alternate key, and so on. A file can have up to 255 keys.

The address of the key to be used in the record lookup is stored in the RAB field RAB$L_KBF. The key size is stored in RAB$B_KSZ. The following $RAB declaration from WHO shows how the key would be specified:

    SYSRAB:                                 ; Record Access Block for SYSUAF
            $RAB    FAB=SYSFAB, -           ; ... The File Access Block
                    RAC=KEY, -              ; ... Record ACcess is keyed
                    KRF=0, -                ; ... Key of ReFerence = position 0
                    KSZ=12, -               ; ... The default Key SiZe is 12 chars
                    KBF=FOR_BUFF, -         ; ... Key is found in FOR_BUFF
                    USZ=UAF$K_LENGTH, -     ; ... Buffer is 1420 chars long
                    UBF=SYSREC              ; ... Address of SYSUAF record buffer

The macro $UAFDEF, found in SYS$LIBRARY:LIB.MLB, defines the symbolic offsets for the records in the SYSUAF file. The fields we are interested in are UAF$T_USERNAME and UAF$T_OWNER. The $FAO system service is used to format the output. The $FAO service will be described in some detail in the next issue.

When a program must create an indexed file, it can use the XABKEY XAB to specify all the information that is normally given using an FDL (File Definition Language) file. FDL files are created using the EDIT/FDL command; they describe the format of the file, the layout of keys, etc. The XABKEY fields include XAB$B_REF to specify the key of reference, XAB$L_KNM to specify the name of the key, etc.

### RMS status values (STS and STV)

Both the FAB and the RAB contain two fields that are used to return status information to a program calling RMS services. The first field is called the STS (the completion status code) and the second is the STV (the completion status value). The STS code is also returned in register R0. The STV is used to return additional information to the calling program. For example, if an invalid device is given in the filename on an $OPEN call, the STS value (and the value in R0) will be RMS$_DEV, which translates to the following error:

    %RMS-F-DEV, error in device name or inappropriate device type for operation

However, this doesn’t really explain what the problem was. The STV is used to provide that additional information. For example, the STV value may be SS$_NOSUCHDEV, which is:

    %SYSTEM-W-NOSUCHDEV, no such device available

If your program just returns the STS code to VMS, the error message may or may not be enough to indicate the problem. Your program can instead use both values by calling the run-time library routine LIB$SIGNAL. LIB$SIGNAL accepts one or more condition codes as parameters, along with parameters to the $FAO system service for each code. For most RMS values, there are no $FAO parameters, so the number of $FAO arguments would be 0. The $FAO arguments will be discussed in more detail next issue.

For now, just know that the RMS STS and STV codes can be combined in an error message by passing them to LIB$SIGNAL as in the following code fragment:

            PUSHL   SYSFAB+FAB$L_STV                ; Signal the exception using
            CLRL    -(SP)                           ; ... both STV and STS
            PUSHL   SYSFAB+FAB$L_STS                ; ...
            CALLS   #3,G^LIB$SIGNAL                 ; Signal the exception

Using the condition codes discussed above, the error messages printed by LIB$SIGNAL would read:

    %RMS-F-DEV, error in device name or inappropriate device type for operation
    -SYSTEM-W-NOSUCHDEV, no such device available

Note that the second message begins with ‘-‘, not ‘%’, indicating that is a continuation of the first error code, as opposed to a separate error message.

The “CLRL -(SP)” instruction is needed to tell LIB$SIGNAL that the STS code takes no $FAO arguments (a 0 is pushed on the stack). Note that most or all of the MACRO examples in the RMS manual incorrectly signal errors by just pushing the STV and STS codes. In those examples, the STV code will never be displayed, because LIB$SIGNAL treats it as the FAO argument count, not as another condition code. For example, the “Use of the Create, Open, and Close Services” (example 4-1) in the *VMS Record Management Services* manual incorrectly shows the following:

            F_ERR:  PUSHL   FAB$L_STV(R6)           ; Push STV and STS of FAB
                    PUSHL   FAB$L_STS(R6)           ; on the stack
                    CALLS   #2, G^LIB$SIGNAL        ; Signal error

The correct version would push a 0 on the stack between them and use \#3 in the CALLS to LIB$SIGNAL:

            F_ERR:  PUSHL   FAB$L_STV(R6)           ; Push STV and STS of FAB
                    CLRL    -(SP)                   ; on the stack (with no FAO
                    PUSHL   FAB$L_STS(R6)           ; args)
                    CALLS   #3, G^LIB$SIGNAL        ; Signal error

### RMS Summary

This series has just barely scratched the surface of the wealth of services provided by RMS. For example, no mention was made of asynchronous RMS calls, multiple keys, user-supplied success and error routines, etc. Fortunately for the MACRO programmer, the RMS routines were designed to be easy-to-use from MACRO. In fact, calling RMS is much easier from MACRO than it is from any other language besides BLISS because the wealth of RMS macros are not available in other languages. Plus, all of the examples in the RMS manual are written in MACRO, providing an excellent source of information for some of the more complicated RMS services.

### NEXT TIME….

Next issue, we’ll look at the $FAO system service in more detail and we’ll look at producing your own VMS-style error messages.

------------------------------------------------------------------------

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

------------------------------------------------------------------------

**<span id="Program1"></span>Program 1**

            .TITLE  FPARSE
            .IDENT  /01-000/
    ;++
    ;
    ;  Facility:    FPARSE
    ;
    ;  Author:      Hunter Goatley, goathunter@WKUVX1.BITNET
    ;
    ;  Date:        December 20, 1992
    ;
    ;  Functional Description:
    ;
    ;       Provide easy access to the $PARSE RMS routine.  This routine is
    ;       based on DCL's F$PARSE routine.  It does a syntax-only parse on
    ;       the name (the existence of the directory is not checked).
    ;
    ;  Modified by:
    ;
    ;       01-000          Hunter Goatley          20-DEC-1992 15:55
    ;               Original version.
    ;
    ;-------------------------------------------------------------------------------
    ;
    ;  Inputs:
    ;
    ;        4(AP)  - Descriptor for buffer to receive information
    ;        8(AP)  - Descriptor for file specification to be parsed
    ;       12(AP)  - Descriptor for default file specification (default is
    ;                 SYS$DISK:[].;)
    ;       16(AP)  - Address of bit mask describing information to be returned
    ;                 (Default is NODE::DEVICE:[DIRECTORY]NAME.TYPE;VERSION)
    ;
    ;                       Bit 5 set - return node name (usually null)
    ;                       Bit 4 set - return device name
    ;                       Bit 3 set - return directory name
    ;                       Bit 2 set - return file name
    ;                       Bit 1 set - return file type name
    ;                       Bit 0 set - return version number
    ;
    ;  Output:
    ;
    ;       4(AP)   - Descriptor for parsed file specification
    ;
    ;  Returns:
    ;
    ;       Status value in R0
    ;
    ;  Calling sequence:
    ;
    ;       status = fparse (&result, &filename, &default, &bitmask);
    ;
    ;--

    RESULT  = 1 * 4                                 ; Descriptor for resultant name
    FILE    = 2 * 4                                 ; File specification
    DEFAULT = 3 * 4                                 ; Default file spec
    OPTIONS = 4 * 4                                 ; Bit mask for return info
    NUMARGS = 4

    FP_V_NODE       = 5                             ; Bit 5 = node name (usually "")
    FP_V_DEV        = 4                             ; Bit 4 = device name
    FP_V_DIR        = 3                             ; Bit 3 = directory name
    FP_V_NAME       = 2                             ; Bit 2 = file name
    FP_V_TYPE       = 1                             ; Bit 1 = file type
    FP_V_VER        = 0                             ; Bit 0 = version number

            $SSDEF                                  ; System service status symbols
            $LIBDEF                                 ; LIB$ error symbols
            $RMSDEF                                 ; RMS definitions
            $FABDEF                                 ; File Access Block symbols
            $RABDEF                                 ; Record Access Block symbols
            $NAMDEF                                 ; Name block symbols

            .PSECT  _FPARSE_DATA,NOEXE,WRT,LONG,SHR

    ;
    ;***  File Access Block for input
    ;
    PARSE_FAB:      $FAB    FOP=NAM, -              ; Options: NAM block
                            NAM=PARSE_NAM           ; NAM block address
    PARSE_NAM:      $NAM    ESA=PARSE_RESULT, -     ; Resultant string address
                            ESS=NAM$C_MAXRSS        ; Buffer size

    PARSE_RESULT:   .BLKB   NAM$C_MAXRSS            ; Buffer for resultant name

                    .ALIGN  LONG
    WORK_BUFFER:    .BLKB   NAM$C_MAXRSS            ; Work buffer for final string

                    .ALIGN  LONG
    DEFAULT_SPEC:   .ASCII  /SYS$DISK:[].;/         ; Default default file
    DEFAULT_SPEC_L = . - DEFAULT_SPEC               ; ... specification and length

            .PSECT  _FPARSE_CODE,EXE,NOWRT,LONG,PIC,SHR
            .ENTRY  FPARSE,^M<r2,r3,r4,r5,r6,r7,r8,r9>

            CMPW    #NUMARGS,(AP)                   ; Were X arguments given?
            BEQLU   10$                             ; Branch if yes - we're OK
            MOVL    #LIB$_WRONUMARG,R0              ; Return error code
            RET                                     ; Return to caller

     10$:   MOVAL   PARSE_FAB,R6                    ; Point R3 to FAB
            MOVAL   PARSE_NAM,R7                    ; Point R4 to resultant NAM
    ;
    ;  Initialize structures
    ;
            CLRB    FAB$B_FNS(R6)                   ; Clear file spec size
            CLRL    FAB$L_FNA(R6)                   ; Clear file spec address
            MOVB    #DEFAULT_SPEC_L,FAB$B_DNS(R6)   ; Set default file spec size
            MOVAB   DEFAULT_SPEC,FAB$L_DNA(R6)      ; Set default file spec addr

            MOVL    DEFAULT(AP),R0                  ; Get related file spec address
            BEQLU   20$                             ; Branch if not given
            JSB     G^LIB$ANALYZE_SDESC_R2          ; Analyze for length and address
            MOVB    R1,FAB$B_DNS(R6)                ; Move length to FAB
            MOVL    R2,FAB$L_DNA(R6)                ; ...
     20$:   MOVL    FILE(AP),R0                     ; Get file spec address
            BEQLU   30$                             ; Branch if not given
            JSB     G^LIB$ANALYZE_SDESC_R2          ; Analyze for length and address
            MOVB    R1,FAB$B_FNS(R6)                ; Move length to FAB
            MOVL    R2,FAB$L_FNA(R6)                ; ...
     30$:
            $PARSE  FAB=(R6)                        ; Go parse it
            BLBS    R0,40$                          ; Branch if successful
            BRW     130$                            ; Branch to return on error
     40$:   MOVL    OPTIONS(AP),R9                  ; Get options address
            BEQLU   50$                             ; Branch if not given
            MOVL    (R9),R9                         ; Get the options
            BRB     60$                             ; Skip over default options
     50$:   MOVZBL  #^XFF,R9                        ; Set all options
     60$:   MOVAL   WORK_BUFFER,R3                  ; Get address of work buffer
                                                    ;
            BBC     #FP_V_NODE,R9,70$               ; Branch if node is not returned
            MOVZBL  NAM$B_NODE(R7),R0               ; Get length of node name
            MOVC3   R0,@NAM$L_NODE(R7),(R3)         ; Copy node to work buffer
                                                    ;
     70$:   BBC     #FP_V_DEV,R9,80$                ; Branch if dev is not returned
            MOVZBL  NAM$B_DEV(R7),R0                ; Get length of device name
            MOVC3   R0,@NAM$L_DEV(R7),(R3)          ; Copy device to work buffer
                                                    ;
     80$:   BBC     #FP_V_DIR,R9,90$                ; Branch if dir is not returned
            MOVZBL  NAM$B_DIR(R7),R0                ; Get length of directory spec
            MOVC3   R0,@NAM$L_DIR(R7),(R3)          ; Copy directory to work buffer
                                                    ;
     90$:   BBC     #FP_V_NAME,R9,100$              ; Branch if name is not returned
            MOVZBL  NAM$B_NAME(R7),R0               ; Get length of filename
            MOVC3   R0,@NAM$L_NAME(R7),(R3)         ; Copy name to work buffer
                                                    ;
     100$:  BBC     #FP_V_TYPE,R9,110$              ; Branch if type is not returned
            MOVZBL  NAM$B_TYPE(R7),R0               ; Get length of type
            MOVC3   R0,@NAM$L_TYPE(R7),(R3)         ; Copy type to work buffer
                                                    ;
     110$:  BBC     #FP_V_VER,R9,120$               ; Branch if ver is not returned
            MOVZBL  NAM$B_VER(R7),R0                ; Get length of version
            MOVC3   R0,@NAM$L_VER(R7),(R3)          ; Copy version to work buffer
                                                    ;
     120$:  MOVAL   WORK_BUFFER,R0                  ; Get address of work buffer
            PUSHL   R0                              ; Build descriptor for it
            SUBL3   R0,R3,-(SP)                     ; Get length on stack
            PUSHAL  (SP)                            ; Copy work buffer to user's
            PUSHAQ  @RESULT(AP)                     ; ... result buffer
            CALLS   #2,G^STR$COPY_DX                ; ...

     130$:  RET                                     ; Return to caller

            .END

------------------------------------------------------------------------

**<span id="Program2"></span>Program 2**

            .TITLE  WHO
            .IDENT  /01-000/
    ;++
    ;
    ;  Program:     WHO.MAR
    ;
    ;  Author:      Hunter Goatley, goathunter@WKUVX1.BITNET
    ;
    ;  Date:        December 20, 1992
    ;
    ;  Abstract:    Sample program to read a record from SYSUAF.
    ;
    ;  Modified by:
    ;
    ;       01-000          Hunter Goatley          20-DEC-1992 14:32
    ;
    ;--
            .LIBRARY        /SYS$LIBRARY:LIB.MLB/   ; For $UAFDEF
            $UAFDEF                                 ; Include SYSUAF symbols

    ;
    ;  Define a macro to check for errors.
    ;
            .MACRO  ON_ERR  DEST,?HERE
            BLBS    R0,HERE
            BRW     DEST
    HERE:   .ENDM   ON_ERR

    ;
    ;  The data psect
    ;
            .PSECT  WHO_DATA,NOEXE,WRT,LONG
    ;
    ;  The FAB for the SYSUAF file.  Note that SHR is given so we don't lock
    ;  others out of the SYSUAF file while we have it open!!
    ;
    SYSFAB:         $FAB    FNM=<sys$system:sysuaf.dat>, -  ; The file name
                            FAC=GET, -                      ; Want to GET from it
                            SHR=<get,put,upd,del,mse>       ; Allow other access

    ;
    ;  The RAB to read a record based on the username key.
    ;
    SYSRAB:         $RAB    FAB=SYSFAB, -           ; The File Access Block
                            RAC=KEY, -              ; Record ACcess is keyed
                            KRF=0, -                ; Key of ReFerence = position 0
                            KSZ=12, -               ; The default Key SiZe
                            KBF=FOR_BUFF, -         ; Key is found in FOR_BUFF
                            USZ=UAF$K_LENGTH, -     ; Buffer is 1420 chars long
                            UBF=SYSREC              ; Addr of SYSUAF record buffer
    ;
    SYSREC:         .BLKB   UAF$K_LENGTH
    ;
    FAO_STR:        .ASCID  /Username:  !AD   Owner:  !AC/
                    .ALIGN  LONG
    FAO_OUT_D:      .WORD   256                     ; Descriptor for $FAO output
                    .BYTE   DSC$K_DTYPE_T           ; ... buffer
                    .BYTE   DSC$K_CLASS_S           ; ...
                    .ADDRESS .+4                    ; ...
                    .BLKB   256                     ; ...

    FOR_BUFF_D:     .WORD   256                     ; LIB$GET_FOREIGN buffer
                    .BYTE   DSC$K_DTYPE_T           ; ... descriptor
                    .BYTE   DSC$K_CLASS_S           ; ...
                    .ADDRESS FOR_BUFF               ; ...
    FOR_BUFF:       .BLKB   256

    PROMPT_D:       .ASCID  /Username: /
                    .ALIGN  LONG
    MSG1:           .ASCID  /Username not found./
                    .ALIGN  LONG

    GET_FOREIGN_ARGLST:
                    .LONG   3                       ; 3 parameters
                    .ADDRESS FOR_BUFF_D             ; Input buffer
                    .ADDRESS PROMPT_D               ; Prompt descriptor address
                    .ADDRESS FOR_BUFF_D             ; Length of username given

    ;===============================================================================
    ;
            .PSECT  WHO,EXE,NOWRT,LONG
            .ENTRY  WHO,^M<>
    ;
    ;  Get the username from the command line, prompting the user if it's absent.
    ;
            CALLG   GET_FOREIGN_ARGLST,-            ; Get the username off the
                    G^LIB$GET_FOREIGN               ; ... command line
                                                    ;
            MOVZWL  FOR_BUFF_D,R1                   ; Get its length
            BNEQU   10$                             ; Branch if something given
            BRW     40$                             ; Exit if nothing or error
    ;
    ;  Use the length of the username given as the size of the key for the $GET.
    ;  Note that a better way to do this would be to blank-pad the key to the
    ;  size of the SYSUAF key (UAF$S_USERNAME), but using the size specified
    ;  will cause RMS to retrieve the first record that matches the partial
    ;  username.
    ;
     10$:   MOVB    R1,SYSRAB+RAB$B_KSZ             ; Set the key size in the RAB
            $OPEN   FAB=SYSFAB                      ; Open the SYSUAF file
            ON_ERR  40$                             ; Branch on error
            $CONNECT -                              ; Connect the RAB
                    RAB=SYSRAB                      ; ...
            ON_ERR  20$                             ; Branch on any error
    ;
    ;  Now try to $GET the record.
    ;
            $GET    RAB=SYSRAB                      ; ...
            ON_ERR  20$                             ; Branch on error
            MOVAL   SYSREC+UAF$T_USERNAME,R0        ; Point to username
            MOVAL   SYSREC+UAF$T_OWNER,R1           ; Point to owner name
    ;
    ;  Now use the $FAO system service to Format the ASCII Output.
    ;
            $FAO_S  CTRSTR=FAO_STR, -               ; Format the output string
                    OUTLEN=FAO_OUT_D, -             ; ... The length returned
                    OUTBUF=FAO_OUT_D, -             ; ...
                    P1=#12,-                        ; ... Only use 12 bytes
                    P2=R0,-                         ; ...
                    P3=R1                           ; ...
            PUSHAQ  FAO_OUT_D                       ; Print it
            CALLS   #1,G^LIB$PUT_OUTPUT             ; ...
                                                    ;
     20$:   CMPL    #RMS$_RNF,R0                    ; Valid user?
            BNEQU   30$                             ; Yes - continue
            PUSHAQ  MSG1                            ; Print "Username not found."
            CALLS   #1,G^LIB$PUT_OUTPUT             ; ...

     30$:   PUSHL   SYSRAB+RAB$L_STV                ; Push the RAB STV value
            CLRL    -(SP)                           ; No FAO args for STS
            PUSHL   SYSRAB+RAB$L_STS                ; Push the RAB STS value
            CALLS   #3,G^LIB$SIGNAL                 ; Signal it
            $CLOSE  FAB=SYSFAB                      ; Close SYSUAF
            BRB     50$                             ; Branch to exit

     40$:   PUSHL   SYSFAB+FAB$L_STV                ; Push the STV value
            CLRL    -(SP)                           ; No FAO args for STS
            PUSHL   SYSFAB+FAB$L_STS                ; Push the STS value
            CALLS   #3,G^LIB$SIGNAL                 ; Signal the error
     50$:   RET                                     ; Return to caller (VMS)

            .END    WHO

