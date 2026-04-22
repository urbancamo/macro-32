**LIB$**, or the **OpenVMS Run-Time Library Facility**, is a facility that provides a callable interface to components of OpenVMS operating systems that are difficult to use in a high-level language. LIB$ routines allow access to the following:

- System services
- The command language interpreter (CLI)
- Some VAX machine instructions or the equivalent Alpha instructions

and allow you to perform the following operations:

- Allocate resources that your process needs, such as virtual memory and event flags
- Convert data types for I/O
- Enable detection of hardware exceptions (VAX only)
- Establish condition handlers (VAX only)
- Generate and display timing statistics while your program is running
- Get and put strings in the process common storage area
- Obtain records from devices
- Obtain the system date and time in various formats
- Process cross-reference data
- Process Compaq DECnet-Plus for OpenVMS full names
- Search for specified files
- Set up and use binary trees
- Signal exceptions

# List of LIB$ Routines

| Routine Name | Description |
|---|---|
| LIB$ADAWI | Add adjacent word with interlock. |
| LIB$ADDX | Add two multiple-precision binary numbers. |
| LIB$ADD_TIMES | Add two quadwords times. |
| LIB$ANALYZE_SDESC | Analyze a string descriptor. |
| LIB$ANALYZE_SDESC_64 | Analyze a string descriptor. |
| LIB$ASN_WTH_MBX | Assign a channel to a [mailbox](/Mailbox "Mailbox"). |
| LIB$AST_IN_PROG | Check for active AST. |
| LIB$ATTACH | Attach a terminal to a process. |
| LIB$BBCCI | Test and clear a bit with interlock. |
| LIB$BBSSI | Test and set a bit with interlock. |
| LIB$BUILD_NODESPEC | Build a node-name specification. |
| LIB$CALLG | Call a procedure with a general argument list. |
| LIB$CALLG_64 | Call a procedure with a general argument list. |
| LIB$CHAR | Transform a byte to the first character of a string. |
| LIB$COMPARE_NODENAME | Compare two node names. |
| LIB$COMPRESS_NODENAME | Compress a node name to its short form equivalent. |
| LIB$CONVERT_DATE_STRING | Convert a date string to a quadword. |
| LIB$CRC | Calculate a cyclic redundancy check (CRC). |
| LIB$CRC_TABLE | Construct a cyclic redundancy check (CRC) table. |
| LIB$CREATE_DIR | Create a directory. |
| LIB$CREATE_USER_VM_ZONE | Create a user-defined storage zone. |
| LIB$CREATE_USER_VM_ZONE_64 | Create a user-defined storage zone. |
| LIB$CREATE_VM_ZONE | Create a new storage zone. |
| LIB$CREATE_VM_ZONE_64 | Create a new storage zone. |
| LIB$CRF_INS_KEY | Insert a key in the cross-reference table. |
| LIB$CRF_INS_REF | Insert a reference to a key in the cross-reference table. |
| LIB$CRF_OUTPUT | Output some cross-reference table information. |
| LIB$CURRENCY | Get the system currency symbol. |
| LIB$CVTF_FROM_INTERNAL_TIME | Convert internal time to external time (F-floating value). |
| LIB$CVTF_TO_INTERNAL_TIME | Convert external time to internal time (F-floating value). |
| LIB$CVT_DX_DX | Convert the specified data type. |
| LIB$CVT_FROM_INTERNAL_TIME | Convert internal time to external time. |
| LIB$CVT_TO_INTERNAL_TIME | Convert external time to internal time. |
| LIB$CVT_VECTIM | Convert 7-word vector to internal time. |
| LIB$CVT_ xTB | Convert numeric text to binary. |
| LIB$CVT_ xTB_64 | Convert numeric text to binary. |
| LIB$DATE_TIME | Return the date and time as a string. |
| LIB$DAY | Return the day number as a longword integer. |
| LIB$DAY_OF_WEEK | Return the numeric day of the week. |
| LIB$DECODE_FAULT | Decode instruction stream during a fault. |
| LIB$DEC_OVER | Enable or disable decimal overflow detection. |
| LIB$DELETE_FILE | Delete one or more [files](/File "File"). |
| LIB$DELETE_LOGICAL | Delete a [logical name](/Logical_Name "Logical Name"). |
| LIB$DELETE_SYMBOL | Delete a [CLI symbol](/Symbol "Symbol"). |
| LIB$DELETE_VM_ZONE | Delete a virtual memory zone. |
| LIB$DELETE_VM_ZONE_64 | Delete a virtual memory zone. |
| LIB$DIGIT_SEP | Get the digit separator symbol. |
| LIB$DISABLE_CTRL | Disable CLI interception of control characters. |
| LIB$DO_COMMAND | Execute the specified command. |
| LIB$EDIV | Perform an extended-precision divide. |
| LIB$EMODD | Perform extended multiply and integerize for D-floating values. |
| LIB$EMODF | Perform extended multiply and integerize for F-floating values. |
| LIB$EMODG | Perform extended multiply and integerize for G-floating values. |
| LIB$EMODH | Perform extended multiply and integerize for H-floating values. |
| LIB$EMUL | Perform an extended-precision multiply. |
| LIB$ENABLE_CTRL | Enable CLI interception of control characters. |
| LIB$ESTABLISH | Establish a condition handler. |
| LIB$EXPAND_NODENAME | Expand a node name to its full name equivalent. |
| LIB$EXTV | Extract a field and sign-extend. |
| LIB$EXTZV | Extract a zero-extended field. |
| LIB$FF x | Find the first clear or set bit. |
| LIB$FID_TO_NAME | Convert a device and [file](/File_ID "File ID") ID to a [file specification](/File_specification "File specification"). |
| LIB$FILE_SCAN | Perform a file scan. |
| LIB$FILE_SCAN_END | End a file scan. |
| LIB$FIND_FILE | Find a file. |
| LIB$FIND_FILE_END | End of find file. |
| LIB$FIND_IMAGE_SYMBOL | Merge activate an image symbol. |
| LIB$FIND_VM_ZONE | Find the next valid zone. |
| LIB$FIND_VM_ZONE_64 | Find the next valid zone. |
| LIB$FIT_NODENAME | Fit a node name into an output field. |
| LIB$FIXUP_FLT | Fix floating reserved operand. |
| LIB$FLT_UNDER | Detect a floating-point underflow. |
| LIB$FORMAT_DATE_TIME | Format a date and/or time. |
| LIB$FORMAT_SOGW_PROT | Format protection mask. |
| LIB$FREE_DATE_TIME_CONTEXT | Free the context used to format a date. |
| LIB$FREE_EF | Free an event flag. |
| LIB$FREE_LUN | Free a logical unit number. |
| LIB$FREE_TIMER | Free timer storage. |
| LIB$FREE_VM | Free virtual memory from the program region. |
| LIB$FREE_VM_64 | Free virtual memory from the program region. |
| LIB$FREE_VM_PAGE | Free a virtual memory page. |
| LIB$FREE_VM_PAGE_64 | Free a virtual memory page. |
| LIB$GETDVI | Get device/volume information. |
| LIB$GETJPI | Get job/process information. |
| LIB$GETQUI | Get [queue](/Queue "Queue") information. |
| LIB$GETSYI | Get systemwide information. |
| LIB$GET_ACCNAM | Get access name table for a security object identified by name. |
| LIB$GET_ACCNAM_BY_CONTEXT | Get access name table for a security object identified by $GET_SECURITY or $SET_SECURITY context. |
| LIB$GET_COMMAND | Get line from SYS$COMMAND. |
| LIB$GET_COMMON | Get string from common area. |
| LIB$GET_CURR_INVO_CONTEXT | Get current invocation context. |
| LIB$GET_DATE_FORMAT | Return the user's date input format. |
| LIB$GET_EF | Get an event flag. |
| LIB$GET_FOREIGN | Get [foreign command](/Foreign_Command "Foreign Command") line. |
| LIB$GET_FULLNAME_OFFSET | Get the offset to the starting position of the most significant part of a full name. |
| LIB$GET_HOSTNAME | Get host node name. |
| LIB$GET_INPUT | Get line from [SYS$INPUT](/SYS$INPUT "SYS$INPUT"). |
| LIB$GET_INVO_CONTEXT | Get invocation context. |
| LIB$GET_INVO_HANDLE | Get invocation handle. |
| LIB$GET_LUN | Get logical unit number. |
| LIB$GET_MAXIMUM_DATE_LENGTH | Get the maximum possible date/time string length. |
| LIB$GET_PREV_INVO_CONTEXT | Get previous invocation context. |
| LIB$GET_PREV_INVO_HANDLE | Get previous invocation handle. |
| LIB$GET_SYMBOL | Get the value of a CLI symbol. |
| LIB$GET_USERS_LANGUAGE | Return the user's language choice. |
| LIB$GET_VM | Allocate virtual memory. |
| LIB$GET_VM_64 | Allocate virtual memory. |
| LIB$GET_VM_PAGE | Get a virtual memory page. |
| LIB$GET_VM_PAGE_64 | Get a virtual memory page. |
| LIB$ICHAR | Convert the first character of a string to an integer. |
| LIB$INDEX | Index to relative position of substring. |
| LIB$INIT_DATE_TIME_CONTEXT | Initialize the context used in formatting date/time strings. |
| LIB$INIT_TIMER | Initialize times and counts. |
| LIB$INSERT_TREE | Insert entry in a balanced binary tree. |
| LIB$INSERT_TREE_64 | Insert entry in a balanced binary tree. 1 |
| LIB$INSQHI | Insert entry at the head of a queue. |
| $INSQHIQ | Insert entry at the head of a queue. |
| LIB$INSQTI | Insert entry at the tail of a queue. |
| LIB$INSQTIQ | Insert entry at the tail of a queue. |
| LIB$INSV | Insert a variable bit field. |
| LIB$INT_OVER | Detect integer overflow. |
| LIB$LEN | Return the length of a string as a longword. |
| LIB$LOCC | Locate a character. |
| LIB$LOOKUP_KEY | Look up keyword in table. |
| LIB$LOOKUP_TREE | Look up an entry in a balanced binary tree. |
| LIB$LOOKUP_TREE_64 | Look up an entry in a balanced binary tree. |
| LIB$LP_LINES | Specify the number of lines on each printer page. |
| LIB$MATCHC | Match characters, return relative position. |
| LIB$MATCH_COND | Match condition values. |
| LIB$MOVC3 | Move characters. |
| LIB$MOVC5 | Move characters with fill. |
| LIB$MOVTC | Move translated characters. |
| LIB$MOVTUC | Move translated until character. |
| LIB$MULTF_DELTA_TIME | Multiply delta time by F-floating scalar. |
| LIB$MULT_DELTA_TIME | Multiply delta time by scalar. |
| LIB$PARSE_ACCESS_CODE | Parse access-encoded name string. |
| LIB$PARSE_SOGW_PROT | Parse [protection string](/UIC_Protection "UIC Protection"). |
| LIB$PAUSE | Pause program execution. |
| LIB$POLYD | Evaluate polynomials for D-floating values. |
| LIB$POLYF | Evaluate polynomials for F-floating values. |
| LIB$POLYG | Evaluate polynomials for G-floating values. |
| LIB$POLYH | Evaluate polynomials for H-floating values. |
| LIB$PUT_COMMON | Put string into common area. |
| LIB$PUT_INVO_REGISTERS | Put invocation registers. |
| LIB$PUT_OUTPUT | Put line to [SYS$OUTPUT](/SYS$OUTPUT "SYS$OUTPUT"). |
| LIB$RADIX_POINT | Radix point symbol. |
| LIB$REMQHI | Remove entry from head of queue. |
| LIB$REMQHIQ | Remove entry from head of queue. |
| LIB$REMQTI | Remove entry from tail of queue. |
| LIB$REMQTIQ | Remove entry from tail of queue. |
| LIB$RENAME_FILE | Rename one or more files. |
| LIB$RESERVE_EF | Reserve an event flag. |
| LIB$RESET_VM_ZONE | Reset virtual memory zone. |
| LIB$RESET_VM_ZONE_64 | Reset virtual memory zone. |
| LIB$REVERT | Revert to the handler of the procedure activator. 2 3 |
| LIB$RUN_PROGRAM | Run new program. |
| LIB$SCANC | Scan for characters and return relative position. |
| LIB$SCOPY_DXDX | Copy source string by descriptor to destination. |
| LIB$SCOPY_R_DX | Copy source string by reference to destination. |
| LIB$SCOPY_R_DX_64 | Copy source string by reference to destination. 1 |
| LIB$SET_LOGICAL | Set logical name. |
| LIB$SET_SYMBOL | Set the value of a CLI symbol. |
| LIB$SFREE1_DD | Free one or more dynamic strings. |
| LIB$SFREEN_DD | Free n dynamic strings. |
| LIB$SGET1_DD | Get one dynamic string. |
| LIB$SGET1_DD_64 | Get one dynamic string. |
| LIB$SHOW_TIMER | Show accumulated times and counts. |
| LIB$SHOW_VM | Show virtual memory statistics. |
| LIB$SHOW_VM_64 | Show virtual memory statistics. |
| LIB$SHOW_VM_ZONE | Display information about a virtual memory zone. |
| LIB$SHOW_VM_ZONE_64 | Display information about a virtual memory zone. |
| LIB$SIGNAL | Signal exception condition. |
| LIB$SIG_TO_RET | Convert a signaled message to a return status. |
| LIB$SIG_TO_STOP | Convert a signaled condition to a signaled stop. |
| LIB$SIM_TRAP | Simulate floating trap. |
| LIB$SKPC | Skip equal characters. |
| LIB$SPANC | Skip selected characters. |
| LIB$SPAWN | Spawn a [subprocess](/Subprocess "Subprocess"). |
| LIB$STAT_TIMER | Return accumulated time and count statistics. |
| LIB$STAT_VM | Return virtual memory statistics. |
| LIB$STAT_VM_64 | Return virtual memory statistics. 1 |
| LIB$STOP | Stop execution and signal the condition. |
| LIB$SUBX | Perform multiple-precision binary subtraction. |
| LIB$SUB_TIMES | Subtract two quadword times. |
| LIB$SYS_ASCTIM | Invoke $ASCTIM to convert binary time to ASCII. |
| LIB$SYS_FAO | Invoke $FAO system service to format output. |
| LIB$SYS_FAOL | Invoke $FAOL system service to format output. |
| LIB$SYS_FAOL_64 | Invoke $FAOL system service to format output. |
| LIB$SYS_GETMSG | Invoke $GETMSG system service to get message text. |
| LIB$TABLE_PARSE | Implement a table-driven, finite-state parser. |
| LIB$TPARSE | Implement a table-driven, finite-state parser. |
| LIB$TRAVERSE_TREE | Traverse a balanced binary tree. |
| LIB$TRAVERSE_TREE_64 | Traverse a balanced binary tree. |
| LIB$TRA_ASC_EBC | Translate ASCII to EBCDIC. |
| LIB$TRA_EBC_ASC | Translate EBCDIC to ASCII. |
| LIB$TRIM_FILESPEC | Fit a long file specification into a fixed field. |
| LIB$TRIM_FULLNAME | Trim a full name to fit into a desired output field. |
| LIB$VERIFY_VM_ZONE | Verify a virtual memory zone. |
| LIB$VERIFY_VM_ZONE_64 | Verify a virtual memory zone. |
| LIB$WAIT | Wait a specified period of time. |

# See also

- OpenVMS RTL Routine Manual

