## OpenVMS RTL String Manipulation(STR$)Manual

Order Number: AA–PV6MD–TK


**April 2001**


This manual documents the string manipulation routines contained in
the STR$ facility of the OpenVMS Run-Time Library.


**Revision/Update Information:** This manual supersedes the _OpenVMS_
_RTL String Manipulation (STR$)_
_Manual_, OpenVMS Alpha Version 7.1
and OpenVMS VAX Version 7.1.


**Software Version:** OpenVMS Alpha Version 7.3
OpenVMS VAX Version 7.3


**Compaq Computer Corporation**
**Houston, Texas**


© 2001 Compaq Computer Corporation


Compaq, VAX, VMS, and the Compaq logo Registered in U.S. Patent and Trademark Office.


OpenVMS is a trademark of Compaq Information Technologies Group, L.P. in the United States and
other countries.


All other product names mentioned herein may be trademarks of their respective companies.


Confidential computer software. Valid license from Compaq required for possession, use, or copying.
Consistent with FAR 12.211 and 12.212, Commercial Computer Software, Computer Software
Documentation, and Technical Data for Commercial Items are licensed to the U.S. Government
under vendor’s standard commercial license.


Compaq shall not be liable for technical or editorial errors or omissions contained herein. The
information in this document is provided "as is" without warranty of any kind and is subject
to change without notice. The warranties for Compaq products are set forth in the express
limited warranty statements accompanying such products. Nothing herein should be construed as
constituting an additional warranty.


ZK5936


The Compaq _OpenVMS_ documentation set is available on CD-ROM.


This document was prepared using DECdocument, Version 3.3-1b.


### **Contents**

- [Preface](#preface)


**Part I** **STR$ Tutorial Section**


**1** **Run-Time Library String Manipulation (STR$) Facility**


- [1.1 Overview](#11-overview)
- 1.1.1 64-Bit Addressing Support (Alpha Only)


**2** **Introduction to String Manipulation (STR$) Routines**


- [2.1 String Semantics in the Run-Time Library](#21-string-semantics-in-the-run-time-library)
- 2.1.1 Fixed-Length Strings
- 2.1.2 Varying-Length Strings
- 2.1.3 Dynamic-Length Strings
- 2.1.4 Examples
- [2.2 Descriptor Classes and String Semantics](#22-descriptor-classes-and-string-semantics)
- 2.2.1 Conventions for Reading Input String Arguments
- 2.2.2 Semantics for Writing Output String Arguments
- [2.3 Selecting String Manipulation Routines](#23-selecting-string-manipulation-routines)
- 2.3.1 Efficiency
- 2.3.2 Argument Passing
- 2.3.3 Error Handling
- [2.4 Allocating Resources for Dynamic Strings](#24-allocating-resources-for-dynamic-strings)
- 2.4.1 String Zone


**Part II** **STR$ Reference Section**


- [STR$ADD](#stradd-add-two-decimal-strings)

- [STR$ANALYZE_SDESC](#stranalyze_sdesc-analyze-string-descriptor)

- [STR$ANALYZE_SDESC_64 (Alpha only)](#stranalyze_sdesc_64-alpha-only-analyze-string-descriptor)

- [STR$APPEND](#strappend-append-string)

- [STR$CASE_BLIND_COMPARE](#strcase_blind_compare-compare-strings-without-regard-to-case)

- [STR$COMPARE](#strcompare-compare-two-strings)

- [STR$COMPARE_EQL](#strcompare_eql-compare-two-strings-for-equality)

- [STR$COMPARE_MULTI](#strcompare_multi-compare-two-strings-for-equality-using-multinational-character-set)

- [STR$CONCAT](#strconcat-concatenate-two-or-more-strings)

- [STR$COPY_DX](#strcopy_dx-copy-a-source-string-passed-by-descriptor-to-a-destination-string)

- [STR$COPY_R](#strcopy_r-copy-a-source-string-passed-by-reference-to-destination-string)

- [STR$COPY_R_64 (Alpha Only)](#strcopy_r_64-alpha-only-copy-a-source-string-passed-by-reference-to-destination-string)

- [STR$DIVIDE](#strdivide-divide-two-decimal-strings)

- [STR$DUPL_CHAR](#strdupl_char-duplicate-character-n-times)


iii


- [STR$ELEMENT](#strelement-extract-delimited-element-substring)

- [STR$FIND_FIRST_IN_SET](#strfind_first_in_set-find-first-character-in-a-set-of-characters)

- [STR$FIND_FIRST_NOT_IN_SET](#strfind_first_not_in_set-find-first-character-that-does-not-occur-in-set)

- [STR$FIND_FIRST_SUBSTRING](#strfind_first_substring-find-first-substring-in-input-string)

- [STR$FREE1_DX](#strfree1_dx-free-one-dynamic-string)

- [STR$GET1_DX](#strget1_dx-allocate-one-dynamic-string)

- [STR$GET1_DX_64 (Alpha Only)](#strget1_dx_64-alpha-only-allocate-one-dynamic-string)

- [STR$LEFT](#strleft-extract-a-substring-of-a-string)

- [STR$LEN_EXTR](#strlen_extr-extract-a-substring-of-a-string)

- [STR$MATCH_WILD](#strmatch_wild-match-wildcard-specification)

- [STR$MUL](#strmul-multiply-two-decimal-strings)

- [STR$POSITION](#strposition-return-relative-position-of-substring)

- [STR$POS_EXTR](#strpos_extr-extract-a-substring-of-a-string)

- [STR$PREFIX](#strprefix-prefix-a-string)

- [STR$RECIP](#strrecip-reciprocal-of-a-decimal-string)

- [STR$REPLACE](#strreplace-replace-a-substring)

- [STR$RIGHT](#strright-extract-a-substring-of-a-string)

- [STR$ROUND](#strround-round-or-truncate-a-decimal-string)

- [STR$TRANSLATE](#strtranslate-translate-matched-characters)

- [STR$TRIM](#strtrim-trim-trailing-blanks-and-tabs)

- [STR$UPCASE](#strupcase-convert-string-to-all-uppercase-characters)


**Index**


**Tables**


- 1–1 STR$ Mathematical Operation Routines
- 1–2 STR$ Compare Routines
- 1–3 STR$ Extract and Replace Routines
- 1–4 STR$ Append and Concatenate Routines
- 1–5 STR$ Copy Routines

- 1–6 STR$ Search Routines

- 1–7 STR$ Allocate and Deallocate Routines

- 1–8 STR$ Miscellaneous Routines

- 2–1 String Passing Techniques Used by the Run-Time Library
- 2–2 How Run-Time Library Routines Read Strings
- 2–3 Output String Semantics and Descriptor Classes
- 2–4 Severe Errors, by Facility
- 2–5 String Zone Attributes


iv


### **Preface**

This manual provides users of the OpenVMS operating system with detailed
usage and reference information about the string manipulation routines supplied
in the STR$ facility of the Run-Time Library.

#### **Intended Audience**


This manual is intended for system and application programmers who write
programs that call STR$ Run-Time Library routines.

#### **Document Structure**


This manual is organized into two parts as follows:


      - Part I is a tutorial, structured as follows:


Chapter 1 provides a brief overview of the STR$ routines and lists the
routines and their functions.


Chapter 2 discusses in detail how to use the Run-Time Library STR$
routines.


      - Part II provides detailed reference information on each routine contained
in the STR$ facility of the Run-Time Library. This information is presented
using the documentation format described in _OpenVMS Programming_
_Concepts Manual_ . Routine descriptions appear in alphabetical order by
routine name.

#### **Related Documents**


The Run-Time Library routines are documented in a series of reference manuals.
A description of how the Run-Time Library routines are accessed and of the
OpenVMS features and functionality available through calls to the STR$
Run-Time Library appear in the _OpenVMS Programming Concepts Manual_ .
Descriptions of other RTL facilities and their corresponding routines and usages
are discussed in the following books:


      - _Compaq Portable Mathematics Library_


      - _OpenVMS VAX RTL Mathematics (MTH$) Manual_


      - _OpenVMS RTL DECtalk (DTK$) Manual_ [1]


      - _OpenVMS RTL Library (LIB$) Manual_


      - _OpenVMS RTL General Purpose (OTS$) Manual_


      - _OpenVMS RTL Parallel Processing (PPL$) Manual_ [1]


1 This manual has been archived but is available on the OpenVMS Documentation
CD-ROM.


v


      - _OpenVMS RTL Screen Management (SMG$) Manual_


The _Guide to the POSIX Threads Library_ contains guidelines and reference
information for Compaq POSIX Threads [2], the Compaq Multithreading Run-Time
Library.


The _OpenVMS Calling Standard_ contains useful information for anyone who
needs to call Run-Time Library routines.


Application programmers using any programming language can refer to the _Guide_
_to Creating OpenVMS Modular Procedures_ for writing modular and reentrant
code.


High-level language programmers will find additional information on calling
Run-Time Library routines in their language reference manual. Additional
information may also be found in the language user’s guide provided with your
OpenVMS language software.


For a complete list and description of the manuals in the OpenVMS
documentation set, see the _OpenVMS Version 7.3 New Features and_
_Documentation Overview_ .


For additional information about Compaq _OpenVMS_ products and services, access
the Compaq website at the following location:

```
        http://www.openvms.compaq.com/

#### **Reader’s Comments**

```

Compaq welcomes your comments on this manual. Please send comments to
either of the following addresses:


Internet **openvmsdoc@compaq.com**


Mail Compaq Computer Corporation
OSSG Documentation Group, ZKO3-4/U08
110 Spit Brook Rd.
Nashua, NH 03062-2698

#### **How To Order Additional Documentation**


Use the following World Wide Web address to order additional documentation:

```
        http://www.openvms.compaq.com/

```

If you need help deciding which documentation best meets your needs, call
800-282-6672.


2 Compaq POSIX Threads was formerly called DECthreads.


vi


#### **Conventions**

The following conventions are used in this manual:


Ctrl/ _x_ A sequence such as Ctrl/ _x_ indicates that you must hold down
the key labeled Ctrl while you press another key or a pointing
device button.


PF1 _x_ A sequence such as PF1 _x_ indicates that you must first press
and release the key labeled PF1 and then press and release
another key or a pointing device button.


Return In examples, a key name enclosed in a box indicates that
you press a key on the keyboard. (In text, a key name is not
enclosed in a box.)


In the HTML version of this document, this convention appears
as brackets, rather than a box.


. . . A horizontal ellipsis in examples indicates one of the following
possibilities:


                  - Additional optional arguments in a statement have been
omitted.


                  - The preceding item or items can be repeated one or more
times.


                  - Additional parameters, values, or other information can be
entered.



.

.

.



A vertical ellipsis indicates the omission of items from a code
example or command format; the items are omitted because
they are not important to the topic being discussed.



( ) In command format descriptions, parentheses indicate that you
must enclose choices in parentheses if you specify more than

one.


[ ] In command format descriptions, brackets indicate optional
choices. You can choose one or more items or no items.
Do not type the brackets on the command line. However,
you must include the brackets in the syntax for OpenVMS
directory specifications and for a substring specification in an
assignment statement.


{ } In command format descriptions, braces indicate a required
choice of options; you must choose one of the items listed. Do
not type the braces on the command line.


**bold text** This typeface represents the introduction of a new term. It
also represents the name of an argument, an attribute, or a

reason.


_italic text_ Italic text indicates important information, complete titles
of manuals, or variables. Variables include information that
varies in system output (Internal error _number_ ), in command
lines (/PRODUCER= _name_ ), and in command parameters in
text (where _dd_ represents the predefined code for the device
type).


UPPERCASE TEXT Uppercase text indicates a command, the name of a routine,
the name of a file, or the abbreviation for a system privilege.


vii


`Monospace text` Monospace type indicates code examples and interactive screen
displays.


In the C programming language, monospace type in text
identifies the following elements: keywords, the names
of independently compiled external functions and files,
syntax summaries, and references to variables or identifiers
introduced in an example.


A hyphen at the end of a command format description,
command line, or code line indicates that the command or
statement continues on the following line.


numbers All numbers in text are assumed to be decimal unless
otherwise noted. Nondecimal radixes—binary, octal, or
hexadecimal—are explicitly indicated.



viii


# **Part I**

### **STR$ Tutorial Section**

This part of the _OpenVMS RTL String Manipulation (STR$) Manual_ contains a
tutorial for the OpenVMS RTL String Manipulation (STR$) facility.


The material is structured as follows:


Chapter 1 provides a brief overview of the STR$ routines and lists the
routines and their functions.


Chapter 2 discusses in detail how to use the Run-Time Library STR$
routines.


# **1**

### **Run-Time Library String Manipulation (STR$)** **Facility**

This chapter contains an overview of the STR$ facility and lists the routines
and their functions. Chapter 2 explains in detail how the STR$ facility handles
strings. The STR$ Reference Section describes all the STR$ routines.

#### **1.1 Overview**


The STR$ facility provides routines to perform the following functions:


      - Perform mathematical operations on strings (see Table 1–1)


      - Compare strings (see Table 1–2)


      - Extract and replace substrings (see Table 1–3)


      - Append and concatenate strings (see Table 1–4)


      - Copy strings (see Table 1–5)


      - Search for characters and substrings (see Table 1–6)


      - Free and allocate dynamic strings (see Table 1–7)


      - Perform miscellaneous functions on strings (see Table 1–8)


**Table 1–1 STR$ Mathematical Operation Routines**


**Routine Name** **Function**


STR$ADD Add two decimal strings


STR$DIVIDE Divide two decimal strings


STR$MUL Multiply two decimal strings


STR$RECIP Return the reciprocal of a decimal string


STR$ROUND Round or truncate a decimal string


Run-Time Library String Manipulation (STR$) Facility **1–1**


**Run-Time Library String Manipulation (STR$) Facility**
**1.1 Overview**


**Table 1–2 STR$ Compare Routines**


**Routine Name** **Function**


STR$CASE_BLIND_COMPARE Compare strings without regard to case


STR$COMPARE Compare two strings


STR$COMPARE_EQL Compare two strings for equality


STR$COMPARE_MULTI Compare two strings for equality using the DEC
Multinational Character Set


**Table 1–3 STR$ Extract and Replace Routines**


**Routine Name** **Function**


STR$ELEMENT Extract delimited element substring


STR$LEFT Extract a substring of a string


STR$LEN_EXTR Extract a substring of a string


STR$POS_EXTR Extract a substring of a string


STR$REPLACE Replace a substring


STR$RIGHT Extract a substring of a string


**Table 1–4 STR$ Append and Concatenate Routines**


**Routine Name** **Function**


STR$APPEND Append a string


STR$CONCAT Concatenate two or more strings


STR$PREFIX Prefix a string


**Table 1–5 STR$ Copy Routines**


**Routine Name** **Function**


STR$COPY_DX Copy a source string passed by descriptor to a
destination string


STR$COPY_R Copy a source string passed by reference to a
destination string


       - STR$COPY_R_64 Copy a source string passed by reference to a
destination string


          - Alpha specific.


**1–2** Run-Time Library String Manipulation (STR$) Facility


**Run-Time Library String Manipulation (STR$) Facility**
**1.1 Overview**


**Table 1–6 STR$ Search Routines**


**Routine Name** **Function**


STR$FIND_FIRST_IN_SET Find the first character in a set of characters


STR$FIND_FIRST_NOT_IN_SET Find the first character that does not occur in
the set


STR$FIND_FIRST_SUBSTRING Find the first substring in the input string


**Table 1–7 STR$ Allocate and Deallocate Routines**


**Routine Name** **Function**


STR$FREE1_DX Free one dynamic string


STR$GET1_DX Allocate one dynamic string


       - STR$GET1_DX_64 Allocate one dynamic string


          - Alpha specific.


**Table 1–8 STR$ Miscellaneous Routines**


**Routine Name** **Function**


STR$ANALYZE_SDESC Analyze a string descriptor


      - STR$ANALYZE_SDESC_64 Analyze a string descriptor


STR$DUPL_CHAR Duplicate character _n_ times


STR$MATCH_WILD Match a wildcard specification


STR$POSITION Return relative position of a substring


STR$TRANSLATE Translate matched characters


STR$TRIM Trim trailing blanks and tabs


STR$UPCASE Convert string to all uppercase


          - Alpha specific.


**1.1.1 64-Bit Addressing Support (Alpha Only)**


On Alpha systems, the String Manipulation (STR$) routines provide 64-bit virtual
addressing capabilities as follows:


      - All STR$ RTL routines now accept 64-bit addresses for arguments passed by
reference.


      - All STR$ RTL routines also accept either 32-bit or 64-bit descriptors for
arguments passed by descriptor.


      - In some cases a new routine was added to support a 64-bit addressing or
data capability. These routines carry the same name as the original routine
but with a _64 suffix. In general, both versions of the routine support 64-bit
addressing but the routine with the _64 suffix also supports additional 64-bit
capability. The 32-bit capabilities of the original routine are unchanged.


See the _OpenVMS Programming Concepts Manual_ for more information about
64-bit virtual addressing capabilities.


Run-Time Library String Manipulation (STR$) Facility **1–3**


# **2**

### **Introduction to String Manipulation (STR$)** **Routines**

This chapter explains in detail the following topics:


      - Types of strings recognized by Run-Time Library routines


      - Relationship of descriptor classes to string semantics


      - Differences in string handling among the LIB$, OTS$, and STR$ facilities of
the Run-Time Library


      - Conventions for reading and writing string arguments in the Run-Time
Library string routines


      - Selection of the proper string manipulation routines


      - Allocation and deallocation of dynamic string resources


**Descriptor Names and Field Names**

In this chapter and throughout this manual it is generally the practice to use
only the main part of a descriptor name or a descriptor field name, without the
32-bit or 64-bit prefix used in the actual code. For example, the length field is
referred to using LENGTH rather than by mentioning both DSC$W_LENGTH
and DSC64$Q_LENGTH. The complete descriptor or field name, including the
prefix, is used only when referring to one particular form of the descriptor.

#### **2.1 String Semantics in the Run-Time Library**


The **semantics** of a string refers to the conventions that determine how a string
is stored, written, and read. The Alpha and VAX architectures support three
string semantics: fixed length, varying length, and dynamic length.


**2.1.1 Fixed-Length Strings**


Fixed-length strings have the following attributes:


      - An address


      - A length


The length of a fixed-length string is constant. It is usually initialized when
the program is compiled or linked. After initialization, this length is read but
never written. When a Run-Time Library routine copies a source string into a
longer fixed-length destination string, the routine pads the destination string
with trailing blanks.


Introduction to String Manipulation (STR$) Routines **2–1**


**Introduction to String Manipulation (STR$) Routines**
**2.1 String Semantics in the Run-Time Library**


When you pass a string to a Run-Time Library routine, you pass the string by
descriptor. For a fixed-length string, the descriptor must contain this information:


      - The descriptor class


      - The data type of the string


      - The length of the string in bytes


      - The address of the beginning of the string


In most cases, you do not have to construct an actual descriptor. By default,
most OpenVMS Alpha and OpenVMS VAX languages pass strings by descriptor.
For information about how the language you are using handles strings, see
your language reference manual. For more information about descriptors used
for fixed-length strings, refer to _OpenVMS Programming Interfaces: Calling a_
_System Routine_ [1]


**Note**


In contrast to Run-Time Library routines, system services do not
pad output strings. For this reason, when a program calls a system
service that returns a fixed-length string, the program should supply an
additional argument that indicates how many bytes the system service
actually deposited in the fixed-length buffer of the calling program. Some
system service routines have corresponding Run-Time Library routines
that provide the proper semantics for fixed-length, varying-length, and
dynamic output strings.


**2.1.2 Varying-Length Strings**


Varying-length strings have the following attributes:


      - A current length


      - An address


      - A maximum length


The current length, in bytes, of a varying-length string is stored in a two-byte
field, called CURLEN, preceding the text of the string. The address of the string
points to the beginning of this CURLEN field, not to the beginning of the string’s

text.


The maximum string length is a field in the string’s descriptor. This field specifies
how much space is allocated to the string in a program. The maximum string
length is fixed and does not change.


The value in the CURLEN field specifies how many bytes beyond the CURLEN
field are occupied by the string’s text. The character positions beyond this range
are reserved for the growth of the string. Their contents are undefined.


For example, assume a varying string whose CURLEN is 3 and whose maximum
length is 6. If a string `’` ABCD `’` is copied into this string, the result is `’` ABCD `’`
and the CURLEN is changed to 4. If a string `’` XYZ `’` is now copied into the
same varying string, the resulting string is `’` XYZ `’` with a CURLEN of 3. The
maximum length is still 6. The bytes beyond the range designated by CURLEN
are undefined.


1 This manual has been archived but is available on the OpenVMS Documentation
CD-ROM.


**2–2** Introduction to String Manipulation (STR$) Routines


**Introduction to String Manipulation (STR$) Routines**
**2.1 String Semantics in the Run-Time Library**


For varying-length strings pointed to by both 32-bit and 64-bit descriptors,
CURLEN is a two-byte field. Because of this, the maximum length of a varyinglength string is limited to 2 [16]         - 1, or 65,535, characters.


**2.1.3 Dynamic-Length Strings**


Dynamic-length strings have the following attributes:


      - A current length


      - An address pointing to the beginning of the text


Theoretically, dynamic strings have unbounded length. However, the descriptor
LENGTH field contains the length of the string as an unsigned value. This
effectively limits the maximum length of the string to the maximum unsigned
integer value this field can hold.


For 32-bit dynamic descriptors, the LENGTH field is an unsigned value occupying
two bytes. Because its maximum value is 2 [16]        - 1, or 65,535, the maximum length
of a string is limited to 65,535 characters.


On Alpha systems, the LENGTH field of a 64-bit dynamic descriptor is an
unsigned value occupying eight bytes. Because its maximum value is 2 [64]        - 1, the
maximum length of a string is 2 [64]        - 1 characters.


The actual space for a dynamic-length string is allocated from heap storage by
the Run-Time Library. When a Run-Time Library routine copies a character
string into a dynamic string, and the currently allocated heap storage is not large
enough to contain the string, the currently allocated storage returns to a pool of
heap storage maintained by the string routines. Then the string routines obtain
a new area of the correct size. As a result of this process of deallocation and
reallocation, both the current-length field and the address portion of the string’s
descriptor may change. Often, dynamic strings are the most convenient type to
write.


**Note**


The Run-Time Library STR$ routines are the only routines that you
should use to alter the length or address of a dynamic string. Do not use
LIB$GET_VM or LIB$GET_VM_64 for this purpose.


**2.1.4 Examples**


The following examples illustrate what happens when the string `’` ABCDEF `’` (of
length 6) is copied into various destination strings:


      - Fixed-length string


If `’` ABCDEF `’` is copied into a fixed-length string, three results are possible:


1. If the length of the output string is greater than the length of the source
string, the string is padded with trailing spaces.


Length of output string 10


Result `’ABCDEF ’`


Introduction to String Manipulation (STR$) Routines **2–3**


**Introduction to String Manipulation (STR$) Routines**
**2.1 String Semantics in the Run-Time Library**


2. If the length of the output string is the same as that of the input string,
the string is simply copied with no modification.


Length of output string 6


Result `’ABCDEF’`


3. If the length of the output string is less than the length of the source
string, truncation on the right occurs.


Length of output string 3


Result `’ABC’`


      - Varying-length string


If the string `’` ABCDEF `’` is copied into a varying-length string, two results are
possible:


1. If the MAXSTRLEN field of the destination is greater than or equal
to the length of the source, the input string is written into the output
string without modification, and the CURLEN (current length) field of the
output string becomes 6.


2. If the MAXSTRLEN field of the destination is less than the length of the
source string, the source string is truncated on the right and the CURLEN
field is rewritten to its current length. For example, if MAXSTRLEN = 4,
the resulting string contains `’` ABCD `’` and CURLEN = 4.


      - Dynamic-length string


If the string `’` ABCDEF `’` is copied into a dynamic destination string, three
results are possible:


1. If the length of the destination string is greater than the length of the
source string ( 6 ), the result is a dynamic string of length 6 containing
`’` ABCDEF `’` . No padding takes place. The Run-Time Library may
deallocate the string and reallocate a new string closer in length to
the length of the source string.


2. If the length of the destination string is less than the length of the source
string, the result is also `’` ABCDEF `’`, with a length of 6. The Run-Time
Library deallocates the destination string and allocates a new string large
enough to hold the 6 characters.


3. If the destination string and source string are of equal length, a simple
copy is done. No allocation, deallocation, or padding takes place, and the
destination descriptor is not modified.

#### **2.2 Descriptor Classes and String Semantics**


A calling program passes strings to an STR$ routine by descriptor. That is, the
argument list entry for an input or output string is actually the address of a
string descriptor. All STR$ routines handle both 32-bit and 64-bit descriptors in
the argument list.


The calling program allocates a descriptor for the input string that indicates the
string’s address and length, so that the called routine can find the string’s text
and operate on it. The calling program also allocates a descriptor for the output
string. In addition to length and address fields, each descriptor contains a field
(DSC$B_CLASS or DSC64$B_CLASS) indicating the descriptor’s class. The STR$
routine reads the class field to determine whether to write the output string as a
fixed-length, varying-length, or dynamic string.


**2–4** Introduction to String Manipulation (STR$) Routines


**Introduction to String Manipulation (STR$) Routines**
**2.2 Descriptor Classes and String Semantics**


To determine the address and length of the data in the input string, RunTime Library routines call one of the string descriptor analysis routines:
LIB$ANALYZE_SDESC, LIB$ANALYZE_SDESC_64, STR$ANALYZE_SDESC, or
STR$ANALYZE_SDESC_64.


The STR$ routines provide a centralized facility for analyzing string descriptors,
allowing string-handling routines to function independently of the class of the
input string. This means that if the Run-Time Library recognizes new string
types, only the analysis routine needs to be changed, not the string routines
themselves. If you are writing a routine that recognizes all the string types
recognized by the Run-Time Library, your routine should first call the appropriate
string-descriptor analysis routine to obtain the address and length of the input
string.


You can also use the string descriptor analysis routines to find the length of
a returned string. Assume that your called routine calls one of the Run-Time
Library string-copying routines to create a new string. You now want the called
routine to return the actual length of the new string to the calling program. The
called routine calls one of the string-descriptor analysis routines to determine
this length. This sequence of calls allows you to create the new string without
knowing its ultimate length at the time it is created.


The Run-Time Library routines recognize the following classes of string
descriptors:


- Z—unspecified


- S—scalar, fixed-length string


- SD—decimal scalar


- VS—varying-length string


- D—dynamic string


- A—array


- NCA—noncontiguous array


For a detailed description of these descriptor classes and their fields, see the
_OpenVMS Calling Standard_ .


Table 2–1 indicates how the Run-Time Library routines access the fields of the
descriptor for input and output string arguments. Given the class of the string
and the field of the descriptor, the table shows whether the routine reads, writes,
or modifies the field.


Introduction to String Manipulation (STR$) Routines **2–5**


**Introduction to String Manipulation (STR$) Routines**
**2.2 Descriptor Classes and String Semantics**


**Table 2–1 String Passing Techniques Used by the Run-Time Library**


**String Descriptor Fields**


**String Type** **Class** **Length** **Pointer**


**Input Argument to Routines**


Input string passed by descriptor Read Read Read


**Output Argument from Routines; Called Routine Assumes the Descriptor Class**


Output string passed by descriptor, Ignored Read Read
fixed-length


Output string passed by descriptor, Ignored Read, can be Read, can be modified
dynamic modified


**Output Argument from Routines; Calling Program Specifies the Descriptor Class in the Descriptor**


Output string, fixed-length— Read Read Read
Descriptor class: S, Z, A, NCA, SD


Output string, dynamic— Read Read, can be Read, can be modified
Descriptor class: D modified



Output string, varying-length— Read MAXSTRLEN is
Descriptor class: VS read; CURLEN is
modified


**2.2.1 Conventions for Reading Input String Arguments**



Read



When a calling program passes a string as an argument to a Run-Time Library
routine, the argument contains the address of a descriptor. The called routine
examines the CLASS field of the descriptor to determine in which fields it can
find the length of the string and the first byte of the string’s text. For each
descriptor class, Table 2–2 indicates which descriptor fields the routine uses
to locate this information. For diagrams of the descriptors, see the _OpenVMS_
_Calling Standard_ manual.


**Table 2–2 How Run-Time Library Routines Read Strings**


**Class** **String Length** **Address of First Byte of Data**


Z DSC$W_LENGTH DSC$A_POINTER
DSC64$Q_LENGTH DSC64$PQ_POINTER


S DSC$W_LENGTH DSC$A_POINTER
DSC64$Q_LENGTH DSC64$PQ_POINTER


D DSC$W_LENGTH DSC$A_POINTER
DSC64$Q_LENGTH DSC64$PQ_POINTER


A DSC$L_ARSIZE DSC$A_POINTER
DSC64$Q_ARSIZE DSC64$PQ_POINTER


SD DSC$W_LENGTH DSC$A_POINTER
DSC64$Q_LENGTH DSC64$PQ_POINTER


NCA DSC$L_ARSIZE DSC$A_POINTER
DSC64$Q_ARSIZE DSC64$PQ_POINTER


(continued on next page)


**2–6** Introduction to String Manipulation (STR$) Routines


**Introduction to String Manipulation (STR$) Routines**
**2.2 Descriptor Classes and String Semantics**


**Table 2–2 (Cont.) How Run-Time Library Routines Read Strings**


**Class** **String Length** **Address of First Byte of Data**



VS Word at DSC$A_POINTER or
at DSC64$PQ_POINTER
(CURLEN field)


**Note:**



Value of DSC$A_POINTER + 2 or
of DSC64$PQ_POINTER + 2
(byte after CURLEN field)




      - If the descriptor class is NCA, it is assumed that the string is actually
contiguous.


      - If the descriptor class is A or NCA, the element size is assumed to be 1 byte.


      - If the descriptor class is A or NCA and the array being passed is
multidimensional, you should be aware of how your language stores arrays
(by column or by row).


**2.2.2 Semantics for Writing Output String Arguments**


Normally, Run-Time Library routines return the result of an operation in one of
the following ways:


      - The called routine returns the result as a **function value** in R0/R1. If the
result is too large to fit in R0/R1, it is returned as a function value in the
first position in the argument list, and the other arguments are shifted one
position to the right.


      - The called routine returns the result as an **output argument** . The calling
program passes to the called routine an argument naming a variable in which
the routine writes the output string. In each RTL routine, the access field of
an output argument contains ‘‘write only’’.


The STR$ routines that produce string results use the first method to pass the
results back to the calling program. Because a result string, by definition, does
not fit in R0/R1, the function value from an STR$ routine is placed in the first
position in the argument list.


The string manipulation routines in the LIB$ and OTS$ facilities use the second
method, returning their results as output arguments.


For example, there are three entry points for the string-copying routine:
LIB$SCOPY_DXDX, OTS$SCOPY_DXDX, and STR$COPY_DX. These copy
the source string to the destination string. Their formats are as follows:


LIB$SCOPY_DXDX(source-string,destination-string)
OTS$SCOPY_DXDX(source-string,destination-string)
STR$COPY_DX(destination-string,source-string)


Because the STR$ entry point places the result string in the first position, you
can call STR$COPY_DX using a function reference in languages that support
string functions. In Fortran, for example, you can use a function reference to
invoke STR$COPY_DX in the following ways:

```
        CHARACTER*80 STR$COPY_DX
        RETURN_STATUS = STR$COPY_DX(DESTINATION_STRING, SOURCE_STRING)

```

or

```
        DESTINATION_STRING = STR$COPY_DX(SOURCE_STRING)

```

Introduction to String Manipulation (STR$) Routines **2–7**


**Introduction to String Manipulation (STR$) Routines**
**2.2 Descriptor Classes and String Semantics**


If you use the second form, you cannot access the return status, which is used to
indicate truncation.


If you use a function reference to invoke a string manipulation routine in a
language that does not support the concept of a string function (such as MACRO,
BLISS, and Pascal), you must place the destination string variable in the
argument list. In Pascal, for example, you can use a function reference to invoke
STR$COPY_DX as follows:

```
        STATUS := STR$COPY_DX(DESTINATION_STRING, SOURCE_STRING);

```

However, the following statement results in an error:

```
        DESTINATION_STRING := STR$COPY_DX(SOURCE_STRING)

```

In addition to allocating a variable for the output string, the calling program
must allocate the space for and fill in the fields of the output string descriptor at
compile, link, or run time. High-level languages do this automatically.


When a Run-Time Library routine returns an output string argument to the
calling program, the argument list entry is the address of a descriptor. The
routine determines the semantics of the output string (fixed, varying, or dynamic)
by examining the class of the descriptor for the destination string. Given the
class of the output string’s descriptor, Table 2–3 specifies the semantics used by
Run-Time Library routines when writing the string.


**Table 2–3 Output String Semantics and Descriptor Classes**


**Class** **Description** **Restrictions** **Semantics**


Z Unspecified Treated as class S. Fixed-length
string


S Scalar, string None. Fixed-length
string


D Dynamic string String length: DSC$W_LENGTH < 2 [16] (64K) Dynamic-length
DSC64$Q_LENGTH < 2 [64] string



A Array Array is one-dimensional (DIMCT = 1).
String length: DSC$L_ARSIZE < 2 [16] (64K)
DSC64$Q_ARSIZE < 2 [64]

Length of array elements is 1 byte (LENGTH = 1).



Fixed-length
string



SD Scalar decimal The DIGITS and SCALE fields are ignored. Fixed-length
string



NCA Noncontiguous Array is one-dimensional (DIMCT = 1).
array String length: DSC$L_ARSIZE < 2 [16] (64K)
DSC64$Q_ARSIZE < 2 [64]

Length of array elements is 1 byte (LENGTH = 1).
Array is contiguous (S1 = LENGTH).



Fixed-length
string



VS Varying string Current length less than maximum string length. Varying-length
(CURLEN  MAXSTRLEN  2 [16] (64K)) string


When a called routine returns a string whose length cannot be determined by
the calling routine, the calling routine should also pass an optional argument to
contain the output length. If the output string is a fixed-length string, the length
argument would reflect the number of characters written, not counting the fill
characters.


**2–8** Introduction to String Manipulation (STR$) Routines


**Introduction to String Manipulation (STR$) Routines**
**2.2 Descriptor Classes and String Semantics**


The output length argument is useful, for instance, when your program is reading
variable-length records. The program can read the input strings into a buffer
that is large enough to contain the largest. When you want to perform the next
operation on the contents of the buffer, the length argument indicates exactly
how many characters have been read, so that the program does not need to
manipulate the whole buffer.


For example, LIB$GET_INPUT has the optional argument **resultant-length** .
If LIB$GET_INPUT is called with a fixed-length, 5-character string as an
argument, and the routine reads a record containing `’` ABC `’`, then **resultant-**
**length** has a value of 3 and the output string ( `’ABC` `’` ) contains the characters
ABC followed by two blanks. But if the routine reads a record containing the
value `’` ABCDEFG `’`, **resultant-length** has a value of 5 and the output string
is `’` ABCDE `’` . In either case, the calling program knows exactly how many
characters (not counting fillers) the routine has read.


A routine such as STR$COPY_DX does not need the length argument, because
the calling program can determine the length of the output string. If the output
string is dynamic, the length is the same as the input string length. If the output
string is fixed-length, the length is the shorter of the two input lengths.

#### **2.3 Selecting String Manipulation Routines**


To perform a given string manipulation operation, you can often choose one of
several routines from the Run-Time Library. The LIB$, OTS$, and STR$ facilities
all contain string copying and dynamic string allocation routines. Furthermore, a
MACRO or BLISS program can call several of these routines using either a JSB
or CALL entry point.


You should consider the factors discussed in the following sections when choosing
a routine to perform the desired operation.

**2.3.1 Efficiency**


One of the major considerations in choosing among several routines is the
efficiency of the various options.


In general, LIB$ and STR$ routines execute more efficiently than the
corresponding OTS$ routines. OTS$ routines usually invoke the LIB$ entry
point to perform an operation.


JSB entry points usually execute more efficiently than CALL entry points.
However, a high-level language cannot explicitly access a JSB entry point.
Further, a JSB entry point does not establish a stack frame and executes entirely
in the environment of the calling program. This means, for instance, that the
called routine cannot establish its own condition handler, so it cannot regain
control if an exception occurs during execution. Also, some of the efficiency
gained by using the JSB entry point may be lost because the calling routine must
explicitly save all of the registers that the called routine uses.


Some routines perform a specific operation that is a subset of a more general
capability. These more specialized routines are usually more efficient.
For example, if you want to join two strings together, STR$APPEND and
STR$PREFIX are more specific, and more efficient, than STR$CONCAT.
Similarly, STR$LEFT and STR$RIGHT are subsets of the capabilities of
STR$POS_EXTR.


Introduction to String Manipulation (STR$) Routines **2–9**


**Introduction to String Manipulation (STR$) Routines**
**2.3 Selecting String Manipulation Routines**


**2.3.2 Argument Passing**


The mechanism by which a routine passes or receives arguments may also help
you to decide among several routines that perform basically the same function.


Routines in the LIB$ and STR$ facilities pass scalar input arguments by
reference to CALL entry points and by immediate value to JSB entry points.
OTS$ routines pass scalar input arguments by immediate value to all entry
points. For most high-level languages, the default passing mechanism is by
reference. Thus, if you call a LIB$ or STR$ routine from one of these languages,
you do not need to specify the passing mechanism for input scalar arguments.


Some routines require you to set up and pass more arguments than others.
For example, some use a single string descriptor, while others require separate
arguments for the length and the address of the string. Which routine you choose
then depends on the form of the information already available in your program.


**2.3.3 Error Handling**


Routines from the LIB$, OTS$, and STR$ facilities handle errors in string
copying differently:


      - LIB$


The LIB$ string-copying routines return a completion status. When an output
string must be truncated and its length depends on input arguments, LIB$
routines consider this to be a partial success; they therefore return LIB$_
STRTRU instead of a severe error. This process corresponds to the convention
of many higher-level languages, which do not consider truncation to be an

error.


      - OTS$


The OTS$ string-copying routines also signal errors that are considered fatal
(such as invalid descriptor class). In addition, the routine returns in R0 the
number of bytes in the source string that were not moved to the destination
string. For VAX systems, this is the same as a MOVC5 instruction. The
JSB entry points for OTS$ string-copying routines also leave registers R1
through R5 as they would be after a VAX MOVC5 instruction. See the _VAX_
_Architecture Reference Manual_ for a complete description of the MOVC5
instruction.


      - STR$


The STR$ string-copying routines generally signal errors instead of returning
a completion status. In the case of truncation errors, STR$ routines return
an error status with a severity of WARNING (STR$_TRU). STR$ routines
consider range errors to be qualified success.


Table 2–4 indicates the errors and the corresponding message that each facility
considers severe.


**2–10** Introduction to String Manipulation (STR$) Routines


**Introduction to String Manipulation (STR$) Routines**
**2.3 Selecting String Manipulation Routines**


**Table 2–4 Severe Errors, by Facility**


**Error** **LIB$_** **OTS$_** **STR$_**


Fatal internal error FATERRLIB FATINTERR FATINTERR


Illegal string class INVSTRDES INVSTRDES ILLSTRCLA


Insufficient virtual memory INSVIRMEM INSVIRMEM INSVIRMEM


Some Run-Time Library routines require you to specify the length of a string or
the position of a character within a string. When you refer to character positions
in a string, the first position is 1. Given a string with length _L_, containing a
substring specified by character positions _M_ to _N_, the following evaluation rules
apply:


      - If _M_ is less than 1, _M_ is considered to equal 1.


      - If _M_ is greater than _L_, the substring specified is the null string.


      - If _N_ is greater than _L_, _N_ is considered to equal the length of the source string.


      - If _M_ is greater than _N_, the substring specified is the null string.


When specifying a substring of length _L_, the following applies:


      - If _L_ is less than 0, the substring specified is the null string. (A null string is
a descriptor with zero length. A descriptor with a nonzero length and a zero
pointer generates an error and yields unspecified results.)


If any of these evaluation rules applies, the range error status (qualified success)
is returned. STR$POSITION represents the exception to this convention. This
routine returns a function value giving the character position of a substring
within a string. If the function value is 0, the substring was not found.

#### **2.4 Allocating Resources for Dynamic Strings**


This section tells how to use the Run-Time Library string resource allocation
routines. These routines allocate virtual memory for a dynamic string and place
the address of the allocated memory in a descriptor.


Dynamic strings may be the most convenient type to write, since you need not
specify constant length, maximum length, or position for them. However, there
are some restrictions on dynamic strings.


      - They may cause program execution to be slower at run time.


      - They require larger address space.


      - They are not supported by all OpenVMS Alpha and OpenVMS VAX languages.


In most cases, when you call a Run-Time Library routine to manipulate dynamic
strings, the Run-Time Library routine itself allocates the required memory for the
string. Your program needs to allocate only the descriptors.


For example, if you are copying a source string into a dynamic destination string,
simply use one of the library’s string-copying routines. Copy the input string
into a dynamic string whose length and address are initialized to zero. The
string-copying routine then allocates the space that the calling program needs.


Introduction to String Manipulation (STR$) Routines **2–11**


**Introduction to String Manipulation (STR$) Routines**
**2.4 Allocating Resources for Dynamic Strings**


However, if your program must explicitly construct or modify a dynamic string
descriptor, it must use the Run-Time Library allocation and deallocation routines.
This technique may be necessary, for instance, if you are constructing a string out
of components that are not themselves in string form. Further, you can use one
of the deallocation routines to free the dynamic string after the string resources
are no longer needed, in order to optimize the program’s use of resources.


The Run-Time Library provides eight entry points for string resource allocation
and deallocation, all with slightly different input arguments, calling techniques,
or methods of indicating errors. The following tables summarize these routines
and their functions.


The following routines allocate a specified number of bytes of dynamic virtual
memory to a specified string descriptor.


**Routine** **JSB Entry Point**


LIB$SGET1_DD LIB$SGET1_DD_R6


LIB$SGET1_DD_64 LIB$SGET1_DD_R6


OTS$SGET1_DD OTS$SGET1_DD_R6


STR$GET1_DX STR$GET1_DX_R4


STR$GET1_DX_64 STR$GET1_DX_R4


The following routines return one dynamic string area to free storage, and set the
descriptor POINTER and LENGTH fields to zero.


**Routine** **JSB Entry Point**


LIB$SFREE1_DD LIB$SFREE1_DD6


OTS$SFREE1_DD OTS$SFREE1_DD6


STR$FREE1_DX STR$FREE1_DX_R4


The following routines return one or more dynamic string areas to free storage,
and set the descriptor POINTER and LENGTH fields to zero.


**Routine** **JSB Entry Point**


LIB$SFREEN_DD LIB$SFREEN_DD6


OTS$SFREEN_DD OTS$SFREEN_DD6


When you call the dynamic string allocation routines, consider the following
factors:


      - When your program calls a string allocation routine, it needs to allocate space
only for the string descriptor before making the call. Your program does this
using the statement of the particular language, either statically at compile
time or dynamically in local stack storage or heap storage.


      - If your routine explicitly allocates dynamic string descriptors in stack storage,
it must explicitly free the associated dynamic string areas by calling the
LIB$SFREE1_DD, OTS$SFREE1_DD, or STR$FREE1_DX routine. Then
your routine must free the storage for the descriptor. After both areas have
been freed, your routine can return to the calling program. If the deallocation
is not done, the dynamic string area becomes unavailable when the RET
instruction removes the descriptors that point to the string area.


**2–12** Introduction to String Manipulation (STR$) Routines


**Introduction to String Manipulation (STR$) Routines**
**2.4 Allocating Resources for Dynamic Strings**


      - If a routine has explicitly allocated dynamic string areas, and the routine
is then unwound by the Condition Handling Facility (CHF), the allocated
address space cannot be referenced again. For this reason, your program
should establish a handler that frees the associated dynamic string areas
when the SS$_UNWIND condition is signaled. The handler can free these
areas by calling one of the deallocation routines. This technique is especially
important if a large amount of address space is involved, or if the routine
allocates space within a repeating loop.


You can call the string resource allocation routines only from user mode, at
asynchronous system trap (AST) or non-AST level. However, be extremely careful
if you manipulate dynamic strings at AST level. The string manipulation routines
in the Run-Time Library do not prevent the strings that they are manipulating at
non-AST level from being modified at AST level.


For example, consider the case in which a string manipulation routine has
calculated the lengths and addresses involved in a concatenation operation. This
string manipulation routine may be interrupted by an AST. The user, at AST
level, may write to the same string, changing its length and address. It is then
possible to resume execution of the routine with addresses that are no longer
allocated or string lengths that are no longer valid. For this reason, if you use
dynamic strings at AST level, you should allocate, use, and deallocate them
within the AST code.


The dynamic string manipulation routines are intended for use at user mode
only. To manipulate dynamic strings at another access mode, you should allocate
and deallocate storage for each string at that access mode to avoid side effects.
Link each segment of your program that runs at a different access mode with the
/NOSYSSHR qualifier. In this way, you establish a separate copy of the string
database for each access mode.


**2.4.1 String Zone**


All virtual memory for dynamic strings is allocated from a Run-Time Library zone
called the string zone.


The string zone has the following benefits:


      - Efficient memory utilization.


      - Allocation and deallocation for long strings (more than 136 bytes for a VAX
system and more than 272 bytes for an Alpha system) is twice as fast.


      - Elimination of paging contention with the default zone by isolation of the
string virtual memory accesses to a separate zone. A direct side effect of this
is that corruptions caused by writing into previously freed strings no longer
affect items allocated in the default zone, directly easing the debugging effort
for such problems.


Table 2–5 shows attribute values for 32-bit and 64-bit string zones. VAX systems
have a 32-bit string zone; Alpha systems have both a 32-bit and a 64-bit string

zone.


Introduction to String Manipulation (STR$) Routines **2–13**


**Introduction to String Manipulation (STR$) Routines**
**2.4 Allocating Resources for Dynamic Strings**


**Table 2–5 String Zone Attributes**


**Attribute** **32-bit String Zone** **64-bit String Zone**


Algorithm Quick fit Quick fit


Number of lookaside lists 17 (short strings from 8 to 17 (short strings from 8 to
136 bytes) 272 bytes)


Area of initial size 4 pages 4 pages


Area of extension size 32 pages 32 pages


Block size 8 bytes 16 bytes


Alignment Longword boundary Quadword boundary


Smallest block size 16 bytes (includes boundary 32 bytes (includes boundary
tags) tags)


Boundary tags Boundary tags are used for Boundary tags are used for
long strings long strings


Page limit No page limit No page limit


Fill on allocate No fill on allocate No fill on allocate


Fill on free No fill on free No fill on free


**2–14** Introduction to String Manipulation (STR$) Routines


# **Part II**

### **STR$ Reference Section**

This section contains detailed descriptions of the routines in the OpenVMS RTL
String Manipulation (STR$) facility.


**STR$ Routines**
**STR$ADD**

#### **STR$ADD** **Add Two Decimal Strings**


The Add Two Decimal Strings routine adds two decimal strings of digits.


**Format**


STR$ADD asign,aexp,adigits,bsign,bexp,bdigits,csign,cexp,cdigits


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**asign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by reference


Sign of the first operand. The **asign** argument is the address of an unsigned
longword containing this sign. A value of 0 is considered positive; a value of 1 is
considered negative.


**aexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Power of 10 by which **adigits** is multiplied to get the absolute value of the first
operand. The **aexp** argument is the address of a signed longword containing this

exponent.


**adigits**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Text string of unsigned digits representing the absolute value of the first operand
before **aexp** is applied. The **adigits** argument is the address of a descriptor
pointing to this string. This string must be an unsigned decimal number.


**bsign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by reference


STR–3


**STR$ Routines**
**STR$ADD**


Sign of the second operand. The **bsign** argument is the address of an unsigned
longword containing the second operand’s sign. A value of 0 is considered positive;
a value of 1 is considered negative.


**bexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Power of 10 by which **bdigits** is multiplied to get the absolute value of the second
operand. The **bexp** argument is the address of a signed longword containing the
second operand’s exponent.


**bdigits**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Text string of unsigned digits representing the absolute value of the second
operand before **bexp** is applied. The **bdigits** argument is the address of a
descriptor pointing to this string. This string must be an unsigned decimal
number.


**csign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: write only
mechanism: by reference


Sign of the result. The **csign** argument is the address of an unsigned longword
containing the result’s sign. A value of 0 is considered positive; a value of 1 is
considered negative.


**cexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by reference


Power of 10 by which **cdigits** is multiplied to get the absolute value of the result.
The **cexp** argument is the address of a signed longword containing this exponent.


**cdigits**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Text string of unsigned digits representing the absolute value of the result before
**cexp** is applied. The **cdigits** argument is the address of a descriptor pointing to
this string. This string is an unsigned decimal number.


STR–4


**Description**



**STR$ Routines**
**STR$ADD**


STR$ADD adds two strings of decimal numbers ( **a** and **b** ). Each number to be
added is passed to STR$ADD in three arguments:


1. **xdigits** —the string portion of the number


2. **xexp** —the power of ten needed to obtain the absolute value of the number


3. **xsign** —the sign of the number


The value of the number **x** is derived by multiplying **xdigits** by 10 _[xexp]_ and
applying **xsign** . Therefore, if **xdigits** is equal to `’` 2 `’` and **xexp** is equal to 3 and
**xsign** is equal to 1, then the number represented in the **x** arguments is 2 * 10 [3]

plus the sign, or –2000.


The result of the addition **c** is also returned in those three parts.



**Condition Values Returned**


SS$_NORMAL Routine successfully completed.

STR$_TRU String truncation warning. The destination
string could not contain all the characters in the
result string.


**Condition Values Signaled**


LIB$_INVARG Invalid argument.

STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$ADD could not
allocate heap storage for a dynamic or temporary
string.

STR$_WRONUMARG Wrong number of arguments.


STR–5


**STR$ Routines**
**STR$ADD**


**Example**

```
        100 !+
          ! This is a sample arithmetic program
          ! showing the use of STR$ADD to add
          ! two decimal strings.
          !
          ASIGN% = 1%

          AEXP% = 3%
          ADIGITS$ = ’1’
          BSIGN% = 0%

          BEXP% = -4%
          BDIGITS$ = ’2’
          CSIGN% = 0%

          CEXP% = 0%
          CDIGITS$ = ’0’
          PRINT "A = "; ASIGN%; AEXP%; ADIGITS$
          PRINT "B = "; BSIGN%; BEXP%; BDIGITS$
          CALL STR$ADD (ASIGN%, AEXP%, ADIGITS$, &
                     BSIGN%, BEXP%, BDIGITS$, &
                     CSIGN%, CEXP%, CDIGITS$)
          PRINT "C = "; CSIGN%; CEXP%; CDIGITS$
        999 END

```

This BASIC example uses STR$ADD to add two decimal strings, where the
following values apply:


A = –1000 (ASIGN = 1, AEXP = 3, ADIGITS = `’` 1 `’` )
B = .0002 (BSIGN = 0, BEXP = –4, BDIGITS = `’` 2 `’` )


The output generated by this program is listed below; note that the decimal value
of C equals –999.9998 (CSIGN = 1, CEXP = –4, CDIGITS = `’` 9999998 `’` ).

```
          A = 1 3 1

          B = 0 -4 2

          C = 1 -4 9999998

```

STR–6


**STR$ Routines**
**STR$ANALYZE_SDESC**

#### **STR$ANALYZE_SDESC** **Analyze String Descriptor**


The Analyze String Descriptor routine extracts the length and starting address of
the data for a variety of string descriptor classes.


**Format**


STR$ANALYZE_SDESC input-descriptor,integer-length,data-address


**Corresponding JSB Entry Point**


STR$ANALYZE_SDESC_R1


**Returns**


OpenVMS usage: word_unsigned
type: word (unsigned)
access: write only
mechanism: by value


Length of the data. The return value is the same value returned to the **integer-**
**length** argument.


**Arguments**


**input-descriptor**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Input descriptor from which STR$ANALYZE_SDESC extracts the length of the
data and the address at which the data starts. The **input-descriptor** argument
is the address of a descriptor pointing to the input data.


**integer-length**
OpenVMS usage: word_unsigned
type: word (unsigned)
access: write only
mechanism: by reference for CALL entry point, by value for JSB entry
point


Length of the data; this length is extracted from the descriptor by
STR$ANALYZE_SDESC. The **integer-length** argument is the address of an
unsigned word integer into which STR$ANALYZE_SDESC writes the data length.


**data-address**

OpenVMS usage: address
type: longword (unsigned)
access: write only
mechanism: by reference for CALL entry point, by value for JSB entry
point


STR–7


**STR$ Routines**
**STR$ANALYZE_SDESC**


Address of the data; this address is extracted from the descriptor by
STR$ANALYZE_SDESC. The **data-address** argument is an unsigned longword
into which STR$ANALYZE_SDESC writes the address of the data.


**Description**


STR$ANALYZE_SDESC takes as input a 32-bit descriptor argument and extracts
from the descriptor the length of the data and the address at which the data
starts for a variety of string descriptor classes. See LIB$ANALYZE_SDESC for a
list of classes.


STR$ANALYZE_SDESC returns the length of the data in the **integer-length**
argument and the starting address of the data in the **data-address** argument.


STR$ANALYZE_SDESC signals an error if an invalid descriptor class is found.


**Condition Values Signaled**


STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.


STR–8


**STR$ Routines**
**STR$ANALYZE_SDESC_64 (Alpha only)**

#### **STR$ANALYZE_SDESC_64 (Alpha only)** **Analyze String Descriptor**


The Analyze String Descriptor routine extracts the length and starting address of
the data for a variety of string descriptor classes.


**Format**


STR$ANALYZE_SDESC_64 input-descriptor,integer-length,data-address

[,descriptor-type]


**Corresponding JSB Entry Point**


STR$ANALYZE_SDESC_R1
Refer to the STR$ANALYZE_SDESC routine
for information about the JSB entry point,
STR$ANALYZE_SDESC_R1. This JSB entry point
returns 64-bit results on Alpha systems.


**Returns**


OpenVMS usage: quadword_unsigned
type: quadword (unsigned)
access: write only
mechanism: by value


Length of the data. The return value is the same value returned to the **integer-**
**length** argument.


**Arguments**


**input-descriptor**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Input descriptor from which STR$ANALYZE_SDESC_64 extracts the length
of the data and the address at which the data starts. The **input-descriptor**
argument is the address of a descriptor pointing to the input data. The input
descriptor can be a longword (unsigned) or a quadword (unsigned).


**integer-length**
OpenVMS usage: quadword_unsigned
type: quadword (unsigned)
access: write only
mechanism: by reference for CALL entry point, by value for JSB entry
point


Length of the data; this length is extracted from the descriptor by
STR$ANALYZE_SDESC_64. The **integer-length** argument is the address of
an unsigned quadword integer into which STR$ANALYZE_SDESC_64 writes the
data length.


STR–9


**STR$ Routines**
**STR$ANALYZE_SDESC_64 (Alpha only)**


**data-address**

OpenVMS usage: address
type: quadword (unsigned)
access: write only
mechanism: by reference for CALL entry point, by value for JSB entry
point


Address of the data; this address is extracted from the descriptor by
STR$ANALYZE_SDESC_64. The **data-address** argument is an unsigned
quadword into which STR$ANALYZE_SDESC_64 writes the address of the data.


**descriptor-type**
OpenVMS usage: word_unsigned
type: word (unsigned)
access: write only
mechanism: by reference


Flag value indicating the type of input descriptor. The **descriptor-type**
argument contains the address of an unsigned word integer to which
STR$ANALYZE_SDESC_64 writes a zero (0) for a 32-bit input descriptor or
a one (1) for a 64-bit descriptor.


This argument is optional.


**Description**


STR$ANALYZE_SDESC_64 takes as input a descriptor argument and extracts
from the descriptor the length of the data and the address at which the data
starts for a variety of string descriptor classes. See LIB$ANALYZE_SDESC_64
for a list of classes.


STR$ANALYZE_SDESC_64 returns the length of the data in the **integer-length**
argument and the starting address of the data in the **data-address** argument.


STR$ANALYZE_SDESC_64 signals an error if an invalid descriptor class is
found.


**Condition Values Signaled**


STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.


STR–10


**STR$ Routines**
**STR$APPEND**

#### **STR$APPEND** **Append String**


The Append String routine appends a source string to the end of a destination
string.


**Format**


STR$APPEND destination-string,source-string


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string to which STR$APPEND appends the source string. The
**destination-string** argument is the address of a descriptor pointing to the
destination string. This destination string must be dynamic or varying length.
The maximum length of the destination string for a 32-bit descriptor is 2 [16] —1, or
65,535, bytes.


On Alpha systems, the maximum length of the destination string for all 64-bit
descriptor classes, except varying-length strings, is 2 [64] —1 bytes. The maximum
length of a varying-length string is 2 [16] —1 for both 32-bit and 64-bit descriptors.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string that STR$APPEND appends to the end of the destination string.
The **source-string** argument is the address of a descriptor pointing to this source
string.


**Description**


STR$APPEND appends a source string to the end of the destination string. The
destination string must be a dynamic string or a varying-length string.


STR–11


**STR$ Routines**
**STR$APPEND**


**Condition Values Returned**


SS$_NORMAL Routine successfully completed.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters
from the concatinated string.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$APPEND
could not allocate heap storage for a dynamic or
temporary string.

STR$_STRTOOLON The combined lengths of the source and
destination strings exceeded the maximum
allowed for the **destination-string** descriptor.


**Example**

```
        10 !+
          ! This example program uses
          ! STR$APPEND to append a source
          ! string to a destination string.
          !
          DST$ = ’DOG/’
          SRC$ = ’CAT’
          CALL STR$APPEND (DST$, SRC$)
          PRINT "DST$ = ";DST$

          END

```

This BASIC example uses STR$APPEND to append a source string `’` CAT `’`, to a
destination string `’` DOG/ `’` .


The output generated by this program is as follows:

```
          DST$ = DOG/CAT

```

STR–12


**STR$ Routines**
**STR$CASE_BLIND_COMPARE**

#### **STR$CASE_BLIND_COMPARE** **Compare Strings Without Regard to Case**


The Compare Strings Without Regard to Case routine compares two input strings
of any supported class and data type without regard to whether the alphabetic
characters are uppercase or lowercase.


**Format**


STR$CASE_BLIND_COMPARE first-source-string,second-source-string


**Returns**


OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by value


The values returned by STR$CASE_BLIND_COMPARE and the conditions to
which they translate are as follows:


**Returned Value** **Condition**


–1 **first-source-string** is less than **second-source-string** .

0 Both are the same (with blank fill for shorter string).

1 **first-source-string** is greater than **second-source-**
**string** .


**Arguments**

**first-source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


First string. The **first-source-string** argument is the address of a descriptor
pointing to the first string.


**second-source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Second string. The **second-source-string** argument is the address of a
descriptor pointing to the second string.


**Description**


STR$CASE_BLIND_COMPARE does not distinguish between uppercase and
lowercase characters. The contents of both strings are converted to uppercase
before the strings are compared, but the source strings themselves are not
changed. STR$CASE_BLIND_COMPARE uses the DEC Multinational Character
Set.


STR–13


**STR$ Routines**
**STR$CASE_BLIND_COMPARE**


**Condition Value Signaled**


STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.


**Example**

```
        PROGRAM CASE_BLIND(INPUT, OUTPUT);

        {+}
        { This program demonstrates the use of
        { STR$CASE_BLIND_COMPARE.
        {
        { First, declare the external function.
        {-}

        FUNCTION STR$CASE_BLIND_COMPARE(STR1 : VARYING
             [A] OF CHAR; STR2 : VARYING [B] OF
             CHAR) : INTEGER; EXTERN;

        {+}
        { Declare the variables to be used in the
        { main program.
        {-}

        VAR

         STRING1 : VARYING [256] OF CHAR;
         STRING2 : VARYING [256] OF CHAR;
         RET_STATUS : INTEGER;

        {+}
        { Begin the main program. Read values for
        { the strings to be compared. Call
        { STR$CASE_BLIND_COMPARE. Print the
        { result.
        {-}

        BEGIN

         WRITELN(’ENTER THE FIRST STRING: ’);
         READLN(STRING1);
         WRITELN(’ENTER THE SECOND STRING: ’);
         READLN(STRING2);
         RET_STATUS := STR$CASE_BLIND_COMPARE(STRING1, STRING2);
         WRITELN(RET_STATUS);

        END.

```

This Pascal example shows how to call STR$CASE_BLIND_COMPARE to
determine whether two strings are equal regardless of case. One example of the
output of this program is as follows:

```
          $ RUN CASE_BLIND

          ENTER THE FIRST STRING: KITTEN

          ENTER THE SECOND STRING: kItTeN

            0

```

STR–14


**STR$ Routines**
**STR$COMPARE**

#### **STR$COMPARE** **Compare Two Strings**


The Compare Two Strings routine compares the contents of two strings.


**Format**


STR$COMPARE first-source-string,second-source-string


**Returns**


OpenVMS usage: longword_signed
type: longword integer (signed)
access: write only
mechanism: by value


The values returned by STR$COMPARE and the conditions to which they
translate are as follows:


**Returned Value** **Condition**


–1 **first-source-string** is less than **second-source-string** .

0 **first-source-string** is equal to **second-source-string** .

1 **first-source-string** is greater than **second-source-**
**string** .


**Arguments**

**first-source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


First string. The **first-source-string** argument is the address of a descriptor
pointing to the first string.


**second-source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Second string. The **second-source-string** argument is the address of a
descriptor pointing to the second string.


**Description**


STR$COMPARE compares two strings for the same contents. If the strings
are unequal in length, the shorter string is considered to be filled with blanks
to the length of the longer string before the comparison is made. This routine
distinguishes between uppercase and lowercase alphabetic characters.


STR–15


**STR$ Routines**
**STR$COMPARE**


**Condition Value Signaled**


STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.


**Example**

```
        100 EXTERNAL INTEGER FUNCTION STR$COMPARE
          SRC1$ = ’ABC’
          SRC2$ = ’BCD ’

          !+
          ! Note that STR$COMPARE will treat SRC1$ as if it were the same
          ! length as SRC2$ for the purpose of the comparison. Thus, it
          ! will treat the contents of SRC1$ as ’ABC ’. However, it
          ! will only ’treat’ the contents as longer; the contents of
          ! the source string are not actually changed.
          !
          I% = STR$COMPARE(SRC1$, SRC2$)
          IF I% = 1 THEN RESULT$ = ’ IS GREATER THAN ’
          IF I% = 0 THEN RESULT$ = ’ IS EQUAL TO ’
          IF I% = -1 THEN RESULT$ = ’ IS LESS THAN ’
          PRINT SRC1$; RESULT$; SRC2$
        999 END

```

This BASIC program uses STR$COMPARE to compare two strings. The output
generated by this program is as follows:

```
          ABC IS LESS THAN BCD

```

STR–16


**STR$ Routines**
**STR$COMPARE_EQL**

#### **STR$COMPARE_EQL** **Compare Two Strings for Equality**


The Compare Two Strings for Equality routine compares two strings to see if they
have the same length and contents. Uppercase and lowercase characters are not
considered equal.


**Format**


STR$COMPARE_EQL first-source-string,second-source-string


**Returns**


OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: write only
mechanism: by value


The values returned by STR$COMPARE and the conditions to which they
translate are as follows:


**Returned Value** **Condition**


0 The length and the contents of **first-source-string** are
equal to the length and contents of **second-source-**
**string** .

1 Either the length of **first-source-string** is not equal
to the length of **second-source-string**, or the contents
of **first-source-string** are not equal to the contents of
**second-source-string**, or both.


**Arguments**

**first-source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


First source string. The **first-source-string** argument is the address of a
descriptor pointing to the first source string.


**second-source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Second source string. The **second-source-string** argument is the address of a
descriptor pointing to the second source string.


STR–17


**STR$ Routines**
**STR$COMPARE_EQL**


**Condition Values Signaled**


STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.


**Example**

```
        PROGRAM COMPARE_EQL(INPUT, OUTPUT);

        {+}
        { This program demonstrates the use of
        { STR$COMPARE_EQL to compare two strings.
        { Strings are considered equal only if they
        { have the same contents and the same length.
        {
        { First, declare the external function.
        {-}

        FUNCTION STR$COMPARE_EQL(SRC1STR : VARYING
             [A] OF CHAR; SRC2STR : VARYING [B]
             OF CHAR) : INTEGER; EXTERN;

        {+}
        { Declare the variables used in the main program.
        {-}

        VAR

         STRING1 : VARYING [256] OF CHAR;
         STRING2 : VARYING [256] OF CHAR;
         RET_STATUS : INTEGER;

        {+}
        { Begin the main program. Read the strings
        { to be compared. Call STR$COMARE_EQL to compare
        { the strings. Print the result.
        {-}

        BEGIN

         WRITELN(’ENTER THE FIRST STRING: ’);
         READLN(STRING1);
         WRITELN(’ENTER THE SECOND STRING: ’);
         READLN(STRING2);
         RET_STATUS := STR$COMPARE_EQL(STRING1, STRING2);
         WRITELN(RET_STATUS);

        END.

```

This Pascal example demonstrates the use of STR$COMPARE_EQL. A sample of
the output generated by this program is as follows:

```
          $ RUN COMPARE_EQL
          ENTER THE FIRST STRING: frog
          ENTER THE SECOND STRING: Frogs
             1

```

STR–18


**STR$ Routines**
**STR$COMPARE_MULTI**

#### **STR$COMPARE_MULTI** **Compare Two Strings for Equality Using Multinational Character Set**


The Compare Two Strings for Equality Using Multinational Character Set
routine compares two character strings for equality using the DEC Multinational
Character Set.


**Format**


STR$COMPARE_MULTI first-source-string,second-source-string [,flags-value]

[,foreign-language]


**Returns**


OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by value


The values returned by STR$COMPARE_MULTI and the conditions to which
they translate are as follows:


**Returned Value** **Condition**


–1 **first-source-string** is less than **second-source-string** .

0 Both strings are the same; the shorter string is blank
filled.

1 **first-source-string** is greater than **second-source-**
**string** .


**Arguments**

**first-source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


First string in the comparison. The **first-source-string** argument is the address
of a descriptor pointing to the first string.


**second-source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Second string in the comparison. The **second-source-string** argument is the
address of a descriptor pointing to the second string.


STR–19


**STR$ Routines**
**STR$COMPARE_MULTI**


**flags-value**
OpenVMS usage: mask_longword
type: longword (unsigned)
access: read only
mechanism: by value


A single flag bit. The **flags-value** argument is a signed longword integer
that contains this flag bit. The **flags-value** argument indicates whether the
comparison is to be case sensitive or case blind. The default value of **flags-value**
is 0, indicating a case sensitive comparison. The following table lists the meaning
of the bit values:


**Value** **Meaning**


0 Uppercase and lowercase characters are not equivalent. (The
comparison is case sensitive.)

1 Uppercase and lowercase characters are equivalent. (The comparison is
case blind.)


**foreign-language**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by value


Indicator that determines the foreign language table to be used. The **foreign-**
**language** argument is an unsigned longword that contains this foreign language
table indicator. The default value of **foreign-language** is 1. The following table
lists the value of the **foreign-language** argument associated with each language
table:


**Value** **Language**


1 Multinational table

2 Danish table

3 Finnish/Swedish table

4 German table

5 Norwegian table

6 Spanish table


**Description**


STR$COMPARE_MULTI compares two character strings to see whether they
have the same contents. Two strings are ‘‘equal’’ if they contain the same
characters in the same sequence, even if one of them is blank filled to a longer
length than the other. The DEC Multinational Character Set, or foreign language
variations of the DEC Multinational Character Set, are used in the comparison.


See the _OpenVMS I/O User’s Reference Manual_ for more information about the
DEC Multinational Character Set.


STR–20


**STR$ Routines**
**STR$COMPARE_MULTI**


**Condition Values Signaled**


STR$_ILLSTRCLA Illegal string class. Severe error. The descriptor
of **first-source-string** and/or **second-source-**
**string** contains a class code that is not supported
by the OpenVMS calling standard.

LIB$_INVARG Invalid argument. Severe error.


STR–21


**STR$ Routines**
**STR$CONCAT**

#### **STR$CONCAT** **Concatenate Two or More Strings**


The Concatenate Two or More Strings routine concatenates all specified source
strings into a single destination string.


**Format**


STR$CONCAT destination-string,source-string [,source-string...]


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$CONCAT concatenates all specified source
strings. The **destination-string** argument is the address of a descriptor pointing
to this destination string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


First source string; STR$CONCAT requires at least one source string. The
**source-string** argument is the address of a descriptor pointing to the first source
string. The maximum number of source strings that STR$CONCAT allows is 254.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Additional source strings; STR$CONCAT requires at least one source string. The
**source-string** argument is the address of a descriptor pointing to the additional
source string. The maximum number of source strings that STR$CONCAT allows
is 254.


STR–22


**Description**



**STR$ Routines**
**STR$CONCAT**


STR$CONCAT concatenates all specified source strings into a single destination
string. The strings can be of any class and data type, provided that the length
fields of the descriptors indicate the lengths of the strings in bytes. You must
specify at least one source string, and you can specify up to 254 source strings.
The maximum length of a concatenated string for a 32-bit descriptor is 2 [16] —1, or
65,535, bytes.


On Alpha systems, the maximum length of the destination string for all 64-bit
descriptor classes, except varying-length strings, is 2 [64] —1 bytes. The maximum
length of a varying-length string is 2 [16] —1 for both 32-bit and 64-bit descriptors.


A warning status is returned if one or more input characters are not copied to the
destination string.



**Condition Values Returned**


SS$_NORMAL Normal successful completion. All characters in
the input strings were copied into the destination
string.

STR$_TRU String truncation warning. One or more input
characters were not copied into the destination
string.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$CONCAT
could not allocate heap storage for a dynamic or
temporary string.

STR$_STRTOOLON The combined length of all the source strings
exceeded the maximum allowed for the

**destination-string** descriptor.

STR$_WRONUMARG Wrong number of arguments. You tried to pass
fewer than two or more than 255 arguments to
STR$CONCAT.


STR–23


**STR$ Routines**
**STR$CONCAT**


**Example**

```
        10 !+
          ! This example program uses STR$CONCAT
          ! to concatenate four source strings into a
          ! single destination string.
          !
          EXTERNAL INTEGER FUNCTION STR$CONCAT
          STATUS% = STR$CONCAT (X$, ’A’, ’B’, ’C’, ’D’)
          PRINT "X$ = ";X$

          END

```

The output generated by this BASIC program is as follows:

```
          X$ = ABCD

```

STR–24


**STR$ Routines**
**STR$COPY_DX**

#### **STR$COPY_DX** **Copy a Source String Passed by Descriptor to a Destination String**


The Copy a Source String Passed by Descriptor to a Destination String routine
copies a source string to a destination string. Both strings are passed by
descriptor.


**Format**


STR$COPY_DX destination-string,source-string


**Corresponding JSB Entry Point**


STR$COPY_DX_R8


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$COPY_DX writes the source string.
Depending on the class of the destination string, the following actions occur:


**Descriptor Class** **Action**


S, Z, SD, A, NCA Copy the source string. If needed, fill space or truncate
on the right.

D If the area specified by the destination descriptor is
large enough to contain the source string, copy the
source string and set the new length in the destination
descriptor. If the area specified is not large enough,
return the previous space allocation (if any) and then
dynamically allocate the amount of space needed. Copy
the source string and set the new length and address in
the destination descriptor.

VS Copy the source string to the destination string up to
the limit of the descriptor’s MAXSTRLEN field with no
padding. Adjust the string’s current length (CURLEN)
field to the actual number of bytes copied.


The **destination-string** argument is the address of a descriptor pointing to the
destination string.


STR–25


**STR$ Routines**
**STR$COPY_DX**


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string that STR$COPY_DX copies into the destination string; the
descriptor class of the source string can be unspecified, fixed length, dynamic
length, scalar decimal, array, noncontiguous array, or varying length. The
**source-string** argument is the address of a descriptor pointing to this source
string. (See the description of LIB$ANALYZE_SDESC for possible restrictions.)


**Description**


STR$COPY_DX copies a source string to a destination string, where both strings
are passed by descriptor. All conditions except success and truncation are
signaled; truncation is returned as a warning condition value.


STR$COPY_DX passes the source string by descriptor. In addition, an equivalent
JSB entry point is provided, with R0 being the first argument (the descriptor of
the destination string), and R1 the second (the descriptor of the source string).


**Condition Values Returned**


SS$_NORMAL Normal successful completion. All characters in
the input string were copied to the destination
string.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters
copied from the source string.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$COPY_DX
could not allocate heap storage for a dynamic or
temporary string.


STR–26


**STR$ Routines**
**STR$COPY_R**

#### **STR$COPY_R** **Copy a Source String Passed by Reference to Destination String**


The Copy a Source String Passed by Reference to a Destination String routine
copies a source string passed by reference to a destination string passed by
descriptor.


**Format**


STR$COPY_R destination-string,word-integer-source-length,source-string-address


**Corresponding JSB Entry Point**


STR$COPY_R_R8


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$COPY_R copies the source string. The
**destination-string** argument is the address of a descriptor pointing to the
destination string.


The class field determines the appropriate action.


See the description of LIB$ANALYZE_SDESC for restrictions associated with
specific descriptor classes.


**word-integer-source-length**
OpenVMS usage: word_unsigned
type: word (unsigned)
access: read only
mechanism: by reference


Length of the source string. The **word-integer-source-length** argument is the
address of an unsigned word containing the length of the source string.


**source-string-address**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by reference


Source string that STR$COPY_R copies into the destination string. The **source-**
**string-address** argument is the address of the source string.


STR–27


**STR$ Routines**
**STR$COPY_R**


**Description**


STR$COPY_R copies a source string passed by reference to a destination string
passed by descriptor. All conditions except success and truncation are signaled;
truncation is returned as a warning condition value.


A JSB entry point is provided, with R0 being the first argument, R1 the second,
and R2 the third. The length argument is passed in bits 15:0 of R1.


The actions taken by STR$COPY_R depend on the descriptor class of the
destination string. The following table describes these actions for each
appropriate descriptor class:


**Descriptor Class** **Action**


S, Z, SD, A, NCA Copy the source string. If needed, space fill or truncate on
the right.

D If the area specified by the destination descriptor is large
enough to contain the source string, copy the source string
and set the new length in the destination descriptor.

If the area specified is not large enough, return the previous
space allocation, if any, and then dynamically allocate the
amount of space needed. Copy the source string and set the
new length and address in the destination descriptor.

VS Copy source string to destination string up to the limit
of the descriptor’s MAXSTRLEN field with no padding.
Readjust the string’s current length (CURLEN) field to the
actual number of bytes copied.


**Condition Values Returned**


SS$_NORMAL Normal successful completion. All characters in
the input string were copied to the destination
string.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters
copied from the source string.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$COPY_R
could not allocate heap storage for a dynamic or
temporary string.


STR–28


**STR$ Routines**
**STR$COPY_R_64 (Alpha Only)**

#### **STR$COPY_R_64 (Alpha Only)** **Copy a Source String Passed by Reference to Destination String**


The Copy a Source String Passed by Reference to a Destination String routine
copies a source string passed by reference to a destination string passed by
descriptor.


**Format**


STR$COPY_R_64 destination-string,quad-integer-source-length
,source-string-address


**Corresponding JSB Entry Point**


STR$COPY_R_R8


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$COPY_R_64 copies the source string. The
**destination-string** argument is the address of a descriptor pointing to the
destination string.


The class field determines the appropriate action.


See the description of LIB$ANALYZE_SDESC for restrictions associated with
specific descriptor classes.


**quad-integer-source-length**
OpenVMS usage: quadword_unsigned
type: quadword (unsigned)
access: read only
mechanism: by reference


Length of the source string. The **quad-integer-source-length** argument is the
address of an unsigned quadword containing the length of the source string.


**source-string-address**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by reference


Source string that STR$COPY_R_64 copies into the destination string. The
**source-string-address** argument is the address of the source string.


STR–29


**STR$ Routines**
**STR$COPY_R_64 (Alpha Only)**


**Description**


STR$COPY_R_64 copies a source string passed by reference to a destination
string passed by descriptor. All conditions except success and truncation are
signaled; truncation is returned as a warning condition value.


A JSB entry point is provided, with R0 being the first argument, R1 the second,
and R2 the third. The length argument is passed in bits 15:0 of R1.


The actions taken by STR$COPY_R_64 depend on the descriptor class of
the destination string. The following table describes these actions for each
appropriate descriptor class:


**Descriptor Class** **Action**


S, Z, SD, A, NCA Copy the source string. If needed, space fill or truncate on
the right.

D If the area specified by the destination descriptor is large
enough to contain the source string, copy the source string
and set the new length in the destination descriptor.

If the area specified is not large enough, return the previous
space allocation, if any, and then dynamically allocate the
amount of space needed. Copy the source string and set the
new length and address in the destination descriptor.

VS Copy source string to destination string up to the limit
of the descriptor’s MAXSTRLEN field with no padding.
Readjust the string’s current length (CURLEN) field to the
actual number of bytes copied.


**Condition Values Returned**


SS$_NORMAL Normal successful completion. All characters in
the input string were copied to the destination
string.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters
copied from the source string.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$COPY_R_64
could not allocate heap storage for a dynamic or
temporary string.


STR–30


**STR$ Routines**
**STR$DIVIDE**

#### **STR$DIVIDE** **Divide Two Decimal Strings**


The Divide Two Decimal Strings routine divides two decimal strings.


**Format**


STR$DIVIDE asign,aexp,adigits,bsign,bexp,bdigits,total-digits
,round-truncate-indicator,csign,cexp,cdigits


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**asign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by reference


Sign of the first operand. The **asign** argument is the address of an unsigned
longword containing the sign of the first operand. A value of 0 is considered
positive; a value of 1 is considered negative.


**aexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Power of 10 by which **adigits** is multiplied to get the absolute value of the first
operand. The **aexp** argument is the address of the first operand’s exponent.


**adigits**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


First operand’s numeric text string. The **adigits** argument is the address of a
descriptor pointing to the first operand’s numeric string. The string must be an
unsigned decimal number.


**bsign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by reference


STR–31


**STR$ Routines**
**STR$DIVIDE**


Sign of the second operand. The **bsign** argument is the address of an unsigned
longword containing the second operand’s string. A value of 0 is considered
positive; a value of 1 is considered negative.


**bexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Power of 10 by which **bdigits** is multiplied to get the absolute value of the second
operand. The **bexp** argument is the address of the second operand’s exponent.


**bdigits**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Second operand’s numeric text string. The **bdigits** argument is the address of a
descriptor pointing to the second operand’s number string. The string must be an
unsigned decimal number.


**total-digits**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Number of digits to the right of the decimal point. The **total-digits** argument
is the address of a signed longword containing the number of total digits.
STR$DIVIDE uses this number to carry out the division.


**round-truncate-indicator**

OpenVMS usage: mask_longword
type: longword (unsigned)
access: read only
mechanism: by reference


Indicator of whether STR$DIVIDE is to round or truncate the result; a value of
0 means truncate; a value of 1 means round. The **round-truncate-indicator**
argument is the address of a longword bit mask containing this indicator.


**csign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: write only
mechanism: by reference


Sign of the result. The **csign** argument is the address of an unsigned longword
containing the sign of the result. A value of 0 is considered positive; a value of 1
is considered negative.


STR–32


**Description**



**STR$ Routines**
**STR$DIVIDE**


**cexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by reference


Power of 10 by which **cdigits** is multiplied to get the absolute value of the result.
The **cexp** argument is the address of a signed longword containing the exponent.


**cdigits**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Result’s numeric text string. The **cdigits** argument is the address of a descriptor
pointing to the numeric string of the result. This string is an unsigned decimal
number.


STR$DIVIDE divides two decimal strings. The divisor and dividend are passed to
STR$DIVIDE in three parts: ( 1 ) the sign of the decimal number, ( 2 ) the power
of 10 needed to obtain the absolute value, and ( 3 ) the numeric string. The result
of the division is also returned in those three parts.



**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters in
the result.


**Condition Values Signaled**


LIB$_INVARG Invalid argument.

STR$_DIVBY_ZER Division by zero.

STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$DIVIDE
could not allocate heap storage for a dynamic
or temporary string.

STR$_WRONUMARG Wrong number of arguments.


STR–33


**STR$ Routines**
**STR$DIVIDE**


**Example**

```
        100 !+
          ! This BASIC example program uses STR$DIVIDE
          ! to divide two decimal strings and truncates
          ! the result.

          !
          ASIGN% = 1%

          AEXP% = 3%
          ADIGITS$ = ’1’
          BSIGN% = 0%

          BEXP% = -4%
          BDIGITS$ = ’2’
          CSIGN% = 0%

          CEXP% = 0%
          CDIGITS$ = ’0’
          PRINT "A = "; ASIGN%; AEXP%; ADIGITS$
          PRINT "B = "; BSIGN%; BEXP%; BDIGITS$
          CALL STR$DIVIDE (ASIGN%, AEXP%, ADIGITS$, &
                     BSIGN%, BEXP%, BDIGITS$, &
                     3%, 0%, CSIGN%, CEXP%, CDIGITS$)
           PRINT "C = "; CSIGN%; CEXP%; CDIGITS$
        1500 END

```

This BASIC program uses STR$DIVIDE to divide two decimal strings, A divided
by B, where the following values apply:


A = –1000 (ASIGN = 1, AEXP = 3, ADIGITS = `’` 1 `’` )
B = .0002 (BSIGN = 0, BEXP = –4, BDIGITS = `’` 2 `’` )


The output generated by this program is as follows:

```
          A = 1 3 1

          B = 0 -4 2

          C = 1 -3 5000000000

```

Thus, the decimal value of C equals –5000000 (CSIGN = 1, CEXP = –3, CDIGITS
= 5000000000).


STR–34


**STR$ Routines**
**STR$DUPL_CHAR**

#### **STR$DUPL_CHAR** **Duplicate Character n Times**


The Duplicate Character _n_ Times routine generates a string containing _n_
duplicates of the input character. If the destination string is an ‘‘empty’’ dynamiclength string descriptor, STR$DUPL_CHAR allocates and initializes the string.


**Format**


STR$DUPL_CHAR destination-string [,repetition-count] [,ASCII-character]


**Corresponding JSB Entry Point**


STR$DUPL_CHAR_R8


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$DUPL_CHAR writes **repetition-count**
copies of the input character. The **destination-string** argument is the address
of a descriptor pointing to the destination string. The maximum length of the
destination string for a 32-bit descriptor is 2 [16] —1, or 65,535, bytes.


On Alpha systems, the maximum length of the destination string for all 64-bit
descriptor classes, except varying strings, is 2 [64] —1 bytes. The maximum length
of a varying-length string is 2 [16] —1 for both 32-bit and 64-bit descriptors.


**repetition-count**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Number of times **ASCII-character** is duplicated; this is an optional argument
(if omitted, the default is 1). The **repetition-count** argument is the address of a
signed longword containing the number.


**ASCII-character**

OpenVMS usage: char_string
type: character string
access: read only
mechanism: by reference


STR–35


**STR$ Routines**
**STR$DUPL_CHAR**


ASCII character that STR$DUPL_CHAR writes **repetition-count** times into the
destination string. The **ASCII-character** argument is the address of a character
string containing this character. This is an optional argument; if omitted, the
default is a space.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_NEGSTRLEN Alternate success. The length argument
contained a negative value; zero was used.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$DUPL_CHAR
could not allocate heap storage for a dynamic or
temporary string.

STR$_STRTOOLON String length exceeds the maximum allowed for
the **destination-string** descriptor.


**Example**

```
        10 !+
          ! This example uses STR$DUPL_CHAR to
          ! duplicate the character ’A’ four times.
          !
          EXTERNAL INTEGER FUNCTION STR$DUPL_CHAR
          STATUS% = STR$DUPL_CHAR (X$, 4%, ’A’ BY REF)
          PRINT X$

          END

```

These BASIC statements set X$ equal to `’` AAAA `’` .


The output generated by this program is as follows:

```
          AAAA

```

STR–36


**STR$ Routines**
**STR$ELEMENT**

#### **STR$ELEMENT** **Extract Delimited Element Substring**


The Extract Delimited Element Substring routine extracts an element from a
string in which the elements are separated by a specified delimiter.


**Format**


STR$ELEMENT destination-string,element-number,delimiter-string,source-string


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$ELEMENT copies the selected substring.
The **destination-string** argument is the address of a descriptor pointing to the
destination string.


**element-number**

OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Element number of the delimited element substring to be returned. The
**element-number** argument is the address of a signed longword containing
the desired element number. Zero is used to represent the first delimited element
substring, one is used to represent the second, and so forth.


**delimiter-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Delimiter string used to separate element substrings. The **delimiter-string**
argument is the address of a descriptor pointing to the delimiter string. The
**delimiter-string** argument must be exactly one character long.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


STR–37


**STR$ Routines**
**STR$ELEMENT**


Source string from which STR$ELEMENT extracts the requested delimited
substring. The **source-string** argument is the address of a descriptor pointing to
the source string.


**Description**


STR$ELEMENT extracts an element from a string in which the elements are
separated by a specified delimiter.


For example, if **source-string** is MON^TUE^WED^THU^FRI^SAT^SUN,
**delimiter-string** is ^, and **element-number** is 2, then STR$ELEMENT returns
the string WED.


Once the specified element is located, all the characters in that delimited element
are returned. That is, all characters between the **element-number** and the
**element-number** + 1 delimiters are written to **destination-string** . At least
**element-number** delimiters must be found. If exactly **element-number**
delimiters are found, then all values from the **element-number** delimiter to the
end of the string are returned. If **element-number** equals 0 and no delimiters
are found, the entire input string is returned.


STR$ELEMENT duplicates the functions of the DCL lexical function
F$ELEMENT.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_INVDELIM Delimiter string is not exactly one character long
(warning).

STR$_NOELEM Not enough delimited characters found to satisfy
requested element number (warning).

STR$_TRU String truncation. The destination string could
not contain all the characters in the delimited

substring (warning).


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$ELEMENT
could not allocate heap storage for a dynamic or
temporary string.


STR–38


**STR$ Routines**
**STR$FIND_FIRST_IN_SET**

#### **STR$FIND_FIRST_IN_SET** **Find First Character in a Set of Characters**


The Find First Character in a Set of Characters routine searches a string,
comparing each character to the characters in a specified set of characters. The
string is searched character by character, from left to right. STR$FIND_FIRST_
IN_SET returns the position of the first character in the string that matches any
of the characters in the selected set of characters.


**Format**


STR$FIND_FIRST_IN_SET source-string,set-of-characters


**Returns**


OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by value


Position in **source-string** where the first match is found; zero if no match is
found.


On Alpha systems, if the relative position of the substring can exceed 2 [32] —1,
assign the return value to a quadword to ensure that you retrieve the correct
relative position.


**Arguments**


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


String that STR$FIND_FIRST_IN_SET compares to the set of characters, looking
for the first match. The **source-string** argument is the address of a descriptor
pointing to the character string.


**set-of-characters**

OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Set of characters that STR$FIND_FIRST_IN_SET is searching for in the string.
The **source-string** argument is the address of a descriptor pointing to the set of
characters.


**Description**


STR$FIND_FIRST_IN_SET compares each character in the string to every
character in the specified set of characters. As soon as the first match is found,
STR$FIND_FIRST_IN_SET returns the position in the string where the matching
character was found. If no match is found, 0 is returned. If either **source-string**
or **set-of-characters** is of zero length, 0 is returned.


STR–39


**STR$ Routines**
**STR$FIND_FIRST_IN_SET**


**Condition Value Signaled**


STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.


**Example**

```
        PROGRAM FIND_FIRST(INPUT, OUTPUT);

        {+}
        { This example uses STR$FIND_FIRST_IN_SET
        { to find the first character in the source
        { string (STRING1) that matches a character
        { in the set of characters being searched for
        { (CHARS).
        {
        { First, declare the external function.
        {-}

        FUNCTION STR$FIND_FIRST_IN_SET(STRING :
             VARYING [A] OF CHAR; SETOFCHARS :
             VARYING [B] OF CHAR) : INTEGER;
             EXTERN;

        {+}
        { Declare the variables used in the main program.
        {-}

        VAR

         STRING1 : VARYING [256] OF CHAR;
         CHARS : VARYING [256] OF CHAR;
         RET_STATUS : INTEGER;

        {+}
        { Begin the main program. Read the source string
        { and the set of characters being searched for. Call
        { STR$FIND_FIRST_IN_SET to find the first match.
        { Print the result.
        {-}

        BEGIN

         WRITELN(’ENTER THE STRING: ’);
         READLN(STRING1);
         WRITELN(’ENTER THE SET OF CHARACTERS: ’);
         READLN(CHARS);
         RET_STATUS := STR$FIND_FIRST_IN_SET(STRING1, CHARS);
         WRITELN(RET_STATUS);

        END.

```

This Pascal program demonstrates the use of STR$FIND_FIRST_IN_SET. If you
run this program and set STRING1 equal to ABCDEFGHIJK and CHARS equal
to XYZA, the value of RET_STATUS is 1. The output generated by this program
is as follows:

```
          ENTER THE STRING:

          ABCDEFGHIJK

          ENTER THE SET OF CHARACTERS:

          XYZA

              1

```

STR–40


**STR$ Routines**
**STR$FIND_FIRST_NOT_IN_SET**

#### **STR$FIND_FIRST_NOT_IN_SET** **Find First Character That Does Not Occur in Set**


The Find First Character That Does Not Occur in Set routine searches a string,
comparing each character to the characters in a specified set of characters. The
string is searched character by character, from left to right. STR$FIND_FIRST_
NOT_IN_SET returns the position of the first character in the string that does
not match any of the characters in the selected set of characters.


**Format**


STR$FIND_FIRST_NOT_IN_SET source-string,set-of-characters


**Returns**


OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by value


Position in **source-string** where a nonmatch was found.


On Alpha systems, if the relative position of the substring can exceed 2 [32] —1,
assign the return value to a quadword to ensure that you retrieve the correct
relative position.


**Returned Value** **Condition**


0 Either all characters in **source-string** match some
characters in **set-of-characters**, or there were no

characters in **set-of-characters** .

1 Either the first nonmatching character in **source-string**
was found in position 1, or there were no characters in
**source-string** .

N The first nonmatching character was found in position N
within **source-string** .


**Arguments**


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


String that STR$FIND_FIRST_NOT_IN_SET searches. The **source-string**
argument is the address of a descriptor pointing to the string.


**set-of-characters**

OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


STR–41


**STR$ Routines**
**STR$FIND_FIRST_NOT_IN_SET**


The set of characters that STR$FIND_FIRST_NOT_IN_SET compares to the
string, looking for a nonmatch. The **set-of-characters** argument is the address
of a descriptor pointing to this set of characters.


**Description**


STR$FIND_FIRST_NOT_IN_SET searches a string, comparing each character to
the characters in a specified set of characters. The string is searched character
by character, from left to right. When STR$FIND_FIRST_NOT_IN_SET finds a
character from the string that is not in **set-of-characters**, it stops searching and
returns, as the value of STR$FIND_FIRST_NOT_IN_SET, the position in **source-**
**string** where it found the nonmatching character. If all characters in the string
match some character in the set of characters, STR$FIND_FIRST_NOT_IN_SET
returns 0. If the string is of zero length, the position returned is 1 since none of
the elements in the set of characters (particularly the first element) can be found
in the string. If there are no characters in the set of characters, 0 is returned
since ‘‘nothing’’ can always be found.


**Condition Value Signaled**


STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.


**Example**

```
        PROGRAM NOT_IN_SET(INPUT, OUTPUT);

        {+}
        { This example uses STR$FIND_FIRST_NOT_IN_SET
        { to find the position of the first nonmatching
        { character from a set of characters (CHARS)
        { in a source string (STRING1).
        {
        { First, declare the external function.
        {-}

        FUNCTION STR$FIND_FIRST_NOT_IN_SET(STRING :
             VARYING [A] OF CHAR; SETOFCHARS :
             VARYING [B] OF CHAR) : INTEGER;
             EXTERN;
        {+}
        { Declare the variables used in the main program.
        {-}

        VAR

         STRING1 : VARYING [256] OF CHAR;
         CHARS : VARYING [256] OF CHAR;
         RET_STATUS : INTEGER;

        {+}
        { Begin the main program. Read the source string
        { and set of characters. Call STR$FIND_FIRST_NOT_IN_SET.
        { Print the result.
        {-}

```

STR–42


**STR$ Routines**
**STR$FIND_FIRST_NOT_IN_SET**

```
BEGIN

 WRITELN(’ENTER THE STRING: ’);
 READLN(STRING1);
 WRITELN(’ENTER THE SET OF CHARACTERS: ’);
 READLN(CHARS);
 RET_STATUS := STR$FIND_FIRST_NOT_IN_SET(STRING1, CHARS);
 WRITELN(RET_STATUS);

END.

```

This Pascal program demonstrates the use of STR$FIND_FIRST_NOT_IN_SET.
If you run this program and set STRING1 equal to FORTUNATE and CHARS
equal to FORT, the value of RET_STATUS is 5.


The output generated by this program is as follows:

```
  ENTER THE STRING:

  FORTUNATE

  ENTER THE SET OF CHARACTERS:

  FORT

      5

```

STR–43


**STR$ Routines**
**STR$FIND_FIRST_SUBSTRING**

#### **STR$FIND_FIRST_SUBSTRING** **Find First Substring in Input String**


The Find First Substring in Input String routine finds the first substring (in a
provided list of substrings) occurring in a given string.


**Format**


STR$FIND_FIRST_SUBSTRING source-string,index,substring-index,substring

[,substring...]


**Returns**


OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: write only
mechanism: by value


The values returned by STR$FIND_FIRST_SUBSTRING and the conditions to
which they translate are as follows:


**Returned Value** **Condition**


0 **source-string** did not contain any of the specified
substrings.

1 STR$FIND_FIRST_SUBSTRING found at least one of
the specified substrings in **source-string** .


**Arguments**


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


String that STR$FIND_FIRST_SUBSTRING searches. The **source-string**
argument is the address of a descriptor pointing to the string.


**index**

OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by reference


Earliest position within **source-string** at which STR$FIND_FIRST_SUBSTRING
found a matching substring; zero if no matching substring was found. The **index**
argument is the address of a signed longword containing this position.


**substring-index**
OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by reference


STR–44


**Description**



**STR$ Routines**
**STR$FIND_FIRST_SUBSTRING**


Ordinal number of the **substring** that matched (1 for the first, 2 for the second,
and so on), or zero if STR$FIND_FIRST_SUBSTRING found no substrings that
matched. The **substring-index** argument is the address of a signed longword
containing this ordinal number.


**substring**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Specified substring for which STR$FIND_FIRST_SUBSTRING searches in
**source-string** . The **substring** argument is the address of a descriptor pointing
to the first substring. You can specify multiple substrings to search for.


**substring**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Additional specified substring for which STR$FIND_FIRST_SUBSTRING
searches in **source-string** . The **substring** argument is the address of a
descriptor pointing to the substring. You can specify multiple substrings to
search for.


STR$FIND_FIRST_SUBSTRING takes as input a string to be searched and an
unspecified number of substrings for which to search. It searches the specified
string and returns the position of the substring that is found earliest in the
string. This is not necessarily the position of the first substring specified. That
is, STR$FIND_FIRST_SUBSTRING returns the position of the leftmost matching
substring. The order in which the substrings are searched for is irrelevant.


Unlike many of the compare and search routines, STR$FIND_FIRST_
SUBSTRING does not return the position in a return value. The position of
the substring which is found earliest in the string is returned in the **index**
argument. If none of the specified substrings is found in the string, the value of
**index** is 0.


Zero-length strings, or null arguments, produce unexpected results. Any time
the routine is called with a null substring as an argument, STR$FIND_FIRST_
SUBSTRING always returns the position of the null substring as the first
substring found. All other substrings are interpreted as appearing in the string
after the null string.



**Condition Values Signaled**


STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_WRONUMARG Wrong number of arguments. You must supply
at least one substring.


STR–45


**STR$ Routines**
**STR$FIND_FIRST_SUBSTRING**


**Example**

```
        1 !+
          ! This is a BASIC program demonstrating the use of
          ! STR$FIND_FIRST_SUBSTRING. This program takes as input
          ! four strings that are listed in a data statement
          ! at the end of the program. STR$FIND_FIRST_SUBSTRING
          ! is called four times (once for each string)
          ! to find the first substring occurring in the given
          ! string.
          !
          OPTION TYPE = EXPLICIT

          DECLARE STRING MATCH_STRING
          DECLARE LONG RET_STATUS, &
                     INDEX, &
                     I, &
                     SUB_STRING_NUM
           EXTERNAL LONG FUNCTION STR$FIND_FIRST_SUBSTRING

           FOR I = 1 TO 4

            READ MATCH_STRING
            RET_STATUS = STR$FIND_FIRST_SUBSTRING( MATCH_STRING, &
              INDEX, SUB_STRING_NUM, ’ING’, ’CK’, ’TH’)
            IF RET_STATUS = 0% THEN
              PRINT MATCH_STRING;" did not contain any of the substrings"
            ELSE

              SELECT SUB_STRING_NUM
                 CASE 1
                   PRINT MATCH_STRING;" contains ING at position";INDEX
                 CASE 2
                   PRINT MATCH_STRING;" contains CK at position";INDEX
                 CASE 3
                   PRINT MATCH_STRING;" contains TH at position";INDEX
              END SELECT

            END IF

           NEXT I

        2 DATA CHUCKLE, RAINING, FOURTH, THICK

        3 END

```

This BASIC program demonstrates the use of STR$FIND_FIRST_SUBSTRING.
The output generated by this program is as follows:

```
          $ BASIC FINDSUB
          $ LINK FINDSUB
          $ RUN FINDSUB
          CHUCKLE contains CK at position 4
          RAINING contains ING at position 5
          FOURTH contains TH at position 5
          THICK contains TH at position 1

```

Note that ‘‘THICK’’ contains both the substrings ‘‘TH’’ and ‘‘CK’’. STR$FIND_
FIRST_SUBSTRING locates the ‘‘CK’’ substring in ‘‘THICK’’, and then locates
the ‘‘TH’’ substring. However, since the ‘‘TH’’ substring is the earliest, or leftmost
matching substring, its ordinal number is returned in **substring-index**, and the
point at which ‘‘TH’’ occurs is returned in **index** .


STR–46


**STR$ Routines**
**STR$FREE1_DX**

#### **STR$FREE1_DX** **Free One Dynamic String**


The Free One Dynamic String routine deallocates one dynamic string.


**Format**


STR$FREE1_DX string-descriptor


**Corresponding JSB Entry Point**


STR$FREE1_DX_R4


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Argument**


**string-descriptor**
OpenVMS usage: char_string
type: character string
access: modify
mechanism: by descriptor


Dynamic string descriptor of the dynamic string that STR$FREE1_DX
deallocates. The **string-descriptor** argument is the address of a descriptor
pointing to the string to be deallocated. The descriptor’s CLASS field is checked.


**Description**


STR$FREE1_DX deallocates the described string space and flags the descriptor
as describing no string at all. The descriptor’s POINTER and LENGTH fields
contain 0.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$ERRFREDYN Error freeing dynamic string descriptor.
LIB$FREE_VM OR LIB$FREE_VM_64 failed
to free the descriptor.


STR–47


**STR$ Routines**
**STR$FREE1_DX**


STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.


STR–48


**STR$ Routines**
**STR$GET1_DX**

#### **STR$GET1_DX** **Allocate One Dynamic String**


The Allocate One Dynamic String routine allocates a specified number of bytes of
virtual memory to a specified dynamic string descriptor.


**Format**


STR$GET1_DX word-integer-length,character-string


**Corresponding JSB Entry Point**


STR$GET1_DX_R4


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**word-integer-length**
OpenVMS usage: word_unsigned
type: word (unsigned)
access: read only
mechanism: by reference


Number of bytes that STR$GET1_DX allocates. The **word-integer-length**
argument is the address of an unsigned word containing this number.


**character-string**
OpenVMS usage: char_string
type: character string
access: modify
mechanism: by descriptor


Dynamic string descriptor to which STR$GET1_DX allocates the area. The
**character-string** argument is the address of the descriptor. The descriptor’s
CLASS field is checked.


**Description**


STR$GET1_DX allocates a specified number of bytes of dynamic virtual memory
to a specified string descriptor. The descriptor must be dynamic.


If the string descriptor already has dynamic memory allocated to it, but the
amount allocated is less than **word-integer-length**, STR$GET1_DX deallocates
that space before it allocates new space.


STR–49


**STR$ Routines**
**STR$GET1_DX**


**Note**


Compaq recommends use of the STR$GET1_DX or STR$GET1_DX_64
(Alpha only) routine for allocating a string to a dynamic-length string
descriptor. Simply filling in the length and pointer fields of a dynamiclength string descriptor can cause serious and unexpected problems with
string management.


Use STR$FREE1_DX to deallocate a string allocated by STR$GET1_DX.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$GET1_DX
could not allocate heap storage for a dynamic or
temporary string.


STR–50


**STR$ Routines**
**STR$GET1_DX_64 (Alpha Only)**

#### **STR$GET1_DX_64 (Alpha Only)** **Allocate One Dynamic String**


The Allocate One Dynamic String routine allocates a specified number of bytes of
virtual memory to a specified dynamic string descriptor.


**Format**


STR$GET1_DX_64 quad-integer-length,character-string


**Corresponding JSB Entry Point**


STR$GET1_DX_R4


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**quad-integer-length**
OpenVMS usage: quadword_unsigned
type: quadword (unsigned)
access: read only
mechanism: by reference


Number of bytes that STR$GET1_DX_64 allocates. The **quad-integer-length**
argument is the address of an unsigned quadword containing this number.


**character-string**
OpenVMS usage: char_string
type: character string
access: modify
mechanism: by descriptor


Dynamic string descriptor to which STR$GET1_DX_64 allocates the area. The
**character-string** argument is the address of the descriptor. The descriptor’s
CLASS field is checked.


**Description**


STR$GET1_DX_64 allocates a specified number of bytes of dynamic virtual
memory to a specified 64-bit string descriptor. The descriptor must be dynamic.


If the string descriptor already has dynamic memory allocated to it, but
the amount allocated is less than **quad-integer-length**, STR$GET1_DX_64
deallocates that space before it allocates new space.


STR–51


**STR$ Routines**
**STR$GET1_DX_64 (Alpha Only)**


**Note**


Compaq recommends use of the STR$GET1_DX or STR$GET1_DX_64
(Alpha only) routine for allocating a string to a dynamic-length string
descriptor. Simply filling in the length and pointer fields of a dynamiclength string descriptor can cause serious and unexpected problems with
string management.


Use STR$FREE1_DX to deallocate a string allocated by STR$GET1_DX_64.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$GET1_DX_64
could not allocate heap storage for a dynamic or
temporary string.


STR–52


**STR$ Routines**
**STR$LEFT**

#### **STR$LEFT** **Extract a Substring of a String**


The Extract a Substring of a String routine copies a substring beginning at the
first character of a source string into a destination string.


**Format**


STR$LEFT destination-string,source-string,end-position


**Corresponding JSB Entry Point**


STR$LEFT_R8


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$LEFT copies the substring. The **destination-**
**string** argument is the address of a descriptor pointing to the destination
string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string from which STR$LEFT extracts the substring that it copies into the
destination string. The **source-string** argument is the address of a descriptor
pointing to the source string.


**end-position**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Relative position in the source string at which the substring ends. The **end-**
**position** argument is the address of a signed longword containing the ending
position.


STR$LEFT copies all characters in the source string from position 1 (the leftmost
position) to the position number specified in this **end-position** argument.


STR–53


**STR$ Routines**
**STR$LEFT**


**Description**


STR$LEFT extracts a substring from a source string and copies that substring
into a destination string. STR$LEFT defines the substring by specifying the
relative ending position in the source string. The relative starting position in
the source string is 1. The source string is unchanged, unless it is also the
destination string.


This is a variation of STR$POS_EXTR. Other routines that may be used to
extract and copy a substring are STR$RIGHT and STR$LEN_EXTR.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_ILLSTRPOS Alternate success. An argument referenced a
character position outside the specified string. A
default value was used.

STR$_ILLSTRSPE Alternate success. The length of the substring
was too long for the specified destination string.
Default values were used.

STR$_TRU String truncation warning. The destination
string could not contain all the characters copied
from the source string.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$LEFT could
not allocate heap storage for a dynamic or
temporary string.


**Example**

```
        PROGRAM LEFT(INPUT, OUTPUT);

        {+}
        { This Pascal program demonstrates the use of
        { STR$LEFT. This program reads in a source string
        { and the ending position of a substring.
        { It returns a substring consisting of all
        { characters from the beginning (left) of the
        { source string to the ending position entered.
        {-}

        {+}
        { Declare the external procedure, STR$LEFT.
        {-}

```

STR–54


**STR$ Routines**
**STR$LEFT**

```
PROCEDURE STR$LEFT(%DESCR DSTSTR: VARYING
     [A] OF CHAR; SRCSTR :
     VARYING [B] OF CHAR; ENDPOS :
     INTEGER); EXTERN;

{+}
{ Declare the variables used by this program.
{-}

VAR

 SRC_STR : VARYING [256] OF CHAR;
 DST_STR : VARYING [256] OF CHAR;
 END_POS : INTEGER;

{+}
{ Begin the main program. Read the source string
{ and ending position. Call STR$LEFT. Print the
{ results.
{-}

BEGIN

 WRITELN(’ENTER THE SOURCE STRING: ’);
 READLN(SRC_STR);
 WRITELN(’ENTER THE ENDING POSITION’);
 WRITELN(’OF THE SUBSTRING: ’);
 READLN(END_POS);
 STR$LEFT(DST_STR, SRC_STR, END_POS);
 WRITELN;
 WRITELN(’THE SUBSTRING IS: ’,DST_STR);

END.

```

This Pascal example shows the use of STR$LEFT. One sample of the output of
this program is as follows:

```
  $ PASCAL LEFT
  $ LINK LEFT
  $ RUN LEFT

  ENTER THE SOURCE STRING: MAGIC CARPET

  ENTER THE ENDING POSITION OF

  THE SUBSTRING: 9

  THE SUBSTRING IS: MAGIC CAR

```

STR–55


**STR$ Routines**
**STR$LEN_EXTR**

#### **STR$LEN_EXTR** **Extract a Substring of a String**


The Extract a Substring of a String routine copies a substring of a source string
into a destination string.


**Format**


STR$LEN_EXTR destination-string,source-string,start-position
,longword-integer-length


**Corresponding JSB Entry Point**


STR$LEN_EXTR_R8


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$LEN_EXTR copies the substring. The
**destination-string** argument is the address of a descriptor pointing to the
destination string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string from which STR$LEN_EXTR extracts the substring that it copies
into the destination string. The **source-string** argument is the address of a
descriptor pointing to the source string.


**start-position**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Relative position in the source string at which STR$LEN_EXTR begins copying
the substring. The **start-position** argument is the address of a signed longword
containing the starting position.


STR–56


**Description**



**STR$ Routines**
**STR$LEN_EXTR**


**longword-integer-length**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Number of characters in the substring that STR$LEN_EXTR copies to the
destination string. The **longword-integer-length** argument is the address of a
signed longword containing the length of the substring.


STR$LEN_EXTR extracts a substring from a source string and copies that
substring into a destination string.


STR$LEN_EXTR defines the substring by specifying the relative starting position
in the source string and the number of characters to be copied. The source string
is unchanged, unless it is also the destination string.


If the starting position is less than 1, 1 is used. If the starting position is greater
than the length of the source string, the null string is returned. If the length is
less than 1, the null string is also returned.


Other substring routines are STR$RIGHT, STR$LEFT, and STR$POS_EXTR.



**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_ILLSTRPOS STR$LEN_EXTR completed successfully, but an
argument referenced a character position outside
the specified string. A default value was used.

STR$_ILLSTRSPE STR$LEN_EXTR completed successfully, except
that the length was too long for the specified
string. Default values were used.

STR$_NEGSTRLEN STR$LEN_EXTR completed successfully, except
that **longword-integer-length** contained a
negative value. Zero was used.

STR$_TRU String truncation warning. The destination
string could not contain all the characters copied
from the source string.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.


STR–57


**STR$ Routines**
**STR$LEN_EXTR**


STR$_INSVIRMEM Insufficient virtual memory. STR$LEN_EXTR
could not allocate heap storage for a dynamic or
temporary string.


**Example**

```
            CHARACTER*131 IN_STRING
            CHARACTER*1 FRONT_CHAR
            CHARACTER*1 TAIL_CHAR
            INTEGER STR$LEN_EXTR, STR$REPLACE, STR$TRIM
            INTEGER FRONT_POSITION, TAIL_POSITION
        10 WRITE (6, 800)
        800 FORMAT (’ Enter a string, 131 characters or less:’,$)
            READ (5, 900, END=200) IN_STRING
        900 FORMAT (A)
            ISTATUS = STR$TRIM (IN_STRING, IN_STRING, LENGTH)

            DO 100 I = 1, LENGTH/2
            FRONT_POSITION = I
            TAIL_POSITION = LENGTH + 1 - I
            ISTATUS = STR$LEN_EXTR ( FRONT_CHAR, IN_STRING, FRONT_POSITION,
           A %REF(1))

            ISTATUS = STR$LEN_EXTR ( TAIL_CHAR, IN_STRING, TAIL_POSITION,
           A %REF(1))

            ISTATUS = STR$REPLACE ( IN_STRING, IN_STRING, FRONT_POSITION,
           A FRONT_POSITION, TAIL_CHAR)

            ISTATUS = STR$REPLACE ( IN_STRING, IN_STRING, TAIL_POSITION,
           A TAIL_POSITION, FRONT_CHAR)
        100 CONTINUE
            WRITE (6, 901) IN_STRING
        901 FORMAT (’ Reversed string is : ’,/,1X,A)
            GOTO 10

        200 CONTINUE

            END

```

This Fortran program accepts a string as input and writes the string in reverse
order as output. This program continues to prompt for input until Ctrl/Z is
pressed. One sample of the output generated by this program is as follows:

```
          $ FORTRAN REVERSE
          $ LINK REVERSE
          $ RUN REVERSE
          Enter a string, 131 characters or less: Elephants often have
          flat feet.
           Reversed string is :
           .teef talf evah netfo stnahpelE
          Enter a string, 131 characters or less: CTRL/Z
          $

```

STR–58


**STR$ Routines**
**STR$MATCH_WILD**

#### **STR$MATCH_WILD** **Match Wildcard Specification**


The Match Wildcard Specification routine compares a pattern string that includes
wildcard characters with a candidate string.


**Format**


STR$MATCH_WILD candidate-string,pattern-string


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


Returns a condition value of STR$_MATCH if the strings match and STR$_
NOMATCH if they do not match.


**Arguments**


**candidate-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


String that is compared to the pattern string. The **candidate-string** argument
is the address of a descriptor pointing to the candidate string.


**pattern-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


String containing wildcard characters. The **pattern-string** argument is the
address of a descriptor pointing to the pattern string. The wildcards in the
pattern string are translated when STR$MATCH_WILD searches the candidate
string to determine if it matches the pattern string.


**Description**


STR$MATCH_WILD translates wildcard characters and searches the candidate
string to determine if it matches the pattern string. The pattern string may
contain either one or both of the two wildcard characters, asterisk ( * ) and
percent ( % ). The asterisk character is mapped to zero or more characters. The
percent character is mapped to only one character.


The two wildcard characters that may be used in the pattern string may be
used only as wildcards. If the candidate string contains an asterisk or percent
character, the condition STR$_MATCH is returned. Wildcard characters are
translated literally. There is no restriction on whether either wildcard character
in the pattern string can match a percent or asterisk that is translated literally
in the candidate string.


STR–59


**STR$ Routines**
**STR$MATCH_WILD**


**Condition Values Returned**


STR$_MATCH The candidate string and the pattern string
match.

STR$_NOMATCH The candidate string and the pattern string do
not match.


**Condition Value Signaled**


STR$_ILLSTRCLA Illegal string class. Severe error. The descriptor
of **candidate-string** and/or **pattern-string**
contains a class code that is not supported by the
OpenVMS calling standard.


**Example**

```
        /*
         * Example program using STR$MATCH_WILD.

         *

         * The following program reads in a master pattern string and then
         * compares that to input strings until it reaches the end of the
         * input file. For each string comparison done, it prints
         * either ’Matches pattern string’ or ’Doesn’t match pattern string’.
         */

        declare str$match_wild
          external entry (character(*) varying, character(*) varying)
          returns (bit(1));

        example: procedure options(main);

          dcl pattern_string character(80) varying;
          dcl test_string character(80) varying;

          on endfile(sysin) stop;

          put skip;

          get list(pattern_string) options(prompt(’Pattern string> ’));

          do while( ’1’b );
            get skip list(test_string) options(prompt(’Test string> ’));
            if str$match_wild(test_string,pattern_string)
              then put skip list(’Matches pattern string’);
              else put skip list(’Doesn’’t match pattern string’);
            end;

          end;

```

STR–60


**STR$ Routines**
**STR$MATCH_WILD**


This PL/I program demonstrates the use of STR$MATCH_WILD. The output
generated by this program is as follows:

```
  $ PLI MATCH
  $ LINK MATCH
  $ RUN MATCH
  Pattern string> ’Must match me exactly.’
  Test string> ’Will this work? Must match me exactly.’
  Doesn’t match pattern string
  Test string> ’must match me exactly’
  Doesn’t match pattern string
  Test string> ’must match me exactly.’
  Doesn’t match pattern string
  Test string> ’Must match me exactly’
  Doesn’t match pattern string
  Test String> ’Must match me exactly.’
  Matches pattern string

```

STR–61


**STR$ Routines**
**STR$MUL**

#### **STR$MUL** **Multiply Two Decimal Strings**


The Multiply Two Decimal Strings routine multiplies two decimal strings.


**Format**


STR$MUL asign,aexp,adigits,bsign,bexp,bdigits,csign,cexp,cdigits


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**asign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by reference


Sign of the first operand. The **asign** argument is the address of an unsigned
longword containing the first operand’s sign. A value of 0 is considered positive; a
value of 1 is considered negative.


**aexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Power of 10 by which **adigits** is multiplied to get the absolute value of the first
operand. The **aexp** argument is the address of a signed longword containing this

exponent.


**adigits**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


First operand’s numeric text string. The **adigits** argument is the address of a
descriptor pointing to the numeric string of the first operand. The string must be
an unsigned decimal number.


**bsign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by reference


STR–62


**STR$ Routines**
**STR$MUL**


Sign of the second operand. The **bsign** argument is the address of an unsigned
longword containing the sign of the second operand. A value of 0 is considered
positive; a value of 1 is considered negative.


**bexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Power of 10 by which **bdigits** is multiplied to get the absolute value of the second
operand. The **bexp** argument is the address of a signed longword containing this

exponent.


**bdigits**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Second operand’s numeric text string. The **bdigits** argument is the address of a
descriptor pointing to the second operand’s numeric string. The string must be an
unsigned decimal number.


**csign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: write only
mechanism: by reference


Sign of the result. The **csign** argument is the address of an unsigned longword
containing the sign of the result. A value of 0 is considered positive; a value of 1
is considered negative.


**cexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by reference


Power of 10 by which **cdigits** is multiplied to get the absolute value of the result.
The **cexp** argument is the address of a signed longword containing this exponent.


**cdigits**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Result’s numeric text string. The **cdigits** argument is the address of a descriptor
pointing to the numeric string of the result. The string is an unsigned decimal
number.


STR–63


**STR$ Routines**
**STR$MUL**


**Description**


STR$MUL multiplies two decimal strings. The numbers to be multiplied are
passed to STR$MUL in three parts: ( 1 ) the sign of the decimal number, ( 2 ) the
power of 10 needed to obtain the absolute value, and ( 3 ) the numeric string. The
result of the multiplication is also returned in those three parts.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_TRU String truncation warning. The destination
string could not contain all the characters in the
result.


**Condition Values Signaled**


LIB$_INVARG Invalid argument.

STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$MUL could not
allocate heap storage for a dynamic or temporary
string.

STR$_WRONUMARG Wrong number of arguments.


**Example**

```
        100 !+
          ! This example program uses
          ! STR$MUL to multiply two decimal
          ! strings (A and B) and place the
          ! results in a third decimal string,
          ! (C)
          !
          ASIGN% = 1%

          AEXP% = 3%
          ADIGITS$ = ’1’
          BSIGN% = 0%

          BEXP% = -4%
          BDIGITS$ = ’2’
          CSIGN% = 0%

          CEXP% = 0%
          CDIGITS$ = ’0’
          PRINT "A = "; ASIGN%; AEXP%; ADIGITS$
          PRINT "B = "; BSIGN%; BEXP%; BDIGITS$
          CALL STR$MUL (ASIGN%, AEXP%, ADIGITS$, &
                     BSIGN%, BEXP%, BDIGITS$, &
                     CSIGN%, CEXP%, CDIGITS$)
          PRINT "C = "; CSIGN%; CEXP%; CDIGITS$
        999 END

```

STR–64


**STR$ Routines**
**STR$MUL**


This BASIC example uses STR$MUL to multiply two decimal strings, where the
following values apply:


A = –1000 (ASIGN = 1, AEXP = 3, ADIGITS = `’` 1 `’` )
B = .0002 (BSIGN = 0, BEXP = –4, BDIGITS = `’` 2 `’` )


The output generated by this program is as follows; note that the decimal value
C equals –.2 (CSIGN = 1, CEXP = –1, CDIGITS = 2).

```
  A = 1 3 1

  B = 0 -4 2

  C = 1 -1 2

```

STR–65


**STR$ Routines**
**STR$POSITION**

#### **STR$POSITION** **Return Relative Position of Substring**


The Return Relative Position of Substring routine searches for the first occurrence
of a single substring within a source string. If STR$POSITION finds the
substring, it returns the relative position of that substring. If the substring
is not found, STR$POSITION returns a zero.


**Format**


STR$POSITION source-string,substring [,start-position]


**Corresponding JSB Entry Point**


STR$POSITION_R6


**Returns**


OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: write only
mechanism: by value


Relative position of the first character of the substring. Zero is the value returned
if STR$POSITION did not find the substring.


On Alpha systems, if the relative position of the substring can exceed 2 [32] —1,
assign the return value to a quadword to ensure that you retrieve the correct
relative position.


**Arguments**


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string within which STR$POSITION searches for the substring. The
**source-string** argument is the address of a descriptor pointing to the source
string.


**substring**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Substring for which STR$POSITION searches. The **substring** argument is the
address of a descriptor pointing to the substring.


**start-position**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


STR–66


**Description**



**STR$ Routines**
**STR$POSITION**


Relative position in the source string at which STR$POSITION begins the search.
The **start-position** argument is the address of a signed longword containing the
starting position. Although this is an optional argument, it is required if you are
using the JSB entry point.


If **start-position** is not supplied, STR$POSITION starts the search at the first
character position of **source-string** .


STR$POSITION returns the relative position of the first occurrence of a substring
in the source string. The value returned is an unsigned longword. The relative
character positions are numbered 1, 2, 3, and so on. A value of 0 indicates that
the substring was not found.


If the substring has a zero length, the minimum value of **start-position** (and the
length of **source-string** plus one) is returned by STR$POSITION.


If the source string has a zero length and the substring has a nonzero length,
zero is returned, indicating that the substring was not found.



**Condition Values Signaled**


STR$_ILLSTRCLA Illegal string class. The class code found in the
string class field of a descriptor is not a string
class code allowed by the OpenVMS calling
standard.


**Example**

```
        PROGRAM POSITION(INPUT,OUTPUT);

        {+}
        { This example uses STR$POSITION to determine
        { the position of the first occurrence of
        { a substring (SUBSTRING) within a source
        { string (STRING1) after the starting
        { position (START).
        {
        { First, declare the external function.
        {-}

        FUNCTION STR$POSITION(SRCSTR : VARYING [A]
             OF CHAR; SUBSTR : VARYING [B] OF CHAR;
             STARTPOS : INTEGER) : INTEGER; EXTERN;
        {+}
        { Declare the variables used in the main program.
        {-}

        VAR

         STRING1 : VARYING [256] OF CHAR;
         SUBSTRING : VARYING [256] OF CHAR;
         START : INTEGER;
         RET_STATUS : INTEGER;

        {+}
        { Begin the main program. Read the string and substring.
        { Set START equal to 1 to begin looking for the substring
        { at the beginning of the source string. Call STR$POSITION
        { and print the result.
        {-}

```

STR–67


**STR$ Routines**
**STR$POSITION**

```
        BEGIN

         WRITELN(’ENTER THE STRING: ’);
         READLN(STRING1);
         WRITELN(’ENTER THE SUBSTRING: ’);
         READLN(SUBSTRING);
         START := 1;
         RET_STATUS := STR$POSITION(STRING1, SUBSTRING, START);
         WRITELN(RET_STATUS);

        END.

```

This Pascal program demonstrates the use of STR$POSITION. If you run this
program and set STRING1 equal to KITTEN and substring equal to TEN, the
value of RET_STATUS is 4.


The output generated by this program is as follows:

```
          ENTER THE STRING:

          KITTEN

          ENTER THE SUBSTRING:

          TEN

               4

```

STR–68


**STR$ Routines**
**STR$POS_EXTR**

#### **STR$POS_EXTR** **Extract a Substring of a String**


The Extract a Substring of a String routine copies a substring of a source string
into a destination string.


**Format**


STR$POS_EXTR destination-string,source-string,start-position,end-position


**Corresponding JSB Entry Point**


STR$POS_EXTR_R8


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$POS_EXTR copies the substring. The
**destination-string** argument is the address of a descriptor pointing to the
destination string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string from which STR$POS_EXTR extracts the substring that it copies
into the destination string. The **source-string** argument is the address of a
descriptor pointing to the source string.


**start-position**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference for CALL entry point, by value for JSB entry
point


Relative position in the source string at which STR$POS_EXTR begins copying
the substring. The **start-position** argument is the address of a signed longword
containing the starting position.


STR–69


**STR$ Routines**
**STR$POS_EXTR**


**end-position**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference for CALL entry point, by value for JSB entry
point


Relative position in the source string at which STR$POS_EXTR stops copying
the substring. The **end-position** argument is the address of a signed longword
containing the ending position.


**Description**


STR$POS_EXTR extracts a substring from a source string and copies the
substring into a destination string. STR$POS_EXTR defines the substring by
specifying the relative starting and ending positions in the source string. The
source string is unchanged, unless it is also the destination string.


If the starting position is less than 1, 1 is used. If the starting position is greater
than the length of the source string, the null string is returned. If the ending
position is greater than the length of the source string, the length of the source
string is used.


Other routines that can be used to extract and copy a substring are STR$LEFT,
STR$RIGHT, and STR$LEN_EXTR.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_ILLSTRPOS Alternate success. An argument referenced a
character position outside the specified string. A
default value was used.

STR$_ILLSTRSPE Alternate success. **End-position** was less than
**start-position** . Default values were used.

STR$_TRU String truncation warning. The destination
string could not contain all the characters copied
from the source string.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$POS_EXTR
could not allocate heap storage for a dynamic or
temporary string.


STR–70


**STR$ Routines**
**STR$PREFIX**

#### **STR$PREFIX** **Prefix a String**


The Prefix a String routine inserts a source string at the beginning of a
destination string. The destination string must be dynamic or varying length.


**Format**


STR$PREFIX destination-string,source-string


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string (dynamic or varying length). STR$PREFIX copies the source
string into the beginning of this destination string. The **destination-string**
argument is the address of a descriptor pointing to the destination string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string that STR$PREFIX copies into the beginning of the destination
string. The **source-string** argument is the address of a descriptor pointing to the
source string.


**Description**


STR$PREFIX inserts the source string at the beginning of the destination string.
The destination string must be dynamic or varying length.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters in
the result.


STR–71


**STR$ Routines**
**STR$PREFIX**


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$PREFIX
could not allocate heap storage for a dynamic or
temporary string.


**Example**

```
        10 !+
          ! This example uses STR$PREFIX to
          ! prefix a destination string (D$)
          ! with a source string (’ABCD’).
          !
          EXTERNAL INTEGER FUNCTION STR$PREFIX
          D$ = ’EFG’
          STATUS% = STR$PREFIX (D$, ’ABCD’)
          PRINT D$

          END

```

These BASIC statements set D$ equal to `’` ABCDEFG `’` .


STR–72


**STR$ Routines**
**STR$RECIP**

#### **STR$RECIP** **Reciprocal of a Decimal String**


The Reciprocal of a Decimal String routine takes the reciprocal of the first decimal
string to the precision limit specified by the second decimal string and returns
the result as a decimal string.


**Format**


STR$RECIP asign,aexp,adigits,bsign,bexp,bdigits,csign,cexp,cdigits


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**asign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by reference


Sign of the first operand. The **asign** argument is the address of an unsigned
longword containing the first operand’s sign. A value of 0 is considered positive; a
value of 1 is considered negative.


**aexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Power of 10 by which **adigits** is multiplied to get the absolute value of the first
operand. The **aexp** argument is the address of a signed longword containing this

exponent.


**adigits**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


First operand’s numeric text string. The **adigits** argument is the address of a
descriptor pointing to the first operand’s numeric string. The string must be an
unsigned decimal number.


**bsign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by reference


STR–73


**STR$ Routines**
**STR$RECIP**


Sign of the second operand. The **bsign** argument is the address of an unsigned
longword containing the sign of the second operand. A value of 0 is considered
positive; a value of 1 is considered negative.


**bexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Power of 10 by which **bdigits** is multiplied to get the absolute value of the second
operand. The **bexp** argument is the address of a signed longword containing this

exponent.


**bdigits**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Second operand’s numeric text string. The **bdigits** argument is the address of a
descriptor pointing to the second operand’s numeric string. The string must be an
unsigned decimal number.


**csign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: write only
mechanism: by reference


Sign of the result. The **csign** argument is the address of an unsigned longword
containing the result’s sign. A value of 0 is considered positive; a value of 1 is
considered negative.


**cexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by reference


Power of 10 by which **cdigits** is multiplied to get the absolute value of the result.
The **cexp** argument is the address of a signed longword containing this exponent.


**cdigits**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Result’s numeric text string. The **cdigits** argument is the address of a descriptor
pointing to the result’s numeric string. The string is an unsigned decimal
number.


STR–74


**Description**



**STR$ Routines**
**STR$RECIP**


STR$RECIP takes the reciprocal of the first decimal string to the precision limit
specified by the second decimal string and returns the result as a decimal string.



**Condition Values Returned**


SS$_NORMAL Routine successfully completed.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters in
the result.


**Condition Values Signaled**


LIB$_INVARG Invalid argument.

STR$_DIVBY_ZER Division by zero.

STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$RECIP could
not allocate heap storage for a dynamic or
temporary string.

STR$_WRONUMARG Wrong number of arguments.


**Example**

```
        100 !+
          ! This example program uses STR$RECIP to find the reciprocal of the
          ! first decimal string (A) to the precision specified in the second
          ! decimal string (B), and place the result in a third decimal string (C).
          !
          ASIGN% = 1%

          AEXP% = 3%
          ADIGITS$ = ’1’
          BSIGN% = 0%

          BEXP% = -4%
          BDIGITS$ = ’2’
          CSIGN% = 0%

          CEXP% = 0%
          CDIGITS$ = ’0’

          PRINT "A = "; ASIGN%; AEXP%; ADIGITS$
          PRINT "B = "; BSIGN%; BEXP%; BDIGITS$
          CALL STR$RECIP (ASIGN%, AEXP%, ADIGITS$, &
                     BSIGN%, BEXP%, BDIGITS$, &
                     CSIGN%, CEXP%, CDIGITS$)
          PRINT "C = "; CSIGN%; CEXP%; CDIGITS$

        999 END

```

STR–75


**STR$ Routines**
**STR$RECIP**


This BASIC example uses STR$RECIP to find the reciprocal of A to the precision
level specified in B, using the following values:


A = –1000 (ASIGN = 1, AEXP = 3, ADIGITS = `’` 1 `’` )
B = .0002 (BSIGN = 0, BEXP = –4, BDIGITS = `’` 2 `’` )


The output generated is as follows, yielding a decimal value of C equal to –.001:

```
          A = 1 3 1

          B = 0 -4 2

          C = 1 -3 1

```

STR–76


**STR$ Routines**
**STR$REPLACE**

#### **STR$REPLACE** **Replace a Substring**


The Replace a Substring routine copies a source string to a destination string,
replacing part of the string with another string. The substring to be replaced is
specified by its starting and ending positions.


**Format**


STR$REPLACE destination-string,source-string,start-position,end-position
,replacement-string


**Corresponding JSB Entry Point**


STR$REPLACE_R8


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$REPLACE writes the new string created when
it replaces the substring. The **destination-string** argument is the address of a
descriptor pointing to the destination string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string. The **source-string** argument is the address of a descriptor
pointing to the source string.


**start-position**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference for CALL entry point, by value for JSB entry
point


Position in the source string at which the substring that STR$REPLACE replaces
begins. The **start-position** argument is the address of a signed longword
containing the starting position. The position is relative to the start of the source
string.


STR–77


**STR$ Routines**
**STR$REPLACE**


**end-position**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference for CALL entry point, by value for JSB entry
point


Position in the source string at which the substring that STR$REPLACE replaces
ends. The **end-position** argument is the address of a signed longword containing
the ending position. The position is relative to the start of the source string.


**replacement-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Replacement string with which STR$REPLACE replaces the substring. The
**replacement-string** argument is the address of a descriptor pointing to
this replacement string. The value of **replacement-string** must be equal to
**end-position** minus **start-position** .


**Description**


STR$REPLACE copies a source string to a destination string, replacing part of
the string with another string. The substring to be replaced is specified by its
starting and ending positions.


If the starting position is less than 1, 1 is used. If the ending position is greater
than the length of the source string, the length of the source string is used. If the
starting position is greater than the ending position, the overlapping portion of
the source string will be copied twice.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_ILLSTRPOS Alternate success. An argument referenced a
character position outside the specified string. A
default value was used.

STR$_ILLSTRSPE Alternate success. The value of **end-position**
was less than the value of **start-position** or
the length of the substring was too long for the
specified string. Default values were used.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters.


STR–78


**STR$ Routines**
**STR$REPLACE**


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

LIB$_INVARG Invalid argument.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$REPLACE
could not allocate heap storage for a dynamic or
temporary string.


**Example**

```
        10 !+
          ! This example uses STR$REPLACE to
          ! replace all characters from the starting
          ! position (2%) to the ending position (3%)
          ! with characters from the replacement string
          ! (’XYZ’).
          !
          EXTERNAL INTEGER FUNCTION STR$REPLACE
          D$ = ’ABCD’
          STATUS% = STR$REPLACE (D$, D$, 2%, 3%, ’XYZ’)
          PRINT D$

          END

```

These BASIC statements set D$ equal to `’` AXYZD `’` .


STR–79


**STR$ Routines**
**STR$RIGHT**

#### **STR$RIGHT** **Extract a Substring of a String**


The Extract a Substring of a String routine copies a substring ending at the last
character of a source string into a destination string.


**Format**


STR$RIGHT destination-string,source-string,start-position


**Corresponding JSB Entry Point**


STR$RIGHT_R8


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$RIGHT copies the substring. The
**destination-string** argument is the address of a descriptor pointing to the
destination string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string from which STR$RIGHT extracts the substring that it copies
into the destination string. The **source-string** argument is the address of a
descriptor pointing to the source string.


**start-position**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference for CALL entry point, by value for JSB entry
point


Relative position in the source string at which the substring that STR$RIGHT
copies starts. The **start-position** argument is the address of a signed longword
containing the starting position.


STR–80


**Description**



**STR$ Routines**
**STR$RIGHT**


STR$RIGHT extracts a substring from a source string and copies that substring
into a destination string. STR$RIGHT defines the substring by specifying the
relative starting position. The relative ending position is equal to the length of
the source string. The source string is unchanged, unless it is also the destination
string.


If the starting position is less than 2, the entire source string is copied. If the
starting position is greater than the length of the source string, a null string is
copied.


This is a variation of STR$POS_EXTR. Other routines that can be used to extract
and copy a substring are STR$LEFT and STR$LEN_EXTR.



**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_ILLSTRPOS Alternate success. An argument referenced a
character position outside the specified string. A
default value was used.

STR$_TRU String truncation warning. The destination
string could not contain all the characters copied
from the source string.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

LIB$_INVARG Invalid argument.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$RIGHT could
not allocate heap storage for a dynamic or
temporary string.


**Example**

```
        PROGRAM RIGHT(INPUT, OUTPUT);

        {+}
        { This example uses STR$RIGHT to extract a substring
        { from a specified starting position (START_POS) to
        { the end (right side) of a source string (SRC_STR)
        { and write the result in a destination string (DST_STR).
        {
        { First, declare the external procedure.
        {-}

```

STR–81


**STR$ Routines**
**STR$RIGHT**

```
        PROCEDURE STR$RIGHT(%DESCR DSTSTR: VARYING
             [A] OF CHAR; SRCSTR : VARYING [B] OF CHAR;
             STARTPOS : INTEGER); EXTERN;
        {+}
        { Declare the variables used in the main program.
        {-}

        VAR

         SRC_STR : VARYING [256] OF CHAR;
         DST_STR : VARYING [256] OF CHAR;
         START_POS : INTEGER;

        {+}
        { Begin the main program. Read the source string
        { and starting position. Call STR$RIGHT to extract
        { the substring. Print the result.
        {-}

        BEGIN

         WRITELN(’ENTER THE SOURCE STRING: ’);
         READLN(SRC_STR);
         WRITELN(’ENTER THE STARTING POSITION’);
         WRITELN(’OF THE SUBSTRING: ’);
         READLN(START_POS);
         STR$RIGHT(DST_STR, SRC_STR, START_POS);
         WRITELN;
         WRITELN(’THE SUBSTRING IS: ’,DST_STR);

        END.

```

This Pascal program uses STR$RIGHT to extract a substring from a specified
starting position (START_POS) to the end of the source string. One sample of the
output is as follows:

```
          $ RUN RIGHT

          ENTER THE SOURCE STRING: BLUE PLANETS ALWAYS HAVE PURPLE PLANTS

          ENTER THE STARTING POSITION

          OF THE SUBSTRING: 27

          THE SUBSTRING IS: URPLE PLANTS

```

STR–82


**STR$ Routines**
**STR$ROUND**

#### **STR$ROUND** **Round or Truncate a Decimal String**


The Round or Truncate a Decimal String routine rounds or truncates a decimal
string to a specified number of significant digits and places the result in another
decimal string.


**Format**


STR$ROUND places,flags,asign,aexp,adigits,csign,cexp,cdigits


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**places**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


Maximum number of decimal digits that STR$ROUND retains in the result. The
**places** argument is the address of a signed longword containing the number of
decimal digits.


**flags**
OpenVMS usage: mask_longword
type: longword (unsigned)
access: read only
mechanism: by reference


Function flag. A value of 0 indicates that the decimal string is rounded; a value of
1 indicates that it is truncated. The **flags** argument is the address of an unsigned
longword containing this function flag.


**asign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: read only
mechanism: by reference


Sign of the decimal input string to be rounded or truncated. The **asign** argument
is the address of an unsigned longword string containing this sign. A value of 0
is considered positive; a value of 1 is considered negative.


**aexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: read only
mechanism: by reference


STR–83


**STR$ Routines**
**STR$ROUND**


Power of 10 by which **adigits** is multiplied to get the absolute value of the
decimal input string. The **aexp** argument is the address of a signed longword
containing this exponent.


**adigits**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Decimal input string. This is the string of digits to which **asign** and **aexp** are
applied. The **adigits** argument is the address of a descriptor pointing to this
numeric string. The string must be an unsigned decimal number.


**csign**
OpenVMS usage: longword_unsigned
type: longword (unsigned)
access: write only
mechanism: by reference


Sign of the result. The **csign** argument is the address of an unsigned longword
containing the result’s sign. A value of 0 is considered positive; a value of 1 is
considered negative.


**cexp**
OpenVMS usage: longword_signed
type: longword (signed)
access: write only
mechanism: by reference


Power of 10 by which **cdigits** is multiplied to get the absolute value of the result.
The **cexp** argument is the address of a signed longword containing this exponent.


**cdigits**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Result’s numeric text string. The **cdigits** argument is the address of a descriptor
pointing to this numeric string. The string is an unsigned decimal number.


**Description**


The Round or Truncate a Decimal String routine rounds or truncates a decimal
string to a specified number of significant digits and places the result in another
decimal string.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters.


STR–84


**STR$ Routines**
**STR$ROUND**


**Condition Values Signaled**


LIB$_INVARG Invalid argument.

STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$ROUND
could not allocate heap storage for a dynamic or
temporary string.

STR$_WRONUMARG Wrong number of arguments.


**Example**

```
        100 !+
          ! This example shows the difference between the values obtained
          ! when rounding or truncating a decimal string.
          !
          ASIGN% = 0%

          AEXP% = -4%
          ADIGITS$ = ’9999998’
          CSIGN% = 0%

          CEXP% = 0%
          CDIGITS$ = ’0’
          PRINT "A = "; ASIGN%; AEXP%; ADIGITS$
          !+
          ! First, call STR$ROUND to round the value of A.
          !          CALL STR$ROUND (3%, 0%, ASIGN%, AEXP%, ADIGITS$, &
                     CSIGN%, CEXP%, CDIGITS$)
          PRINT "ROUNDED: C = "; CSIGN%; CEXP%; CDIGITS$
          !+
          ! Now, call STR$ROUND to truncate the value of A.
          !          CALL STR$ROUND (3%, 1%, ASIGN%, AEXP%, ADIGITS$, &
                     CSIGN%, CEXP%, CDIGITS$)
          PRINT "TRUNCATED: C = "; CSIGN%; CEXP%; CDIGITS$
        999 END

```

This BASIC example uses STR$ROUND to round and truncate the value of A to
the number of decimal places specified by **places** . The following values apply:

```
            A = 999.9998 (ASIGN = 0, AEXP = --4, ADIGITS = ’9999998’)

```

The output generated by this program is as follows; note that the decimal value
of C equals 1000 when rounded and 999 when truncated.

```
          A = 0 -4 9999998

          ROUNDED: C = 0 1 100

          TRUNCATED: C = 0 0 999

```

STR–85


**STR$ Routines**
**STR$TRANSLATE**

#### **STR$TRANSLATE** **Translate Matched Characters**


The Translate Matched Characters routine successively compares each character
in a source string to all characters in a match string. If a source character has a
match, the destination character is taken from the translate string. Otherwise,
STR$TRANSLATE moves the source character to the destination string.


**Format**


STR$TRANSLATE destination-string,source-string,translation-string,match-string


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string. The **destination-string** argument is the address of a
descriptor pointing to the destination string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string. The **source-string** argument is the address of a descriptor
pointing to the source string.


**translation-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Translate string. The **translation-string** argument is the address of a descriptor
pointing to the translate string.


**match-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Match string. The **match-string** argument is the address of a descriptor pointing
to the match string.


STR–86


**Description**



**STR$ Routines**
**STR$TRANSLATE**


STR$TRANSLATE successively compares each character in a source string
to all characters in a match string. If a source character matches any of the
characters in the match string, STR$TRANSLATE moves a character from the
translate string to the destination string. Otherwise, STR$TRANSLATE moves
the character from the source string to the destination string.


The character taken from the translate string has the same relative position
as the matching character had in the match string. When a character appears
more than once in the match string, the position of the leftmost occurrence of
the multiply-defined character is used to select the translate string character. If
the translate string is shorter than the match string and the matched character
position is greater than the translate string length, the destination character is a

space.



**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_TRU String truncation warning. The destination
string could not contain all of the characters.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$TRANSLATE
could not allocate heap storage for a dynamic or
temporary string.


**Example**

```
        10 !+
            ! This example program uses STR$TRANSLATE to
            ! translate all characters of a source string
            ! from uppercase to lowercase characters.
            !
            EXTERNAL INTEGER FUNCTION STR$TRANSLATE(STRING,STRING,STRING,STRING)
            TO$=’abcdefghijklmnopqrstuvwxyz’
            FROM$=’ABCDEFGHIJKLMNOPQRSTUVWXYZ’
            X% = STR$TRANSLATE(OUT$,’TEST’,TO$,FROM$)
            PRINT ’Status = ’;x%
            PRINT ’Resulting string = ’;out$
        32767 END

```

This BASIC example translates uppercase letters to lowercase letters, thus
performing a function similar to but the opposite of STR$UPCASE.


STR–87


**STR$ Routines**
**STR$TRANSLATE**


The output generated by this example is as follows:

```
          $ RUN TRANSLATE
          Status = 1
          Resulting string = test

```

A more practical although more complicated use for STR$TRANSLATE is to
encrypt data by translating the characters to obscure combinations of numbers
and alphabetic characters.


STR–88


**STR$ Routines**
**STR$TRIM**

#### **STR$TRIM** **Trim Trailing Blanks and Tabs**


The Trim Trailing Blanks and Tabs routine copies a source string to a destination
string and deletes the trailing blank and tab characters.


**Format**


STR$TRIM destination-string,source-string [,resultant-length]


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$TRIM copies the trimmed string. The
**destination-string** argument is the address of a descriptor pointing to the
destination string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string which STR$TRIM trims and then copies into the destination string.
The **source-string** argument is the address of a descriptor pointing to the source
string.


**resultant-length**
OpenVMS usage: word_unsigned
type: word (unsigned)
access: write only
mechanism: by reference


Number of bytes that STR$TRIM writes into **destination-string**, not counting
padding in the case of a fixed-length string. The **resultant-length** argument
is the address of an unsigned word into which STR$TRIM writes the length of
the output string. If the input string is truncated to the size specified in the
**destination-string** description, **resultant-length** is set to this size. Therefore,
**resultant-length** can always be used by the calling program to access a valid
substring of **destination-string** .


STR–89


**STR$ Routines**
**STR$TRIM**


**Description**


STR$TRIM copies a source string to a destination string and deletes the trailing
blank and tab characters.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_TRU String truncation warning. The destination
string could not contain all the characters.


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$TRIM could
not allocate heap storage for a dynamic or
temporary string.


STR–90


**STR$ Routines**
**STR$UPCASE**

#### **STR$UPCASE** **Convert String to All Uppercase Characters**


The Convert String to All Uppercase Characters routine converts a source string

to uppercase.


**Format**


STR$UPCASE destination-string,source-string


**Returns**


OpenVMS usage: cond_value
type: longword (unsigned)
access: write only
mechanism: by value


**Arguments**


**destination-string**
OpenVMS usage: char_string
type: character string
access: write only
mechanism: by descriptor


Destination string into which STR$UPCASE writes the string it has converted
to uppercase. The **destination-string** argument is the address of a descriptor
pointing to the destination string.


**source-string**
OpenVMS usage: char_string
type: character string
access: read only
mechanism: by descriptor


Source string that STR$UPCASE converts to uppercase. The **source-string**
argument is the address of a descriptor pointing to the source string.


**Description**


STR$UPCASE converts successive characters in a source string to uppercase and
writes the converted character into the destination string. The routine converts
all characters in the DEC Multinational Character Set.


**Condition Values Returned**


SS$_NORMAL Normal successful completion.

STR$_TRU String truncation warning. The destination
string could not contain all the characters.


STR–91


**STR$ Routines**
**STR$UPCASE**


**Condition Values Signaled**


STR$_FATINTERR Fatal internal error. An internal consistency
check has failed. This usually indicates an
internal error in the Run-Time Library and
should be reported to your Compaq support
representative.

STR$_ILLSTRCLA Illegal string class. The class code found in the
class field of a descriptor is not a string class
code allowed by the OpenVMS calling standard.

STR$_INSVIRMEM Insufficient virtual memory. STR$UPCASE
could not allocate heap storage for a dynamic or
temporary string.


**Example**

```
        30 !+
          ! This example uses STR$UPCASE
          ! to convert all characters in
          ! the source string (SRC$) to
          ! uppercase and write the result
          ! in the destination string (DST$).
          !
          SRC$ = ’abcd’
          PRINT "SRC$ =";SRC$
          CALL STR$UPCASE (DST$, SRC$)
          PRINT "DST$ =";DST$

          END

```

This BASIC program generates the following output:

```
          SCR$ =abcd
          DST$ =ABCD

```

STR–92


#### **A**

Addition of decimal strings, STR–5
AST level

danger of manipulating strings, 2–13

#### **D**


DEC Multinational character set

string comparison, STR–13, STR–20
string conversion, STR–91
Descriptors, 2–8
analysis of, 2–5, STR–7
Division of decimal strings, STR–33
Dynamic length strings, 2–3, 2–4, STR–71
allocating, STR–49 to STR–51
deallocating, STR–47

#### **E**


Entry points
CALL entry points, 2–9

#### **F**


Fixed length strings, 2–1
Function return values, 2–7
returned in output argument, 2–7
returned in R0/R1, 2–7

#### **H**


Heap storage, 2–3

#### **J**


JSB entry points, 2–9

#### **L**


LIB$ANALYZE_SDESC routine, 2–4
LIB$ANALYZE_SDESC_64 routine, 2–4
LIB$GET_INPUT routine, 2–9
LIB$GET_VM routine, 2–3
LIB$GET_VM_64 routine, 2–3


### **Index**

LIB$SCOPY_DXDX routine, 2–7

#### **M**


Manipulating strings
danger at AST level, 2–13
Memory allocation
for dynamic length strings, STR–49 to STR–51
freeing dynamic length strings, STR–47
Multiplication
of decimal strings, STR–64

#### **O**


OTS$SCOPY_DXDX routine, 2–7

#### **R**


Reciprocal of decimal strings, STR–75

#### **S**


STR$ADD routine, STR–3
STR$ANALYZE_SDESC routine, 2–4, STR–7
STR$ANALYZE_SDESC_64 routine, 2–4, STR–9
STR$APPEND routine, 2–10, STR–11
STR$CASE_BLIND_COMPARE routine, STR–13
STR$COMPARE routine, STR–15
STR$COMPARE_EQL routine, STR–17
STR$COMPARE_MULTI routine, STR–19
STR$CONCAT routine, 2–10, STR–22
STR$COPY_DX routine, 2–7, 2–9, STR–25
STR$COPY_R routine, STR–27
STR$COPY_R_64 routine, STR–29
STR$DIVIDE routine, STR–31
STR$DUPL_CHAR routine, STR–35
STR$ELEMENT routine, STR–37
STR$FIND_FIRST_IN_SET routine, STR–39
STR$FIND_FIRST_NOT_IN_SET routine,

STR–41

STR$FIND_FIRST_SUBSTRING routine, STR–44
STR$FREE1_DX routine, STR–47
STR$GET1_DX routine, STR–49
STR$GET1_DX_64 routine, STR–51
STR$LEFT routine, 2–10, STR–53


**Index–1**


STR$LEN_EXTR routine, STR–56
STR$MATCH_WILD routine, STR–59
STR$MUL routine, STR–62
STR$POSITION routine, STR–66
STR$POS_EXTR routine, 2–10, STR–69
STR$PREFIX routine, 2–10, STR–71
STR$RECIP routine, STR–73
STR$REPLACE routine, STR–77
STR$RIGHT routine, 2–10, STR–80
STR$ROUND routine, STR–83
STR$TRANSLATE routine, STR–86
STR$TRIM routine, STR–89
STR$UPCASE routine, STR–91
String arithmetic
addition of decimal strings, STR–5
division of decimal strings, STR–33
multiplication, STR–64
String descriptors, STR–7, STR–10
String manipulation routines, 2–1
descriptor classes and string semantics, 2–4
how to select, 2–9
list of severe errors, 2–11
reading input string arguments, 2–6
writing output string arguments, 2–7
Strings

See also Descriptors

See also String manipulation routines
appending, STR–11
comparing for equality, no padding, STR–17
comparing two, STR–15
comparing without regard to case, STR–13
concatenating, STR–22
converting to uppercase, STR–91
copying by descriptor, STR–25
copying by reference, STR–27 to STR–29
dividing two decimal strings, STR–33
duplicating characters in, STR–35
dynamic length, 2–3, 2–11, 2–12
allocating, STR–49 to STR–51
deallocating, STR–47
evaluation rules, 2–1
fixed length, 2–1
inserting source string at front of destination,
STR–71

maximum length of, 2–1
null strings, 2–11
output length argument, 2–8
position of character in, STR–39, STR–41
position of substring in, STR–66
reciprocal of decimal string, STR–75
removing trailing blanks and tabs, STR–90
rounding or truncating a decimal string,
STR–84

semantics of, 2–1, 2–4
translating matched characters, STR–87


**Index–2**



Substrings, 2–1
replacing, STR–78

#### **V**


Varying-length strings, 2–2, 2–4, STR–25,
STR–71


