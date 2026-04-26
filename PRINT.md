# FILESYM -- a custom OpenVMS print symbiont that captures output to a file

`src/macro32/symbiont/filesym.mar` is a small (~270 lines of MACRO-32)
user-modified print symbiont built on the OpenVMS Print Symbiont
Modification (PSM) API. It looks like a normal print queue to DCL --
you `PRINT` files to it the way you would to any other queue -- but
instead of feeding the formatted output stream to a line printer it
writes that stream verbatim to an RMS sequential file on disk.

The captured file contains everything the standard symbiont (PRTSMB)
would have sent to the printer:

- Job and file burst pages (the ASCII-art "who-printed-what" banners)
- File flag / file header / page headers
- Form-feed bytes (`^L`) at page boundaries
- Carriage control between records
- The actual file's contents

It is the OpenVMS equivalent of "Print to PDF" -- minus the PDF.
Useful for archiving listings, exfiltrating printable output to a
workstation for inspection, or just understanding what the print
symbiont actually emits.

## How it works

The Print Symbiont Modification (PSM) facility lets you replace
individual routines inside the standard print symbiont (PRTSMB)
with your own. FILESYM replaces just one routine -- `PSM$K_OUTPUT`
-- which is the routine PRTSMB calls each time it has a buffered
record ready to write to the device. Everything else (reading the
spool file, generating burst / flag pages, applying the queue's
form characteristics, formatting page headers, deciding where the
form feeds go) is still handled by PRTSMB.

```
+------------------+     PSM$K_OPEN    +-----------------+
|                  |    PSM$K_WRITE    |                 |
|  Standard print  |  -------------->  |  OUR_OUTPUT     |
|  symbiont        |    PSM$K_CLOSE    |  (in FILESYM)   |
|  (PRTSMB)        |                   |                 |
|                  |                   |       v         |
+------------------+                   |  RMS $CREATE /  |
                                       |  $PUT / $CLOSE  |
                                       |       v         |
                                       |  CAPTURED.PRN   |
                                       +-----------------+
```

`OUR_OUTPUT` dispatches on PSM's function code:

| Function code             | Action                                              |
| ---                       | ---                                                 |
| `PSM$K_OPEN`              | `$CREATE` + `$CONNECT` the output file; report device capabilities |
| `PSM$K_WRITE`             | `$PUT` the formatted record from `funcdesc` to the file |
| `PSM$K_WRITE_NOFORMAT`    | Same as `WRITE` (the symbiont uses this for `PASSALL` data) |
| `PSM$K_CLOSE`             | `$CLOSE` the output file                            |
| anything else             | Return `PSM$_FUNNOTSUP` -- the symbiont applies its default |

The main routine just calls `PSM$REPLACE(PSM$K_OUTPUT, OUR_OUTPUT)`
to install the override, then `PSM$PRINT` to enter the standard
event loop. `PSM$PRINT` blocks until the queue is stopped.

## Where output goes

By default the captured file is `DISK$USERS:[MSW.CLAUDE]CAPTURED.PRN`,
hardcoded in the FAB inside `filesym.mar`. The path is committed
this way deliberately:

- It must resolve in the **detached SYSTEM-owned symbiont process**,
  which has *no* per-process logical name table from a normal login.
  `SYS$LOGIN`, `SYS$SCRATCH`, etc. are not defined there. `DISK$USERS`
  is in `LNM$SYSTEM_TABLE` so it resolves the same in every process.
- SYSTEM has SYSPRV, so writes into `[MSW.CLAUDE]` succeed even though
  MSW owns that directory.

Each START of the queue causes `$CREATE` to run again, which bumps the
file version (`CAPTURED.PRN;1`, `CAPTURED.PRN;2`, ...). The file stays
**open and locked** until the queue is stopped, which is when
`PSM$K_CLOSE` fires and `$CLOSE` flushes RMS buffers.

To change the path, edit the `FNM=<...>` argument of the `$FAB` macro
near the bottom of `filesym.mar`'s data PSECT, then rebuild + reinstall
(see "Rebuilding and updating" below). A future enhancement noted in
the source is to look up `FILESYM$OUTPUT` via `$TRNLNM` so the path can
be reconfigured per-install via `DEFINE/SYSTEM` without rebuilding.

## One-time install (SYSTEM, OPER privilege required)

These steps need OPER. On `orac` only the SYSTEM account has it; the
MSW account does not. So this section runs from a SYSTEM session.

```
$ COPY DISK$USERS:[MSW.CLAUDE]FILESYM.EXE SYS$SYSTEM:
$ INITIALIZE/QUEUE/PROCESSOR=FILESYM/ON=NL: FILEQ
$ START/QUEUE FILEQ
$ SHOW QUEUE FILEQ                  ! confirm "idle"
```

Three things to know:

1. **`/PROCESSOR=` only takes a bare file name** and always loads from
   `SYS$SYSTEM:.EXE`. A full path on the qualifier silently fails at
   `START` time with `%RMS-F-SYN`. This is why the COPY step is
   non-negotiable: the symbiont image *must* live in `SYS$SYSTEM:`.
2. **`/ON=NL:` is a placeholder.** The queue manager wants a device
   name on the qualifier; `NL:` (the null device) suffices because our
   output routine never actually writes to it -- we hijack the data
   stream before any device I/O happens.
3. **The queue persists across reboots once initialized.** You only do
   `INITIALIZE/QUEUE` once per system. After a reboot you may need
   `START/QUEUE FILEQ` again if the queue manager doesn't auto-restart
   it; that's a one-line operator action.

## Day-to-day use (any user with PRINT access)

Once the queue is up, anyone who can normally `PRINT` can target it.
No OPER needed. From MSW, via `tools/vmsdrive`:

```sh
tools/vmsdrive/vmsdrive.py cmd 'PRINT/QUEUE=FILEQ/HEADER/FLAG HELLO.MAR'
```

Or in a DCL session directly:

```
$ PRINT/QUEUE=FILEQ/HEADER/FLAG HELLO.MAR
$ PRINT/QUEUE=FILEQ/HEADER/FLAG/COPIES=2 PRIMES.LIS
$ SHOW QUEUE/ALL FILEQ              ! see the spool state
```

`/HEADER` produces a file-header line on each page; `/FLAG` produces
the bursting flag page at the start of each file. Both are the
standard PRTSMB qualifiers, and FILESYM passes them through untouched.

## Fetching the captured file

`CAPTURED.PRN` is locked while the symbiont has it open. To get a
clean copy you have to flush:

```
$$ STOP/QUEUE/RESET FILEQ           ! triggers PSM$K_CLOSE -> $CLOSE
```

Then from MSW:

```sh
tools/vmsftp/vmsftp.py get CAPTURED.PRN src/macro32/symbiont/captured.prn
```

The fetched file is plain ASCII with `^L` form-feeds at page
boundaries. `cat`, `less`, `vim`, etc. all handle it fine. To
re-print it on a real (or terminal-as-printer) device the form-feeds
do the right thing.

To start a fresh capture session, restart the queue. Each START fires
PSM$K_OPEN, which `$CREATE`s a new file version:

```
$$ START/QUEUE FILEQ
```

## Rebuilding and updating

After editing `filesym.mar`:

```sh
make vms-build-release PROG=symbiont/filesym
```

This pushes the source, runs `MACRO/LIST` + `LINK/NOTRACEBACK/NODEBUG`,
and fetches the listing back to `src/macro32/symbiont/filesym.lis`.
**Critical: use `vms-build-release`, not the default `vms-build`.**

The default `make vms-build` passes `/DEBUG` to LINK, which embeds
the debugger stub. That's fine for ordinary user images but **fatal
for symbionts**: when the queue manager spawns the symbiont as a
detached process there is no terminal for the debugger to attach to,
the image dies on activation, and OPCOM logs

```
%QMAN-E-SYMDEL, unexpected symbiont process termination
-DEBUG-S-NOMSG, Message number 00028009
```

`vms-build-release` instead emits `MACRO/LIST` + `LINK/NOTRACEBACK
/NODEBUG`, exactly as the PSM section of the OpenVMS Utility Routines
manual prescribes for production symbiont builds.

After every rebuild SYSTEM has to re-deploy the new EXE -- the queue
manager loads from `SYS$SYSTEM:`, not from where the source build
lives:

```
$$ STOP/QUEUE/RESET FILEQ
$$ COPY DISK$USERS:[MSW.CLAUDE]FILESYM.EXE SYS$SYSTEM:
$$ START/QUEUE FILEQ
```

## Customizing it

Things you might reasonably want to change, with rough effort
estimates:

| Change | Where | Effort |
| --- | --- | --- |
| Output path | `LOG_FAB`'s `FNM=<...>` in the data PSECT of `filesym.mar`. Use any path that resolves in the system logical-name table. | One-line edit + rebuild + reinstall |
| Output path configurable at runtime | Add `$TRNLNM("FILESYM$OUTPUT")` in `DO_OPEN`, fall back to the hardcoded default if undefined. Set with `DEFINE/SYSTEM/EXEC FILESYM$OUTPUT path` before `START/QUEUE`. | ~30 lines of MACRO + a string buffer for the translated name |
| Record format / carriage control | `LOG_FAB`'s `RFM=` and `RAT=` keywords. Currently `RFM=VAR`, `RAT=CR`. Use `RAT=<CR,PRN>` to preserve the FORTRAN carriage-control byte the symbiont prepends; use `RFM=STM` if you want a stream-of-bytes file with no record structure. | One-line edit + rebuild + reinstall |
| Claim more device capabilities | `DEV_LOWERCASE = ^X01` near the top of `filesym.mar`. Bit 0 = lowercase capable. The full bit map (terminal, remote, etc.) isn't documented in the manual we have; see `PSM$K_OPEN` in `reference/VAX-VMS-731/utility-routines.md`. | One constant to change |
| Multiple simultaneous queues | Bump `STREAMS:` from 1 to up to 16 (manager limit), add per-stream state (the symbiont gives each stream its own `work_area` arg -- use it to hold per-stream FAB/RAB pointers instead of the global ones). | Significant -- needs reentrant data and per-stream `$CREATE` |
| Hook other PSM phases (e.g. custom page header) | Replace additional routines via `PSM$REPLACE(PSM$K_PAGE_HEADER, ...)` etc. See `reference/VAX-VMS-731/utility-routines.md` Table 17-1 for all replaceable routines. | A new replacement routine per phase |

When in doubt, the canonical reference is
`reference/VAX-VMS-731/utility-routines.md` Chapter 17 (PSM
routines). It includes a complete worked MACRO-32 example of a
page-header replacement that's structurally identical to FILESYM and
shows the exact calling conventions for every replaceable routine.

## Verification

To verify a captured file looks right after a printing session:

```sh
# fetch it (requires the queue to have been stopped first)
tools/vmsftp/vmsftp.py get CAPTURED.PRN src/macro32/symbiont/captured.prn

# inspect
head -60 src/macro32/symbiont/captured.prn         # burst + flag
grep -n "Page [0-9]" src/macro32/symbiont/captured.prn
od -c src/macro32/symbiont/captured.prn | grep '\\f'   # form-feeds
wc -l src/macro32/symbiont/captured.prn
```

A "good" capture has:

- 3 lines of `AAAAA...0000...VAX Version V7.3...0000...AAAAA` (the
  burst banner)
- ASCII-art block letters spelling the user name, file name, and
  version
- One-line "File _DSA0:[...]NAME.TYPE;V (...) ... is a N block
  sequential file ..." description
- One-line "Job NAME (n) queued to FILEQ on date by user ..."
- Repeating header line `_DSA0:[...]NAME.TYPE;V    date    Page N`
- The actual file content
- Form-feed bytes (`^L` = 0x0C) at page transitions

If anything is missing, check the queue's form attributes
(`SHOW QUEUE/FULL FILEQ`); the symbiont obeys them, so changing the
form changes what FILESYM captures.

## Gotcha index

Captured here once so neither future-me nor future-you re-pay the
debugging cost:

| Symptom | Cause | Fix |
| --- | --- | --- |
| `%RMS-F-SYN` on `START/QUEUE` | `/PROCESSOR=` had a directory in it | Bare filename only; `COPY` the EXE into `SYS$SYSTEM:` first |
| `%RMS-E-FNF` on `START/QUEUE` | EXE not found in `SYS$SYSTEM:` | Same fix as above |
| `%QMAN-E-SYMDEL` with `-DEBUG-S-NOMSG` continuation in OPCOM | symbiont was linked with `/DEBUG`; debugger fails to attach in the detached process | Rebuild with `make vms-build-release` (uses `LINK/NOTRACEBACK/NODEBUG`) |
| `%QMAN-E-SYMDEL` *without* a `-DEBUG-` continuation | symbiont's `PSM$K_OPEN` returned an error -- usually `$CREATE` couldn't resolve the FNM | Use a path that resolves in the system logical table (e.g. `DISK$USERS:`, not `SYS$LOGIN:`) |
| `vmsftp get` fails with "file currently locked by another user" | symbiont still has the file open | `STOP/QUEUE/RESET FILEQ` from SYSTEM to flush + close |
| Output is upper-cased | symbiont treats us as an UC-only line printer | Already fixed in this version: we set bit 0 in the device-status longword on PSM$K_OPEN |
| Banners / flag pages missing from capture | the queue's form doesn't include them | `MODIFY QUEUE/DEFAULT=(FORM=DEFAULT,FEED) FILEQ` and `PRINT/HEADER/FLAG ...` |
