# primes.mar + primesio.mar — design notes

Two variants of the same program, both in this directory:

| File | Output target |
|---|---|
| `primes.mar` | `SYS$OUTPUT` (i.e. the terminal, via `LIB$PUT_OUTPUT`) |
| `primesio.mar` | `PRIMES.TXT` in the current default directory (via RMS) |

The primality / formatting logic is identical. Only the output path differs. Design notes below cover `primes.mar` first, then the RMS-specific additions in `primesio.mar`.

---

## primes.mar

Prints the first 100 prime numbers (2, 3, 5, ..., 541) to `SYS$OUTPUT`, one per line.

## Algorithm

Standard trial-division with two small optimisations.

1. Emit `2` as a special case, then iterate odd candidates `C = 3, 5, 7, …`.
2. For each `C`, trial-divide by odd divisors `D = 3, 5, 7, …`.
3. Stop as soon as `D² > C` — if no factor `≤ √C` divides `C`, then `C` is prime.
4. **Divisibility test without `EDIV`:** `EDIV` requires a quadword dividend (two-register setup). Instead, compute the quotient with `DIVL3` and reconstruct the product:

   ```
   DIVL3   D, C, Q         ; Q = C / D (integer)
   MULL3   D, Q, P         ; P = Q * D
   CMPL    P, C            ; if P == C, D divides C exactly
   BEQL    not_prime
   ```

   Three register-to-register instructions, no memory scratch, no quadword pair.

## Register allocation

All captured in the `.ENTRY` save mask `^M<R2,R3,R4,R5,R6,R7>` so that DCL sees the registers untouched on return.

| Reg | Role |
|---|---|
| `R2` | prime count (stops at 100) |
| `R3` | current candidate `C` |
| `R4` | current trial divisor `D` |
| `R5` | scratch — `D²` for the `√C` bound check |
| `R6` | scratch — `C / D` quotient from `DIVL3` |
| `R7` | scratch — `Q * D` for the divisibility reconstruction |

`R0` and `R1` are deliberately *not* in the mask — they are scratch / return-value registers that LIB$ and OTS$ calls will clobber. The program relies on the final `LIB$PUT_OUTPUT` having left `SS$_NORMAL` in `R0`, which `RET` then returns to DCL as the image exit status.

## Output formatting

`OTS$CVT_L_TU` (Convert Unsigned Integer to Decimal Text) writes a right-justified decimal representation into a fixed-length buffer, padding with leading spaces. The 100th prime is 541 (three digits), so a 6-byte buffer is ample.

The same descriptor (`OUT_DESC`) is reused for both:
- `OTS$CVT_L_TU` — writes into it (buffer is an output destination)
- `LIB$PUT_OUTPUT` — reads from it (buffer is the message to emit)

One call to `LIB$PUT_OUTPUT` produces one record; RMS's implied carriage control gives us one line per call. No explicit `<CR><LF>` is needed.

## Code structure

```
.PSECT PRIMES_DATA (NOEXE, WRT, LONG)    ← CANDIDATE_L, OUT_STR, OUT_DESC
.PSECT PRIMES_CODE (EXE, NOWRT, LONG)
    .ENTRY PRIMES, ^M<R2..R7>            ← image transfer address
    ; print 2, then loop over odd candidates
    BSBW PRINT_CANDIDATE                 ← cheap local call
    ...
    RET

PRINT_CANDIDATE:                         ← BSB/RSB subroutine
    CALLS #2, G^OTS$CVT_L_TU             ← format R3's decimal text
    CALLS #1, G^LIB$PUT_OUTPUT           ← emit it
    RSB
.END PRIMES
```

`PRINT_CANDIDATE` is entered via `BSB` (no stack frame, no register save), which is fine because (a) it uses no registers of its own and (b) the inner `CALLS` preserves the caller's `R2–R7` through the *called* routines' save masks.

## Control flow / worked examples

| Candidate | Inner loop | Outcome |
|---:|---|---|
| 3 | `D=3`, `D²=9 > 3` → prime | prints `3` |
| 5 | `D=3`, `D²=9 > 5` → prime | prints `5` |
| 7 | `D=3`, `D²=9 > 7` → prime | prints `7` |
| 9 | `D=3`, `D²=9 == 9` (not greater), `Q=3`, `Q·D=9 == C` | **not prime** |
| 11 | `D=3`, `Q=3`, `Q·D=9 ≠ 11`; `D=5`, `D²=25 > 11` → prime | prints `11` |
| 25 | `D=3`, `Q=8`, `Q·D=24 ≠ 25`; `D=5`, `D²=25 == 25`, `Q=5`, `Q·D=25 == C` | **not prime** |

The `BGTR` on the `D² > C` test (strictly greater) correctly handles the `C = D²` case — it falls through into the divisibility check, which then correctly catches exact squares like 9 and 25.

## References consulted

All in this repo:

| Topic | File |
|---|---|
| `OTS$CVT_L_TU` — 2 mandatory args, value by reference, output by fixed-length descriptor | `reference/VAX-VMS-731/rtl-ots.md` |
| `LIB$PUT_OUTPUT` — 1 arg, message-string by descriptor | `reference/VAX-VMS-731/rtl-lib.md` |
| `DIVL3`, `MULL3`, `CMPL`, `ADDL2`, `INCL`, conditional branches | `reference/VAX-VMS-731/vax-macro-ref-2001.md` ch. 9 |
| `.PSECT`, `.ENTRY`, register save mask semantics | `reference/VAX-VMS-731/vax-macro-ref-2001.md` ch. 6 |
| `$DSCDEF`, descriptor layout, `.PSECT` attribute patterns | `reference/macro-made-easy/part-01-introductions.md` (REVERSE.MAR skeleton) |
| Meta-index entry points for LIB$/OTS$ | `reference/INDEX.md` |

## Build on OpenVMS

```
$ MACRO PRIMES
$ LINK PRIMES
$ RUN PRIMES
```

No toolchain on macOS, so the program is verified by specification only — the runtime check would need SIMH + an OpenVMS install, or a real VAX/Alpha system.

---

## primesio.mar — the RMS variant

Same algorithm, same register allocation, same format routine. The only difference is that each prime becomes one **record in `PRIMES.TXT`** instead of one line on `SYS$OUTPUT`.

### File layout

A statically-declared pair of RMS control blocks in the data PSECT:

```
OUT_FAB:  $FAB  FNM=<SYS$DISK:[]PRIMES.TXT>,
                FAC=PUT, ORG=SEQ, RFM=VAR, MRS=6

OUT_RAB:  $RAB  FAB=OUT_FAB,
                RAC=SEQ, RBF=OUT_STR, RSZ=6
```

- **`FNM=<SYS$DISK:[]PRIMES.TXT>`** — the bracketed syntax pins the file to the current default directory. Without the explicit device/directory, the file would be created relative to whatever RMS resolves `SYS$DISK` to at the moment of `$CREATE`.
- **`FAC=PUT`** — write access (required for `$CREATE`).
- **`ORG=SEQ`, `RFM=VAR`, `MRS=6`** — sequential file, variable-length records, max 6 bytes. That's the standard OpenVMS text-file format; `TYPE PRIMES.TXT` will display it line-by-line.
- **`RAC=SEQ`** — record access is sequential (append-on-$PUT).
- **`RBF=OUT_STR`, `RSZ=6`** — the record buffer address and length, set once statically. `OUT_STR` doubles as both the `OTS$CVT_L_TU` destination buffer and the `$PUT` record source.

### RMS service sequence

```
$CREATE  FAB=OUT_FAB        ; create the file, open it for write
$CONNECT RAB=OUT_RAB        ; attach the record stream
loop:
  <format prime into OUT_STR>
  $PUT   RAB=OUT_RAB        ; emit one record
$CLOSE   FAB=OUT_FAB        ; flush and close
```

Each macro expands to a few stack pushes + a `CALLG` into the RMS entry point; the service's status lands in R0 (low bit set = success, clear = failure).

### Error handling

RMS services return status in R0. The pattern throughout is:

```
BLBC  R0, <cleanup-label>   ; branch on Low Bit Clear
```

There are two cleanup labels:

- **`99$`** — after `$CREATE` failure: nothing to clean up, just `RET` with the error status.
- **`90$`** — after `$CONNECT` or any `$PUT` failure: `PUSHL R0` to preserve the status, best-effort `$CLOSE` the file (ignoring its own return), `POPL R0`, `RET`.

The normal exit path at `80$` runs `$CLOSE` and returns its status directly — so on success, DCL sees `SS$_NORMAL` in `$STATUS`.

### Buffer sharing

`OUT_STR` is the single 6-byte buffer used for both directions:

1. `OTS$CVT_L_TU` writes the decimal representation into it (via `OUT_DESC`, a static descriptor).
2. `$PUT` reads it as the record source (via `RBF`/`RSZ` in the RAB).

No copying, no buffer juggling — the order within `WRITE_CANDIDATE` (convert, then put) guarantees the data is current by the time `$PUT` fires.

### Build and verify

```
$ MACRO PRIMESIO
$ LINK PRIMESIO
$ RUN PRIMESIO
$ TYPE PRIMES.TXT
```

`TYPE` will show 100 lines, each a right-justified decimal prime in a 6-column field.
