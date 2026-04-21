
# MACRO Made Easy – Part XII: A MACRO-32 Example for both VAX and AXP

## MACRO Made Easy

Part XII: Revisiting the Extended DCL RECALL\
A MACRO-32 Example for both VAX and AXP
---------------------------------------------

#### by

### Hunter Goatley

#### Western Kentucky University

------------------------------------------------------------------------

**Note:** This article describes a program that hasn’t been relevant since OpenVMS V6.2 or so. It is presented here anyway because it’s a useful example of a real-life MACRO program.

In December of 1988, VAX Professional published my article “Extending DCL RECALL: A DCL Patch to Get the Most Out of RECALL.” As old-timers may remember, the article described some patches to DCL.EXE that would allow you to recall as many as 62 previous commands, instead of DCL’s limit of 20. Once my patches had been applied, the extended DCL recall was available through the normal means of recalling commands: the up- and down-arrow keys and the DCL RECALL command. Although it did require an unofficial patch to DCL, the benefits it provided were well worth the trouble.

The first time I generated the patches, I started by looking at the micro-fiche source for DCL to find out how the 20-command limit was imposed. I discovered that the value was hardcoded, instead of stored somewhere in the DCL data area. I then used Andy Pavlin’s DISM32 to disassemble DCL.EXE. (DISM32 is a VMS disassembler that can be found on the DECUS VAX SIG tapes from the last few years. It understands most VMS images, including device drivers, and produces MACRO source code that can oftentimes be assembled without modification.) Once I had the disassembled “source” for DCL.EXE, I was able to quickly find the instructions containing the hardcoded values. From there, it was pretty simple to use PATCH to locate the offsets within DCL of the instructions.

One of the largest drawbacks to my method is that DCL.EXE changes in most VMS upgrades, making it necessary to relocate the new offsets after each upgrade. After coming with separate patches for a half-dozen versions of VMS and since it appears that Digital has no plans to allow the user to SET the limit, I decided to finally write a program to apply the patches.

The result was DCLPATCH.MAR ([Program 1](#Program1)), a MACRO-32 program that reads the DCL image into memory, applies the patches, and creates a new image file. While I considered several ways to do this (including a TPU routine to do the patch), I decided to go with the most straight-forward approach. The program will be described in some detail below; while it is a simple program, it has some “neat tricks” that you might be able to use in your own MACRO programs.

This program runs under all versions of OpenVMS from VAX/VMS v4.0 through OpenVMS V6.0. It also will compile and run under OpenVMS AXP V1.0 and V1.5.

### BUT FIRST, A BRIEF REFRESHER

For a full explanation of the patches involved, please refer to my previous article, “Extending DCL RECALL” (VAX Professional, December 1988). To refresh your memory, the reason there is a limit of 62 commands is that the hardcoded limits are stored in the image as short literals. A short literal is stored as a byte whose two high bits must be zero to identify it as a short literal. This leaves 6 bits for the actual number, making the largest possible short literal 63 (2 raised to the 6th minus 1). Because the code itself actually uses WRK_C_RECALLMAX+1, the patched value can be no larger than 63, and the new recall maximum becomes 62.

Under OpenVMS AXP, the limit has been extended to 99. This limit is not set by the size of the bits available for patching as on the VAX, but is instead determined by the two-character number displayed by RECALL/ALL. In theory, DCL could also be changed to display more values, but I’ve chosen not to do so. (It’s not trivial under AXP!)

Note that there may not actually be 62 commands available for recall. The command recall buffer is 1024 bytes long; the length of the commands themselves determines how many commands will fit in the buffer. If your commands are very short, you could have more than 100 in the buffer; if they were very long you could have as few as 4. The number of commands available for recall is actually the number of commands still in the buffer, but no more than 62. (For more information on the DCL command recall buffer, please consult my October 1987 VAX Professional article entitled “Flushing the Buffer”).

### HOW DCLPATCH.MAR WORKS

The program’s logic flow is very straight-forward and makes use of the RMS calls that have been discussed in previous articles in this series. The main routine first branches to the internal subroutine READ_OLD_IMAGE. The target image, SYS$SYSTEM:DCL.EXE in this case, is opened using RMS calls ($OPEN and $CONNECT). An Extended Attribute Block (XAB) is provided so RMS will return the File Header Characteristics ($XABFHC). Once the file has been opened, the XABFHC contains, among other data, the number of the end-of-file block—which also happens to be the size of the file in blocks. This value is multiplied by 512 to convert the size from blocks to bytes. The program then dynamically allocates a buffer large enough to hold the entire file by calling the Run-Time Library routine LIB$GET_VM. If the image is too large (not enough contiguous memory can be allocated), the program simply returns the error to VMS.

Once the buffer has been successfully allocated, the Record Access Block (RAB) for the file is modified to point to the new buffer; this buffer will be used to receive each block read by RMS. The $GET RMS routine is called to read the file in 512-byte chunks. As each record is read, the address of the input buffer is increased by 512, so that the RAB points to the next 512-byte piece of memory. Modifying the RAB directly with the following instruction eliminates the need for extra registers to keep track of the next available byte:

            ADDL2    #512,RAB$L_UBF(R6)

A separate counter is incremented for each successful block that is read. Instead of using XAB$L_EBK, I used a separate counter to ensure that I know exactly how many blocks were read. The value returned in XAB$L_EBK may actually point to the block just past the end-of-file block, if the last block in the file is full. While this is not normally true for .EXE files, I think it’s good programming practice.

NOTE: I used $GET (record I/O) instead of $READ (block I/O) purely for convenience. Using $GET to read 512-bytes is actually faster than using $READ to read 512-byte blocks, though the code could have been written to read in larger chunks with block I/O. Had I been seriously concerned about overhead, using block I/O would have been better.

Once the entire file has been read into the buffer, the program starts replacing instructions by calling REPLACE_STREAM. Actually, I wrote a macro named REPLACE that sets up the input registers before branching to the REPLACE_STREAM subroutine. I chose the macro to increase the program’s readability. The name STREAM refers to a contiguous stream of bytes.

The input parameters that are passed to REPLACE_STREAM include the length of the stream to replace, the address of the old stream, and the address of the new stream. REPLACE_STREAM simply starts at the beginning of the buffer and steps through it byte-by-byte, looking for a match on the first byte of the stream to be replaced. Once a match is made, the following bytes are compared until either a match is found or a dissimilar byte is found. If the entire stream is not matched, the routine proceeds through the buffer. Once a match is made, the pointers are adjusted to point to the beginning of the stream and the new bytes are copied into the buffer, overlaying the old bytes. A message is printed to the terminal indicating the offset of the replaced stream. Once the stream has been replaced, the search for the next match resumes.

Again, there are other ways this could have been coded, using the LOCC (LOCate Character) instruction. I chose the simple byte-by-byte loops so that I could easily maintain pointers and counters.

Once all of the instruction streams have been replaced, the program calls WRITE_NEW_IMAGE to create a new image called DCL_RECALL.EXE in the default directory. This is accomplished by writing 512-byte chunks of the contiguous memory buffer to the output file using $PUT.

### COMPILING DCLPATCH FOR OPENVMS AXP

When compiling MACRO programs using the MACRO-32 AXP compiler, a file containing architecture symbols should be included in the compilation. This file is SYS$LIBRARY:ARCH_DEFS.MAR on OpenVMS AXP. The file is not currently included with OpenVMS VAX, though one could easily be made. This is the file from AXP:

    ;
    ; This is the ALPHA (previously called "EVAX") version of ARCH_DEFS.MAR,
    ; which contains architectural definitions for compiling VMS sources
    ; for VAX and ALPHA systems.
    ;
    EVAX = 1
    ALPHA = 1
    BIGPAGE = 1
    ADDRESSBITS = 32

To include the file when compiling a MACRO-32 program, you would use the ‘+’ operator on the MACRO DCL command line:

    $ macro/migrate/obj=dclpatch sys$library:arch_defs.mar+sys$disk:[]dclpatch.mar

It is an (in this case anyway) unfortunate side effect that the MACRO compiler and assembler propagate the device and directory from the first file spec to the second, which is why the SYS$DISK:\[\] string, which refers to the current default directory, was included. If it had been omitted, the compiler would have looked for DCLPATCH.MAR in SYS$LIBRARY:.

By including the ARCH_DEFS.MAR file, the DCLPATCH source can check to see whether or not the EVAX or ALPHA symbol is defined for determining whether or not the program is being compiled for AXP or assembled for VAX. For example, the following .IF/.IFF directives delimit the AXP and VAX code.

            .IF DEFINED ALPHA
            ....AXP-specific code/data....
            .IFF
            ....VAX-specific code/data....
            .ENDC

Because I could see a case where someone may want to assemble DCLPATCH on a VAX, but process DCL.EXE from an AXP system, and vice versa, I added some conditional directives to be beginning of the program to determine the platform for which DCLPATCH should be built.

    ;
    ;  To build DCLPATCH on the VAX but allow it to handle AXP DCL.EXE images,
    ;  uncomment the following line.
    ;
    ;DO_ALPHA = 1
    ;
    ;  To build DCLPATCH on AXP but allow it to handle VAX DCL.EXE images,
    ;  uncomment the following line.
    ;
    ;DO_ALPHA = 0
    ;
    ;  This line says, "If DO_ALPHA is not defined and we're compiling under
    ;  OpenVMS AXP, then define the DO_ALPHA symbol."
    ;
    .IF NOT_DEFINED DO_ALPHA                ; If user has not set a preference,
    DO_ALPHA = 0                            ; ... then assume VAX unless
    .IIF DF,EVAX,   DO_ALPHA = 1            ; ... compiling under AXP
    .ENDC

The conditional .IF NOT_DEFINED DO_ALPHA causes DO_ALPHA to be set to 0 or 1 depending on whether or not EVAX is defined \*if\* the user has not already specified a preference by defining DO_ALPHA to 0 or 1. Note that the DO_ALPHA symbol is used to determine the type of image that DCLPATCH can process; the EVAX symbol is used to determine whether or not the program is being compiled for AXP.

Because DCLPATCH uses local subroutines called via BSBW (or JSB), each of the JSB entry points had to be declared as such when using the MACRO-32 compiler. The following line causes the .JSB_ENTRY to be included in this if EVAX is defined:

            REPLACE_STREAM:
            .IIF DF,EVAX,   .JSB_ENTRY

The .JSB_ENTRY allows you to specify input and output registers, but it wasn’t necessary to include them in this program.

### THE AXP PATCHES

MACRO-64, the AXP assembly language, is radically different from MACRO-32. For one thing, the AXP has more registers than the VAX and they are used differently. On the VAX, the patches to DCL were straightforward—replace VAX instructions with different instructions. Under AXP, the same DCL source code, written in MACRO-32, has been compiled, making the instruction selection more difficult to trace. The proper values were determined by looking at the source code listings for DCL and locating the machine code generated for the MACRO-32 instructions that needed to be modified. For example, for this VAX instruction:

            CMPB    B^WRK_B_RECALLCNT(R10),-        ;Old instruction
                    S^#WRK_C_RECALLMAX+1            ;... (occurs 3 times)

the following three AXP instructions were generated:

    ;A30AFFC0     0FB0              LDL     R24, -64(R10)   ; 003517
    ;4B0070D8     0FB4              EXTBL   R24, 3, R24
    ;4302B530     0FB8              SUBQ    R24, 21, R16

On the VAX, the goal was to replace the value of WRK_C_RECALLMAX+1 (21) with the new value. On AXP, the same thing is desired, but the actual instruction is the SUBQ instruction above. The hexadecimal value on the extreme-left of the instruction is the binary code for that instruction. To replace the “21” in the instruction, I had to decode the AXP instruction format and replace the literal 21 with a literal 100. The decoding is beyond the scope of this article, but it was accomplished by looking up the instruction formats in the *Alpha Architecture Handbook*, which is published by Digital.

The end result is that for AXP, I had to hardcode the binary values for the AXP instructions (both the one to replace and the replacement):

    OINST1:         .LONG   ^X4302B530
                    OINST1_L = .-OINST1

    NINST1:         .LONG   ^X430C9530      ; 21 -> 100
                    NINST1_L = .-NINST1

For the VAX, the actual assembly code was included as data, letting the assembler produce the proper binary values. But this was not practical on the AXP since just including the instruction would not have produced the same register usage (not to mention the fact that the compiler would complain about having code in the data psect).

The data psect containing the replacement code includes comments that describe the purpose of the various longwords and instructions. While it appears quite convoluted, is does allow DCLPATCH to work in both environments.

This has one severe limitation of DCLPATCH for AXP. In a future version of OpenVMS AXP (beyond V1.5), the binary code generated by the MACRO-32 compiler for DCL could use different registers, which will cause DCLPATCH to fail, since it expects the registers used to be R24 and R16. If that ever changes, then DCLPATCH will have to be modified to handle the new registers too.

The replacement code to handle the RECALL/ALL display is more complex under AXP than it is under the VAX, but the same general approach is taken. The original DCL algorithm for displaying the command number

            if (ones digit is a 9)
               if (tens digit is a 1)
                  insert string "2/"
               else (tens digit is not a 1)
                  insert string "1/"
               endif
            endif
            increment ones count
            display

The way this is coded, if the tens digit is not a 1, it’s assumed to be zero. A ‘9’ is converted to “1/” and then the byte increment of ‘/’ yields a ‘0’ (‘9’ -\> “10”). Left alone, this makes the RECALL/ALL display go from 29 back to 10. The patch replaces that algorithm with the following:

            if (ones digit is a 9)
               if (tens digit is a 0 (space))
                  insert string "1/"
               else (tens digit is not a 0)
                 increment tens count
               endif
            endif
            increment ones count
            display

The modifications necessary for implementing this under AXP (and the logic flow descriptions) were provided by Ehud Gavron of ACES Consulting, who spent time on it when I didn’t have the time—thanks, Ehud!

### THE FINE POINTS

There are a few points that I wanted to emphasize, plus a couple of assumptions that the program has to make in order to work as simply as it does:

1.  The instruction streams are assumed to be the same size. If two different-size streams were involved, the physical size of the output file would have to change, which would, basically, trash the image being patched. This program was designed to apply the patches in a manner similar to the REPLACE command in PATCH. If you need to add instructions, PATCH is the only way to go, since it will create patch buffers, adjust pointers, etc.Note that PATCH is not provided with OpenVMS AXP.If you look at the data area in DCLPATCH.MAR, you’ll find the instructions that are to be replaced (labelled OINST1, OINST2, etc.). The replacement instructions are labelled NINST1, NINST2, etc. To ensure that the old and new streams are the same size, I used the ASSUME macro:

          OINST3:         MOVL    S^#WRK_C_RECALLMAX,R6           ;Old instruction 3
                          OINST3_L = .-OINST3                     ;...
          NINST3:         MOVL    S^#NEW_C_RECALLMAX,R6           ;...
                          NINST3_L = .-NINST3                     ;...
                          ASSUME  OINST3_L EQ NINST3_L            ;...

    In this fragment, the first line is the old instruction that is to be replaced. The second line generates a symbol, OINST3_L, that is equated with the length of the instruction. The ‘.’ represents the current address at assembly-time; specifying “.-OINST3” tells the assembler to subtract the address of OINST3 from the current address, which happens to be the byte after the instruction. This difference, 3 in this case, is then assigned to the symbol OINST3_L. The third line is the new instruction, and the fourth calculates the length of it. The fifth line invokes the ASSUME macro to ensure that the two lengths are equal (it can also be used to check for greater than, less than, etc.; the ASSUME macro is not documented, but can be found in the STARLET macro library). If the two values are not equal, the assembler will generate an error stating so.

2.  Because the program is written in MACRO, I was able to specify the two instruction streams in normal mnemonic format for the VAX. In a high-level language, each of the instructions would have to be broken down into their individual bytes, which would mean looking up opcodes and the internal storage format for the operands. Note that this had to be done for AXP support.

3.  To help ensure that the program doesn’t have to be modified for new versions of DCL.EXE on the VAX, the program is linked with the DCL symbol table. The following line in DCLPATCH.MAR tells the linker to link with DCLDEF.STB to resolve the following external symbols:

                   .LINK   "SYS$SYSTEM:DCLDEF.STB"/selective_search
           ;
           ;  Global variables used here:
           ;
                   .EXTRN  WRK_B_RECALLCNT                 ; Symbol from DCLDEF.STB
                   .EXTRN  WRK_C_RECALLMAX                 ; Symbol from DCLDEF.STB

    The .LINK directive is ignored under the MACRO-32 compiler.

4.  The largest assumption made by the program is that the instructions to be replaced are unique. Since the program replaces all occurrences of a stream, care must be taken to ensure that the correct instructions have been located. In the case of DCL.EXE, I got lucky: the only occurrences of the instructions are the ones that need to be replaced. This would not have been true if one of the instructions had been something common, like:

                CLRL R0

    In that case, the instruction streams could be expanded to include the two or three instructions preceding or following the one to replace in order to qualify it better. For example, if I needed to replace only one CLRL R0 and it is preceded or followed by an uncommon instruction like “EXTZV \#3,#16,R0,R10”, specifying the EXTZV would help ensure that we only replace the instruction we want to replace.

    Just in case one of the instructions is duplicated in some future version of DCL, the program checks that only a certain number of each were found. If the number of replacements doesn’t match the expected number, no new file is created.

5.  Unlike PATCH, my program does not create a patch history. Since the patch is made in place, the only difference between DCL_RECALL and DCL is that a few bytes have been changed. Using the PATCH instructions from my previous article, a patch history was added to DCL.EXE which showed the patches that were made (using ANALYZE/IMAGE).The drawback to this is that it’s more difficult to tell whether or not the extended RECALL patch has been applied. The advantage is that future “official” patches to DCL will go smoothly, since there will be no indication that the “unofficial” patch was made. (Not that this ever caused a problem before during upgrades, but it could have.)Note that when using PATCH/ABSOLUTE, PATCH does not write a patch history.

6.  The address printed to the terminal by REPLACE_STREAM is the offset that would have been supplied to the PATCH utility on the VAX. If you feel better about using my old patches, you can just plug the printed addresses into the old patch command file. (If you wanted to use PATCH/ABSOLUTE, you’d need to add 200 (hex) to each address to allow for the image header.)

7.  For the VAX, if you don’t want 62 commands to be recallable, you can change the following definition in DCLPATCH.MAR to specify any number from 0 to 62:

         NEW_C_RECALL_MAX = 62

8.  As you look at the main routine, you’ll notice that informational messages are printed to the screen using the PRINT macro. The macro is defined as:

                .MACRO  PRINT   STRING,?TEXT                    ;* Macro to print text
                .SAVE_PSECT LOCAL_BLOCK                         ;* Save this PSECT
                .PSECT  _DCLPATCH_DATA,NOEXE,WRT,LONG,SHR       ;* Change to data PSECT
                .ALIGN  LONG                                    ;* Align on longword
         TEXT:  .ASCID  ~STRING~                                ;* Create .ASCID string
                PRINT_TEXT = TEXT                               ;* Save the address
                .RESTORE_PSECT                                  ;* Go back to code
                PUSHAQ  PRINT_TEXT                              ; Write the string
                CALLS   #1,G^LIB$PUT_OUTPUT                     ; ... to SYS$OUTPUT
                .ENDM   PRINT                                   ;* End of PRINT macro

    When invoked, the macro will cause the assembler to create a .ASCID string (a string with a descriptor) in the PSECT (program section) named _DCLPATCH_DATA, and then return to the code PSECT to call LIB$PUT_OUTPUT to print the string. For more information on how this works, you can study the comments above and consult the VAX MACRO AND INSTRUCTION SET REFERENCE MANUAL for more information about .SAVE_PSECT and .RESTORE_PSECT. Essentially, it provides a quick way to hop between a data area and a program area with in-line assembler directives.

### CUSTOMIZING DCLPATCH.MAR

As you may have noticed by now, this program has several other possible applications. It would be trivial to modify the program to patch other images and replace other streams. One of the most useful applications for the program is to change ASCII strings within an image. For example, suppose you have an executable image that has a logical name that doesn’t suit your site (or even worse, a full device/directory file specification). You could modify DCLPATCH.MAR to replace all occurrences of the string with a more suitable string. For example, the following would replace all occurrences of DUA0:\[UTILS.SYS\] with the logical SYSTEM_UTILITYS:

       OINST1:         .ASCII  /DUA0:[UTILS.SYS]/
                       OINST1_L = .-OINST1
       NINST1:         .ASCII  /SYSTEM_UTILITYS:/
                       NINST1_L = .-NINST1
                       ASSUME  OINST1_L EQ NINST1_L

Even in this case, you must make sure the two streams are the same length because you don’t know how many times the length of the original string is stored (in descriptors, in the code, etc). You sometimes have to be creative when generating the logical names (like the misspelling of SYSTEM_UTILITYS above), but at least it provides some way to reduce site-dependencies when you don’t have the source code.

### BUILDING DCLPATCH

To build DCLPATCH.EXE (either as-is or customized), simply use the following DCL commands:

       $ MACRO DCLPATCH
       $ LINK DCLPATCH

Under OpenVMS AXP, you’d have to use the MACRO/MIGRATE command:

       $ MACRO/MIGRATE/OBJ=DCLPATCH SYS$LIBRARY:ARCH_DEFS.MAR+SYS$DISK:[]DCLPATCH
       $ LINK DCLPATCH

Here is a sample run under OpenVMS AXP V1.5:

      $ macro/migrate/obj=dclpatch sys$library:arch_defs.mar+sys$disk:[]dclpatch
      $ link/notrace dclpatch
      $ run dclpatch
      Extending recall capability of SYS$SYSTEM:DCL.EXE....
      Special ALPHA Version!!!
      Replacing "CMPB WRK_B_RECALLCNT(R10),#WRK_C_RECALLMAX+1" (3 occurrences)....
      Patching at image address 0001E0D0
      Patching at image address 0001DFB8
      Patching at image address 0001E028
      Replacing "CMPL R1,#WRK_C_RECALLMAX" (1 occurrence)....
      Patching at image address 0001F3B0
      Replacing "MOVL #WRK_C_RECALLMAX,R6" (1 occurrence)....
      Patching at image address 0001F450
      Replacing "MOVL #WRK_C_RECALLMAX,R9" (1 occurrence)....
      Patching at image address 0001F49C
      Replacing RECALL output code comparison (1 occurrence)...
      Patching at image address 0001F680
      Replacing RECALL output code increment (1 occurrence)...
      Patching at image address 0001F688
      Replacing RECALL output code insertion (1 occurrence)...
      Patching at image address 0001F75C
      Creating file DCL_RECALL.EXE
      Extended DCL RECALL image DCL_RECALL.EXE created
      $

Once the patch has been made, you can test it by copying DCL_RECALL.EXE to SYS$SYSTEM: and installing it. Once it has been installed, an account can be set up to use it by running AUTHORIZE and specifying the DCL_RECALL as the CLI the user is to use:

       $ INSTALL ADD DCL_RECALL/OPEN/HEADER/SHARED
       $ SET DEFAULT SYS$SYSTEM:
       $ RUN AUTHORIZE
       UAF>  MODIFY HUNTER/CLI=DCL_RECALL
       User record(s) updated
       UAF>  EXIT

Now when someone logs in under username HUNTER, he/she will be using the patched version of DCL. You can test the patches by entering more than twenty commands and then using RECALL/ALL and the arrow keys. To access the command numbered 56, simply give the following command:

       $ RECALL 56

Once you are confident that the patch works, you can rename it as DCL.EXE and reinstall DCL so that all users will get it by default (I suggest keeping a copy of the original around, “just in case….”):

       $ INSTALL REMOVE DCL_RECALL
       $ COPY SYS$SYSTEM:DCL.EXE SYS$SYSTEM:DCL_ORIGINAL.EXE
       $ COPY SYS$SYSTEM:DCL_RECALL.EXE SYS$SYSTEM:DCL.EXE
       $ INSTALL REPLACE DCL

As usual, you use this program at your own risk. If you don’t feel comfortable using the patches, then don’t apply them. I’ve been using the patches since VMS version 4.2 without ever having a problem. By finally taking the time to write DCLPATCH.MAR, I’ve eliminated the minor headache of regenerating a new patch each time a VMS upgrade arrives. With some very minor changes, the program has many other possible uses. And remember: there are other ways it could have been written. Perhaps you’ll explore some of the others?

### THE END

This is the final entry in the MACRO Made Easy series. I hope you’ve found them interesting and that they may have helped ease the process of learning and using MACRO-32. There are, of course, many areas that I have not touched upon, including the MACRO-32 queue instructions and the various arithmetic instructions. MACRO-32 is fully documented in the VMS documentation set. My reference of choice is the 1982 *VAX Architecture Handbook*, if you can find a copy. This program shown here, though quite simple, does show that MACRO-32 is not a dead language now that AXP is a reality.

------------------------------------------------------------------------

Hunter Goatley, goathunter@WKUVX1.BITNET, Western Kentucky University, Bowling Green, KY.

------------------------------------------------------------------------

<span id="Program1"></span>**DCLPATCH.MAR**

            .TITLE  DCLPATCH
            .IDENT  /02-000/
    ;++
    ;
    ;  Facility:    DCLPATCH
    ;
    ;  Author:      Hunter Goatley
    ;               Western Kentucky University
    ;               Academic Computing, STH 226
    ;               Bowling Green, KY 42101
    ;               E-mail: goathunter@wkuvx1.bitnet
    ;               Voice:  502-745-5251
    ;
    ;  Date:        February 21, 1991
    ;
    ;  Functional Description:
    ;
    ;       Applies the "extended RECALL" patch to DCL.EXE.
    ;
    ;       SYS$SYSTEM:DCL.EXE is read into memory and the instructions to
    ;       to patch are located and replaced.  When all patches have been
    ;       made, a new image file, DCL_RECALL.EXE, is created.
    ;
    ;       Once applied, DCL_RECALL.EXE can recall as many as 62 commands
    ;       (instead of the DCL limit of 20).  The limit is imposed by the
    ;       instructions being replaced: the maximum number is stored as a
    ;       short literal, which has a maximum value of 63. Since the code
    ;       actually checks against max+1, 63 became max+1.
    ;
    ;       Under AXP, the limit is 99 characters.  The limit could be
    ;       higher, but we're restricted to 2 digits for the RECALL/ALL
    ;       display.
    ;
    ;  Modified by:
    ;
    ;       02-000          Hunter Goatley          13-MAR-1993 20:52
    ;               Merge the two into one program.
    ;
    ;       01-002          Ehud Gavron             15-Jan-1993 All day!
    ;               Patch DCL.EXE so RECALL/ALL numbers correctly.
    ;               Remove conditional IFDEFs on .JSB_ENTRYs.
    ;
    ;       01-001          Hunter Goatley          November 1992
    ;               Converted to work on AXP.  All but RECALL/ALL numbers.
    ;
    ;       01-000          Hunter Goatley          21-FEB-1991 09:12
    ;               Original version.
    ;
    ;--
            .SBTTL  Symbols and macros
    ;
    ;  To build DCLPATCH on the VAX but allow it to handle AXP DCL.EXE images,
    ;  uncomment the following line.
    ;
    ;DO_ALPHA = 1
    ;
    ;  To build DCLPATCH on AXP but allow it to handle VAX DCL.EXE images,
    ;  uncomment the following line.
    ;
    ;DO_ALPHA = 0
    ;
    ;  This line says, "If DO_ALPHA is not defined and we're compiling under
    ;  OpenVMS AXP, then define the DO_ALPHA symbol."
    ;
    .IF NOT_DEFINED DO_ALPHA                ; If user has not set a preference,
    DO_ALPHA = 0                            ; ... then assume VAX unless
    .IIF DF,EVAX,   DO_ALPHA = 1            ; ... compiling under AXP
    .ENDC
    .IF NOT_DEFINED EVAX                    ; .PRINT is ugly under AXP compiler
    .IF EQ DO_ALPHA
            .PRINT  ;Producing VAX version of DCLPATCH
    .IFF
            .PRINT  ;Producing AXP version of DCLPATCH
    .ENDC
    .ENDC
            .LINK   "SYS$SYSTEM:DCLDEF.STB"/selective_search

            .DSABL  GLOBAL                          ; Declare external references
            .ENABL  SUPPRESSION                     ; Don't list unreference symbols
            .NOSHOW BINARY                          ; Skip binary until data
    ;
    ;  External routines:
    ;
            .EXTRN  LIB$GET_VM                      ; Allocate memory
            .EXTRN  LIB$PUT_OUTPUT                  ; Write to SYS$OUTPUT
    ;
    ;  Global variables used here:
    ;
    .IF NOT_DEFINED EVAX
            .EXTRN  WRK_B_RECALLCNT                 ; Symbol from DCLDEF.STB
            .EXTRN  WRK_C_RECALLMAX                 ; Symbol from DCLDEF.STB
    .ENDC

            $DSCDEF                                 ; Descriptor symbols
            $FABDEF                                 ; File Access Block symbols
            $RABDEF                                 ; Record Access Block symbols
            $RMSDEF                                 ; RMS definitions
            $SSDEF                                  ; System service status symbols
            $XABDEF                                 ; Extended attribute block

            .MACRO  ON_ERR  LAB,?TMPLAB             ;* BRW on error condition
            BLBS    R0,TMPLAB                       ; Branch if R0 indicates success
            BRW     LAB                             ; Branch to error address
    TMPLAB: .ENDM   ON_ERR                          ;* End of ON_ERR macro

            .MACRO  PRINT   STRING,?TEXT                    ;* Macro to print text
            .SAVE_PSECT LOCAL_BLOCK                         ;* Save this PSECT
            .PSECT  _DCLPATCH_DATA,NOEXE,WRT,LONG,SHR       ;* Change to data PSECT
            .ALIGN  LONG                                    ;* Align on longword
     TEXT:  .ASCID  ~STRING~                                ;* Create .ASCID string
            PRINT_TEXT = TEXT                               ;* Save the address
            .RESTORE_PSECT                                  ;* Go back to code
            PUSHAQ  PRINT_TEXT                              ; Write the string
            CALLS   #1,G^LIB$PUT_OUTPUT                     ; ... to SYS$OUTPUT
            .ENDM   PRINT                                   ;* End of PRINT macro

            .MACRO  REPLACE LEN,OLD,NEW,CNT,ERR,?CONT
            MOVL    LEN,R5                          ; R5 = Size
            MOVAL   OLD,R6                          ; R6 -> old instruction
            MOVAL   NEW,R7                          ; R7 -> new instruction
            BSBW    REPLACE_STREAM                  ; Go replace it
            CMPL    CNT,R0                          ; Right number found?
            BEQL    CONT                            ; Branch if OK
            BRW     ERR                             ; Branch to print error message
     CONT:  .ENDM   REPLACE                         ;* End of REPLACE macro

            .SHOW   BINARY                          ; Include binary in listings

            .SBTTL  Data area
            .PSECT  _DCLPATCH_DATA,NOEXE,WRT,LONG,SHR
    ;
    ;***  File Access Block for input
    ;
    INFAB:          $FAB    FNM=, -            ; File name
                            DNM=<SYS$SYSTEM:DCL.EXE>,-      ; Default name
                            FAC=, -            ; File Access (GET only)
                            SHR=, -            ; Allow others to read also
                            XAB=INXAB               ; eXtended attribute block
    ;
    ;***  Record Access Block for input
    ;
    INRAB:          $RAB    FAB=INFAB, -            ; The File Access Block
                            RAC=SEQ, -              ; Record Access is sequential
                            USZ=512                 ; The max size of input record
    INXAB:          $XABFHC                         ; XAB - File Header Chars
    ;
    ;
    ;***  File Access Block for output
    ;
    OUTFAB:         $FAB    FNM=<SYS$DISK:[]DCL_RECALL.EXE>,-
                            FAC=, -            ; File Access (GET only)
                            FOP=MXV, -              ; Maximize Version number
                            RFM=FIX, -              ; VARiable length records
                            MRS=512, -              ; Maximum record size
                            ORG=SEQ                 ; SEQuential organization
    ;
    ;***  Record Access Block for output
    ;
    OUTRAB:         $RAB    FAB=OUTFAB, -           ; The File Access Block
                            RAC=SEQ, -              ; Record Access is sequential
                            RSZ=512                 ; Record size is 512 bytes

    DCL_IMAGE:      .LONG   0                       ; Holds address of GET_VM mem.
    IMAGE_SIZE:     .LONG   0                       ; Size of the image in bytes
    ;
    ;  The DCL instructions to replace.
    ;
    NEW_C_RECALLMAX = 62                            ; New limit is 62 commands

    ;+
    ;
    ;  The sections below include the AXP instruction sequences that are to
    ;  be modified, followed by the actual new values.  The AXP listings came
    ;  from the DCL source listings CD for OpenVMS AXP V1.0.
    ;
    ;-
    .IF NE DO_ALPHA                         ; The AXP sections....
    ;A30AFFC0     0FB0              LDL     R24, -64(R10)   ; 003517
    ;4B0070D8     0FB4              EXTBL   R24, 3, R24
    ;4302B530     0FB8              SUBQ    R24, 21, R16
    ;E61FFF06     0FBC              BEQ     R16, 22_30$     ; 003519
    ;43C1153E     0FC0              SUBQ    SP, 8, SP       ; 003521

    OINST1:         .LONG   ^X4302B530
                    OINST1_L = .-OINST1

    NINST1:         .LONG   ^X430C9530      ; 21 -> 100
                    NINST1_L = .-NINST1

    ;010000
    ;11000  24
    ;00010101       21      =>
    ;
    ;01100100       100
    ;11111111       255

    ;1  Bit 12 indicates that it is a literal

    ; 0101 0011 0000
    ;

    ;A2EAFFC0     13E0              LDL     R23, -64(R10)           ; 003439
    ;4AE070D7     13E4              EXTBL   R23, 3, R23
    ;42E2B530     13E8              SUBQ    R23, 21, R16
    ;E61FFDEC     13EC              BEQ     R16, END_OF_LIST        ; 003441

    OINST2:         .LONG   ^X42E2B530
                    OINST2_L = .-OINST2

    NINST2:         .LONG   ^X42EC9530      ; 21 -> 100
                    NINST2_L = .-NINST2

    ;A34AFFC0     1450              LDL     R26, -64(R10)
    ;4B4070DA     1454              EXTBL   R26, 3, R26
    ;4342B530     1458              SUBQ    R26, 21, R16
    ;E61FFDCE     145C              BEQ     R16, 19_20$             ; 003454

    OINST3:         .LONG   ^X4342B530
                    OINST3_L = .-OINST3

    NINST3:         .LONG   ^X434C9530      ; 21 -> 100
                    NINST3_L = .-NINST3

    ;47E0341A     1FD4              BIS     R31, 1, R26             ; 004209
    ;40229530     1FD8              SUBQ    R1, 20, R16             ; 004208
    ;402293B1     1FDC              CMPULT  R1, 20, R17
    ;461F04DA     1FE0              CMOVNE  R16, R31, R26           ; 004209

    OINST4:         .LONG   ^X40229530
                    .LONG   ^X402293B1
                    OINST4_L = .-OINST4

    NINST4:         .LONG   ^X402C7530
                    .LONG   ^X402C73B1
                    NINST4_L = .-NINST4

    ;47E29406     2078              BIS     R31, 20, R6
    ;F120005E     207C              BLBS    R9, 32_50$              ; 004236
    ;45205017     2080              AND     R9, 2, R23              ; 004237

    OINST5:         .LONG   ^X47E29406
                    OINST5_L = .-OINST5

    NINST5:         .LONG   ^X47EC7406
                    NINST5_L = .-NINST5

    ;43C1153E     20C0              SUBQ    SP, 8, SP               ; 004248
    ;47E29409     20C4              BIS     R31, 20, R9             ; 004247
    ;B7FE0000     20C8              STQ     R31, (SP)               ; 004248

    OINST6:         .LONG   ^X47E29409
                    OINST6_L = .-OINST6

    NINST6:         .LONG   ^X47EC7409
                    NINST6_L = .-NINST6

    OINST8:         .LONG   ^X43063530
                    OINST8_L = .-OINST8

    NINST8:         .LONG   ^X43041530
                    NISTN8_L = .-NINST8

    OINST10:        .LONG   ^X239F2F32
                    OINST10_L =.-OINST10

    NINST10:        .LONG   ^X239F2F31
                    NINST10_L =.-NINST10

    ;
    ;  The RECALL display code.  Same basic modification as for the VAX.
    ;
    OINST9:         .LONG   ^X2F820000      ; LDQ_U R28,(R2)
                    .LONG   ^X22DF2F31      ; LDA   R22, 12081(R31)
                    .LONG   ^X4AC2037A      ; INSWL R22, R2, R26
                    .LONG   ^X4B82025C      ; MSKWL R28, R2, R28

                    .LONG   ^X479A041C      ; BIS   R28, R26, R28
                    .LONG   ^XF0400036      ; BLBS  R2, $L51
                    .LONG   ^X3F820000      ; $L52: STQ_U R28, (R2)
                    .LONG   ^X47FF041F      ; NOP
                    OINST9_L = .-OINST9

    NINST9:
                    .LONG   ^XA3420000      ; LDL   R26, (R2)
                    .LONG   ^X22DF09FF      ; LDA   R22, 2559(R31)
                    .LONG   ^X4356013A      ; SUBL  R26, R22, R26
                    .LONG   ^XB3420000      ; STL   R26, (R2)

                    .LONG   ^X2FFE0000      ; LNOP
                    .LONG   ^X47FF041F      ; NOP
                    .LONG   ^X47FF041F      ; NOP
                    .LONG   ^X47FF041F      ; NOP
                    NINST9_L = .-NINST9

    ;+
    ;
    ;  The sections below contain the VAX instructions that are to be replaced.
    ;  The values are stored as hexadecimal values for the MACRO-32 compiler,
    ;  which would produce AXP object code, not VAX object code.  To enhance
    ;  readability, the original VAX instructions are still included for
    ;  assembling on the VAX.
    ;
    ;-
    .IFF                                    ;Producing VAX version.....
    .IF DEFINED EVAX                                        ;Compiling for AXP....
    OINST1:         .LONG   ^X15C3AA91
    OINST1_L = 4
    NINST1:         .LONG   ^X3FC3AA91
    NINST1_L = 4
    .IFF                                                    ;Assembling for VAX....
    OINST1:         CMPB    B^WRK_B_RECALLCNT(R10),-        ;Old instruction
                            S^#WRK_C_RECALLMAX+1            ;... (occurs 3 times)
                    OINST1_L = .-OINST1                     ;... (calc inst. length)
    NINST1:         CMPB    B^WRK_B_RECALLCNT(R10),-        ;New instruction
                            S^#NEW_C_RECALLMAX+1            ;...
                    NINST1_L = .-NINST1                     ;...
    .ENDC
                    ASSUME  OINST1_L EQ NINST1_L            ;Ensure equal lengths

    .IF DEFINED EVAX                                        ;Compiling for AXP....
    OINST2:         .BYTE   ^XD1,^X51,^X14
    OINST2_L = 3
    NINST2:         .BYTE   ^XD1,^X51,^X3E
    NINST2_L = 3
    .IFF                                                    ;Assembling for VAX....
    OINST2:         CMPL    R1,S^#WRK_C_RECALLMAX           ;Old instruction 2
                    OINST2_L = .-OINST2                     ;...
    NINST2:         CMPL    R1,S^#NEW_C_RECALLMAX           ;...
                    NINST2_L = .-NINST2                     ;...
    .ENDC
                    ASSUME  OINST2_L EQ NINST2_L            ;...

    .IF DEFINED EVAX                                        ;Compiling for AXP....
    OINST3:         .BYTE   ^XD0,^X14,^X56
    OINST3_L = 3
    NINST3:         .BYTE   ^XD0,^X3E,^X56
    NINST3_L = 3
    .IFF                                                    ;Assembling for VAX....
    OINST3:         MOVL    S^#WRK_C_RECALLMAX,R6           ;Old instruction 3
                    OINST3_L = .-OINST3                     ;...
    NINST3:         MOVL    S^#NEW_C_RECALLMAX,R6           ;...
                    NINST3_L = .-NINST3                     ;...
    .ENDC
                    ASSUME  OINST3_L EQ NINST3_L            ;...

    .IF DEFINED EVAX                                        ;Compiling for AXP....
    OINST4:         .BYTE   ^XD0,^X14,^X59
    OINST4_L = 3
    NINST4:         .BYTE   ^XD0,^X3E,^X59
    NINST4_L = 3
    .IFF                                                    ;Assembling for VAX....
    OINST4:         MOVL    S^#WRK_C_RECALLMAX,R9           ;Old instruction 4
                    OINST4_L = .-OINST4                     ;...
    NINST4:         MOVL    S^#NEW_C_RECALLMAX,R9           ;...
                    NINST4_L = .-NINST4                     ;...
    .ENDC
                    ASSUME  OINST4_L EQ NINST4_L            ;...
    ;
    ;  DEC's RECALL code that is replaced
    ;
    .IF DEFINED EVAX                                        ;Compiling for AXP....
    OINST5:         .LONG   ^X12316291
                    .LONG   ^X328FB007
                    .LONG   ^X0511622F
                    .LONG   ^X2F318FB0
                    .BYTE   ^X62
    OINST5_L = .-OINST5
    NINST5:         .LONG   ^X12206291
                    .LONG   ^X62309003
                    .LONG   ^X2F906296
                    .LONG   ^X010101A2
                    .BYTE   ^X01
    NINST5_L = .-NINST5
    .IFF                                                    ;Assembling for VAX....
    OINST5:         CMPB    (R2),#^A/1/             ; Is tens digit a "1"?
                    BNEQ    10$                     ; Branch if not
                    MOVW    #^A"2/",(R2)            ; Move "2/" into command buffer
                    BRB     20$
            10$:    MOVW    #^A"1/",(R2)            ; Move "1/" into command buffer
            20$:
                    OINST5_L = .-OINST5
    NINST5:         CMPB    (R2),#^A/ /             ; Is the tens digit " "?
                    BNEQU   10$                     ; Branch if not
                    MOVB    #^A/0/,(R2)             ; Move a "0" in
            10$:    INCB    (R2)                    ; Bump tens digit
                    MOVB    #^A"/",1(R2)            ; Move "/" in after tens digit
                    NOP                             ; Use NOPs to blank out old
                    NOP                             ; ... code
                    NOP
                    NINST5_L = .-NINST5
    .ENDC
                    ASSUME  OINST5_L EQ NINST5_L
    .ENDC                                           ; End of .IF NE DO_ALPHA

                   .ALIGN  LONG
    PATCH_ADDR_MSG: .ASCID  /Patching at image address !XL/
                    .ALIGN  LONG

    MSGBUF_L = 256
    MSGBUF:         .WORD   MSGBUF_L                ; Buffer for messages
                    .BYTE   DSC$K_DTYPE_T           ; ...  Text string
                    .BYTE   DSC$K_CLASS_S           ; ...  Static string
                    .ADDRESS .+4                    ; ...  Buffer follows
                    .BLKB   MSGBUF_L                ; The actual output buffer

            .SBTTL  DCLPATCH main routine

            .PSECT  _DCLPATCH_CODE,EXE,NOWRT,LONG,PIC,SHR
            .ENTRY  DCLPATCH,^M<R2,R3,R4,R5,R6,R7,R8,R9,R10,R11>

            PRINT   
    .IF NE DO_ALPHA
            PRINT   
    .ENDC

            BSBW    READ_OLD_IMAGE                  ; Go open the image
    ;
    ;  Now do a search and replace for each of the instructions.
    ;
            PRINT   -
     <Replacing "CMPB WRK_B_RECALLCNT(R10),#WRK_C_RECALLMAX+1" (3 occurrences)....>
    .IF NE DO_ALPHA
            REPLACE #OINST1_L,OINST1,NINST1,#1,10$  ; Go replace instruction
            REPLACE #OINST2_L,OINST2,NINST2,#1,10$  ; Go replace instruction
            REPLACE #OINST3_L,OINST3,NINST3,#1,10$  ; Go replace instruction
    .IFF
            REPLACE #OINST1_L,OINST1,NINST1,#3,10$  ; Go replace instruction
    .ENDC

            PRINT   <Replacing "CMPL R1,#WRK_C_RECALLMAX" (1 occurrence)....>
    .IF NE DO_ALPHA
            REPLACE #OINST4_L,OINST4,NINST4,#1,10$  ; Go replace instruction
    .IFF
            REPLACE #OINST2_L,OINST2,NINST2,#1,10$  ; Go replace instruction
    .ENDC

            PRINT   <Replacing "MOVL #WRK_C_RECALLMAX,R6" (1 occurrence)....>
    .IF NE DO_ALPHA
            REPLACE #OINST5_L,OINST5,NINST5,#1,10$  ; Go replace instruction
    .IFF
            REPLACE #OINST3_L,OINST3,NINST3,#1,10$  ; Go replace instruction
    .ENDC

            PRINT   <Replacing "MOVL #WRK_C_RECALLMAX,R9" (1 occurrence)....>
    .IF NE DO_ALPHA
            REPLACE #OINST6_L,OINST6,NINST6,#1,10$  ; Go replace instruction
    .IFF
            REPLACE #OINST4_L,OINST4,NINST4,#1,10$  ; Go replace instruction
    .ENDC

    .IF NE DO_ALPHA
            PRINT   
            REPLACE #OINST8_L,OINST8,NINST8,#1,10$

            PRINT   
            REPLACE #OINST9_L,OINST9,NINST9,#1,10$

            PRINT   
            REPLACE #OINST10_L,OINST10,NINST10,#1,10$
    .IFF
            PRINT   
            REPLACE #OINST5_L,OINST5,NINST5,#1,10$  ; Go replace instructions
    .ENDC

            PRINT     ; Print info message
            BSBW    WRITE_NEW_IMAGE                 ; Go create the "patched" image
            BLBC    R0,20$                          ; Branch if not successful
            PRINT   
            BRB     20$                             ; Branch to return to DCL

     10$:   PRINT   <Error; invalid number of occurrences detected>
            PRINT   

     20$:   PUSHL   R0                              ; Save the status
            $CLOSE  FAB=INFAB                       ; Close the input file
            POPL    R0                              ; Restore the status

     30$:   RET                                     ; Return to caller

    ;+
    ;
    ;  Function:    REPLACE_STREAM
    ;
    ;  Functional description:
    ;
    ;       This internal subroutine searches for all occurrences of a stream
    ;       of bytes and replaces the stream with a new stream of bytes.
    ;
    ;       It is assumed that the streams are the same length.
    ;
    ;  Inputs:
    ;
    ;       R5      - Length of stream to find/replace
    ;       R6      - Address of stream of bytes to find
    ;       R7      - Address of stream of replacement bytes
    ;
    ;  Outputs:
    ;
    ;       R0      - Number of replacements made
    ;
    ;-
    REPLACE_STREAM:
    .IIF DF,EVAX,   .JSB_ENTRY
            PUSHR   #^M<R1,R2,R3,R4,R5,R6,R7,R8,R11>
            MOVL    DCL_IMAGE,R4                    ; Point to DCL image
            MOVL    IMAGE_SIZE,R3                   ; R3 = # of blocks to check
            MULL2   #512,R3                         ; R3 = # of bytes to check
            CLRL    R11                             ; Clear # of matches
     10$:   MOVL    R6,R2                           ; Move instruction to R2
    ;
    ;  Look for the stream of bytes.
    ;
     20$:   CMPB    (R2),(R4)+                      ; Found first byte?
            BEQL    40$                             ; Branch if so
     30$:   SOBGTR  R3,20$                          ; Decrement # of bytes to search
            BRW     70$                             ; Branch to return
    ;
    ;  The first byte has been matched.  Check to see if all the others match.
    ;
     40$:   DECL    R3                              ; Decrement # of bytes
            BEQL    70$                             ; Branch if no more image bytes
            MOVL    R5,R0                           ; Get length of instruction
            DECL    R0                              ; Don't count byte just found
            MOVL    #1,R1                           ; Init index value

     50$:   CMPB    (R2)[R1],(R4)+                  ; Check each additional byte
            BNEQ    30$                             ; Branch if not the same
            DECL    R3                              ; Decrement this byte
            BEQL    70$                             ; Branch if no more image bytes
            INCL    R1                              ; Bump index value
            SOBGTR  R0,50$                          ; Loop until no more bytes
    ;
    ;  Here we found an occurrence of the string (all bytes matched).
    ;
            MOVW    #MSGBUF_L,MSGBUF                ; Reset length of output buffer
            SUBL3   DCL_IMAGE,R4,R0                 ; R0 = virtual address
            SUBL2   R5,R0                           ; R0 -- offset in DCL_IMAGE
            SUBL2   #512,R0                         ; Account for header
            $FAO_S  CTRSTR=PATCH_ADDR_MSG,-         ; Format the output string
                    OUTBUF=MSGBUF,-                 ; ...
                    OUTLEN=MSGBUF,-                 ; ...
                    P1=R0                           ; ...
            PUSHAQ  MSGBUF                          ; Print the string out
            CALLS   #1,G^LIB$PUT_OUTPUT             ; ...
    ;
    ;  Now replace the old stream with the new stream of bytes.
    ;
            SUBL2   R5,R4                           ; R4 -> beginning of string
            MOVL    R5,R0                           ; Copy length to counter
            MOVL    R7,R2                           ; R2 -> replacement bytes
     60$:   MOVB    (R2)+,(R4)+                     ; Copy the new byte
            SOBGTR  R0,60$                          ; Loop until no more bytes
            INCL    R11                             ; Increment # of matches
            BRW     10$                             ; Branch to continue search

     70$:   MOVL    R11,R0                          ; Return # of matches as status
            POPR    #^M<R1,R2,R3,R4,R5,R6,R7,R8,R11>
            RSB                                     ; Return to caller

    ;+
    ;
    ;  Function:    READ_OLD_IMAGE
    ;
    ;  Functional description:
    ;
    ;       Opens image file described by INFAB, allocates enough virtual memory
    ;       to contain the whole file, and reads the whole file into memory.
    ;
    ;  Inputs:
    ;
    ;       INFAB, INRAB, INXAB, DCL_IMAGE
    ;
    ;  Outputs:
    ;
    ;       R0              - RMS Status
    ;       DCL_IMAGE       - Address of allocated memory
    ;       IMAGE_SIZE      - The size of the file (in blocks)
    ;
    ;-
    READ_OLD_IMAGE:
    .IIF DF,EVAX,   .JSB_ENTRY
            $OPEN   FAB=INFAB                       ; Open the image file
            ON_ERR  50$                             ; Branch on error
            $CONNECT RAB=INRAB                      ; Connect the RAB
            BLBC    R0,40$                          ; Branch on error

            MOVL    INXAB+XAB$L_EBK,R0              ; Get size of file in blocks
            MULL2   #512,R0                         ; Get size in bytes
            PUSHL   R0                              ; Push onto the stack
            PUSHAL  DCL_IMAGE                       ; Allocate some P0 space
            PUSHAL  4(SP)                           ; ... to hold entire file
            CALLS   #2,G^LIB$GET_VM                 ; Go allocate the memory
            POPL    R1                              ; Pop size off stack
            BLBC    R0,40$                          ; Branch on error
    ;
    ;  Read the whole file into one big buffer.
    ;
            MOVAL   INRAB,R6                        ; R6 -> input file RAB
            MOVL    DCL_IMAGE,RAB$L_UBF(R6)         ; Start reading into DCL_IMAGE
            CLRL    R7                              ; Clear # of blocks
     10$:   $GET    RAB=(R6)                        ; Read a record
            BLBS    R0,20$                          ; Branch if successful
            CMPL    #RMS$_EOF,R0                    ; Was it EOF?
            BEQL    30$                             ; Branch if so
            BRW     40$                             ; Branch to report other error
     20$:   ADDL2   #512,RAB$L_UBF(R6)              ; Bump buffer address to next
            INCL    R7                              ; ... block (and counter)
            BRB     10$                             ; Branch to read next block
     30$:   TSTL    R7                              ; Was anything read?
            BEQL    40$                             ; ...
            MOVL    R7,IMAGE_SIZE                   ; # of blocks actually read
            MOVL    #SS$_NORMAL,R0                  ; Set success status
     40$:   PUSHL   R0                              ; Save status
            $CLOSE  FAB=INFAB                       ; Close the input file
            POPL    R0                              ; Restore the status
     50$:   RSB                                     ; Return to caller

    ;+
    ;
    ;  Function:    WRITE_NEW_IMAGE
    ;
    ;  Functional description:
    ;
    ;       Creates image file described by OUTFAB and writes data in allocated
    ;       memory to the file (in 512-byte (block) chunks).
    ;
    ;  Inputs:
    ;
    ;       OUTFAB, OUTFAB, DCL_IMAGE, IMAGE_SIZE
    ;
    ;  Outputs:
    ;
    ;       R0      - RMS Status
    ;
    ;-
    WRITE_NEW_IMAGE:
    .IIF DF,EVAX,   .JSB_ENTRY
            $CREATE FAB=OUTFAB                      ; Create the output file
            BLBC    R0,30$                          ; Branch on error
            $CONNECT RAB=OUTRAB                     ; Connect the RAB
            BLBC    R0,20$                          ; Branch on error

            MOVAL   OUTRAB,R6                       ; R6 -> output file RAB
            MOVL    DCL_IMAGE,RAB$L_RBF(R6)         ; Start reading into DCL_IMAGE
            MOVL    IMAGE_SIZE,R7                   ; Initialize # of blocks

     10$:   $PUT    RAB=(R6)                        ; Write a block out
            BLBC    R0,20$                          ; Branch on error
            ADDL2   #512,RAB$L_RBF(R6)              ; ...
            SOBGTR  R7,10$                          ; Loop until all finished

     20$:   PUSHL   R0                              ; Save status
            $CLOSE  FAB=INFAB                       ; Close the input file
            POPL    R0                              ; Restore the status
     30$:   RSB                                     ; Return to caller

            .END    DCLPATCH

