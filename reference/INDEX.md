# Reference Index — Callable Routines & Services

All callable routines across the OpenVMS V7.3 reference corpus, grouped by facility, alphabetical within each group. Each entry links directly to its reference section.

Generated from the `#### **NAME** **Description**` headings in the per-manual markdown files — see `build-index.py` in the repo history if you need to regenerate.

## Facility overview

| Facility | Count | Jump |
|---|---:|---|
| SYS$ — System Services | 300 | [↓](#sys-system-services) |
| RMS — Record Management Services | 55 | [↓](#rms-record-management-services) |
| LIB$ — OpenVMS Run-Time Library | 199 | [↓](#lib-openvms-run-time-library) |
| CVT$ — Data Conversion | 2 | [↓](#cvt-data-conversion) |
| STR$ — String Manipulation | 35 | [↓](#str-string-manipulation) |
| MTH$ — Mathematics | 74 | [↓](#mth-mathematics) |
| OTS$ — General Purpose / Language Support | 41 | [↓](#ots-general-purpose-language-support) |
| SMG$ — Screen Management | 121 | [↓](#smg-screen-management) |
| ACLEDIT$ Utility Routines | 1 | [↓](#acledit-utility-routines) |
| BACKUP$ Utility Routines | 1 | [↓](#backup-utility-routines) |
| BLAS1$ Utility Routines | 10 | [↓](#blas1-utility-routines) |
| CLI$ — Command Line Interface Utility | 4 | [↓](#cli-command-line-interface-utility) |
| CONV$ — Convert Utility | 4 | [↓](#conv-convert-utility) |
| DCX$ — Data Compression Utility | 10 | [↓](#dcx-data-compression-utility) |
| EDT$ — EDT Editor Callable Interface | 1 | [↓](#edt-edt-editor-callable-interface) |
| FDL$ — File Definition Language | 4 | [↓](#fdl-file-definition-language) |
| LBR$ — Librarian Utility | 25 | [↓](#lbr-librarian-utility) |
| LGI$ Utility Routines | 21 | [↓](#lgi-utility-routines) |
| MAIL$ — Mail Utility | 28 | [↓](#mail-mail-utility) |
| NCS$ — National Character Set Utility | 10 | [↓](#ncs-national-character-set-utility) |
| Other Utility Routines | 8 | [↓](#other-utility-routines) |
| PSM$ — Print Symbiont Modification | 4 | [↓](#psm-print-symbiont-modification) |
| SMB$ — Symbiont Manager | 5 | [↓](#smb-symbiont-manager) |
| SOR$ — Sort/Merge Utility | 10 | [↓](#sor-sortmerge-utility) |
| TPU$ — TPU Editor Callable Interface | 18 | [↓](#tpu-tpu-editor-callable-interface) |
| UTIL$ Utility Routines | 4 | [↓](#util-utility-routines) |

**Total: 995 routines.**

## SYS$ — System Services

| Routine | Description |
|---|---|
| [$ABORT_TRANS](VAX-VMS-731/system-services-a-g-2003.md#abort_trans-abort-transaction) | Abort Transaction |
| [$ABORT_TRANSW](VAX-VMS-731/system-services-a-g-2003.md#abort_transw-abort-transaction-and-wait) | Abort Transaction and Wait |
| [$ACK_EVENT](VAX-VMS-731/system-services-a-g-2003.md#ack_event-acknowledge-event) | Acknowledge Event |
| [$ACM](VAX-VMS-731/system-services-a-g-2003.md#acm-alpha-only-authentication-and-credential-management) | Authentication and Credential Management |
| [$ACMW](VAX-VMS-731/system-services-a-g-2003.md#acmw-alpha-only-authentication-and-credential-management) | Authentication and Credential Management |
| [$ACQUIRE_GALAXY_LOCK](VAX-VMS-731/system-services-a-g-2003.md#acquire_galaxy_lock-alpha-only-acquire-galaxy-lock) | Acquire GALAXY Lock |
| [$ADD_BRANCH](VAX-VMS-731/system-services-a-g-2003.md#add_branch-add-branch) | Add Branch |
| [$ADD_BRANCHW](VAX-VMS-731/system-services-a-g-2003.md#add_branchw-add-branch-and-wait) | Add Branch and Wait |
| [$ADD_HOLDER](VAX-VMS-731/system-services-a-g-2003.md#add_holder-add-holder-record-to-rights-database) | Add Holder Record to Rights Database |
| [$ADD_IDENT](VAX-VMS-731/system-services-a-g-2003.md#add_ident-add-identifier-to-rights-database) | Add Identifier to Rights Database |
| [$ADD_PROXY](VAX-VMS-731/system-services-a-g-2003.md#add_proxy-add-or-modify-proxy) | Add or Modify Proxy |
| [$ADJSTK](VAX-VMS-731/system-services-a-g-2003.md#adjstk-adjust-outer-mode-stack-pointer) | Adjust Outer Mode Stack Pointer |
| [$ADJWSL](VAX-VMS-731/system-services-a-g-2003.md#adjwsl-adjust-working-set-limit) | Adjust Working Set Limit |
| [$ALLOC](VAX-VMS-731/system-services-a-g-2003.md#alloc-allocate-device) | Allocate Device |
| [$ASCEFC](VAX-VMS-731/system-services-a-g-2003.md#ascefc-associate-common-event-flag-cluster) | Associate Common Event Flag Cluster |
| [$ASCTIM](VAX-VMS-731/system-services-a-g-2003.md#asctim-convert-binary-time-to-ascii-string) | Convert Binary Time to ASCII String |
| [$ASCTOID](VAX-VMS-731/system-services-a-g-2003.md#asctoid-translate-identifier-name-to-identifier) | Translate Identifier Name to Identifier |
| [$ASCUTC](VAX-VMS-731/system-services-a-g-2003.md#ascutc-convert-utc-to-ascii) | Convert UTC to ASCII |
| [$ASSIGN](VAX-VMS-731/system-services-a-g-2003.md#assign-assign-io-channel) | Assign I/O Channel |
| [$AUDIT_EVENT](VAX-VMS-731/system-services-a-g-2003.md#audit_event-audit-event) | Audit Event |
| [$AUDIT_EVENTW](VAX-VMS-731/system-services-a-g-2003.md#audit_eventw-audit-event-and-wait) | Audit Event and Wait |
| [$AVOID_PREEMPT](VAX-VMS-731/system-services-a-g-2003.md#avoid_preempt-avoid-process-preemption) | Avoid Process Preemption |
| [$BINTIM](VAX-VMS-731/system-services-a-g-2003.md#bintim-convert-ascii-string-to-binary-time) | Convert ASCII String to Binary Time |
| [$BINUTC](VAX-VMS-731/system-services-a-g-2003.md#binutc-convert-ascii-string-to-utc-binary-time) | Convert ASCII String to UTC Binary Time |
| [$BRKTHRU](VAX-VMS-731/system-services-a-g-2003.md#brkthru-breakthrough) | Breakthrough |
| [$BRKTHRUW](VAX-VMS-731/system-services-a-g-2003.md#brkthruw-breakthrough-and-wait) | Breakthrough and Wait |
| [$CANCEL](VAX-VMS-731/system-services-a-g-2003.md#cancel-cancel-io-on-channel) | Cancel I/O on Channel |
| [$CANEXH](VAX-VMS-731/system-services-a-g-2003.md#canexh-cancel-exit-handler) | Cancel Exit Handler |
| [$CANTIM](VAX-VMS-731/system-services-a-g-2003.md#cantim-cancel-timer) | Cancel Timer |
| [$CANWAK](VAX-VMS-731/system-services-a-g-2003.md#canwak-cancel-wakeup) | Cancel Wakeup |
| [$CHECK_ACCESS](VAX-VMS-731/system-services-a-g-2003.md#check_access-check-access) | Check Access |
| [$CHECK_FEN](VAX-VMS-731/system-services-a-g-2003.md#check_fen-alpha-only-check-floating-point) | Check Floating Point |
| [$CHECK_PRIVILEGE](VAX-VMS-731/system-services-a-g-2003.md#check_privilege-check-privilege) | Check Privilege |
| [$CHECK_PRIVILEGEW](VAX-VMS-731/system-services-a-g-2003.md#check_privilegew-check-privilege-and-wait) | Check Privilege and Wait |
| [$CHKPRO](VAX-VMS-731/system-services-a-g-2003.md#chkpro-check-access-protection) | Check Access Protection |
| [$CLEAR_SYSTEM_EVENT](VAX-VMS-731/system-services-a-g-2003.md#clear_system_event-alpha-only-clear-system-event) | Clear System Event |
| [$CLRAST](VAX-VMS-731/system-services-a-g-2003.md#clrast-clear-ast) | Clear AST |
| [$CLRCLUEVT](VAX-VMS-731/system-services-a-g-2003.md#clrcluevt-clear-cluster-event) | Clear Cluster Event |
| [$CLREF](VAX-VMS-731/system-services-a-g-2003.md#clref-clear-event-flag) | Clear Event Flag |
| [$CMEXEC](VAX-VMS-731/system-services-a-g-2003.md#cmexec-change-to-executive-mode) | Change to Executive Mode |
| [$CMEXEC_64](VAX-VMS-731/system-services-a-g-2003.md#cmexec_64-alpha-only-change-to-executive-mode-with-quadword-argument-list) | Change to Executive Mode with Quadword Argument List |
| [$CMKRNL](VAX-VMS-731/system-services-a-g-2003.md#cmkrnl-change-to-kernel-mode) | Change to Kernel Mode |
| [$CMKRNL_64](VAX-VMS-731/system-services-a-g-2003.md#cmkrnl_64-alpha-only-change-to-kernel-mode-with-quadword-argument-list) | Change to Kernel Mode with Quadword Argument List |
| [$CPU_CAPABILITIES](VAX-VMS-731/system-services-a-g-2003.md#cpu_capabilities-alpha-only-modify-cpu-user-capabilities) | Modify CPU User Capabilities |
| [$CPU_TRANSITION](VAX-VMS-731/system-services-a-g-2003.md#cpu_transition-alpha-only-cpu-transition) | CPU Transition |
| [$CPU_TRANSITIONW](VAX-VMS-731/system-services-a-g-2003.md#cpu_transitionw-alpha-only-cpu-transition-and-wait) | CPU Transition and Wait |
| [$CREATE_BUFOBJ_64](VAX-VMS-731/system-services-a-g-2003.md#create_bufobj_64-alpha-only-create-buffer-object) | Create Buffer Object |
| [$CREATE_GALAXY_LOCK](VAX-VMS-731/system-services-a-g-2003.md#create_galaxy_lock-alpha-only-create-openvms-galaxy-lock) | Create OpenVMS Galaxy Lock |
| [$CREATE_GALAXY_LOCK_TABLE](VAX-VMS-731/system-services-a-g-2003.md#create_galaxy_lock_table-alpha-only-create-openvms-galaxy-lock-table) | Create OpenVMS Galaxy Lock Table |
| [$CREATE_GDZRO](VAX-VMS-731/system-services-a-g-2003.md#create_gdzro-alpha-only-create-permanent-global-demand-zero-section) | Create Permanent Global Demand-Zero Section |
| [$CREATE_GFILE](VAX-VMS-731/system-services-a-g-2003.md#create_gfile-alpha-only-create-permanent-global-disk-file-section) | Create Permanent Global Disk File Section |
| [$CREATE_GPFILE](VAX-VMS-731/system-services-a-g-2003.md#create_gpfile-alpha-only-create-permanent-global-page-file-section) | Create Permanent Global Page File Section |
| [$CREATE_GPFN](VAX-VMS-731/system-services-a-g-2003.md#create_gpfn-alpha-only-create-permanent-global-page-frame-section) | Create Permanent Global Page Frame Section |
| [$CREATE_RDB](VAX-VMS-731/system-services-a-g-2003.md#create_rdb-create-rights-database) | Create Rights Database |
| [$CREATE_REGION_64](VAX-VMS-731/system-services-a-g-2003.md#create_region_64-alpha-only-create-virtual-region) | Create Virtual Region |
| [$CREATE_UID](VAX-VMS-731/system-services-a-g-2003.md#create_uid-create-uid) | Create UID |
| [$CREATE_USER_PROFILE](VAX-VMS-731/system-services-a-g-2003.md#create_user_profile-create-user-profile) | Create User Profile |
| [$CRELNM](VAX-VMS-731/system-services-a-g-2003.md#crelnm-create-logical-name) | Create Logical Name |
| [$CRELNT](VAX-VMS-731/system-services-a-g-2003.md#crelnt-create-logical-name-table) | Create Logical Name Table |
| [$CREMBX](VAX-VMS-731/system-services-a-g-2003.md#crembx-create-mailbox-and-assign-channel) | Create Mailbox and Assign Channel |
| [$CREPRC](VAX-VMS-731/system-services-a-g-2003.md#creprc-create-process) | Create Process |
| [$CRETVA](VAX-VMS-731/system-services-a-g-2003.md#cretva-create-virtual-address-space) | Create Virtual Address Space |
| [$CRETVA_64](VAX-VMS-731/system-services-a-g-2003.md#cretva_64-alpha-only-create-virtual-address-space) | Create Virtual Address Space |
| [$CRMPSC](VAX-VMS-731/system-services-a-g-2003.md#crmpsc-create-and-map-section) | Create and Map Section |
| [$CRMPSC_FILE_64](VAX-VMS-731/system-services-a-g-2003.md#crmpsc_file_64-alpha-only-create-and-map-private-disk-file-section) | Create and Map Private Disk File Section |
| [$CRMPSC_GDZRO_64](VAX-VMS-731/system-services-a-g-2003.md#crmpsc_gdzro_64-alpha-only-create-and-map-to-global-demand-zero-section) | Create and Map to Global Demand-Zero Section |
| [$CRMPSC_GFILE_64](VAX-VMS-731/system-services-a-g-2003.md#crmpsc_gfile_64-alpha-only-create-and-map-global-disk-file-section) | Create and Map Global Disk File Section |
| [$CRMPSC_GPFILE_64](VAX-VMS-731/system-services-a-g-2003.md#crmpsc_gpfile_64-alpha-only-create-and-map-global-page-file-section) | Create and Map Global Page File Section |
| [$CRMPSC_GPFN_64](VAX-VMS-731/system-services-a-g-2003.md#crmpsc_gpfn_64-alpha-only-create-and-map-global-page-frame-section) | Create and Map Global Page Frame Section |
| [$CRMPSC_PFN_64](VAX-VMS-731/system-services-a-g-2003.md#crmpsc_pfn_64-alpha-only-create-and-map-private-page-frame-section) | Create and Map Private Page Frame Section |
| [$CVT_FILENAME](VAX-VMS-731/system-services-a-g-2003.md#cvt_filename-alpha-only-converts-string) | Converts String |
| [$DACEFC](VAX-VMS-731/system-services-a-g-2003.md#dacefc-disassociate-common-event-flag-cluster) | Disassociate Common Event Flag Cluster |
| [$DALLOC](VAX-VMS-731/system-services-a-g-2003.md#dalloc-deallocate-device) | Deallocate Device |
| [$DASSGN](VAX-VMS-731/system-services-a-g-2003.md#dassgn-deassign-io-channel) | Deassign I/O Channel |
| [$DCLAST](VAX-VMS-731/system-services-a-g-2003.md#dclast-declare-ast) | Declare AST |
| [$DCLCMH](VAX-VMS-731/system-services-a-g-2003.md#dclcmh-declare-change-mode-or-compatibility-mode-handler) | Declare Change Mode or Compatibility Mode Handler |
| [$DCLEXH](VAX-VMS-731/system-services-a-g-2003.md#dclexh-declare-exit-handler) | Declare Exit Handler |
| [$DECLARE_RM](VAX-VMS-731/system-services-a-g-2003.md#declare_rm-declare-resource-manager) | Declare Resource Manager |
| [$DECLARE_RMW](VAX-VMS-731/system-services-a-g-2003.md#declare_rmw-declare-resource-manager-and-wait) | Declare Resource Manager and Wait |
| [$DELETE_BUFOBJ](VAX-VMS-731/system-services-a-g-2003.md#delete_bufobj-alpha-only-delete-buffer-object) | Delete Buffer Object |
| [$DELETE_GALAXY_LOCK](VAX-VMS-731/system-services-a-g-2003.md#delete_galaxy_lock-alpha-only-delete-an-openvms-galaxy-lock) | Delete an OpenVMS Galaxy Lock |
| [$DELETE_GALAXY_LOCK_TABLE](VAX-VMS-731/system-services-a-g-2003.md#delete_galaxy_lock_table-alpha-only-delete-openvms-galaxy-lock-table) | Delete OpenVMS Galaxy Lock Table |
| [$DELETE_INTRUSION](VAX-VMS-731/system-services-a-g-2003.md#delete_intrusion-delete-intrusion-records) | Delete Intrusion Records |
| [$DELETE_PROXY](VAX-VMS-731/system-services-a-g-2003.md#delete_proxy-delete-or-modify-proxy) | Delete or Modify Proxy |
| [$DELETE_REGION_64](VAX-VMS-731/system-services-a-g-2003.md#delete_region_64-alpha-only-delete-a-virtual-region) | Delete a Virtual Region |
| [$DELLNM](VAX-VMS-731/system-services-a-g-2003.md#dellnm-delete-logical-name) | Delete Logical Name |
| [$DELMBX](VAX-VMS-731/system-services-a-g-2003.md#delmbx-delete-mailbox) | Delete Mailbox |
| [$DELPRC](VAX-VMS-731/system-services-a-g-2003.md#delprc-delete-process) | Delete Process |
| [$DELTVA](VAX-VMS-731/system-services-a-g-2003.md#deltva-delete-virtual-address-space) | Delete Virtual Address Space |
| [$DELTVA_64](VAX-VMS-731/system-services-a-g-2003.md#deltva_64-alpha-only-delete-virtual-address-space) | Delete Virtual Address Space |
| [$DEQ](VAX-VMS-731/system-services-a-g-2003.md#deq-dequeue-lock-request) | Dequeue Lock Request |
| [$DEVICE_PATH_SCAN](VAX-VMS-731/system-services-a-g-2003.md#device_path_scan-alpha-only-scan-for-device-paths) | Scan for Device Paths |
| [$DEVICE_SCAN](VAX-VMS-731/system-services-a-g-2003.md#device_scan-scan-for-devices) | Scan for Devices |
| [$DGBLSC](VAX-VMS-731/system-services-a-g-2003.md#dgblsc-delete-global-section) | Delete Global Section |
| [$DISMOU](VAX-VMS-731/system-services-a-g-2003.md#dismou-dismount-volume) | Dismount Volume |
| [$DISPLAY_PROXY](VAX-VMS-731/system-services-a-g-2003.md#display_proxy-display-proxy-information) | Display Proxy Information |
| [$DLCEFC](VAX-VMS-731/system-services-a-g-2003.md#dlcefc-delete-common-event-flag-cluster) | Delete Common Event Flag Cluster |
| [$DNS](VAX-VMS-731/system-services-a-g-2003.md#dns-vax-only-distributed-name-service-clerk) | Distributed Name Service Clerk |
| [$DNSW](VAX-VMS-731/system-services-a-g-2003.md#dnsw-vax-only-distributed-name-service-clerk-and-wait) | Distributed Name Service Clerk and Wait |
| [$END_BRANCH](VAX-VMS-731/system-services-a-g-2003.md#end_branch-end-branch) | End Branch |
| [$END_BRANCHW](VAX-VMS-731/system-services-a-g-2003.md#end_branchw-end-branch-and-wait) | End Branch and Wait |
| [$END_TRANS](VAX-VMS-731/system-services-a-g-2003.md#end_trans-end-transaction) | End Transaction |
| [$END_TRANSW](VAX-VMS-731/system-services-a-g-2003.md#end_transw-end-transaction-and-wait) | End Transaction and Wait |
| [$ENQ](VAX-VMS-731/system-services-a-g-2003.md#enq-enqueue-lock-request) | Enqueue Lock Request |
| [$ENQW](VAX-VMS-731/system-services-a-g-2003.md#enqw-enqueue-lock-request-and-wait) | Enqueue Lock Request and Wait |
| [$ERAPAT](VAX-VMS-731/system-services-a-g-2003.md#erapat-get-security-erase-pattern) | Get Security Erase Pattern |
| [$EXIT](VAX-VMS-731/system-services-a-g-2003.md#exit-exit) | Exit |
| [$EXPREG](VAX-VMS-731/system-services-a-g-2003.md#expreg-expand-programcontrol-region) | Expand Program/Control Region |
| [$EXPREG_64](VAX-VMS-731/system-services-a-g-2003.md#expreg_64-alpha-only-expand-virtual-address-space) | Expand Virtual Address Space |
| [$FAOL_64](VAX-VMS-731/system-services-a-g-2003.md#faol_64-alpha-only-formatted-asci-output-with-list-parameter-for-64-bit-virtual-addresses) | Formatted ASCI Output with List Parameter for 64-Bit Virtual** **Addresses |
| [$FILESCAN](VAX-VMS-731/system-services-a-g-2003.md#filescan-scan-string-for-file-specification) | Scan String for File Specification |
| [$FIND_HELD](VAX-VMS-731/system-services-a-g-2003.md#find_held-find-identifiers-held-by-user) | Find Identifiers Held by User |
| [$FIND_HOLDER](VAX-VMS-731/system-services-a-g-2003.md#find_holder-find-holder-of-identifier) | Find Holder of Identifier |
| [$FINISH_RDB](VAX-VMS-731/system-services-a-g-2003.md#finish_rdb-terminate-rights-database-context) | Terminate Rights Database Context |
| [$FORCEX](VAX-VMS-731/system-services-a-g-2003.md#forcex-force-exit) | Force Exit |
| [$FORGET_RM](VAX-VMS-731/system-services-a-g-2003.md#forget_rm-forget-resource-manager) | Forget Resource Manager |
| [$FORGET_RMW](VAX-VMS-731/system-services-a-g-2003.md#forget_rmw-forget-resource-manager-and-wait) | Forget Resource Manager and Wait |
| [$FORMAT_ACL](VAX-VMS-731/system-services-a-g-2003.md#format_acl-format-access-control-list-entry) | Format Access Control List Entry |
| [$FORMAT_AUDIT](VAX-VMS-731/system-services-a-g-2003.md#format_audit-format-security-audit-event-message) | Format Security Audit Event Message |
| [$FREE_USER_CAPABILITY](VAX-VMS-731/system-services-a-g-2003.md#free_user_capability-alpha-only-release-a-reserved-user-capability) | Release a Reserved User Capability |
| [$GETDTI](VAX-VMS-731/system-services-a-g-2003.md#getdti-get-distributed-transaction-information) | Get Distributed Transaction Information |
| [$GETDTIW](VAX-VMS-731/system-services-a-g-2003.md#getdtiw-get-distributed-transaction-information-and-wait) | Get Distributed Transaction Information and Wait |
| [$GETDVI](VAX-VMS-731/system-services-a-g-2003.md#getdvi-get-devicevolume-information) | Get Device/Volume Information |
| [$GETDVIW](VAX-VMS-731/system-services-a-g-2003.md#getdviw-get-devicevolume-information-and-wait) | Get Device/Volume Information and Wait |
| [$GETENV](VAX-VMS-731/system-services-a-g-2003.md#getenv-alpha-only-get-environment) | Get Environment |
| [$GETJPI](VAX-VMS-731/system-services-a-g-2003.md#getjpi-get-jobprocess-information) | Get Job/Process Information |
| [$GETJPIW](VAX-VMS-731/system-services-a-g-2003.md#getjpiw-get-jobprocess-information-and-wait) | Get Job/Process Information and Wait |
| [$GETLKI](VAX-VMS-731/system-services-a-g-2003.md#getlki-get-lock-information) | Get Lock Information |
| [$GETLKIW](VAX-VMS-731/system-services-a-g-2003.md#getlkiw-get-lock-information-and-wait) | Get Lock Information and Wait |
| [$GETMSG](VAX-VMS-731/system-services-a-g-2003.md#getmsg-get-message) | Get Message |
| [$GETQUI](VAX-VMS-731/system-services-a-g-2003.md#getqui-get-queue-information) | Get Queue Information |
| [$GETQUIW](VAX-VMS-731/system-services-a-g-2003.md#getquiw-get-queue-information-and-wait) | Get Queue Information and Wait |
| [$GETRMI](VAX-VMS-731/system-services-a-g-2003.md#getrmi-get-resource-monitor-information) | Get Resource Monitor Information |
| [$GETSYI](VAX-VMS-731/system-services-a-g-2003.md#getsyi-get-systemwide-information) | Get Systemwide Information |
| [$GETSYIW](VAX-VMS-731/system-services-a-g-2003.md#getsyiw-get-systemwide-information-and-wait) | Get Systemwide Information and Wait |
| [$GETTIM](VAX-VMS-731/system-services-a-g-2003.md#gettim-get-time) | Get Time |
| [$GETUAI](VAX-VMS-731/system-services-a-g-2003.md#getuai-get-user-authorization-information) | Get User Authorization Information |
| [$GETUTC](VAX-VMS-731/system-services-g-z-2003.md#getutc-get-utc-time) | Get UTC Time |
| [$GET_ALIGN_FAULT_DATA](VAX-VMS-731/system-services-g-z-2003.md#get_align_fault_data-alpha-only-get-alignment-fault-data) | Get Alignment Fault Data |
| [$GET_ARITH_EXCEPTION](VAX-VMS-731/system-services-g-z-2003.md#get_arith_exception-alpha-only-get-arithmetic-exception-information) | Get Arithmetic Exception Information |
| [$GET_DEFAULT_TRANS](VAX-VMS-731/system-services-g-z-2003.md#get_default_trans-get-default-transaction) | Get Default Transaction |
| [$GET_GALAXY_LOCK_INFO](VAX-VMS-731/system-services-g-z-2003.md#get_galaxy_lock_info-alpha-only-get-openvms-galaxy-lock-information) | Get OpenVMS Galaxy Lock Information |
| [$GET_GALAXY_LOCK_SIZE](VAX-VMS-731/system-services-g-z-2003.md#get_galaxy_lock_size-alpha-only-get-openvms-galaxy-lock-size) | Get OpenVMS Galaxy Lock Size |
| [$GET_REGION_INFO](VAX-VMS-731/system-services-g-z-2003.md#get_region_info-alpha-only-get-information-about-a-specified-virtual-region) | Get Information About a Specified Virtual Region |
| [$GET_SECURITY](VAX-VMS-731/system-services-g-z-2003.md#get_security-get-security-characteristics) | Get Security Characteristics |
| [$GET_SYS_ALIGN_FAULT_DATA](VAX-VMS-731/system-services-g-z-2003.md#get_sys_align_fault_data-alpha-only-get-system-alignment-fault-data) | Get System Alignment Fault Data |
| [$GET_USER_CAPABILITY](VAX-VMS-731/system-services-g-z-2003.md#get_user_capability-alpha-only-reserve-a-user-capability) | Reserve a User Capability |
| [$GOTO_UNWIND](VAX-VMS-731/system-services-g-z-2003.md#goto_unwind-alpha-only-unwind-call-stack) | Unwind Call Stack |
| [$GOTO_UNWIND_64](VAX-VMS-731/system-services-g-z-2003.md#goto_unwind_64-alpha-and-i64-only-unwind-call-stack) | Unwind Call Stack |
| [$GRANTID](VAX-VMS-731/system-services-g-z-2003.md#grantid-grant-identifier-to-process) | Grant Identifier to Process |
| [$HASH_PASSWORD](VAX-VMS-731/system-services-g-z-2003.md#hash_password-hash-password) | Hash Password |
| [$HIBER](VAX-VMS-731/system-services-g-z-2003.md#hiber-hibernate) | Hibernate |
| [$ICC_ACCEPT](VAX-VMS-731/system-services-g-z-2003.md#icc_accept-accept-for-intra-cluster-communications-icc) | Accept for Intra-Cluster Communications (ICC) |
| [$ICC_CLOSE_ASSOC](VAX-VMS-731/system-services-g-z-2003.md#icc_close_assoc-close-association-for-intra-cluster-communications-icc) | Close Association for Intra-Cluster Communications (ICC) |
| [$ICC_CONNECT](VAX-VMS-731/system-services-g-z-2003.md#icc_connect-connect-for-intra-cluster-communications-icc) | Connect for Intra-Cluster Communications (ICC) |
| [$ICC_CONNECTW](VAX-VMS-731/system-services-g-z-2003.md#icc_connectw-connect-for-intra-cluster-communications-and-wait) | Connect for Intra-Cluster Communications and Wait |
| [$ICC_DISCONNECT](VAX-VMS-731/system-services-g-z-2003.md#icc_disconnect-disconnect-for-intra-cluster-communications-icc) | Disconnect for Intra-Cluster Communications (ICC) |
| [$ICC_DISCONNECTW](VAX-VMS-731/system-services-g-z-2003.md#icc_disconnectw-disconnect-and-wait-for-intra-cluster-communications-icc) | Disconnect and Wait for Intra-Cluster Communications (ICC) |
| [$ICC_OPEN_ASSOC](VAX-VMS-731/system-services-g-z-2003.md#icc_open_assoc-open-association-for-intra-cluster-communications-icc) | Open Association for Intra-Cluster Communications (ICC) |
| [$ICC_RECEIVE](VAX-VMS-731/system-services-g-z-2003.md#icc_receive-receive-for-intra-cluster-communications-icc) | Receive for Intra-Cluster Communications (ICC) |
| [$ICC_RECEIVEW](VAX-VMS-731/system-services-g-z-2003.md#icc_receivew-receive-and-wait-for-intra-cluster-communications-icc) | Receive and Wait for Intra-Cluster Communications (ICC) |
| [$ICC_REJECT](VAX-VMS-731/system-services-g-z-2003.md#icc_reject-reject-for-intra-cluster-communications-icc) | Reject for Intra-Cluster Communications (ICC) |
| [$ICC_REPLY](VAX-VMS-731/system-services-g-z-2003.md#icc_reply-reply-for-intra-cluster-communications-icc) | Reply for Intra-Cluster Communications (ICC) |
| [$ICC_REPLYW](VAX-VMS-731/system-services-g-z-2003.md#icc_replyw-reply-and-wait-for-intra-cluster-communications-icc) | Reply and Wait for Intra-Cluster Communications (ICC) |
| [$ICC_TRANSCEIVE](VAX-VMS-731/system-services-g-z-2003.md#icc_transceive-transceive-for-intra-cluster-communications-icc) | Transceive for Intra-Cluster Communications (ICC) |
| [$ICC_TRANSCEIVEW](VAX-VMS-731/system-services-g-z-2003.md#icc_transceivew-transceive-and-wait-for-intra-cluster-communications-icc) | Transceive and Wait for Intra-Cluster Communications (ICC) |
| [$ICC_TRANSMIT](VAX-VMS-731/system-services-g-z-2003.md#icc_transmit-transmit-for-intra-cluster-communications-icc) | Transmit for Intra-Cluster Communications (ICC) |
| [$ICC_TRANSMITW](VAX-VMS-731/system-services-g-z-2003.md#icc_transmitw-transmit-and-wait-for-intra-cluster-communications-icc) | Transmit and Wait for Intra-Cluster Communications (ICC) |
| [$IDTOASC](VAX-VMS-731/system-services-g-z-2003.md#idtoasc-translate-identifier-to-identifier-name) | Translate Identifier to Identifier Name |
| [$IEEE_SET_FP_CONTROL](VAX-VMS-731/system-services-g-z-2003.md#ieee_set_fp_control-alpha-only-set-ieee-floating-point-control-register) | Set IEEE Floating-Point Control Register |
| [$INIT_SYS_ALIGN_FAULT_REPORT](VAX-VMS-731/system-services-g-z-2003.md#init_sys_align_fault_report-alpha-only-initialize-system-alignment-fault-reporting) | Initialize System Alignment Fault Reporting |
| [$INIT_VOL](VAX-VMS-731/system-services-g-z-2003.md#init_vol-initialize-volume) | Initialize Volume |
| [$IO_CLEANUP](VAX-VMS-731/system-services-g-z-2003.md#io_cleanup-alpha-only-clean-up-fast-io) | Clean Up Fast I/O |
| [$IO_FASTPATH](VAX-VMS-731/system-services-g-z-2003.md#io_fastpath-alpha-only-control-fast-path-devices) | Control Fast Path Devices |
| [$IO_FASTPATHW](VAX-VMS-731/system-services-g-z-2003.md#io_fastpathw-alpha-only-control-fast-path-devices) | Control Fast Path Devices |
| [$IO_PERFORM](VAX-VMS-731/system-services-g-z-2003.md#io_perform-alpha-only-perform-fast-io) | Perform Fast I/O |
| [$IO_PERFORMW](VAX-VMS-731/system-services-g-z-2003.md#io_performw-alpha-only-perform-fast-io-and-wait) | Perform Fast I/O and Wait |
| [$IO_SETUP](VAX-VMS-731/system-services-g-z-2003.md#io_setup-alpha-only-set-up-fast-io) | Set Up Fast I/O |
| [$JOIN_RM](VAX-VMS-731/system-services-g-z-2003.md#join_rm-join-resource-manager) | Join Resource Manager |
| [$JOIN_RMW](VAX-VMS-731/system-services-g-z-2003.md#join_rmw-join-resource-manager-and-wait) | Join Resource Manager and Wait |
| [$LCKPAG](VAX-VMS-731/system-services-g-z-2003.md#lckpag-lock-pages-in-memory) | Lock Pages in Memory |
| [$LCKPAG_64](VAX-VMS-731/system-services-g-z-2003.md#lckpag_64-alpha-only-lock-pages-in-memory) | Lock Pages in Memory |
| [$LKWSET](VAX-VMS-731/system-services-g-z-2003.md#lkwset-lock-pages-in-working-set) | Lock Pages in Working Set |
| [$LKWSET_64](VAX-VMS-731/system-services-g-z-2003.md#lkwset_64-alpha-only-lock-pages-in-working-set) | Lock Pages in Working Set |
| [$MGBLSC](VAX-VMS-731/system-services-g-z-2003.md#mgblsc-map-global-section) | Map Global Section |
| [$MGBLSC_64](VAX-VMS-731/system-services-g-z-2003.md#mgblsc_64-alpha-only-map-to-global-section) | Map to Global Section |
| [$MGBLSC_GPFN_64](VAX-VMS-731/system-services-g-z-2003.md#mgblsc_gpfn_64-alpha-only-map-global-page-frame-section) | Map Global Page Frame Section |
| [$MOD_HOLDER](VAX-VMS-731/system-services-g-z-2003.md#mod_holder-modify-holder-record-in-rights-database) | Modify Holder Record in Rights Database |
| [$MOD_IDENT](VAX-VMS-731/system-services-g-z-2003.md#mod_ident-modify-identifier-in-rights-database) | Modify Identifier in Rights Database |
| [$MOUNT](VAX-VMS-731/system-services-g-z-2003.md#mount-mount-volume) | Mount Volume |
| [$MTACCESS](VAX-VMS-731/system-services-g-z-2003.md#mtaccess-magnetic-tape-accessibility) | Magnetic Tape Accessibility |
| [$NUMTIM](VAX-VMS-731/system-services-g-z-2003.md#numtim-convert-binary-time-to-numeric-time) | Convert Binary Time to Numeric Time |
| [$NUMUTC](VAX-VMS-731/system-services-g-z-2003.md#numutc-convert-utc-time-to-numeric-components) | Convert UTC Time to Numeric Components |
| [$PARSE_ACL](VAX-VMS-731/system-services-g-z-2003.md#parse_acl-parse-access-control-list-entry) | Parse Access Control List Entry |
| [$PERM_DIS_ALIGN_FAULT_REPORT](VAX-VMS-731/system-services-g-z-2003.md#perm_dis_align_fault_report-alpha-only-disable-alignment-fault-reporting) | Disable Alignment Fault Reporting |
| [$PERM_REPORT_ALIGN_FAULT](VAX-VMS-731/system-services-g-z-2003.md#perm_report_align_fault-alpha-only-report-alignment-fault) | Report Alignment Fault |
| [$PERSONA_ASSUME](VAX-VMS-731/system-services-g-z-2003.md#persona_assume-vax-only-assume-persona) | Assume Persona |
| [$PERSONA_CLONE](VAX-VMS-731/system-services-g-z-2003.md#persona_clone-alpha-only-clone-persona) | Clone Persona |
| [$PERSONA_CREATE](VAX-VMS-731/system-services-g-z-2003.md#persona_create-vax-only-create-persona) | Create Persona |
| [$PERSONA_CREATE_EXTENSION](VAX-VMS-731/system-services-g-z-2003.md#persona_create_extension-alpha-only-create-persona-extension) | Create Persona Extension |
| [$PERSONA_DELEGATE](VAX-VMS-731/system-services-g-z-2003.md#persona_delegate-alpha-only-delegate-persona-to-a-server-process) | Delegate Persona to a Server Process |
| [$PERSONA_DELETE](VAX-VMS-731/system-services-g-z-2003.md#persona_delete-delete-persona) | Delete Persona |
| [$PERSONA_DELETE_EXTENSION](VAX-VMS-731/system-services-g-z-2003.md#persona_delete_extension-alpha-only-delete-persona-extension) | Delete Persona Extension |
| [$PERSONA_EXTENSION_LOOKUP](VAX-VMS-731/system-services-g-z-2003.md#persona_extension_lookup-alpha-only-translates-an-extension-name) | Translates an Extension Name |
| [$PERSONA_FIND](VAX-VMS-731/system-services-g-z-2003.md#persona_find-alpha-only-find-persona-with-characteristics) | Find Persona with Characteristics |
| [$PERSONA_MODIFY](VAX-VMS-731/system-services-g-z-2003.md#persona_modify-alpha-only-modify-persona-data) | Modify Persona Data |
| [$PERSONA_QUERY](VAX-VMS-731/system-services-g-z-2003.md#persona_query-alpha-only-query-for-persona-data) | Query for Persona Data |
| [$PERSONA_RESERVE](VAX-VMS-731/system-services-g-z-2003.md#persona_reserve-alpha-only-reserve-persona-slot) | Reserve Persona Slot |
| [$PROCESS_AFFINITY](VAX-VMS-731/system-services-g-z-2003.md#process_affinity-alpha-only-modify-process-affinity) | Modify Process Affinity |
| [$PROCESS_CAPABILITIES](VAX-VMS-731/system-services-g-z-2003.md#process_capabilities-alpha-only-modify-process-user-capabilities) | Modify Process User Capabilities |
| [$PROCESS_SCAN](VAX-VMS-731/system-services-g-z-2003.md#process_scan-process-scan) | Process Scan |
| [$PURGE_WS](VAX-VMS-731/system-services-g-z-2003.md#purge_ws-alpha-only-purge-working-set) | Purge Working Set |
| [$PURGWS](VAX-VMS-731/system-services-g-z-2003.md#purgws-purge-working-set) | Purge Working Set |
| [$PUTMSG](VAX-VMS-731/system-services-g-z-2003.md#putmsg-put-message) | Put Message |
| [$QIO](VAX-VMS-731/system-services-g-z-2003.md#qio-queue-io-request) | Queue I/O Request |
| [$QIOW](VAX-VMS-731/system-services-g-z-2003.md#qiow-queue-io-request-and-wait) | Queue I/O Request and Wait |
| [$READEF](VAX-VMS-731/system-services-g-z-2003.md#readef-read-event-flags) | Read Event Flags |
| [$REGISTRY](VAX-VMS-731/system-services-g-z-2003.md#registry-alpha-only-interface-to-the-openvms-registry-database) | Interface to the OpenVMS Registry Database |
| [$REGISTRYW](VAX-VMS-731/system-services-g-z-2003.md#registryw-alpha-only-interface-to-the-openvms-registry-database-and-wait) | Interface to the OpenVMS Registry Database and Wait |
| [$RELEASE_GALAXY_LOCK](VAX-VMS-731/system-services-g-z-2003.md#release_galaxy_lock-alpha-only-release-openvms-galaxy-lock) | Release OpenVMS Galaxy Lock |
| [$RELEASE_VP](VAX-VMS-731/system-services-g-z-2003.md#release_vp-vax-only-release-vector-processor) | Release Vector Processor |
| [$REM_HOLDER](VAX-VMS-731/system-services-g-z-2003.md#rem_holder-remove-holder-record-from-rights-database) | Remove Holder Record from Rights Database |
| [$REM_IDENT](VAX-VMS-731/system-services-g-z-2003.md#rem_ident-remove-identifier-from-rights-database) | Remove Identifier from Rights Database |
| [$RESCHED](VAX-VMS-731/system-services-g-z-2003.md#resched-reschedule-process) | Reschedule Process |
| [$RESTORE_VP_EXCEPTION](VAX-VMS-731/system-services-g-z-2003.md#restore_vp_exception-vax-only-restore-vector-processor-exception-state) | Restore Vector Processor Exception State |
| [$RESTORE_VP_STATE](VAX-VMS-731/system-services-g-z-2003.md#restore_vp_state-vax-only-restore-vector-state) | Restore Vector State |
| [$RESUME](VAX-VMS-731/system-services-g-z-2003.md#resume-resume-process) | Resume Process |
| [$REVOKID](VAX-VMS-731/system-services-g-z-2003.md#revokid-revoke-identifier-from-process) | Revoke Identifier from Process |
| [$RMSRUNDWN](VAX-VMS-731/system-services-g-z-2003.md#rmsrundwn-rms-rundown) | RMS Rundown |
| [$SAVE_VP_EXCEPTION](VAX-VMS-731/system-services-g-z-2003.md#save_vp_exception-vax-only-save-vector-processor-exception-state) | Save Vector Processor Exception State |
| [$SCAN_INTRUSION](VAX-VMS-731/system-services-g-z-2003.md#scan_intrusion-scan-intrusion-database) | Scan Intrusion Database |
| [$SCHDWK](VAX-VMS-731/system-services-g-z-2003.md#schdwk-schedule-wakeup) | Schedule Wakeup |
| [$SCHED](VAX-VMS-731/system-services-g-z-2003.md#sched-affect-process-scheduling) | Affect Process Scheduling |
| [$SETAST](VAX-VMS-731/system-services-g-z-2003.md#setast-set-ast-enable) | Set AST Enable |
| [$SETCLUEVT](VAX-VMS-731/system-services-g-z-2003.md#setcluevt-set-cluster-event) | Set Cluster Event |
| [$SETDDIR](VAX-VMS-731/system-services-g-z-2003.md#setddir-set-default-directory) | Set Default Directory |
| [$SETDFPROT](VAX-VMS-731/system-services-g-z-2003.md#setdfprot-set-default-file-protection) | Set Default File Protection |
| [$SETDTI](VAX-VMS-731/system-services-g-z-2003.md#setdti-set-distributed-transaction-information) | Set Distributed Transaction Information |
| [$SETDTIW](VAX-VMS-731/system-services-g-z-2003.md#setdtiw-set-distributed-transaction-information-and-wait) | Set Distributed Transaction Information and Wait |
| [$SETEF](VAX-VMS-731/system-services-g-z-2003.md#setef-set-event-flag) | Set Event Flag |
| [$SETEXV](VAX-VMS-731/system-services-g-z-2003.md#setexv-set-exception-vector) | Set Exception Vector |
| [$SETIME](VAX-VMS-731/system-services-g-z-2003.md#setime-set-system-time) | Set System Time |
| [$SETIMR](VAX-VMS-731/system-services-g-z-2003.md#setimr-set-timer) | Set Timer |
| [$SETPRA](VAX-VMS-731/system-services-g-z-2003.md#setpra-set-power-recovery-ast) | Set Power Recovery AST |
| [$SETPRI](VAX-VMS-731/system-services-g-z-2003.md#setpri-set-priority) | Set Priority |
| [$SETPRN](VAX-VMS-731/system-services-g-z-2003.md#setprn-set-process-name) | Set Process Name |
| [$SETPRT](VAX-VMS-731/system-services-g-z-2003.md#setprt-set-protection-on-pages) | Set Protection on Pages |
| [$SETPRT_64](VAX-VMS-731/system-services-g-z-2003.md#setprt_64-alpha-only-set-protection-on-pages) | Set Protection on Pages |
| [$SETPRV](VAX-VMS-731/system-services-g-z-2003.md#setprv-set-privileges) | Set Privileges |
| [$SETRWM](VAX-VMS-731/system-services-g-z-2003.md#setrwm-set-resource-wait-mode) | Set Resource Wait Mode |
| [$SETSHLV](VAX-VMS-731/system-services-g-z-2003.md#setshlv-set-automatic-unshelving) | Set Automatic Unshelving |
| [$SETSTK](VAX-VMS-731/system-services-g-z-2003.md#setstk-set-stack-limits) | Set Stack Limits |
| [$SETSWM](VAX-VMS-731/system-services-g-z-2003.md#setswm-set-process-swap-mode) | Set Process Swap Mode |
| [$SETUAI](VAX-VMS-731/system-services-g-z-2003.md#setuai-set-user-authorization-information) | Set User Authorization Information |
| [$SETUP_AVOID_PREEMPT](VAX-VMS-731/system-services-g-z-2003.md#setup_avoid_preempt-setup-for-process-preemption-avoidance) | Setup for Process Preemption Avoidance |
| [$SET_DEFAULT_TRANS](VAX-VMS-731/system-services-g-z-2003.md#set_default_trans-set-default-transaction) | Set Default Transaction |
| [$SET_DEFAULT_TRANSW](VAX-VMS-731/system-services-g-z-2003.md#set_default_transw-set-default-transaction-and-wait) | Set Default Transaction and Wait |
| [$SET_DEVICE](VAX-VMS-731/system-services-g-z-2003.md#set_device-set-device-characteristics) | Set Device Characteristics |
| [$SET_DEVICEW](VAX-VMS-731/system-services-g-z-2003.md#set_devicew-set-device-characteristics-and-wait) | Set Device Characteristics and Wait |
| [$SET_IMPLICIT_AFFINITY](VAX-VMS-731/system-services-g-z-2003.md#set_implicit_affinity-alpha-only-modify-process-implicit-affinity) | Modify Process Implicit Affinity |
| [$SET_PROCESS_PROPERTIESW](VAX-VMS-731/system-services-g-z-2003.md#set_process_propertiesw-alpha-only-sets-simple-value) | Sets Simple Value |
| [$SET_RESOURCE_DOMAIN](VAX-VMS-731/system-services-g-z-2003.md#set_resource_domain-set-resource-domain) | Set Resource Domain |
| [$SET_RETURN_VALUE](VAX-VMS-731/system-services-g-z-2003.md#set_return_value-alpha-and-i64-only-sets-the-return-value-of) | Sets the return value of |
| [$SET_SECURITY](VAX-VMS-731/system-services-g-z-2003.md#set_security-set-security-characteristics) | Set Security Characteristics |
| [$SET_SYSTEM_EVENT](VAX-VMS-731/system-services-g-z-2003.md#set_system_event-alpha-only-set-system-event) | Set System Event |
| [$SHOW_INTRUSION](VAX-VMS-731/system-services-g-z-2003.md#show_intrusion-show-intrusion-information) | Show Intrusion Information |
| [$SIGNAL_ARRAY_64](VAX-VMS-731/system-services-g-z-2003.md#signal_array_64-signal-array) | Signal Array |
| [$SNDERR](VAX-VMS-731/system-services-g-z-2003.md#snderr-send-message-to-error-logger) | Send Message to Error Logger |
| [$SNDJBC](VAX-VMS-731/system-services-g-z-2003.md#sndjbc-send-to-job-controller) | Send to Job Controller |
| [$SNDJBCW](VAX-VMS-731/system-services-g-z-2003.md#sndjbcw-send-to-job-controller-and-wait) | Send to Job Controller and Wait |
| [$SNDOPR](VAX-VMS-731/system-services-g-z-2003.md#sndopr-send-message-to-operator) | Send Message to Operator |
| [$START_ALIGN_FAULT_REPORT](VAX-VMS-731/system-services-g-z-2003.md#start_align_fault_report-alpha-only-start-alignment-fault-reporting) | Start Alignment Fault Reporting |
| [$START_BRANCH](VAX-VMS-731/system-services-g-z-2003.md#start_branch-start-branch) | Start Branch |
| [$START_BRANCHW](VAX-VMS-731/system-services-g-z-2003.md#start_branchw-start-branch-and-wait) | Start Branch and Wait |
| [$START_TRANS](VAX-VMS-731/system-services-g-z-2003.md#start_trans-start-transaction) | Start Transaction |
| [$START_TRANSW](VAX-VMS-731/system-services-g-z-2003.md#start_transw-start-transaction-and-wait) | Start Transaction and Wait |
| [$STOP_ALIGN_FAULT_REPORT](VAX-VMS-731/system-services-g-z-2003.md#stop_align_fault_report-alpha-only-stop-alignment-fault-reporting) | Stop Alignment Fault Reporting |
| [$STOP_SYS_ALIGN_FAULT_REPORT](VAX-VMS-731/system-services-g-z-2003.md#stop_sys_align_fault_report-alpha-only-stop-system-alignment-fault-reporting) | Stop System Alignment Fault Reporting |
| [$SUBSYSTEM](VAX-VMS-731/system-services-g-z-2003.md#subsystem-subsystem) | Subsystem |
| [$SUSPND](VAX-VMS-731/system-services-g-z-2003.md#suspnd-suspend-process) | Suspend Process |
| [$SYNCH](VAX-VMS-731/system-services-g-z-2003.md#synch-synchronize) | Synchronize |
| [$TIMCON](VAX-VMS-731/system-services-g-z-2003.md#timcon-time-converter) | Time Converter |
| [$TRANS_EVENT](VAX-VMS-731/system-services-g-z-2003.md#trans_event-transaction-event) | Transaction Event |
| [$TRANS_EVENTW](VAX-VMS-731/system-services-g-z-2003.md#trans_eventw-transaction-event-and-wait) | Transaction Event and Wait |
| [$TRNLNM](VAX-VMS-731/system-services-g-z-2003.md#trnlnm-translate-logical-name) | Translate Logical Name |
| [$TSTCLUEVT](VAX-VMS-731/system-services-g-z-2003.md#tstcluevt-test-cluster-event) | Test Cluster Event |
| [$ULKPAG](VAX-VMS-731/system-services-g-z-2003.md#ulkpag-unlock-pages-from-memory) | Unlock Pages from Memory |
| [$ULKPAG_64](VAX-VMS-731/system-services-g-z-2003.md#ulkpag_64-alpha-only-unlock-pages-from-memory) | Unlock Pages from Memory |
| [$ULWSET](VAX-VMS-731/system-services-g-z-2003.md#ulwset-unlock-pages-from-working-set) | Unlock Pages from Working Set |
| [$ULWSET_64](VAX-VMS-731/system-services-g-z-2003.md#ulwset_64-alpha-only-unlock-pages-from-working-set) | Unlock Pages from Working Set |
| [$UNWIND](VAX-VMS-731/system-services-g-z-2003.md#unwind-unwind-call-stack) | Unwind Call Stack |
| [$UPDSEC](VAX-VMS-731/system-services-g-z-2003.md#updsec-update-section-file-on-disk) | Update Section File on Disk |
| [$UPDSECW](VAX-VMS-731/system-services-g-z-2003.md#updsecw-update-section-file-on-disk-and-wait) | Update Section File on Disk and Wait |
| [$UPDSEC_64](VAX-VMS-731/system-services-g-z-2003.md#updsec_64-alpha-only-update-global-section-file-on-disk) | Update Global Section File on Disk |
| [$UPDSEC_64W](VAX-VMS-731/system-services-g-z-2003.md#updsec_64w-alpha-only-update-global-section-file-on-disk-and-wait) | Update Global Section File on Disk and Wait |
| [$VERIFY_PROXY](VAX-VMS-731/system-services-g-z-2003.md#verify_proxy-verify-a-proxy) | Verify a Proxy |
| [$WAITFR](VAX-VMS-731/system-services-g-z-2003.md#waitfr-wait-for-single-event-flag) | Wait for Single Event Flag |
| [$WAKE](VAX-VMS-731/system-services-g-z-2003.md#wake-wake-process-from-hibernation) | Wake Process from Hibernation |
| [$WFLAND](VAX-VMS-731/system-services-g-z-2003.md#wfland-wait-for-logical-and-of-event-flags) | Wait for Logical AND of Event Flags |
| [$WFLOR](VAX-VMS-731/system-services-g-z-2003.md#wflor-wait-for-logical-or-of-event-flags) | Wait for Logical OR of Event Flags |

## RMS — Record Management Services

| Routine | Description |
|---|---|
| [$CLOSE](VAX-VMS-731/rms-reference.md#close) |  |
| [$CONNECT](VAX-VMS-731/rms-reference.md#connect) |  |
| [$CREATE](VAX-VMS-731/rms-reference.md#create) |  |
| [$DELETE](VAX-VMS-731/rms-reference.md#delete) |  |
| [$DISCONNECT](VAX-VMS-731/rms-reference.md#disconnect) |  |
| [$DISPLAY](VAX-VMS-731/rms-reference.md#display) |  |
| [$ENTER](VAX-VMS-731/rms-reference.md#enter) |  |
| [$ERASE](VAX-VMS-731/rms-reference.md#erase) |  |
| [$EXTEND](VAX-VMS-731/rms-reference.md#extend) |  |
| [$FAB](VAX-VMS-731/rms-reference.md#fab) |  |
| [$FAB_STORE](VAX-VMS-731/rms-reference.md#fab_store) |  |
| [$FIND](VAX-VMS-731/rms-reference.md#find) |  |
| [$FLUSH](VAX-VMS-731/rms-reference.md#flush) |  |
| [$FREE](VAX-VMS-731/rms-reference.md#free) |  |
| [$GET](VAX-VMS-731/rms-reference.md#get) |  |
| [$NAM](VAX-VMS-731/rms-reference.md#nam) |  |
| [$NAML](VAX-VMS-731/rms-reference.md#naml) |  |
| [$NAML_STORE](VAX-VMS-731/rms-reference.md#naml_store) |  |
| [$NAM_STORE](VAX-VMS-731/rms-reference.md#nam_store) |  |
| [$NXTVOL](VAX-VMS-731/rms-reference.md#nxtvol) |  |
| [$OPEN](VAX-VMS-731/rms-reference.md#open) |  |
| [$PARSE](VAX-VMS-731/rms-reference.md#parse) |  |
| [$PUT](VAX-VMS-731/rms-reference.md#put) |  |
| [$RAB](VAX-VMS-731/rms-reference.md#rab) |  |
| [$RAB64](VAX-VMS-731/rms-reference.md#rab64-alpha-only) |  |
| [$RAB64_STORE](VAX-VMS-731/rms-reference.md#rab64_store-alpha-only) |  |
| [$RAB_STORE](VAX-VMS-731/rms-reference.md#rab_store) |  |
| [$READ](VAX-VMS-731/rms-reference.md#read) |  |
| [$RELEASE](VAX-VMS-731/rms-reference.md#release) |  |
| [$REMOVE](VAX-VMS-731/rms-reference.md#remove) |  |
| [$RENAME](VAX-VMS-731/rms-reference.md#rename) |  |
| [$REWIND](VAX-VMS-731/rms-reference.md#rewind) |  |
| [$SEARCH](VAX-VMS-731/rms-reference.md#search) |  |
| [$SPACE](VAX-VMS-731/rms-reference.md#space) |  |
| [$TRUNCATE](VAX-VMS-731/rms-reference.md#truncate) |  |
| [$UPDATE](VAX-VMS-731/rms-reference.md#update) |  |
| [$WAIT](VAX-VMS-731/rms-reference.md#wait) |  |
| [$WRITE](VAX-VMS-731/rms-reference.md#write) |  |
| [$XABALL](VAX-VMS-731/rms-reference.md#xaball) |  |
| [$XABALL_STORE](VAX-VMS-731/rms-reference.md#xaball_store) |  |
| [$XABDAT](VAX-VMS-731/rms-reference.md#xabdat) |  |
| [$XABDAT_STORE](VAX-VMS-731/rms-reference.md#xabdat_store) |  |
| [$XABFHC](VAX-VMS-731/rms-reference.md#xabfhc) |  |
| [$XABFHC_STORE](VAX-VMS-731/rms-reference.md#xabfhc_store) |  |
| [$XABITM](VAX-VMS-731/rms-reference.md#xabitm) |  |
| [$XABKEY](VAX-VMS-731/rms-reference.md#xabkey) |  |
| [$XABKEY_STORE](VAX-VMS-731/rms-reference.md#xabkey_store) |  |
| [$XABPRO](VAX-VMS-731/rms-reference.md#xabpro) |  |
| [$XABPRO_STORE](VAX-VMS-731/rms-reference.md#xabpro_store) |  |
| [$XABRDT](VAX-VMS-731/rms-reference.md#xabrdt) |  |
| [$XABRDT_STORE](VAX-VMS-731/rms-reference.md#xabrdt_store) |  |
| [$XABSUM](VAX-VMS-731/rms-reference.md#xabsum) |  |
| [$XABSUM_STORE](VAX-VMS-731/rms-reference.md#xabsum_store) |  |
| [$XABTRM](VAX-VMS-731/rms-reference.md#xabtrm) |  |
| [$XABTRM_STORE](VAX-VMS-731/rms-reference.md#xabtrm_store) |  |

## LIB$ — OpenVMS Run-Time Library

| Routine | Description |
|---|---|
| [LIB$ADAWI](VAX-VMS-731/rtl-lib.md#libadawi-add-aligned-word-with-interlock) | Add Aligned Word with Interlock |
| [LIB$ADDX](VAX-VMS-731/rtl-lib.md#libaddx-add-two-multiple-precision-binary-numbers) | Add Two Multiple-Precision Binary Numbers |
| [LIB$ADD_TIMES](VAX-VMS-731/rtl-lib.md#libadd_times-add-two-quadword-times) | Add Two Quadword Times |
| [LIB$ANALYZE_SDESC](VAX-VMS-731/rtl-lib.md#libanalyze_sdesc-analyze-string-descriptor) | Analyze String Descriptor |
| [LIB$ANALYZE_SDESC_64](VAX-VMS-731/rtl-lib.md#libanalyze_sdesc_64-alpha-only-analyze-string-descriptor) | Analyze String Descriptor |
| [LIB$ASN_WTH_MBX](VAX-VMS-731/rtl-lib.md#libasn_wth_mbx-assign-channel-with-mailbox) | Assign Channel with Mailbox |
| [LIB$AST_IN_PROG](VAX-VMS-731/rtl-lib.md#libast_in_prog-ast-in-progress) | AST in Progress |
| [LIB$ATTACH](VAX-VMS-731/rtl-lib.md#libattach-attach-terminal-to-process) | Attach Terminal to Process |
| [LIB$BBCCI](VAX-VMS-731/rtl-lib.md#libbbcci-test-and-clear-bit-with-interlock) | Test and Clear Bit with Interlock |
| [LIB$BBSSI](VAX-VMS-731/rtl-lib.md#libbbssi-test-and-set-bit-with-interlock) | Test and Set Bit with Interlock |
| [LIB$BUILD_NODESPEC](VAX-VMS-731/rtl-lib.md#libbuild_nodespec-build-a-node-name-specification) | Build a Node-Name Specification |
| [LIB$CALLG](VAX-VMS-731/rtl-lib.md#libcallg-call-routine-with-general-argument-list) | Call Routine with General Argument List |
| [LIB$CALLG_64](VAX-VMS-731/rtl-lib.md#libcallg_64-alpha-only-call-routine-with-general-argument-list) | Call Routine with General Argument List |
| [LIB$CHAR](VAX-VMS-731/rtl-lib.md#libchar-transform-byte-to-first-character-of-string) | Transform Byte to First Character of String |
| [LIB$COMPARE_NODENAME](VAX-VMS-731/rtl-lib.md#libcompare_nodename-compare-two-node-names) | Compare Two Node Names |
| [LIB$COMPRESS_NODENAME](VAX-VMS-731/rtl-lib.md#libcompress_nodename-compress-a-node-name-to-its-short-form-equivalence) | Compress a Node Name to Its Short Form Equivalence |
| [LIB$CONVERT_DATE_STRING](VAX-VMS-731/rtl-lib.md#libconvert_date_string-convert-date-string-to-quadword) | Convert Date String to Quadword |
| [LIB$CRC](VAX-VMS-731/rtl-lib.md#libcrc-calculate-a-cyclic-redundancy-check-crc) | Calculate a Cyclic Redundancy Check (CRC) |
| [LIB$CRC_TABLE](VAX-VMS-731/rtl-lib.md#libcrc_table-construct-a-cyclic-redundancy-check-crc-table) | Construct a Cyclic Redundancy Check (CRC) Table |
| [LIB$CREATE_DIR](VAX-VMS-731/rtl-lib.md#libcreate_dir-create-a-directory) | Create a Directory |
| [LIB$CREATE_USER_VM_ZONE](VAX-VMS-731/rtl-lib.md#libcreate_user_vm_zone-create-user-defined-storage-zone) | Create User-Defined Storage Zone |
| [LIB$CREATE_USER_VM_ZONE_64](VAX-VMS-731/rtl-lib.md#libcreate_user_vm_zone_64-alpha-only-create-user-defined-storage-zone) | Create User-Defined Storage Zone |
| [LIB$CREATE_VM_ZONE](VAX-VMS-731/rtl-lib.md#libcreate_vm_zone-create-a-new-zone) | Create a New Zone |
| [LIB$CREATE_VM_ZONE_64](VAX-VMS-731/rtl-lib.md#libcreate_vm_zone_64-alpha-only-create-a-new-zone) | Create a New Zone |
| [LIB$CRF_INS_KEY](VAX-VMS-731/rtl-lib.md#libcrf_ins_key-insert-key-in-cross-reference-table) | Insert Key in Cross-Reference Table |
| [LIB$CRF_INS_REF](VAX-VMS-731/rtl-lib.md#libcrf_ins_ref-insert-reference-to-a-key-in-the-cross-reference-table) | Insert Reference to a Key in the Cross-Reference Table |
| [LIB$CRF_OUTPUT](VAX-VMS-731/rtl-lib.md#libcrf_output-output-cross-reference-table-information) | Output Cross-Reference Table Information |
| [LIB$CURRENCY](VAX-VMS-731/rtl-lib.md#libcurrency-get-system-currency-symbol) | Get System Currency Symbol |
| [LIB$CVTF_FROM_INTERNAL_TIME](VAX-VMS-731/rtl-lib.md#libcvtf_from_internal_time-convert-internal-time-to-external-time-f-floating-point-value) | Convert Internal Time to External Time (F-Floating-Point Value) |
| [LIB$CVTF_TO_INTERNAL_TIME](VAX-VMS-731/rtl-lib.md#libcvtf_to_internal_time-convert-external-time-to-internal-time-f-floating-point-value) | Convert External Time to Internal Time (F-Floating-Point Value) |
| [LIB$CVT_DX_DX](VAX-VMS-731/rtl-lib.md#libcvt_dx_dx-general-data-type-conversion-routine) | General Data Type Conversion Routine |
| [LIB$CVT_FROM_INTERNAL_TIME](VAX-VMS-731/rtl-lib.md#libcvt_from_internal_time-convert-internal-time-to-external-time) | Convert Internal Time to External Time |
| [LIB$CVT_TO_INTERNAL_TIME](VAX-VMS-731/rtl-lib.md#libcvt_to_internal_time-convert-external-time-to-internal-time) | Convert External Time to Internal Time |
| [LIB$CVT_VECTIM](VAX-VMS-731/rtl-lib.md#libcvt_vectim-convert-7-word-vector-to-internal-time) | Convert 7-Word Vector to Internal Time |
| [LIB$CVT_xTB](VAX-VMS-731/rtl-lib.md#libcvt_xtb-convert-numeric-text-to-binary) | Convert Numeric Text to Binary |
| [LIB$CVT_xTB_64](VAX-VMS-731/rtl-lib.md#libcvt_xtb_64-alpha-only-convert-numeric-text-to-binary) | Convert Numeric Text to Binary |
| [LIB$DATE_TIME](VAX-VMS-731/rtl-lib.md#libdate_time-date-and-time-returned-as-a-string) | Date and Time Returned as a String |
| [LIB$DAY](VAX-VMS-731/rtl-lib.md#libday-day-number-returned-as-a-longword-integer) | Day Number Returned as a Longword Integer |
| [LIB$DAY_OF_WEEK](VAX-VMS-731/rtl-lib.md#libday_of_week-show-numeric-day-of-week) | Show Numeric Day of Week |
| [LIB$DECODE_FAULT](VAX-VMS-731/rtl-lib.md#libdecode_fault-decode-instruction-stream-during-fault) | Decode Instruction Stream During Fault |
| [LIB$DEC_OVER](VAX-VMS-731/rtl-lib.md#libdec_over-enable-or-disable-decimal-overflow-detection) | Enable or Disable Decimal Overflow Detection |
| [LIB$DELETE_FILE](VAX-VMS-731/rtl-lib.md#libdelete_file-delete-one-or-more-files) | Delete One or More Files |
| [LIB$DELETE_LOGICAL](VAX-VMS-731/rtl-lib.md#libdelete_logical-delete-logical-name) | Delete Logical Name |
| [LIB$DELETE_SYMBOL](VAX-VMS-731/rtl-lib.md#libdelete_symbol-delete-cli-symbol) | Delete CLI Symbol |
| [LIB$DELETE_VM_ZONE](VAX-VMS-731/rtl-lib.md#libdelete_vm_zone-delete-virtual-memory-zone) | Delete Virtual Memory Zone |
| [LIB$DELETE_VM_ZONE_64](VAX-VMS-731/rtl-lib.md#libdelete_vm_zone_64-alpha-only-delete-virtual-memory-zone) | Delete Virtual Memory Zone |
| [LIB$DIGIT_SEP](VAX-VMS-731/rtl-lib.md#libdigit_sep-get-digit-separator-symbol) | Get Digit Separator Symbol |
| [LIB$DISABLE_CTRL](VAX-VMS-731/rtl-lib.md#libdisable_ctrl-disable-cli-interception-of-control-characters) | Disable CLI Interception of Control Characters |
| [LIB$DO_COMMAND](VAX-VMS-731/rtl-lib.md#libdo_command-execute-command) | Execute Command |
| [LIB$EDIV](VAX-VMS-731/rtl-lib.md#libediv-extended-precision-divide) | Extended-Precision Divide |
| [LIB$EMODD](VAX-VMS-731/rtl-lib.md#libemodd-extended-multiply-and-integerize-routine-for-d-floating-point-values) | Extended Multiply and Integerize Routine for D-Floating-Point Values |
| [LIB$EMODF](VAX-VMS-731/rtl-lib.md#libemodf-extended-multiply-and-integerize-routine-for-f-floating-point-values) | Extended Multiply and Integerize Routine for F-Floating-Point Values |
| [LIB$EMODG](VAX-VMS-731/rtl-lib.md#libemodg-extended-multiply-and-integerize-routine-for-g-floating-point-values) | Extended Multiply and Integerize Routine for G-Floating-Point Values |
| [LIB$EMODH](VAX-VMS-731/rtl-lib.md#libemodh-extended-multiply-and-integerize-routine-for-h-floating-point-values) | Extended Multiply and Integerize Routine for H-Floating-Point Values |
| [LIB$EMUL](VAX-VMS-731/rtl-lib.md#libemul-extended-precision-multiply) | Extended-Precision Multiply |
| [LIB$ENABLE_CTRL](VAX-VMS-731/rtl-lib.md#libenable_ctrl-enable-cli-interception-of-control-characters) | Enable CLI Interception of Control Characters |
| [LIB$ESTABLISH](VAX-VMS-731/rtl-lib.md#libestablish-establish-a-condition-handler) | Establish a Condition Handler |
| [LIB$EXPAND_NODENAME](VAX-VMS-731/rtl-lib.md#libexpand_nodename-expand-a-node-name-to-its-full-name-equivalent) | Expand a Node Name to Its Full Name Equivalent |
| [LIB$EXTV](VAX-VMS-731/rtl-lib.md#libextv-extract-a-field-and-sign-extend) | Extract a Field and Sign-Extend |
| [LIB$EXTZV](VAX-VMS-731/rtl-lib.md#libextzv-extract-a-zero-extended-field) | Extract a Zero-Extended Field |
| [LIB$FFx](VAX-VMS-731/rtl-lib.md#libffx-find-first-clear-or-set-bit) | Find First Clear or Set Bit |
| [LIB$FID_TO_NAME](VAX-VMS-731/rtl-lib.md#libfid_to_name-convert-device-and-file-id-to-file-specification) | Convert Device and File ID to File Specification |
| [LIB$FILE_SCAN](VAX-VMS-731/rtl-lib.md#libfile_scan-file-scan) | File Scan |
| [LIB$FILE_SCAN_END](VAX-VMS-731/rtl-lib.md#libfile_scan_end-end-of-file-scan) | End-of-File Scan |
| [LIB$FIND_FILE](VAX-VMS-731/rtl-lib.md#libfind_file-find-file) | Find File |
| [LIB$FIND_FILE_END](VAX-VMS-731/rtl-lib.md#libfind_file_end-end-of-find-file) | End of Find File |
| [LIB$FIND_IMAGE_SYMBOL](VAX-VMS-731/rtl-lib.md#libfind_image_symbol-find-universal-symbol-in-shareable-image-file) | Find Universal Symbol in Shareable Image File |
| [LIB$FIND_VM_ZONE](VAX-VMS-731/rtl-lib.md#libfind_vm_zone-return-the-next-valid-zone-identifier) | Return the Next Valid Zone Identifier |
| [LIB$FIND_VM_ZONE_64](VAX-VMS-731/rtl-lib.md#libfind_vm_zone_64-alpha-only-return-the-next-valid-zone-identifier) | Return the Next Valid Zone Identifier |
| [LIB$FIT_NODENAME](VAX-VMS-731/rtl-lib.md#libfit_nodename-fit-a-node-name-into-an-output-field) | Fit a Node Name into an Output Field |
| [LIB$FIXUP_FLT](VAX-VMS-731/rtl-lib.md#libfixup_flt-fix-floating-reserved-operand) | Fix Floating Reserved Operand |
| [LIB$FLT_UNDER](VAX-VMS-731/rtl-lib.md#libflt_under-floating-point-underflow-detection) | Floating-Point Underflow Detection |
| [LIB$FORMAT_DATE_TIME](VAX-VMS-731/rtl-lib.md#libformat_date_time-format-date-andor-time) | Format Date and/or Time |
| [LIB$FORMAT_SOGW_PROT](VAX-VMS-731/rtl-lib.md#libformat_sogw_prot-format-protection-mask) | Format Protection Mask |
| [LIB$FREE_DATE_TIME_CONTEXT](VAX-VMS-731/rtl-lib.md#libfree_date_time_context-free-the-context-area-used-when-formatting-dates-and-times-for-input-or-output) | Free the Context Area Used When Formatting Dates and Times for** **Input or Output |
| [LIB$FREE_EF](VAX-VMS-731/rtl-lib.md#libfree_ef-free-event-flag) | Free Event Flag |
| [LIB$FREE_LUN](VAX-VMS-731/rtl-lib.md#libfree_lun-free-logical-unit-number) | Free Logical Unit Number |
| [LIB$FREE_TIMER](VAX-VMS-731/rtl-lib.md#libfree_timer-free-timer-storage) | Free Timer Storage |
| [LIB$FREE_VM](VAX-VMS-731/rtl-lib.md#libfree_vm-free-virtual-memory-from-program-region) | Free Virtual Memory from Program Region |
| [LIB$FREE_VM_64](VAX-VMS-731/rtl-lib.md#libfree_vm_64-alpha-only-free-virtual-memory-from-program-region) | Free Virtual Memory from Program Region |
| [LIB$FREE_VM_PAGE](VAX-VMS-731/rtl-lib.md#libfree_vm_page-free-virtual-memory-page) | Free Virtual Memory Page |
| [LIB$FREE_VM_PAGE_64](VAX-VMS-731/rtl-lib.md#libfree_vm_page_64-alpha-only-free-virtual-memory-page) | Free Virtual Memory Page |
| [LIB$GETDVI](VAX-VMS-731/rtl-lib.md#libgetdvi-get-devicevolume-information) | Get Device/Volume Information |
| [LIB$GETJPI](VAX-VMS-731/rtl-lib.md#libgetjpi-get-jobprocess-information) | Get Job/Process Information |
| [LIB$GETQUI](VAX-VMS-731/rtl-lib.md#libgetqui-get-queue-information) | Get Queue Information |
| [LIB$GETSYI](VAX-VMS-731/rtl-lib.md#libgetsyi-get-systemwide-information) | Get Systemwide Information |
| [LIB$GET_ACCNAM](VAX-VMS-731/rtl-lib.md#libget_accnam-get-access-name-table-for-protected-object-class-by-name) | Get Access Name Table for Protected Object Class (by Name) |
| [LIB$GET_ACCNAM_BY_CONTEXT](VAX-VMS-731/rtl-lib.md#libget_accnam_by_context-get-access-name-table-for-protected-object-class-by-context) | Get Access Name Table for Protected Object Class (by Context) |
| [LIB$GET_COMMAND](VAX-VMS-731/rtl-lib.md#libget_command-get-line-from-syscommand) | Get Line from SYS$COMMAND |
| [LIB$GET_COMMON](VAX-VMS-731/rtl-lib.md#libget_common-get-string-from-common) | Get String from Common |
| [LIB$GET_CURR_INVO_CONTEXT](VAX-VMS-731/rtl-lib.md#libget_curr_invo_context-alpha-only-get-current-invocation-context) | Get Current Invocation Context |
| [LIB$GET_DATE_FORMAT](VAX-VMS-731/rtl-lib.md#libget_date_format-get-the-users-date-input-format) | Get the User’s Date Input Format |
| [LIB$GET_EF](VAX-VMS-731/rtl-lib.md#libget_ef-get-event-flag) | Get Event Flag |
| [LIB$GET_FOREIGN](VAX-VMS-731/rtl-lib.md#libget_foreign-get-foreign-command-line) | Get Foreign Command Line |
| [LIB$GET_FULLNAME_OFFSET](VAX-VMS-731/rtl-lib.md#libget_fullname_offset-get-the-offset-to-the-starting-position-of-the-most-significant-part-of-a-full-name) | Get the Offset to the Starting Position of the Most Significant Part of** **a Full Name |
| [LIB$GET_HOSTNAME](VAX-VMS-731/rtl-lib.md#libget_hostname-get-host-node-name) | Get Host Node Name |
| [LIB$GET_INPUT](VAX-VMS-731/rtl-lib.md#libget_input-get-line-from-sysinput) | Get Line from SYS$INPUT |
| [LIB$GET_INVO_CONTEXT](VAX-VMS-731/rtl-lib.md#libget_invo_context-alpha-only-get-invocation-context) | Get Invocation Context |
| [LIB$GET_INVO_HANDLE](VAX-VMS-731/rtl-lib.md#libget_invo_handle-alpha-only-get-invocation-handle) | Get Invocation Handle |
| [LIB$GET_LOGICAL](VAX-VMS-731/rtl-lib.md#libget_logical-get-logical-name) | Get Logical Name |
| [LIB$GET_LUN](VAX-VMS-731/rtl-lib.md#libget_lun-get-logical-unit-number) | Get Logical Unit Number |
| [LIB$GET_MAXIMUM_DATE_LENGTH](VAX-VMS-731/rtl-lib.md#libget_maximum_date_length-retrieve-the-maximum-length-of-a-datetime-string) | Retrieve the Maximum Length of a Date/Time String |
| [LIB$GET_PREV_INVO_CONTEXT](VAX-VMS-731/rtl-lib.md#libget_prev_invo_context-alpha-only-get-previous-invocation-context) | Get Previous Invocation Context |
| [LIB$GET_PREV_INVO_HANDLE](VAX-VMS-731/rtl-lib.md#libget_prev_invo_handle-alpha-only-get-previous-invocation-handle) | Get Previous Invocation Handle |
| [LIB$GET_SYMBOL](VAX-VMS-731/rtl-lib.md#libget_symbol-get-value-of-cli-symbol) | Get Value of CLI Symbol |
| [LIB$GET_USERS_LANGUAGE](VAX-VMS-731/rtl-lib.md#libget_users_language-return-the-users-language) | Return the User’s Language |
| [LIB$GET_VM](VAX-VMS-731/rtl-lib.md#libget_vm-allocate-virtual-memory) | Allocate Virtual Memory |
| [LIB$GET_VM_64](VAX-VMS-731/rtl-lib.md#libget_vm_64-alpha-only-allocate-virtual-memory) | Allocate Virtual Memory |
| [LIB$GET_VM_PAGE](VAX-VMS-731/rtl-lib.md#libget_vm_page-get-virtual-memory-page) | Get Virtual Memory Page |
| [LIB$GET_VM_PAGE_64](VAX-VMS-731/rtl-lib.md#libget_vm_page_64-alpha-only-get-virtual-memory-page) | Get Virtual Memory Page |
| [LIB$ICHAR](VAX-VMS-731/rtl-lib.md#libichar-convert-first-character-of-string-to-integer) | Convert First Character of String to Integer |
| [LIB$INDEX](VAX-VMS-731/rtl-lib.md#libindex-index-to-relative-position-of-substring) | Index to Relative Position of Substring |
| [LIB$INIT_DATE_TIME_CONTEXT](VAX-VMS-731/rtl-lib.md#libinit_date_time_context-initialize-the-context-area-used-in-formatting-dates-and-times-for-input-or-output) | Initialize the Context Area Used in Formatting Dates and Times for** **Input or Output |
| [LIB$INIT_TIMER](VAX-VMS-731/rtl-lib.md#libinit_timer-initialize-times-and-counts) | Initialize Times and Counts |
| [LIB$INSERT_TREE](VAX-VMS-731/rtl-lib.md#libinsert_tree-insert-entry-in-a-balanced-binary-tree) | Insert Entry in a Balanced Binary Tree |
| [LIB$INSERT_TREE_64](VAX-VMS-731/rtl-lib.md#libinsert_tree_64-alpha-only-insert-entry-in-a-balanced-binary-tree) | Insert Entry in a Balanced Binary Tree |
| [LIB$INSQHI](VAX-VMS-731/rtl-lib.md#libinsqhi-insert-entry-at-head-of-queue) | Insert Entry at Head of Queue |
| [LIB$INSQHIQ](VAX-VMS-731/rtl-lib.md#libinsqhiq-alpha-only-insert-entry-at-head-of-queue) | Insert Entry at Head of Queue |
| [LIB$INSQTI](VAX-VMS-731/rtl-lib.md#libinsqti-insert-entry-at-tail-of-queue) | Insert Entry at Tail of Queue |
| [LIB$INSQTIQ](VAX-VMS-731/rtl-lib.md#libinsqtiq-alpha-only-insert-entry-at-tail-of-queue) | Insert Entry at Tail of Queue |
| [LIB$INSV](VAX-VMS-731/rtl-lib.md#libinsv-insert-a-variable-bit-field) | Insert a Variable Bit Field |
| [LIB$INT_OVER](VAX-VMS-731/rtl-lib.md#libint_over-integer-overflow-detection) | Integer Overflow Detection |
| [LIB$LEN](VAX-VMS-731/rtl-lib.md#liblen-length-of-string-returned-as-longword-value) | Length of String Returned as Longword Value |
| [LIB$LOCC](VAX-VMS-731/rtl-lib.md#liblocc-locate-a-character) | Locate a Character |
| [LIB$LOOKUP_KEY](VAX-VMS-731/rtl-lib.md#liblookup_key-look-up-keyword-in-table) | Look Up Keyword in Table |
| [LIB$LOOKUP_TREE](VAX-VMS-731/rtl-lib.md#liblookup_tree-look-up-an-entry-in-a-balanced-binary-tree) | Look Up an Entry in a Balanced Binary Tree |
| [LIB$LOOKUP_TREE_64](VAX-VMS-731/rtl-lib.md#liblookup_tree_64-alpha-only-look-up-an-entry-in-a-balanced-binary-tree) | Look Up an Entry in a Balanced Binary Tree |
| [LIB$LP_LINES](VAX-VMS-731/rtl-lib.md#liblp_lines-lines-on-each-printer-page) | Lines on Each Printer Page |
| [LIB$MATCHC](VAX-VMS-731/rtl-lib.md#libmatchc-match-characters-return-relative-position) | Match Characters, Return Relative Position |
| [LIB$MATCH_COND](VAX-VMS-731/rtl-lib.md#libmatch_cond-match-condition-values) | Match Condition Values |
| [LIB$MOVC3](VAX-VMS-731/rtl-lib.md#libmovc3-move-characters) | Move Characters |
| [LIB$MOVC5](VAX-VMS-731/rtl-lib.md#libmovc5-move-characters-with-fill) | Move Characters with Fill |
| [LIB$MOVTC](VAX-VMS-731/rtl-lib.md#libmovtc-move-translated-characters) | Move Translated Characters |
| [LIB$MOVTUC](VAX-VMS-731/rtl-lib.md#libmovtuc-move-translated-until-character) | Move Translated Until Character |
| [LIB$MULTF_DELTA_TIME](VAX-VMS-731/rtl-lib.md#libmultf_delta_time-multiply-delta-time-by-an-f-floating-scalar) | Multiply Delta Time by an F-Floating Scalar |
| [LIB$MULT_DELTA_TIME](VAX-VMS-731/rtl-lib.md#libmult_delta_time-multiply-delta-time-by-scalar) | Multiply Delta Time by Scalar |
| [LIB$PARSE_ACCESS_CODE](VAX-VMS-731/rtl-lib.md#libparse_access_code-parse-access-encoded-name-string) | Parse Access Encoded Name String |
| [LIB$PARSE_SOGW_PROT](VAX-VMS-731/rtl-lib.md#libparse_sogw_prot-parse-protection-string) | Parse Protection String |
| [LIB$PAUSE](VAX-VMS-731/rtl-lib.md#libpause-pause-program-execution) | Pause Program Execution |
| [LIB$POLYD](VAX-VMS-731/rtl-lib.md#libpolyd-evaluate-polynomials) | Evaluate Polynomials |
| [LIB$POLYF](VAX-VMS-731/rtl-lib.md#libpolyf-evaluate-polynomials) | Evaluate Polynomials |
| [LIB$POLYG](VAX-VMS-731/rtl-lib.md#libpolyg-evaluate-polynomials) | Evaluate Polynomials |
| [LIB$POLYH](VAX-VMS-731/rtl-lib.md#libpolyh-evaluate-polynomials) | Evaluate Polynomials |
| [LIB$PUT_COMMON](VAX-VMS-731/rtl-lib.md#libput_common-put-string-to-common) | Put String to Common |
| [LIB$PUT_INVO_REGISTERS](VAX-VMS-731/rtl-lib.md#libput_invo_registers-alpha-only-put-invocation-registers) | Put Invocation Registers |
| [LIB$PUT_OUTPUT](VAX-VMS-731/rtl-lib.md#libput_output-put-line-to-sysoutput) | Put Line to SYS$OUTPUT |
| [LIB$RADIX_POINT](VAX-VMS-731/rtl-lib.md#libradix_point-radix-point-symbol) | Radix Point Symbol |
| [LIB$REMQHI](VAX-VMS-731/rtl-lib.md#libremqhi-remove-entry-from-head-of-queue) | Remove Entry from Head of Queue |
| [LIB$REMQHIQ](VAX-VMS-731/rtl-lib.md#libremqhiq-alpha-only-remove-entry-from-head-of-queue) | Remove Entry from Head of Queue |
| [LIB$REMQTI](VAX-VMS-731/rtl-lib.md#libremqti-remove-entry-from-tail-of-queue) | Remove Entry from Tail of Queue |
| [LIB$REMQTIQ](VAX-VMS-731/rtl-lib.md#libremqtiq-alpha-only-remove-entry-from-tail-of-queue) | Remove Entry from Tail of Queue |
| [LIB$RENAME_FILE](VAX-VMS-731/rtl-lib.md#librename_file-rename-one-or-more-files) | Rename One or More Files |
| [LIB$RESERVE_EF](VAX-VMS-731/rtl-lib.md#libreserve_ef-reserve-event-flag) | Reserve Event Flag |
| [LIB$RESET_VM_ZONE](VAX-VMS-731/rtl-lib.md#libreset_vm_zone-reset-virtual-memory-zone) | Reset Virtual Memory Zone |
| [LIB$RESET_VM_ZONE_64](VAX-VMS-731/rtl-lib.md#libreset_vm_zone_64-alpha-only-reset-virtual-memory-zone) | Reset Virtual Memory Zone |
| [LIB$REVERT](VAX-VMS-731/rtl-lib.md#librevert-revert-to-the-handler-of-the-routine-activator) | Revert to the Handler of the Routine Activator |
| [LIB$RUN_PROGRAM](VAX-VMS-731/rtl-lib.md#librun_program-run-new-program) | Run New Program |
| [LIB$SCANC](VAX-VMS-731/rtl-lib.md#libscanc-scan-for-characters-and-return-relative-position) | Scan for Characters and Return Relative Position |
| [LIB$SCOPY_DXDX](VAX-VMS-731/rtl-lib.md#libscopy_dxdx-copy-source-string-passed-by-descriptor-to-destination) | Copy Source String Passed by Descriptor to Destination |
| [LIB$SCOPY_R_DX](VAX-VMS-731/rtl-lib.md#libscopy_r_dx-copy-source-string-passed-by-reference-to-destination-string) | Copy Source String Passed by Reference to Destination String |
| [LIB$SCOPY_R_DX_64](VAX-VMS-731/rtl-lib.md#libscopy_r_dx_64-alpha-only-copy-source-string-passed-by-reference-to-destination-string) | Copy Source String Passed by Reference to Destination String |
| [LIB$SET_LOGICAL](VAX-VMS-731/rtl-lib.md#libset_logical-set-logical-name) | Set Logical Name |
| [LIB$SET_SYMBOL](VAX-VMS-731/rtl-lib.md#libset_symbol-set-value-of-cli-symbol) | Set Value of CLI Symbol |
| [LIB$SFREE1_DD](VAX-VMS-731/rtl-lib.md#libsfree1_dd-free-one-dynamic-string) | Free One Dynamic String |
| [LIB$SFREEN_DD](VAX-VMS-731/rtl-lib.md#libsfreen_dd-free-one-or-more-dynamic-strings) | Free One or More Dynamic Strings |
| [LIB$SGET1_DD](VAX-VMS-731/rtl-lib.md#libsget1_dd-get-one-dynamic-string) | Get One Dynamic String |
| [LIB$SGET1_DD_64](VAX-VMS-731/rtl-lib.md#libsget1_dd_64-alpha-only-get-one-dynamic-string) | Get One Dynamic String |
| [LIB$SHOW_TIMER](VAX-VMS-731/rtl-lib.md#libshow_timer-show-accumulated-times-and-counts) | Show Accumulated Times and Counts |
| [LIB$SHOW_VM](VAX-VMS-731/rtl-lib.md#libshow_vm-show-virtual-memory-statistics) | Show Virtual Memory Statistics |
| [LIB$SHOW_VM_64](VAX-VMS-731/rtl-lib.md#libshow_vm_64-alpha-only-show-virtual-memory-statistics) | Show Virtual Memory Statistics |
| [LIB$SHOW_VM_ZONE](VAX-VMS-731/rtl-lib.md#libshow_vm_zone-return-information-about-a-zone) | Return Information About a Zone |
| [LIB$SHOW_VM_ZONE_64](VAX-VMS-731/rtl-lib.md#libshow_vm_zone_64-alpha-only-return-information-about-a-zone) | Return Information About a Zone |
| [LIB$SIGNAL](VAX-VMS-731/rtl-lib.md#libsignal-signal-exception-condition) | Signal Exception Condition |
| [LIB$SIG_TO_RET](VAX-VMS-731/rtl-lib.md#libsig_to_ret-signal-converted-to-a-return-status) | Signal Converted to a Return Status |
| [LIB$SIG_TO_STOP](VAX-VMS-731/rtl-lib.md#libsig_to_stop-convert-a-signaled-condition-to-a-signaled-stop) | Convert a Signaled Condition to a Signaled Stop |
| [LIB$SIM_TRAP](VAX-VMS-731/rtl-lib.md#libsim_trap-simulate-floating-trap) | Simulate Floating Trap |
| [LIB$SKPC](VAX-VMS-731/rtl-lib.md#libskpc-skip-equal-characters) | Skip Equal Characters |
| [LIB$SPANC](VAX-VMS-731/rtl-lib.md#libspanc-skip-selected-characters) | Skip Selected Characters |
| [LIB$SPAWN](VAX-VMS-731/rtl-lib.md#libspawn-spawn-subprocess) | Spawn Subprocess |
| [LIB$STAT_TIMER](VAX-VMS-731/rtl-lib.md#libstat_timer-statistics-return-accumulated-times-and-counts) | Statistics, Return Accumulated Times and Counts |
| [LIB$STAT_VM](VAX-VMS-731/rtl-lib.md#libstat_vm-return-virtual-memory-statistics) | Return Virtual Memory Statistics |
| [LIB$STAT_VM_64](VAX-VMS-731/rtl-lib.md#libstat_vm_64-alpha-only-return-virtual-memory-statistics) | Return Virtual Memory Statistics |
| [LIB$STOP](VAX-VMS-731/rtl-lib.md#libstop-stop-execution-and-signal-the-condition) | Stop Execution and Signal the Condition |
| [LIB$SUBX](VAX-VMS-731/rtl-lib.md#libsubx-multiple-precision-binary-subtraction) | Multiple-Precision Binary Subtraction |
| [LIB$SUB_TIMES](VAX-VMS-731/rtl-lib.md#libsub_times-subtract-two-quadword-times) | Subtract Two Quadword Times |
| [LIB$SYS_ASCTIM](VAX-VMS-731/rtl-lib.md#libsys_asctim-invoke-asctim-to-convert-binary-time-to-ascii-string) | Invoke $ASCTIM to Convert Binary Time to ASCII String |
| [LIB$SYS_FAO](VAX-VMS-731/rtl-lib.md#libsys_fao-invoke-fao-system-service-to-format-output) | Invoke $FAO System Service to Format Output |
| [LIB$SYS_FAOL](VAX-VMS-731/rtl-lib.md#libsys_faol-invoke-faol-system-service-to-format-output) | Invoke $FAOL System Service to Format Output |
| [LIB$SYS_FAOL_64](VAX-VMS-731/rtl-lib.md#libsys_faol_64-alpha-only-invoke-faol_64-system-service-to-format-output) | Invoke $FAOL_64 System Service to Format Output |
| [LIB$SYS_GETMSG](VAX-VMS-731/rtl-lib.md#libsys_getmsg-invoke-getmsg-system-service-to-get-message-text) | Invoke $GETMSG System Service to Get Message Text |
| [LIB$TRAVERSE_TREE](VAX-VMS-731/rtl-lib.md#libtraverse_tree-traverse-a-balanced-binary-tree) | Traverse a Balanced Binary Tree |
| [LIB$TRAVERSE_TREE_64](VAX-VMS-731/rtl-lib.md#libtraverse_tree_64-alpha-only-traverse-a-balanced-binary-tree) | Traverse a Balanced Binary Tree |
| [LIB$TRA_ASC_EBC](VAX-VMS-731/rtl-lib.md#libtra_asc_ebc-translate-ascii-to-ebcdic) | Translate ASCII to EBCDIC |
| [LIB$TRA_EBC_ASC](VAX-VMS-731/rtl-lib.md#libtra_ebc_asc-translate-ebcdic-to-ascii) | Translate EBCDIC to ASCII |
| [LIB$TRIM_FILESPEC](VAX-VMS-731/rtl-lib.md#libtrim_filespec-fit-long-file-specification-into-fixed-field) | Fit Long File Specification into Fixed Field |
| [LIB$TRIM_FULLNAME](VAX-VMS-731/rtl-lib.md#libtrim_fullname-trim-a-full-name-to-fit-into-a-desired-output-field) | Trim a Full Name to Fit into a Desired Output Field |
| [LIB$VERIFY_VM_ZONE](VAX-VMS-731/rtl-lib.md#libverify_vm_zone-verify-a-zone) | Verify a Zone |
| [LIB$VERIFY_VM_ZONE_64](VAX-VMS-731/rtl-lib.md#libverify_vm_zone_64-alpha-only-verify-a-zone) | Verify a Zone |
| [LIB$WAIT](VAX-VMS-731/rtl-lib.md#libwait-wait-a-specified-period-of-time) | Wait a Specified Period of Time |

## CVT$ — Data Conversion

| Routine | Description |
|---|---|
| [CVT$CONVERT_FLOAT](VAX-VMS-731/rtl-lib.md#cvtconvert_float-convert-floating-point-data-type) | Convert Floating-Point Data Type |
| [CVT$FTOF](VAX-VMS-731/rtl-lib.md#cvtftof-convert-floating-point-data-type) | Convert Floating-Point Data Type |

## STR$ — String Manipulation

| Routine | Description |
|---|---|
| [STR$ADD](VAX-VMS-731/rtl-str.md#stradd-add-two-decimal-strings) | Add Two Decimal Strings |
| [STR$ANALYZE_SDESC](VAX-VMS-731/rtl-str.md#stranalyze_sdesc-analyze-string-descriptor) | Analyze String Descriptor |
| [STR$ANALYZE_SDESC_64](VAX-VMS-731/rtl-str.md#stranalyze_sdesc_64-alpha-only-analyze-string-descriptor) | Analyze String Descriptor |
| [STR$APPEND](VAX-VMS-731/rtl-str.md#strappend-append-string) | Append String |
| [STR$CASE_BLIND_COMPARE](VAX-VMS-731/rtl-str.md#strcase_blind_compare-compare-strings-without-regard-to-case) | Compare Strings Without Regard to Case |
| [STR$COMPARE](VAX-VMS-731/rtl-str.md#strcompare-compare-two-strings) | Compare Two Strings |
| [STR$COMPARE_EQL](VAX-VMS-731/rtl-str.md#strcompare_eql-compare-two-strings-for-equality) | Compare Two Strings for Equality |
| [STR$COMPARE_MULTI](VAX-VMS-731/rtl-str.md#strcompare_multi-compare-two-strings-for-equality-using-multinational-character-set) | Compare Two Strings for Equality Using Multinational Character Set |
| [STR$CONCAT](VAX-VMS-731/rtl-str.md#strconcat-concatenate-two-or-more-strings) | Concatenate Two or More Strings |
| [STR$COPY_DX](VAX-VMS-731/rtl-str.md#strcopy_dx-copy-a-source-string-passed-by-descriptor-to-a-destination-string) | Copy a Source String Passed by Descriptor to a Destination String |
| [STR$COPY_R](VAX-VMS-731/rtl-str.md#strcopy_r-copy-a-source-string-passed-by-reference-to-destination-string) | Copy a Source String Passed by Reference to Destination String |
| [STR$COPY_R_64](VAX-VMS-731/rtl-str.md#strcopy_r_64-alpha-only-copy-a-source-string-passed-by-reference-to-destination-string) | Copy a Source String Passed by Reference to Destination String |
| [STR$DIVIDE](VAX-VMS-731/rtl-str.md#strdivide-divide-two-decimal-strings) | Divide Two Decimal Strings |
| [STR$DUPL_CHAR](VAX-VMS-731/rtl-str.md#strdupl_char-duplicate-character-n-times) | Duplicate Character n Times |
| [STR$ELEMENT](VAX-VMS-731/rtl-str.md#strelement-extract-delimited-element-substring) | Extract Delimited Element Substring |
| [STR$FIND_FIRST_IN_SET](VAX-VMS-731/rtl-str.md#strfind_first_in_set-find-first-character-in-a-set-of-characters) | Find First Character in a Set of Characters |
| [STR$FIND_FIRST_NOT_IN_SET](VAX-VMS-731/rtl-str.md#strfind_first_not_in_set-find-first-character-that-does-not-occur-in-set) | Find First Character That Does Not Occur in Set |
| [STR$FIND_FIRST_SUBSTRING](VAX-VMS-731/rtl-str.md#strfind_first_substring-find-first-substring-in-input-string) | Find First Substring in Input String |
| [STR$FREE1_DX](VAX-VMS-731/rtl-str.md#strfree1_dx-free-one-dynamic-string) | Free One Dynamic String |
| [STR$GET1_DX](VAX-VMS-731/rtl-str.md#strget1_dx-allocate-one-dynamic-string) | Allocate One Dynamic String |
| [STR$GET1_DX_64](VAX-VMS-731/rtl-str.md#strget1_dx_64-alpha-only-allocate-one-dynamic-string) | Allocate One Dynamic String |
| [STR$LEFT](VAX-VMS-731/rtl-str.md#strleft-extract-a-substring-of-a-string) | Extract a Substring of a String |
| [STR$LEN_EXTR](VAX-VMS-731/rtl-str.md#strlen_extr-extract-a-substring-of-a-string) | Extract a Substring of a String |
| [STR$MATCH_WILD](VAX-VMS-731/rtl-str.md#strmatch_wild-match-wildcard-specification) | Match Wildcard Specification |
| [STR$MUL](VAX-VMS-731/rtl-str.md#strmul-multiply-two-decimal-strings) | Multiply Two Decimal Strings |
| [STR$POSITION](VAX-VMS-731/rtl-str.md#strposition-return-relative-position-of-substring) | Return Relative Position of Substring |
| [STR$POS_EXTR](VAX-VMS-731/rtl-str.md#strpos_extr-extract-a-substring-of-a-string) | Extract a Substring of a String |
| [STR$PREFIX](VAX-VMS-731/rtl-str.md#strprefix-prefix-a-string) | Prefix a String |
| [STR$RECIP](VAX-VMS-731/rtl-str.md#strrecip-reciprocal-of-a-decimal-string) | Reciprocal of a Decimal String |
| [STR$REPLACE](VAX-VMS-731/rtl-str.md#strreplace-replace-a-substring) | Replace a Substring |
| [STR$RIGHT](VAX-VMS-731/rtl-str.md#strright-extract-a-substring-of-a-string) | Extract a Substring of a String |
| [STR$ROUND](VAX-VMS-731/rtl-str.md#strround-round-or-truncate-a-decimal-string) | Round or Truncate a Decimal String |
| [STR$TRANSLATE](VAX-VMS-731/rtl-str.md#strtranslate-translate-matched-characters) | Translate Matched Characters |
| [STR$TRIM](VAX-VMS-731/rtl-str.md#strtrim-trim-trailing-blanks-and-tabs) | Trim Trailing Blanks and Tabs |
| [STR$UPCASE](VAX-VMS-731/rtl-str.md#strupcase-convert-string-to-all-uppercase-characters) | Convert String to All Uppercase Characters |

## MTH$ — Mathematics

| Routine | Description |
|---|---|
| [MTH$CCOS](VAX-VMS-731/rtl-mth.md#mthccoscosine-of-a-complex-number-f-floating-value) | Cosine of a Complex Number (F-Floating Value) |
| [MTH$CEXP](VAX-VMS-731/rtl-mth.md#mthcexpcomplex-exponential-f-floating-value) | Complex Exponential (F-Floating Value) |
| [MTH$CLOG](VAX-VMS-731/rtl-mth.md#mthclogcomplex-natural-logarithm-f-floating-value) | Complex Natural Logarithm (F-Floating Value) |
| [MTH$CMPLX](VAX-VMS-731/rtl-mth.md#mthcmplxcomplex-number-made-from-f-floating-point) | Complex Number Made from F-Floating Point |
| [MTH$CONJG](VAX-VMS-731/rtl-mth.md#mthconjgconjugate-of-a-complex-number-f-floating-value) | Conjugate of a Complex Number (F-Floating Value) |
| [MTH$CSIN](VAX-VMS-731/rtl-mth.md#mthcsinsine-of-a-complex-number-f-floating-value) | Sine of a Complex Number (F-Floating Value) |
| [MTH$CSQRT](VAX-VMS-731/rtl-mth.md#mthcsqrtcomplex-square-root-f-floating-value) | Complex Square Root (F-Floating Value) |
| [MTH$CVT_xA_xA](VAX-VMS-731/rtl-mth.md#mthcvt_xa_xaconvert-an-array-of-double-precision-values) | Convert an Array of Double-Precision Values |
| [MTH$CVT_x_x](VAX-VMS-731/rtl-mth.md#mthcvt_x_xconvert-one-double-precision-value) | Convert One Double-Precision Value |
| [MTH$CxABS](VAX-VMS-731/rtl-mth.md#mthcxabscomplex-absolute-value) | Complex Absolute Value |
| [MTH$CxCOS](VAX-VMS-731/rtl-mth.md#mthcxcoscosine-of-a-complex-number) | Cosine of a Complex Number |
| [MTH$CxEXP](VAX-VMS-731/rtl-mth.md#mthcxexpcomplex-exponential) | Complex Exponential |
| [MTH$CxLOG](VAX-VMS-731/rtl-mth.md#mthcxlogcomplex-natural-logarithm) | Complex Natural Logarithm |
| [MTH$CxSIN](VAX-VMS-731/rtl-mth.md#mthcxsinsine-of-a-complex-number) | Sine of a Complex Number |
| [MTH$CxSQRT](VAX-VMS-731/rtl-mth.md#mthcxsqrtcomplex-square-root) | Complex Square Root |
| [MTH$HACOS](VAX-VMS-731/rtl-mth.md#mthhacosarc-cosine-of-angle-expressed-in-radians-h-floating-value) | Arc Cosine of Angle Expressed in Radians** **(H-Floating Value) |
| [MTH$HACOSD](VAX-VMS-731/rtl-mth.md#mthhacosdarc-cosine-of-angle-expressed-in-degrees-h-floating-value) | Arc Cosine of Angle Expressed in Degrees** **(H-Floating Value) |
| [MTH$HASIN](VAX-VMS-731/rtl-mth.md#mthhasinarc-sine-in-radians-h-floating-value) | Arc Sine in Radians (H-Floating Value) |
| [MTH$HASIND](VAX-VMS-731/rtl-mth.md#mthhasindarc-sine-in-degrees-h-floating-value) | Arc Sine in Degrees (H-Floating Value) |
| [MTH$HATAN](VAX-VMS-731/rtl-mth.md#mthhatanarc-tangent-in-radians-h-floating-value) | Arc Tangent in Radians (H-Floating Value) |
| [MTH$HATAN2](VAX-VMS-731/rtl-mth.md#mthhatan2arc-tangent-in-radians-h-floating-value-with-two-arguments) | Arc Tangent in Radians (H-Floating Value) with Two** **Arguments |
| [MTH$HATAND](VAX-VMS-731/rtl-mth.md#mthhatandarc-tangent-in-degrees-h-floating-value) | Arc Tangent in Degrees (H-Floating Value) |
| [MTH$HATAND2](VAX-VMS-731/rtl-mth.md#mthhatand2arc-tangent-in-degrees-h-floating-value-with-two-arguments) | Arc Tangent in Degrees (H-Floating Value) with Two** **Arguments |
| [MTH$HATANH](VAX-VMS-731/rtl-mth.md#mthhatanhhyperbolic-arc-tangent-h-floating-value) | Hyperbolic Arc Tangent (H-Floating Value) |
| [MTH$HCOS](VAX-VMS-731/rtl-mth.md#mthhcoscosine-of-angle-expressed-in-radians-h-floating-value) | Cosine of Angle Expressed in Radians (H-Floating** **Value) |
| [MTH$HCOSD](VAX-VMS-731/rtl-mth.md#mthhcosdcosine-of-angle-expressed-in-degrees-h-floating-value) | Cosine of Angle Expressed in Degrees (H-Floating** **Value) |
| [MTH$HCOSH](VAX-VMS-731/rtl-mth.md#mthhcoshhyperbolic-cosine-h-floating-value) | Hyperbolic Cosine (H-Floating Value) |
| [MTH$HEXP](VAX-VMS-731/rtl-mth.md#mthhexpexponential-h-floating-value) | Exponential (H-Floating Value) |
| [MTH$HLOG](VAX-VMS-731/rtl-mth.md#mthhlognatural-logarithm-h-floating-value) | Natural Logarithm (H-Floating Value) |
| [MTH$HLOG10](VAX-VMS-731/rtl-mth.md#mthhlog10common-logarithm-h-floating-value) | Common Logarithm (H-Floating Value) |
| [MTH$HLOG2](VAX-VMS-731/rtl-mth.md#mthhlog2base-2-logarithm-h-floating-value) | Base 2 Logarithm (H-Floating Value) |
| [MTH$HSIN](VAX-VMS-731/rtl-mth.md#mthhsinsine-of-angle-expressed-in-radians-h-floating-value) | Sine of Angle Expressed in Radians (H-Floating Value) |
| [MTH$HSIND](VAX-VMS-731/rtl-mth.md#mthhsindsine-of-angle-expressed-in-degrees-h-floating-value) | Sine of Angle Expressed in Degrees (H-Floating Value) |
| [MTH$HSINH](VAX-VMS-731/rtl-mth.md#mthhsinhhyperbolic-sine-h-floating-value) | Hyperbolic Sine (H-Floating Value) |
| [MTH$HSQRT](VAX-VMS-731/rtl-mth.md#mthhsqrtsquare-root-h-floating-value) | Square Root (H-Floating Value) |
| [MTH$HTAN](VAX-VMS-731/rtl-mth.md#mthhtantangent-of-angle-expressed-in-radians-h-floating-value) | Tangent of Angle Expressed in Radians (H-Floating** **Value) |
| [MTH$HTAND](VAX-VMS-731/rtl-mth.md#mthhtandtangent-of-angle-expressed-in-degrees-h-floating-value) | Tangent of Angle Expressed in Degrees (H-Floating** **Value) |
| [MTH$HTANH](VAX-VMS-731/rtl-mth.md#mthhtanhcompute-the-hyperbolic-tangent-h-floating-value) | Compute the Hyperbolic Tangent (H-Floating Value) |
| [MTH$RANDOM](VAX-VMS-731/rtl-mth.md#mthrandomrandom-number-generator-uniformly-distributed) | Random Number Generator, Uniformly Distributed |
| [MTH$UMAX](VAX-VMS-731/rtl-mth.md#mthumaxcompute-unsigned-maximum) | Compute Unsigned Maximum |
| [MTH$UMIN](VAX-VMS-731/rtl-mth.md#mthumincompute-unsigned-minimum) | Compute Unsigned Minimum |
| [MTH$VxFOLRLy_MA_V5](VAX-VMS-731/rtl-mth.md#mthvxfolrly_ma_v5first-order-linear-recurrence-multiplication-and-addition-last-value) | First Order Linear Recurrence —** **Multiplication and Addition — Last Value |
| [MTH$VxFOLRLy_z_V2](VAX-VMS-731/rtl-mth.md#mthvxfolrly_z_v2first-order-linear-recurrence-multiplication-or-addition-last-value) | First Order Linear Recurrence —** **Multiplication or Addition — Last Value |
| [MTH$VxFOLRy_MA_V15](VAX-VMS-731/rtl-mth.md#mthvxfolry_ma_v15first-order-linear-recurrence-multiplication-and-addition) | First Order Linear Recurrence —** **Multiplication and Addition |
| [MTH$VxFOLRy_z_V8](VAX-VMS-731/rtl-mth.md#mthvxfolry_z_v8first-order-linear-recurrence-multiplication-or-addition) | First Order Linear Recurrence —** **Multiplication or Addition |
| [MTH$xACOS](VAX-VMS-731/rtl-mth.md#mthxacosarc-cosine-of-angle-expressed-in-radians) | Arc Cosine of Angle Expressed in Radians |
| [MTH$xACOSD](VAX-VMS-731/rtl-mth.md#mthxacosdarc-cosine-of-angle-expressed-in-degrees) | Arc Cosine of Angle Expressed in Degrees |
| [MTH$xASIN](VAX-VMS-731/rtl-mth.md#mthxasinarc-sine-in-radians) | Arc Sine in Radians |
| [MTH$xASIND](VAX-VMS-731/rtl-mth.md#mthxasindarc-sine-in-degrees) | Arc Sine in Degrees |
| [MTH$xATAN](VAX-VMS-731/rtl-mth.md#mthxatanarc-tangent-in-radians) | Arc Tangent in Radians |
| [MTH$xATAN2](VAX-VMS-731/rtl-mth.md#mthxatan2arc-tangent-in-radians-with-two-arguments) | Arc Tangent in Radians with Two Arguments |
| [MTH$xATAND](VAX-VMS-731/rtl-mth.md#mthxatandarc-tangent-in-degrees) | Arc Tangent in Degrees |
| [MTH$xATAND2](VAX-VMS-731/rtl-mth.md#mthxatand2arc-tangent-in-degrees-with-two-arguments) | Arc Tangent in Degrees with Two Arguments |
| [MTH$xATANH](VAX-VMS-731/rtl-mth.md#mthxatanhhyperbolic-arc-tangent) | Hyperbolic Arc Tangent |
| [MTH$xCMPLX](VAX-VMS-731/rtl-mth.md#mthxcmplxcomplex-number-made-from-d-or-g-floating-point) | Complex Number Made from D- or** **G-Floating Point |
| [MTH$xCONJG](VAX-VMS-731/rtl-mth.md#mthxconjgconjugate-of-a-complex-number) | Conjugate of a Complex Number |
| [MTH$xCOS](VAX-VMS-731/rtl-mth.md#mthxcoscosine-of-angle-expressed-in-radians) | Cosine of Angle Expressed in Radians |
| [MTH$xCOSD](VAX-VMS-731/rtl-mth.md#mthxcosdcosine-of-angle-expressed-in-degrees) | Cosine of Angle Expressed in Degrees |
| [MTH$xCOSH](VAX-VMS-731/rtl-mth.md#mthxcoshhyperbolic-cosine) | Hyperbolic Cosine |
| [MTH$xEXP](VAX-VMS-731/rtl-mth.md#mthxexpexponential) | Exponential |
| [MTH$xIMAG](VAX-VMS-731/rtl-mth.md#mthximagimaginary-part-of-a-complex-number) | Imaginary Part of a Complex Number |
| [MTH$xLOG](VAX-VMS-731/rtl-mth.md#mthxlognatural-logarithm) | Natural Logarithm |
| [MTH$xLOG10](VAX-VMS-731/rtl-mth.md#mthxlog10common-logarithm) | Common Logarithm |
| [MTH$xLOG2](VAX-VMS-731/rtl-mth.md#mthxlog2base-2-logarithm) | Base 2 Logarithm |
| [MTH$xREAL](VAX-VMS-731/rtl-mth.md#mthxrealreal-part-of-a-complex-number) | Real Part of a Complex Number |
| [MTH$xSIN](VAX-VMS-731/rtl-mth.md#mthxsinsine-of-angle-expressed-in-radians) | Sine of Angle Expressed in Radians |
| [MTH$xSINCOS](VAX-VMS-731/rtl-mth.md#mthxsincossine-and-cosine-of-angle-expressed-in-radians) | Sine and Cosine of Angle Expressed in Radians |
| [MTH$xSINCOSD](VAX-VMS-731/rtl-mth.md#mthxsincosdsine-and-cosine-of-angle-expressed-in-degrees) | Sine and Cosine of Angle Expressed in Degrees |
| [MTH$xSIND](VAX-VMS-731/rtl-mth.md#mthxsindsine-of-angle-expressed-in-degrees) | Sine of Angle Expressed in Degrees |
| [MTH$xSINH](VAX-VMS-731/rtl-mth.md#mthxsinhhyperbolic-sine) | Hyperbolic Sine |
| [MTH$xSQRT](VAX-VMS-731/rtl-mth.md#mthxsqrtsquare-root) | Square Root |
| [MTH$xTAN](VAX-VMS-731/rtl-mth.md#mthxtantangent-of-angle-expressed-in-radians) | Tangent of Angle Expressed in Radians |
| [MTH$xTAND](VAX-VMS-731/rtl-mth.md#mthxtandtangent-of-angle-expressed-in-degrees) | Tangent of Angle Expressed in Degrees |
| [MTH$xTANH](VAX-VMS-731/rtl-mth.md#mthxtanhcompute-the-hyperbolic-tangent) | Compute the Hyperbolic Tangent |

## OTS$ — General Purpose / Language Support

| Routine | Description |
|---|---|
| [OTS$CNVOUT](VAX-VMS-731/rtl-ots.md#otscnvout-convert-d-floating-g-floating-or-h-floating-number-to-character-string) | Convert D-Floating, G-Floating or H-Floating Number to Character** **String |
| [OTS$CVT_L_TB](VAX-VMS-731/rtl-ots.md#otscvt_l_tb-convert-an-unsigned-integer-to-binary-text) | Convert an Unsigned Integer to Binary Text |
| [OTS$CVT_L_TI](VAX-VMS-731/rtl-ots.md#otscvt_l_ti-convert-signed-integer-to-decimal-text) | Convert Signed Integer to Decimal Text |
| [OTS$CVT_L_TL](VAX-VMS-731/rtl-ots.md#otscvt_l_tl-convert-integer-to-logical-text) | Convert Integer to Logical Text |
| [OTS$CVT_L_TO](VAX-VMS-731/rtl-ots.md#otscvt_l_to-convert-unsigned-integer-to-octal-text) | Convert Unsigned Integer to Octal Text |
| [OTS$CVT_L_TU](VAX-VMS-731/rtl-ots.md#otscvt_l_tu-convert-unsigned-integer-to-decimal-text) | Convert Unsigned Integer to Decimal Text |
| [OTS$CVT_L_TZ](VAX-VMS-731/rtl-ots.md#otscvt_l_tz-convert-integer-to-hexadecimal-text) | Convert Integer to Hexadecimal Text |
| [OTS$CVT_TB_L](VAX-VMS-731/rtl-ots.md#otscvt_tb_l-convert-binary-text-to-unsigned-integer) | Convert Binary Text to Unsigned Integer |
| [OTS$CVT_TI_L](VAX-VMS-731/rtl-ots.md#otscvt_ti_l-convert-signed-integer-text-to-integer) | Convert Signed Integer Text to Integer |
| [OTS$CVT_TL_L](VAX-VMS-731/rtl-ots.md#otscvt_tl_l-convert-logical-text-to-integer) | Convert Logical Text to Integer |
| [OTS$CVT_TO_L](VAX-VMS-731/rtl-ots.md#otscvt_to_l-convert-octal-text-to-unsigned-integer) | Convert Octal Text to Unsigned Integer |
| [OTS$CVT_TU_L](VAX-VMS-731/rtl-ots.md#otscvt_tu_l-convert-unsigned-decimal-text-to-integer) | Convert Unsigned Decimal Text to Integer |
| [OTS$CVT_TZ_L](VAX-VMS-731/rtl-ots.md#otscvt_tz_l-convert-hexadecimal-text-to-unsigned-integer) | Convert Hexadecimal Text to Unsigned Integer |
| [OTS$CVT_T_x](VAX-VMS-731/rtl-ots.md#otscvt_t_x-convert-numeric-text-to-d-f-g-or-h-floating-value) | Convert Numeric Text to D-, F-, G-, or H-Floating Value |
| [OTS$DIVCx](VAX-VMS-731/rtl-ots.md#otsdivcx-complex-division) | Complex Division |
| [OTS$DIV_PK_LONG](VAX-VMS-731/rtl-ots.md#otsdiv_pk_long-packed-decimal-division-with-long-divisor) | Packed Decimal Division with Long Divisor |
| [OTS$DIV_PK_SHORT](VAX-VMS-731/rtl-ots.md#otsdiv_pk_short-packed-decimal-division-with-short-divisor) | Packed Decimal Division with Short Divisor |
| [OTS$MOVE3](VAX-VMS-731/rtl-ots.md#otsmove3-move-data-without-fill) | Move Data Without Fill |
| [OTS$MOVE5](VAX-VMS-731/rtl-ots.md#otsmove5-move-data-with-fill) | Move Data with Fill |
| [OTS$MULCx](VAX-VMS-731/rtl-ots.md#otsmulcx-complex-multiplication) | Complex Multiplication |
| [OTS$POWCxCx](VAX-VMS-731/rtl-ots.md#otspowcxcx-raise-a-complex-base-to-a-complex-floating-point-exponent) | Raise a Complex Base to a Complex Floating-Point Exponent |
| [OTS$POWCxJ](VAX-VMS-731/rtl-ots.md#otspowcxj-raise-a-complex-base-to-a-signed-longword-integer-exponent) | Raise a Complex Base to a Signed Longword Integer Exponent |
| [OTS$POWDD](VAX-VMS-731/rtl-ots.md#otspowdd-raise-a-d-floating-base-to-a-d-floating-exponent) | Raise a D-Floating Base to a D-Floating Exponent |
| [OTS$POWDJ](VAX-VMS-731/rtl-ots.md#otspowdj-raise-a-d-floating-base-to-a-longword-exponent) | Raise a D-Floating Base to a Longword Exponent |
| [OTS$POWDR](VAX-VMS-731/rtl-ots.md#otspowdr-raise-a-d-floating-base-to-an-f-floating-exponent) | Raise a D-Floating Base to an F-Floating Exponent |
| [OTS$POWGG](VAX-VMS-731/rtl-ots.md#otspowgg-raise-a-g-floating-base-to-a-g-floating-exponent) | Raise a G-Floating Base to a G-Floating Exponent |
| [OTS$POWGJ](VAX-VMS-731/rtl-ots.md#otspowgj-raise-a-g-floating-base-to-a-longword-exponent) | Raise a G-Floating Base to a Longword Exponent |
| [OTS$POWHH_R3](VAX-VMS-731/rtl-ots.md#otspowhh_r3-vax-only-raise-an-h-floating-base-to-an-h-floating-exponent) | Raise an H-Floating Base to an H-Floating Exponent |
| [OTS$POWHJ_R3](VAX-VMS-731/rtl-ots.md#otspowhj_r3-vax-only-raise-an-h-floating-base-to-a-longword-exponent) | Raise an H-Floating Base to a Longword Exponent |
| [OTS$POWII](VAX-VMS-731/rtl-ots.md#otspowii-raise-a-word-base-to-a-word-exponent) | Raise a Word Base to a Word Exponent |
| [OTS$POWJJ](VAX-VMS-731/rtl-ots.md#otspowjj-raise-a-longword-base-to-a-longword-exponent) | Raise a Longword Base to a Longword Exponent |
| [OTS$POWLULU](VAX-VMS-731/rtl-ots.md#otspowlulu-raise-an-unsigned-longword-base-to-an-unsigned-longword-exponent) | Raise an Unsigned Longword Base to an Unsigned Longword** **Exponent |
| [OTS$POWRD](VAX-VMS-731/rtl-ots.md#otspowrd-raise-an-f-floating-base-to-a-d-floating-exponent) | Raise an F-Floating Base to a D-Floating Exponent |
| [OTS$POWRJ](VAX-VMS-731/rtl-ots.md#otspowrj-raise-an-f-floating-base-to-a-longword-exponent) | Raise an F-Floating Base to a Longword Exponent |
| [OTS$POWRR](VAX-VMS-731/rtl-ots.md#otspowrr-raise-an-f-floating-base-to-an-f-floating-exponent) | Raise an F-Floating Base to an F-Floating Exponent |
| [OTS$POWxLU](VAX-VMS-731/rtl-ots.md#otspowxlu-raise-a-floating-point-base-to-an-unsigned-longword-integer-exponent) | Raise a Floating-Point Base to an Unsigned Longword Integer** **Exponent |
| [OTS$SCOPY_DXDX](VAX-VMS-731/rtl-ots.md#otsscopy_dxdx-copy-a-source-string-passed-by-descriptor-to-a-destination-string) | Copy a Source String Passed by Descriptor to a Destination String |
| [OTS$SCOPY_R_DX](VAX-VMS-731/rtl-ots.md#otsscopy_r_dx-copy-a-source-string-passed-by-reference-to-a-destination-string) | Copy a Source String Passed by Reference to a Destination String |
| [OTS$SFREE1_DD](VAX-VMS-731/rtl-ots.md#otssfree1_dd-strings-free-one-dynamic) | Strings, Free One Dynamic |
| [OTS$SFREEN_DD](VAX-VMS-731/rtl-ots.md#otssfreen_dd-strings-free-n-dynamic) | Strings, Free n Dynamic |
| [OTS$SGET1_DD](VAX-VMS-731/rtl-ots.md#otssget1_dd-strings-get-one-dynamic) | Strings, Get One Dynamic |

## SMG$ — Screen Management

| Routine | Description |
|---|---|
| [SMG$ADD_KEY_DEF](VAX-VMS-731/rtl-smg.md#smgadd_key_def-add-key-definition) | Add Key Definition |
| [SMG$BEGIN_DISPLAY_UPDATE](VAX-VMS-731/rtl-smg.md#smgbegin_display_update-begin-batching-of-display-updates) | Begin Batching of Display Updates |
| [SMG$BEGIN_PASTEBOARD_UPDATE](VAX-VMS-731/rtl-smg.md#smgbegin_pasteboard_update-begin-batching-of-pasteboard-updates) | Begin Batching of Pasteboard Updates |
| [SMG$CANCEL_INPUT](VAX-VMS-731/rtl-smg.md#smgcancel_input-cancel-input-request) | Cancel Input Request |
| [SMG$CHANGE_PBD_CHARACTERISTICS](VAX-VMS-731/rtl-smg.md#smgchange_pbd_characteristics-change-pasteboard-characteristics) | Change Pasteboard Characteristics |
| [SMG$CHANGE_RENDITION](VAX-VMS-731/rtl-smg.md#smgchange_rendition-change-default-rendition) | Change Default Rendition |
| [SMG$CHANGE_VIEWPORT](VAX-VMS-731/rtl-smg.md#smgchange_viewport-change-the-viewport-associated-with-a-virtual-display) | Change the Viewport Associated with a Virtual Display |
| [SMG$CHANGE_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgchange_virtual_display-change-virtual-display) | Change Virtual Display |
| [SMG$CHECK_FOR_OCCLUSION](VAX-VMS-731/rtl-smg.md#smgcheck_for_occlusion-check-for-occlusion) | Check for Occlusion |
| [SMG$CONTROL_MODE](VAX-VMS-731/rtl-smg.md#smgcontrol_mode-control-mode) | Control Mode |
| [SMG$COPY_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgcopy_virtual_display-copy-a-virtual-display) | Copy a Virtual Display |
| [SMG$CREATE_KEY_TABLE](VAX-VMS-731/rtl-smg.md#smgcreate_key_table-create-key-table) | Create Key Table |
| [SMG$CREATE_MENU](VAX-VMS-731/rtl-smg.md#smgcreate_menu-fill-the-virtual-display-with-a-menu) | Fill the Virtual Display with a Menu |
| [SMG$CREATE_PASTEBOARD](VAX-VMS-731/rtl-smg.md#smgcreate_pasteboard-create-a-pasteboard) | Create a Pasteboard |
| [SMG$CREATE_SUBPROCESS](VAX-VMS-731/rtl-smg.md#smgcreate_subprocess-create-and-initialize-a-subprocess) | Create and Initialize a Subprocess |
| [SMG$CREATE_VIEWPORT](VAX-VMS-731/rtl-smg.md#smgcreate_viewport-create-a-virtual-viewport) | Create a Virtual Viewport |
| [SMG$CREATE_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgcreate_virtual_display-create-a-virtual-display) | Create a Virtual Display |
| [SMG$CREATE_VIRTUAL_KEYBOARD](VAX-VMS-731/rtl-smg.md#smgcreate_virtual_keyboard-create-a-virtual-keyboard) | Create a Virtual Keyboard |
| [SMG$CURSOR_COLUMN](VAX-VMS-731/rtl-smg.md#smgcursor_column-return-cursor-column-position) | Return Cursor Column Position |
| [SMG$CURSOR_ROW](VAX-VMS-731/rtl-smg.md#smgcursor_row-return-cursor-row-position) | Return Cursor Row Position |
| [SMG$DEFINE_KEY](VAX-VMS-731/rtl-smg.md#smgdefine_key-perform-a-definekey-command) | Perform a DEFINE/KEY Command |
| [SMG$DELETE_CHARS](VAX-VMS-731/rtl-smg.md#smgdelete_chars-delete-characters) | Delete Characters |
| [SMG$DELETE_KEY_DEF](VAX-VMS-731/rtl-smg.md#smgdelete_key_def-delete-key-definition) | Delete Key Definition |
| [SMG$DELETE_LINE](VAX-VMS-731/rtl-smg.md#smgdelete_line-delete-line) | Delete Line |
| [SMG$DELETE_MENU](VAX-VMS-731/rtl-smg.md#smgdelete_menu-end-access-to-a-menu-in-the-virtual-display) | End Access to a Menu in the Virtual Display |
| [SMG$DELETE_PASTEBOARD](VAX-VMS-731/rtl-smg.md#smgdelete_pasteboard-delete-pasteboard) | Delete Pasteboard |
| [SMG$DELETE_SUBPROCESS](VAX-VMS-731/rtl-smg.md#smgdelete_subprocess-terminate-a-subprocess) | Terminate a Subprocess |
| [SMG$DELETE_VIEWPORT](VAX-VMS-731/rtl-smg.md#smgdelete_viewport-delete-a-viewport) | Delete a Viewport |
| [SMG$DELETE_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgdelete_virtual_display-delete-virtual-display) | Delete Virtual Display |
| [SMG$DELETE_VIRTUAL_KEYBOARD](VAX-VMS-731/rtl-smg.md#smgdelete_virtual_keyboard-delete-virtual-keyboard) | Delete Virtual Keyboard |
| [SMG$DEL_TERM_TABLE](VAX-VMS-731/rtl-smg.md#smgdel_term_table-delete-terminal-table) | Delete Terminal Table |
| [SMG$DISABLE_BROADCAST_TRAPPING](VAX-VMS-731/rtl-smg.md#smgdisable_broadcast_trapping-disable-broadcast-trapping) | Disable Broadcast Trapping |
| [SMG$DISABLE_UNSOLICITED_INPUT](VAX-VMS-731/rtl-smg.md#smgdisable_unsolicited_input-disable-unsolicited-input) | Disable Unsolicited Input |
| [SMG$DRAW_CHAR](VAX-VMS-731/rtl-smg.md#smgdraw_char-draw-a-character-in-a-virtual-display) | Draw a Character in a Virtual Display |
| [SMG$DRAW_LINE](VAX-VMS-731/rtl-smg.md#smgdraw_line-draw-a-line) | Draw a Line |
| [SMG$DRAW_RECTANGLE](VAX-VMS-731/rtl-smg.md#smgdraw_rectangle-draw-a-rectangle) | Draw a Rectangle |
| [SMG$ENABLE_UNSOLICITED_INPUT](VAX-VMS-731/rtl-smg.md#smgenable_unsolicited_input-enable-unsolicited-input) | Enable Unsolicited Input |
| [SMG$END_DISPLAY_UPDATE](VAX-VMS-731/rtl-smg.md#smgend_display_update-end-display-update) | End Display Update |
| [SMG$END_PASTEBOARD_UPDATE](VAX-VMS-731/rtl-smg.md#smgend_pasteboard_update-end-pasteboard-update) | End Pasteboard Update |
| [SMG$ERASE_CHARS](VAX-VMS-731/rtl-smg.md#smgerase_chars-erase-characters) | Erase Characters |
| [SMG$ERASE_COLUMN](VAX-VMS-731/rtl-smg.md#smgerase_column-erase-column-from-display) | Erase Column from Display |
| [SMG$ERASE_DISPLAY](VAX-VMS-731/rtl-smg.md#smgerase_display-erase-virtual-display) | Erase Virtual Display |
| [SMG$ERASE_LINE](VAX-VMS-731/rtl-smg.md#smgerase_line-erase-line) | Erase Line |
| [SMG$ERASE_PASTEBOARD](VAX-VMS-731/rtl-smg.md#smgerase_pasteboard-erase-pasteboard) | Erase Pasteboard |
| [SMG$EXECUTE_COMMAND](VAX-VMS-731/rtl-smg.md#smgexecute_command-execute-command-in-a-subprocess) | Execute Command in a Subprocess |
| [SMG$FIND_CURSOR_DISPLAY](VAX-VMS-731/rtl-smg.md#smgfind_cursor_display-find-display-that-contains-the-cursor) | Find Display that Contains the Cursor |
| [SMG$FLUSH_BUFFER](VAX-VMS-731/rtl-smg.md#smgflush_buffer-flush-buffer) | Flush Buffer |
| [SMG$FLUSH_DISPLAY_UPDATE](VAX-VMS-731/rtl-smg.md#smgflush_display_update-flush-display-update) | Flush Display Update |
| [SMG$GET_BROADCAST_MESSAGE](VAX-VMS-731/rtl-smg.md#smgget_broadcast_message-get-broadcast-message) | Get Broadcast Message |
| [SMG$GET_CHAR_AT_PHYSICAL_CURSOR](VAX-VMS-731/rtl-smg.md#smgget_char_at_physical_cursor-return-character-at-cursor) | Return Character at Cursor |
| [SMG$GET_DISPLAY_ATTR](VAX-VMS-731/rtl-smg.md#smgget_display_attr-get-display-attributes) | Get Display Attributes |
| [SMG$GET_KEYBOARD_ATTRIBUTES](VAX-VMS-731/rtl-smg.md#smgget_keyboard_attributes-get-keyboard-attributes) | Get Keyboard Attributes |
| [SMG$GET_KEY_DEF](VAX-VMS-731/rtl-smg.md#smgget_key_def-get-key-definition) | Get Key Definition |
| [SMG$GET_NUMERIC_DATA](VAX-VMS-731/rtl-smg.md#smgget_numeric_data-get-numeric-terminal-data) | Get Numeric Terminal Data |
| [SMG$GET_PASTEBOARD_ATTRIBUTES](VAX-VMS-731/rtl-smg.md#smgget_pasteboard_attributes-get-pasteboard-attributes) | Get Pasteboard Attributes |
| [SMG$GET_PASTING_INFO](VAX-VMS-731/rtl-smg.md#smgget_pasting_info-return-pasting-information) | Return Pasting Information |
| [SMG$GET_TERM_DATA](VAX-VMS-731/rtl-smg.md#smgget_term_data-get-terminal-data) | Get Terminal Data |
| [SMG$GET_VIEWPORT_CHAR](VAX-VMS-731/rtl-smg.md#smgget_viewport_char-get-characteristics-of-display-viewport) | Get Characteristics of Display Viewport |
| [SMG$HOME_CURSOR](VAX-VMS-731/rtl-smg.md#smghome_cursor-home-cursor) | Home Cursor |
| [SMG$INIT_TERM_TABLE](VAX-VMS-731/rtl-smg.md#smginit_term_table-initialize-terminal-table) | Initialize Terminal Table |
| [SMG$INIT_TERM_TABLE_BY_TYPE](VAX-VMS-731/rtl-smg.md#smginit_term_table_by_type-initialize-termtable-by-openvms-terminal-type) | Initialize TERMTABLE by OpenVMS Terminal Type |
| [SMG$INSERT_CHARS](VAX-VMS-731/rtl-smg.md#smginsert_chars-insert-characters) | Insert Characters |
| [SMG$INSERT_LINE](VAX-VMS-731/rtl-smg.md#smginsert_line-insert-line) | Insert Line |
| [SMG$INVALIDATE_DISPLAY](VAX-VMS-731/rtl-smg.md#smginvalidate_display-mark-a-display-as-invalid) | Mark a Display as Invalid |
| [SMG$KEYCODE_TO_NAME](VAX-VMS-731/rtl-smg.md#smgkeycode_to_name-translate-a-key-code-into-a-key-name) | Translate a Key Code into a Key Name |
| [SMG$LABEL_BORDER](VAX-VMS-731/rtl-smg.md#smglabel_border-label-a-virtual-display-border) | Label a Virtual Display Border |
| [SMG$LIST_KEY_DEFS](VAX-VMS-731/rtl-smg.md#smglist_key_defs-list-key-definitions) | List Key Definitions |
| [SMG$LIST_PASTEBOARD_ORDER](VAX-VMS-731/rtl-smg.md#smglist_pasteboard_order-return-pasting-information) | Return Pasting Information |
| [SMG$LIST_PASTING_ORDER](VAX-VMS-731/rtl-smg.md#smglist_pasting_order-return-virtual-display-pasting-information) | Return Virtual Display Pasting Information |
| [SMG$LOAD_KEY_DEFS](VAX-VMS-731/rtl-smg.md#smgload_key_defs-load-key-definitions) | Load Key Definitions |
| [SMG$LOAD_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgload_virtual_display-load-a-virtual-display-from-a-file) | Load a Virtual Display from a File |
| [SMG$MOVE_TEXT](VAX-VMS-731/rtl-smg.md#smgmove_text-move-text-from-one-virtual-display-to-another) | Move Text from One Virtual Display to Another |
| [SMG$MOVE_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgmove_virtual_display-move-virtual-display) | Move Virtual Display |
| [SMG$NAME_TO_KEYCODE](VAX-VMS-731/rtl-smg.md#smgname_to_keycode-translate-a-key-name-into-a-key-code) | Translate a Key Name into a Key Code |
| [SMG$PASTE_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgpaste_virtual_display-paste-virtual-display) | Paste Virtual Display |
| [SMG$POP_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgpop_virtual_display-delete-a-series-of-virtual-displays) | Delete a Series of Virtual Displays |
| [SMG$PRINT_PASTEBOARD](VAX-VMS-731/rtl-smg.md#smgprint_pasteboard-print-pasteboard-using-a-print-queue) | Print Pasteboard Using a Print Queue |
| [SMG$PUT_CHARS](VAX-VMS-731/rtl-smg.md#smgput_chars-write-characters-to-a-virtual-display) | Write Characters to a Virtual Display |
| [SMG$PUT_CHARS_HIGHWIDE](VAX-VMS-731/rtl-smg.md#smgput_chars_highwide-write-double-height-double-width-characters) | Write Double-Height Double-Width Characters |
| [SMG$PUT_CHARS_MULTI](VAX-VMS-731/rtl-smg.md#smgput_chars_multi-put-text-with-multiple-renditions-to-display) | Put Text with Multiple Renditions to Display |
| [SMG$PUT_CHARS_WIDE](VAX-VMS-731/rtl-smg.md#smgput_chars_wide-write-double-width-characters) | Write Double-Width Characters |
| [SMG$PUT_HELP_TEXT](VAX-VMS-731/rtl-smg.md#smgput_help_text-output-help-text-to-the-display) | Output Help Text to the Display |
| [SMG$PUT_LINE](VAX-VMS-731/rtl-smg.md#smgput_line-write-line-to-virtual-display) | Write Line to Virtual Display |
| [SMG$PUT_LINE_HIGHWIDE](VAX-VMS-731/rtl-smg.md#smgput_line_highwide-write-double-height-and-double-width-line) | Write Double-Height and Double-Width Line |
| [SMG$PUT_LINE_MULTI](VAX-VMS-731/rtl-smg.md#smgput_line_multi-write-line-with-multiple-renditions-to-display) | Write Line with Multiple Renditions to Display |
| [SMG$PUT_LINE_WIDE](VAX-VMS-731/rtl-smg.md#smgput_line_wide-write-double-width-line) | Write Double-Width Line |
| [SMG$PUT_PASTEBOARD](VAX-VMS-731/rtl-smg.md#smgput_pasteboard-output-pasteboard-using-routine) | Output Pasteboard Using Routine |
| [SMG$PUT_STATUS_LINE](VAX-VMS-731/rtl-smg.md#smgput_status_line-output-line-of-text-to-hardware-status-line) | Output Line of Text to Hardware Status Line |
| [SMG$READ_COMPOSED_LINE](VAX-VMS-731/rtl-smg.md#smgread_composed_line-read-composed-line) | Read Composed Line |
| [SMG$READ_FROM_DISPLAY](VAX-VMS-731/rtl-smg.md#smgread_from_display-read-text-from-display) | Read Text from Display |
| [SMG$READ_KEYSTROKE](VAX-VMS-731/rtl-smg.md#smgread_keystroke-read-a-single-character) | Read a Single Character |
| [SMG$READ_LOCATOR](VAX-VMS-731/rtl-smg.md#smgread_locator-read-locator-information) | Read Locator Information |
| [SMG$READ_STRING](VAX-VMS-731/rtl-smg.md#smgread_string-read-string) | Read String |
| [SMG$READ_VERIFY](VAX-VMS-731/rtl-smg.md#smgread_verify-read-and-verify-a-string) | Read and Verify a String |
| [SMG$REMOVE_LINE](VAX-VMS-731/rtl-smg.md#smgremove_line-remove-a-line-from-a-virtual-display) | Remove a Line from a Virtual Display |
| [SMG$REPAINT_LINE](VAX-VMS-731/rtl-smg.md#smgrepaint_line-repaint-one-or-more-lines-on-the-current-pasteboard) | Repaint One or More Lines on the Current Pasteboard |
| [SMG$REPAINT_SCREEN](VAX-VMS-731/rtl-smg.md#smgrepaint_screen-repaint-current-pasteboard) | Repaint Current Pasteboard |
| [SMG$REPASTE_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgrepaste_virtual_display-repaste-virtual-display) | Repaste Virtual Display |
| [SMG$REPLACE_INPUT_LINE](VAX-VMS-731/rtl-smg.md#smgreplace_input_line-replace-input-line) | Replace Input Line |
| [SMG$RESTORE_PHYSICAL_SCREEN](VAX-VMS-731/rtl-smg.md#smgrestore_physical_screen-restore-physical-pasteboard) | Restore Physical Pasteboard |
| [SMG$RETURN_CURSOR_POS](VAX-VMS-731/rtl-smg.md#smgreturn_cursor_pos-return-cursor-position) | Return Cursor Position |
| [SMG$RETURN_INPUT_LINE](VAX-VMS-731/rtl-smg.md#smgreturn_input_line-return-input-line) | Return Input Line |
| [SMG$RING_BELL](VAX-VMS-731/rtl-smg.md#smgring_bell-ring-the-terminal-bell-or-buzzer) | Ring the Terminal Bell or Buzzer |
| [SMG$SAVE_PHYSICAL_SCREEN](VAX-VMS-731/rtl-smg.md#smgsave_physical_screen-save-physical-screen) | Save Physical Screen |
| [SMG$SAVE_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgsave_virtual_display-save-the-virtual-display-to-a-file) | Save the Virtual Display to a File |
| [SMG$SCROLL_DISPLAY_AREA](VAX-VMS-731/rtl-smg.md#smgscroll_display_area-scroll-display-area) | Scroll Display Area |
| [SMG$SCROLL_VIEWPORT](VAX-VMS-731/rtl-smg.md#smgscroll_viewport-scroll-a-display-under-a-viewport) | Scroll a Display Under a Viewport |
| [SMG$SELECT_FROM_MENU](VAX-VMS-731/rtl-smg.md#smgselect_from_menu-make-a-selection-from-the-menu) | Make a Selection from the Menu |
| [SMG$SET_BROADCAST_TRAPPING](VAX-VMS-731/rtl-smg.md#smgset_broadcast_trapping-enable-broadcast-trapping) | Enable Broadcast Trapping |
| [SMG$SET_CURSOR_ABS](VAX-VMS-731/rtl-smg.md#smgset_cursor_abs-set-absolute-cursor-position) | Set Absolute Cursor Position |
| [SMG$SET_CURSOR_MODE](VAX-VMS-731/rtl-smg.md#smgset_cursor_mode-set-the-cursor-mode) | Set the Cursor Mode |
| [SMG$SET_CURSOR_REL](VAX-VMS-731/rtl-smg.md#smgset_cursor_rel-move-cursor-relative-to-current-position) | Move Cursor Relative to Current Position |
| [SMG$SET_DEFAULT_STATE](VAX-VMS-731/rtl-smg.md#smgset_default_state-set-default-state) | Set Default State |
| [SMG$SET_DISPLAY_SCROLL_REGION](VAX-VMS-731/rtl-smg.md#smgset_display_scroll_region-create-display-scrolling-region) | Create Display Scrolling Region |
| [SMG$SET_KEYPAD_MODE](VAX-VMS-731/rtl-smg.md#smgset_keypad_mode-set-keypad-mode) | Set Keypad Mode |
| [SMG$SET_OUT_OF_BAND_ASTS](VAX-VMS-731/rtl-smg.md#smgset_out_of_band_asts-set-out-of-band-asts) | Set Out-of-Band ASTs |
| [SMG$SET_PHYSICAL_CURSOR](VAX-VMS-731/rtl-smg.md#smgset_physical_cursor-set-cursor-on-physical-screen) | Set Cursor on Physical Screen |
| [SMG$SET_TERM_CHARACTERISTICS](VAX-VMS-731/rtl-smg.md#smgset_term_characteristics-change-terminal-characteristics) | Change Terminal Characteristics |
| [SMG$SNAPSHOT](VAX-VMS-731/rtl-smg.md#smgsnapshot-write-snapshot) | Write Snapshot |
| [SMG$SNAPSHOT_TO_PRINTER](VAX-VMS-731/rtl-smg.md#smgsnapshot_to_printer-write-snapshot-to-printer) | Write Snapshot to Printer |
| [SMG$UNPASTE_VIRTUAL_DISPLAY](VAX-VMS-731/rtl-smg.md#smgunpaste_virtual_display-remove-virtual-display) | Remove Virtual Display |

## ACLEDIT$ Utility Routines

| Routine | Description |
|---|---|
| [ACLEDIT$EDIT](VAX-VMS-731/utility-routines.md#aclediteditedit-access-control-list) | Edit Access Control List |

## BACKUP$ Utility Routines

| Routine | Description |
|---|---|
| [BACKUP$START](VAX-VMS-731/utility-routines.md#backupstartcall-backup-utility) | Call BACKUP Utility |

## BLAS1$ Utility Routines

| Routine | Description |
|---|---|
| [BLAS1$VIxAMAX](VAX-VMS-731/rtl-mth.md#blas1vixamaxobtain-the-index-of-the-first-element-of-a-vector-having-the-largest-absolute-value) | Obtain the Index of the First Element of a Vector** **Having the Largest Absolute Value |
| [BLAS1$VxASUM](VAX-VMS-731/rtl-mth.md#blas1vxasumobtain-the-sum-of-the-absolute-values-of-the-elements-of-a-vector) | Obtain the Sum of the Absolute Values of the** **Elements of a Vector |
| [BLAS1$VxAXPY](VAX-VMS-731/rtl-mth.md#blas1vxaxpymultiply-a-vector-by-a-scalar-and-add-a-vector) | Multiply a Vector by a Scalar and Add a Vector |
| [BLAS1$VxCOPY](VAX-VMS-731/rtl-mth.md#blas1vxcopycopy-a-vector) | Copy a Vector |
| [BLAS1$VxDOTx](VAX-VMS-731/rtl-mth.md#blas1vxdotxobtain-the-inner-product-of-two-vectors) | Obtain the Inner Product of Two Vectors |
| [BLAS1$VxNRM2](VAX-VMS-731/rtl-mth.md#blas1vxnrm2obtain-the-euclidean-norm-of-a-vector) | Obtain the Euclidean Norm of a Vector |
| [BLAS1$VxROT](VAX-VMS-731/rtl-mth.md#blas1vxrotapply-a-givens-plane-rotation) | Apply a Givens Plane Rotation |
| [BLAS1$VxROTG](VAX-VMS-731/rtl-mth.md#blas1vxrotggenerate-the-elements-for-a-givens-plane-rotation) | Generate the Elements for a Givens Plane** **Rotation |
| [BLAS1$VxSCAL](VAX-VMS-731/rtl-mth.md#blas1vxscalscale-the-elements-of-a-vector) | Scale the Elements of a Vector |
| [BLAS1$VxSWAP](VAX-VMS-731/rtl-mth.md#blas1vxswapswap-the-elements-of-two-vectors) | Swap the Elements of Two Vectors |

## CLI$ — Command Line Interface Utility

| Routine | Description |
|---|---|
| [CLI$DCL_PARSE](VAX-VMS-731/utility-routines.md#clidcl_parseparse-dcl-command-string) | Parse DCL Command String |
| [CLI$DISPATCH](VAX-VMS-731/utility-routines.md#clidispatchdispatch-to-action-routine) | Dispatch to Action Routine |
| [CLI$GET_VALUE](VAX-VMS-731/utility-routines.md#cliget_valueget-value-of-entity-in-command-string) | Get Value of Entity in Command String |
| [CLI$PRESENT](VAX-VMS-731/utility-routines.md#clipresentdetermine-presence-of-entity-in-command-string) | Determine Presence of Entity in Command String |

## CONV$ — Convert Utility

| Routine | Description |
|---|---|
| [CONV$CONVERT](VAX-VMS-731/utility-routines.md#convconvertinitiate-conversion) | Initiate Conversion |
| [CONV$PASS_FILES](VAX-VMS-731/utility-routines.md#convpass_filesspecify-conversion-files) | Specify Conversion Files |
| [CONV$PASS_OPTIONS](VAX-VMS-731/utility-routines.md#convpass_optionsspecify-processing-options) | Specify Processing Options |
| [CONV$RECLAIM](VAX-VMS-731/utility-routines.md#convreclaiminvoke-convertreclaim-utility) | Invoke Convert/Reclaim Utility |

## DCX$ — Data Compression Utility

| Routine | Description |
|---|---|
| [DCX$ANALYZE_DATA](VAX-VMS-731/utility-routines.md#dcxanalyze_dataperform-statistical-analysis-on-a-data-record) | Perform Statistical Analysis on a Data** **Record |
| [DCX$ANALYZE_DONE](VAX-VMS-731/utility-routines.md#dcxanalyze_donespecify-analysis-completed) | Specify Analysis Completed |
| [DCX$ANALYZE_INIT](VAX-VMS-731/utility-routines.md#dcxanalyze_initinitialize-analysis-context) | Initialize Analysis Context |
| [DCX$COMPRESS_DATA](VAX-VMS-731/utility-routines.md#dcxcompress_datacompress-a-data-record) | Compress a Data Record |
| [DCX$COMPRESS_DONE](VAX-VMS-731/utility-routines.md#dcxcompress_donespecify-compression-complete) | Specify Compression Complete |
| [DCX$COMPRESS_INIT](VAX-VMS-731/utility-routines.md#dcxcompress_initinitialize-compression-context) | Initialize Compression Context |
| [DCX$EXPAND_DATA](VAX-VMS-731/utility-routines.md#dcxexpand_dataexpand-a-compressed-data-record) | Expand a Compressed Data Record |
| [DCX$EXPAND_DONE](VAX-VMS-731/utility-routines.md#dcxexpand_donespecify-expansion-complete) | Specify Expansion Complete |
| [DCX$EXPAND_INIT](VAX-VMS-731/utility-routines.md#dcxexpand_initinitialize-expansion-context) | Initialize Expansion Context |
| [DCX$MAKE_MAP](VAX-VMS-731/utility-routines.md#dcxmake_mapcompute-the-compressionexpansion-function) | Compute the Compression/Expansion Function |

## EDT$ — EDT Editor Callable Interface

| Routine | Description |
|---|---|
| [EDT$EDIT](VAX-VMS-731/utility-routines.md#edteditedit-a-file) | Edit a File |

## FDL$ — File Definition Language

| Routine | Description |
|---|---|
| [FDL$CREATE](VAX-VMS-731/utility-routines.md#fdlcreatecreate-a-file-from-an-fdl-specification-and-close-the-file) | Create a File from an FDL Specification and Close** **the File |
| [FDL$GENERATE](VAX-VMS-731/utility-routines.md#fdlgenerategenerate-an-fdl-specification) | Generate an FDL Specification |
| [FDL$PARSE](VAX-VMS-731/utility-routines.md#fdlparseparse-an-fdl-specification) | Parse an FDL Specification |
| [FDL$RELEASE](VAX-VMS-731/utility-routines.md#fdlreleasefree-virtual-memory-obtained-by-fdlparse) | Free Virtual Memory Obtained By FDL$PARSE |

## LBR$ — Librarian Utility

| Routine | Description |
|---|---|
| [LBR$CLOSE](VAX-VMS-731/utility-routines.md#lbrcloseclose-a-library) | Close a Library |
| [LBR$DELETE_DATA](VAX-VMS-731/utility-routines.md#lbrdelete_datadelete-a-modules-data) | Delete a Module’s Data |
| [LBR$DELETE_KEY](VAX-VMS-731/utility-routines.md#lbrdelete_keydelete-a-key) | Delete a Key |
| [LBR$FIND](VAX-VMS-731/utility-routines.md#lbrfindlook-up-a-module-by-its-rfa) | Look Up a Module by Its RFA |
| [LBR$FLUSH](VAX-VMS-731/utility-routines.md#lbrflushrecover-virtual-memory) | Recover Virtual Memory |
| [LBR$GET_HEADER](VAX-VMS-731/utility-routines.md#lbrget_headerretrieve-library-header-information) | Retrieve Library Header Information |
| [LBR$GET_HELP](VAX-VMS-731/utility-routines.md#lbrget_helpretrieve-help-text) | Retrieve Help Text |
| [LBR$GET_HISTORY](VAX-VMS-731/utility-routines.md#lbrget_historyretrieve-a-library-update-history-record) | Retrieve a Library Update History Record |
| [LBR$GET_INDEX](VAX-VMS-731/utility-routines.md#lbrget_indexcall-a-routine-for-selected-index-keys) | Call a Routine for Selected Index Keys |
| [LBR$GET_RECORD](VAX-VMS-731/utility-routines.md#lbrget_recordread-a-data-record) | Read a Data Record |
| [LBR$INI_CONTROL](VAX-VMS-731/utility-routines.md#lbrini_controlinitialize-a-library-control-structure) | Initialize a Library Control Structure |
| [LBR$INSERT_KEY](VAX-VMS-731/utility-routines.md#lbrinsert_keyinsert-a-new-key) | Insert a New Key |
| [LBR$LOOKUP_KEY](VAX-VMS-731/utility-routines.md#lbrlookup_keylook-up-a-library-key) | Look Up a Library Key |
| [LBR$OPEN](VAX-VMS-731/utility-routines.md#lbropenopen-or-create-a-library) | Open or Create a Library |
| [LBR$OUTPUT_HELP](VAX-VMS-731/utility-routines.md#lbroutput_helpoutput-help-messages) | Output Help Messages |
| [LBR$PUT_END](VAX-VMS-731/utility-routines.md#lbrput_endwrite-an-end-of-module-record) | Write an End-of-Module Record |
| [LBR$PUT_HISTORY](VAX-VMS-731/utility-routines.md#lbrput_historywrite-an-update-history-record) | Write an Update History Record |
| [LBR$PUT_RECORD](VAX-VMS-731/utility-routines.md#lbrput_recordwrite-a-data-record) | Write a Data Record |
| [LBR$REPLACE_KEY](VAX-VMS-731/utility-routines.md#lbrreplace_keyreplace-a-library-key) | Replace a Library Key |
| [LBR$RET_RMSSTV](VAX-VMS-731/utility-routines.md#lbrret_rmsstvreturn-openvms-rms-status-value) | Return OpenVMS RMS Status Value |
| [LBR$SEARCH](VAX-VMS-731/utility-routines.md#lbrsearchsearch-an-index) | Search an Index |
| [LBR$SET_INDEX](VAX-VMS-731/utility-routines.md#lbrset_indexset-the-current-index-number) | Set the Current Index Number |
| [LBR$SET_LOCATE](VAX-VMS-731/utility-routines.md#lbrset_locateset-record-access-to-locate-mode) | Set Record Access to Locate Mode |
| [LBR$SET_MODULE](VAX-VMS-731/utility-routines.md#lbrset_moduleread-or-update-a-module-header) | Read or Update a Module Header |
| [LBR$SET_MOVE](VAX-VMS-731/utility-routines.md#lbrset_moveset-record-access-to-move-mode) | Set Record Access to Move Mode |

## LGI$ Utility Routines

| Routine | Description |
|---|---|
| [LGI$ICB_ACCTEXPIRED](VAX-VMS-731/utility-routines.md#lgiicb_acctexpiredaccount-expiration) | Account Expiration |
| [LGI$ICB_AUTOLOGIN](VAX-VMS-731/utility-routines.md#lgiicb_autologincheck-for-autologin) | Check for Autologin |
| [LGI$ICB_CHECK_PASS](VAX-VMS-731/utility-routines.md#lgiicb_check_passcheck-password) | Check Password |
| [LGI$ICB_DISUSER](VAX-VMS-731/utility-routines.md#lgiicb_disusercheck-for-disabled-user-account) | Check for Disabled User Account |
| [LGI$ICB_GET_INPUT](VAX-VMS-731/utility-routines.md#lgiicb_get_inputget-user-input) | Get User Input |
| [LGI$ICB_GET_SYSPWD](VAX-VMS-731/utility-routines.md#lgiicb_get_syspwdget-system-password) | Get System Password |
| [LGI$ICB_MODALHOURS](VAX-VMS-731/utility-routines.md#lgiicb_modalhoursperform-access-checks) | Perform Access Checks |
| [LGI$ICB_PASSWORD](VAX-VMS-731/utility-routines.md#lgiicb_passwordproduce-password-prompt) | Produce Password Prompt |
| [LGI$ICB_PWDEXPIRED](VAX-VMS-731/utility-routines.md#lgiicb_pwdexpiredpassword-expiration) | Password Expiration |
| [LGI$ICB_USERPARSE](VAX-VMS-731/utility-routines.md#lgiicb_userparseparse-username) | Parse Username |
| [LGI$ICB_USERPROMPT](VAX-VMS-731/utility-routines.md#lgiicb_userpromptprompt-for-username) | Prompt for Username |
| [LGI$ICB_VALIDATE](VAX-VMS-731/utility-routines.md#lgiicb_validatevalidate-user-name-and-passwords) | Validate User Name and Passwords |
| [LGI$ICR_AUTHENTICATE](VAX-VMS-731/utility-routines.md#lgiicr_authenticateauthenticate-the-password) | Authenticate the Password |
| [LGI$ICR_CHKRESTRICT](VAX-VMS-731/utility-routines.md#lgiicr_chkrestrictcheck-access-restrictions) | Check Access Restrictions |
| [LGI$ICR_DECWINIT](VAX-VMS-731/utility-routines.md#lgiicr_decwinitdecwindows-initialization) | DECwindows Initialization |
| [LGI$ICR_FINISH](VAX-VMS-731/utility-routines.md#lgiicr_finishfinal-site-action) | Final Site Action |
| [LGI$ICR_IACT_START](VAX-VMS-731/utility-routines.md#lgiicr_iact_startcharacter-cell-initialization) | Character-Cell Initialization |
| [LGI$ICR_IDENTIFY](VAX-VMS-731/utility-routines.md#lgiicr_identifyidentify-the-user) | Identify the User |
| [LGI$ICR_INIT](VAX-VMS-731/utility-routines.md#lgiicr_initinitialization-callout-routine) | Initialization Callout Routine |
| [LGI$ICR_JOBSTEP](VAX-VMS-731/utility-routines.md#lgiicr_jobstepbatch-job-step) | Batch Job Step |
| [LGI$ICR_LOGOUT](VAX-VMS-731/utility-routines.md#lgiicr_logoutinstallation-logout) | Installation Logout |

## MAIL$ — Mail Utility

| Routine | Description |
|---|---|
| [MAIL$MAILFILE_BEGIN](VAX-VMS-731/utility-routines.md#mailmailfile_beginstart-mail-file-processing) | Start Mail File Processing |
| [MAIL$MAILFILE_CLOSE](VAX-VMS-731/utility-routines.md#mailmailfile_closeclose-the-current-mail-file) | Close the Current Mail File |
| [MAIL$MAILFILE_COMPRESS](VAX-VMS-731/utility-routines.md#mailmailfile_compresscompress-mail-file) | Compress Mail File |
| [MAIL$MAILFILE_END](VAX-VMS-731/utility-routines.md#mailmailfile_endend-mail-file-processing) | End Mail File Processing |
| [MAIL$MAILFILE_INFO_FILE](VAX-VMS-731/utility-routines.md#mailmailfile_info_fileget-information-about-a-mail-file) | Get Information About a Mail File |
| [MAIL$MAILFILE_MODIFY](VAX-VMS-731/utility-routines.md#mailmailfile_modifymodify-record-of-an-indexed-file) | Modify Record of an Indexed File |
| [MAIL$MAILFILE_OPEN](VAX-VMS-731/utility-routines.md#mailmailfile_openopen-a-mail-file-for-processing) | Open a Mail File for Processing |
| [MAIL$MAILFILE_PURGE_WASTE](VAX-VMS-731/utility-routines.md#mailmailfile_purge_wastedelete-wastebasket-messages) | Delete Wastebasket Messages |
| [MAIL$MESSAGE_BEGIN](VAX-VMS-731/utility-routines.md#mailmessage_beginstart-message-processing) | Start Message Processing |
| [MAIL$MESSAGE_COPY](VAX-VMS-731/utility-routines.md#mailmessage_copycopy-messages-to-another-file-or-folder) | Copy Messages to Another File or Folder |
| [MAIL$MESSAGE_DELETE](VAX-VMS-731/utility-routines.md#mailmessage_deletedelete-message-from-current-folder) | Delete Message From Current Folder |
| [MAIL$MESSAGE_END](VAX-VMS-731/utility-routines.md#mailmessage_endend-message-processing) | End Message Processing |
| [MAIL$MESSAGE_GET](VAX-VMS-731/utility-routines.md#mailmessage_getget-message-from-a-set-of-messages) | Get Message From a Set of Messages |
| [MAIL$MESSAGE_INFO](VAX-VMS-731/utility-routines.md#mailmessage_infoget-information-about-a-message) | Get Information About a Message |
| [MAIL$MESSAGE_MODIFY](VAX-VMS-731/utility-routines.md#mailmessage_modifymodify-header-information) | Modify Header Information |
| [MAIL$MESSAGE_SELECT](VAX-VMS-731/utility-routines.md#mailmessage_selectselect-message-from-current-mail-file) | Select Message from Current Mail File |
| [MAIL$SEND_ABORT](VAX-VMS-731/utility-routines.md#mailsend_abortcancel-send-operation) | Cancel Send Operation |
| [MAIL$SEND_ADD_ADDRESS](VAX-VMS-731/utility-routines.md#mailsend_add_addressadd-address-to-list) | Add Address to List |
| [MAIL$SEND_ADD_ATTRIBUTE](VAX-VMS-731/utility-routines.md#mailsend_add_attributeadd-attribute-to-the-current-message) | Add Attribute to the Current** **Message |
| [MAIL$SEND_ADD_BODYPART](VAX-VMS-731/utility-routines.md#mailsend_add_bodypartbuild-message-body) | Build Message Body |
| [MAIL$SEND_BEGIN](VAX-VMS-731/utility-routines.md#mailsend_beginstart-sending-message) | Start Sending Message |
| [MAIL$SEND_END](VAX-VMS-731/utility-routines.md#mailsend_endend-sending-message) | End Sending Message |
| [MAIL$SEND_MESSAGE](VAX-VMS-731/utility-routines.md#mailsend_message) |  |
| [MAIL$USER_BEGIN](VAX-VMS-731/utility-routines.md#mailuser_beginaccess-the-user-profile-database) | Access the User Profile Database |
| [MAIL$USER_DELETE_INFO](VAX-VMS-731/utility-routines.md#mailuser_delete_infodelete-database-record) | Delete Database Record |
| [MAIL$USER_END](VAX-VMS-731/utility-routines.md#mailuser_endend-access-to-the-user-profile-database) | End Access to the User Profile Database |
| [MAIL$USER_GET_INFO](VAX-VMS-731/utility-routines.md#mailuser_get_infoget-user-profile-information) | Get User Profile Information |
| [MAIL$USER_SET_INFO](VAX-VMS-731/utility-routines.md#mailuser_set_infoadd-user-profile-information) | Add User Profile Information |

## NCS$ — National Character Set Utility

| Routine | Description |
|---|---|
| [NCS$COMPARE](VAX-VMS-731/utility-routines.md#ncscomparecompare-strings) | Compare Strings |
| [NCS$CONVERT](VAX-VMS-731/utility-routines.md#ncsconvertconvert-string) | Convert String |
| [NCS$END_CF](VAX-VMS-731/utility-routines.md#ncsend_cfend-conversion-function) | End Conversion Function |
| [NCS$END_CS](VAX-VMS-731/utility-routines.md#ncsend_csend-collating-sequence) | End Collating Sequence |
| [NCS$GET_CF](VAX-VMS-731/utility-routines.md#ncsget_cfget-conversion-function) | Get Conversion Function |
| [NCS$GET_CS](VAX-VMS-731/utility-routines.md#ncsget_csget-collating-sequence) | Get Collating Sequence |
| [NCS$RESTORE_CF](VAX-VMS-731/utility-routines.md#ncsrestore_cfrestore-conversion-function) | Restore Conversion Function |
| [NCS$RESTORE_CS](VAX-VMS-731/utility-routines.md#ncsrestore_csrestore-collating-sequence) | Restore Collating Sequence |
| [NCS$SAVE_CF](VAX-VMS-731/utility-routines.md#ncssave_cfsave-conversion-function) | Save Conversion Function |
| [NCS$SAVE_CS](VAX-VMS-731/utility-routines.md#ncssave_cssave-collating-sequence) | Save Collating Sequence |

## Other Utility Routines

| Routine | Description |
|---|---|
| [FILEIO](VAX-VMS-731/utility-routines.md#fileiouser-written-routine-to-perform-file-operations) | User-Written Routine to Perform File Operations |
| [FILE_PARSE](VAX-VMS-731/utility-routines.md#file_parseuser-written-routine-to-perform-file-parse-operations) | User-Written Routine to Perform File Parse** **Operations |
| [FILE_SEARCH](VAX-VMS-731/utility-routines.md#file_searchuser-written-routine-to-perform-file-search-operations) | User-Written Routine to Perform File Search** **Operations |
| [HANDLER](VAX-VMS-731/utility-routines.md#handleruser-written-condition-handling-routine) | User-Written Condition Handling Routine |
| [INITIALIZE](VAX-VMS-731/utility-routines.md#initializeuser-written-initialization-routine) | User-Written Initialization Routine |
| [USER](VAX-VMS-731/utility-routines.md#useruser-written-routine-called-from-a-dectpu-editing-session) | User-Written Routine Called from a DECTPU Editing Session |
| [WORKIO](VAX-VMS-731/utility-routines.md#workio) |  |
| [XLATE](VAX-VMS-731/utility-routines.md#xlate) |  |

## PSM$ — Print Symbiont Modification

| Routine | Description |
|---|---|
| [PSM$PRINT](VAX-VMS-731/utility-routines.md#psmprintinvoke-openvms-supplied-print-symbiont) | Invoke OpenVMS-Supplied Print Symbiont |
| [PSM$READ_ITEM_DX](VAX-VMS-731/utility-routines.md#psmread_item_dxobtain-value-of-message-items) | Obtain Value of Message Items |
| [PSM$REPLACE](VAX-VMS-731/utility-routines.md#psmreplacedeclare-user-service-routine) | Declare User Service Routine |
| [PSM$REPORT](VAX-VMS-731/utility-routines.md#psmreportreport-completion-status) | Report Completion Status |

## SMB$ — Symbiont Manager

| Routine | Description |
|---|---|
| [SMB$CHECK_FOR_MESSAGE](VAX-VMS-731/utility-routines.md#smbcheck_for_messagecheck-for-message-from-job-controller) | Check for Message from Job** **Controller |
| [SMB$INITIALIZE](VAX-VMS-731/utility-routines.md#smbinitializeinitialize-user-written-symbiont) | Initialize User-Written Symbiont |
| [SMB$READ_MESSAGE](VAX-VMS-731/utility-routines.md#smbread_messageobtain-message-sent-by-job-controller) | Obtain Message Sent by Job Controller |
| [SMB$READ_MESSAGE_ITEM](VAX-VMS-731/utility-routines.md#smbread_message_itemparse-next-item-from-message-buffer) | Parse Next Item from Message** **Buffer |
| [SMB$SEND_TO_JOBCTL](VAX-VMS-731/utility-routines.md#smbsend_to_jobctlsend-message-to-job-controller) | Send Message to Job Controller |

## SOR$ — Sort/Merge Utility

| Routine | Description |
|---|---|
| [SOR$BEGIN_MERGE](VAX-VMS-731/utility-routines.md#sorbegin_mergeinitialize-a-merge-operation) | Initialize a Merge Operation |
| [SOR$BEGIN_SORT](VAX-VMS-731/utility-routines.md#sorbegin_sortbegin-a-sort-operation) | Begin a Sort Operation |
| [SOR$DTYPE](VAX-VMS-731/utility-routines.md#sordtypedefine-data-type) | Define Data Type |
| [SOR$END_SORT](VAX-VMS-731/utility-routines.md#sorend_sortend-a-sort-operation) | End a Sort Operation |
| [SOR$PASS_FILES](VAX-VMS-731/utility-routines.md#sorpass_filespass-file-name) | Pass File Name |
| [SOR$RELEASE_REC](VAX-VMS-731/utility-routines.md#sorrelease_recpass-one-record-to-sort) | Pass One Record to Sort |
| [SOR$RETURN_REC](VAX-VMS-731/utility-routines.md#sorreturn_recreturn-one-sorted-record) | Return One Sorted Record |
| [SOR$SORT_MERGE](VAX-VMS-731/utility-routines.md#sorsort_mergesort) | Sort |
| [SOR$SPEC_FILE](VAX-VMS-731/utility-routines.md#sorspec_filepass-a-specification-file-name) | Pass a Specification File Name |
| [SOR$STAT](VAX-VMS-731/utility-routines.md#sorstatobtain-a-statistic) | Obtain a Statistic |

## TPU$ — TPU Editor Callable Interface

| Routine | Description |
|---|---|
| [TPU$CLEANUP](VAX-VMS-731/utility-routines.md#tpucleanupfree-system-resources-used-during-dectpu-session) | Free System Resources Used During DECTPU** **Session |
| [TPU$CLIPARSE](VAX-VMS-731/utility-routines.md#tpucliparseparse-a-command-line) | Parse a Command Line |
| [TPU$CLOSE_TERMINAL](VAX-VMS-731/utility-routines.md#tpuclose_terminalclose-channel-to-terminal) | Close Channel to Terminal |
| [TPU$CONTROL](VAX-VMS-731/utility-routines.md#tpucontrolpass-control-to-dectpu) | Pass Control to DECTPU |
| [TPU$EDIT](VAX-VMS-731/utility-routines.md#tpueditedit-a-file) | Edit a File |
| [TPU$EXECUTE_COMMAND](VAX-VMS-731/utility-routines.md#tpuexecute_commandexecute-one-or-more-dectpu-statements) | Execute One or More DECTPU** **Statements |
| [TPU$EXECUTE_INIFILE](VAX-VMS-731/utility-routines.md#tpuexecute_inifileexecute-initialization-files) | Execute Initialization Files |
| [TPU$FILEIO](VAX-VMS-731/utility-routines.md#tpufileioperform-file-operations) | Perform File Operations |
| [TPU$FILE_PARSE](VAX-VMS-731/utility-routines.md#tpufile_parse-parse-the-given-file-specification) | Parse the Given File Specification |
| [TPU$FILE_SEARCH](VAX-VMS-731/utility-routines.md#tpufile_searchsearch-file-system-for-specified-file) | Search File System for Specified File |
| [TPU$HANDLER](VAX-VMS-731/utility-routines.md#tpuhandlerdectpu-condition-handler) | DECTPU Condition Handler |
| [TPU$INITIALIZE](VAX-VMS-731/utility-routines.md#tpuinitializeinitialize-dectpu-for-processing) | Initialize DECTPU for Processing |
| [TPU$MESSAGE](VAX-VMS-731/utility-routines.md#tpumessagewrite-message-string) | Write Message String |
| [TPU$PARSEINFO](VAX-VMS-731/utility-routines.md#tpuparseinfoparse-command-line-and-build-item-list) | Parse Command Line and Build Item List |
| [TPU$SIGNAL](VAX-VMS-731/utility-routines.md#tpusignalsignal-a-tpu-status) | Signal a TPU Status |
| [TPU$SPECIFY_ASYNC_ACTION](VAX-VMS-731/utility-routines.md#tpuspecify_async_actionregister-an-asynchronous-action) | Register an Asynchronous Action |
| [TPU$TPU](VAX-VMS-731/utility-routines.md#tputpuinvoke-dectpu) | Invoke DECTPU |
| [TPU$TRIGGER_ASYNC_ACTION](VAX-VMS-731/utility-routines.md#tputrigger_async_actionexecute-dectpu-command-at-asynchronous-level) | Execute DECTPU Command at** **Asynchronous Level |

## UTIL$ Utility Routines

| Routine | Description |
|---|---|
| [UTIL$CQUAL_CONFIRM_ACT](VAX-VMS-731/utility-routines.md#utilcqual_confirm_actask-user-for-confirmation) | Ask User for Confirmation |
| [UTIL$CQUAL_FILE_END](VAX-VMS-731/utility-routines.md#utilcqual_file_endend-processing) | End Processing |
| [UTIL$CQUAL_FILE_MATCH](VAX-VMS-731/utility-routines.md#utilcqual_file_matchmatch-a-file-with-selection-criteria) | Match a File with Selection Criteria |
| [UTIL$CQUAL_FILE_PARSE](VAX-VMS-731/utility-routines.md#utilcqual_file_parseparse-the-command-line) | Parse the Command Line |

