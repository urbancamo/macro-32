# Round-trip targets for driving the VAX/VMS host (vmsdrive + vmsftp).
#
# Defaults to the HELLOWORLD example -- override with PROG=<dir>/<basename>:
#
#   make vms-build PROG=helloworld/hello
#   make vms-run   PROG=helloworld/hello
#   make vms-debug PROG=helloworld/hello
#
# Each program lives at  src/macro32/<dir>/<basename>.mar  and produces
# <basename>.lis (assembly listing, fetched back) and <basename>.log
# (captured run output) in the same directory.

PROG     ?= helloworld/hello
SRC_DIR  := src/macro32
SRC      := $(SRC_DIR)/$(PROG).mar
NAME     := $(notdir $(basename $(SRC)))
NAME_UC  := $(shell echo $(NAME) | tr '[:lower:]' '[:upper:]')
OUT_DIR  := $(dir $(SRC))
LIS      := $(OUT_DIR)$(NAME).lis
LOG      := $(OUT_DIR)$(NAME).log

VMSDRIVE := tools/vmsdrive/vmsdrive.py
VMSFTP   := tools/vmsftp/vmsftp.py

.PHONY: vms-up vms-down vms-status vms-push vms-build vms-build-release \
        vms-fetch-lis vms-run vms-run-input vms-debug vms-clean help

help:
	@echo "VAX/VMS round-trip targets (override PROG=<dir>/<base>):"
	@echo "  make vms-up                  # start vmsdrived (idempotent login)"
	@echo "  make vms-down                # logout + stop daemon"
	@echo "  make vms-status              # show daemon health"
	@echo "  make vms-push PROG=...       # push source to VMS working dir"
	@echo "  make vms-build PROG=...      # push + MACRO/LIST/DEBUG + LINK/DEBUG + fetch .lis"
	@echo "  make vms-build-release PROG=...  # same but MACRO/LIST + LINK/NOTRACEBACK/NODEBUG"
	@echo "                               # required for symbionts and other detached-process images"
	@echo "  make vms-run PROG=...        # build + RUN + capture stdout to .log + fetch .lis"
	@echo "  make vms-run-input PROG=... INPUT=N PROMPT='text: ' [OUTFILE=NAME.TXT]"
	@echo "                               # build + RUN + answer one program prompt"
	@echo "                               # with INPUT once PROMPT appears, optionally"
	@echo "                               # fetching OUTFILE back into the source dir"
	@echo "  make vms-debug PROG=...      # build + RUN/DEBUG (leaves at DBG> prompt)"
	@echo "  make vms-clean PROG=...      # purge old VMS versions of <PROG>.*"
	@echo ""
	@echo "After 'vms-debug' (or any time the daemon is up):"
	@echo "  $(VMSDRIVE) dbg 'STEP'"
	@echo "  $(VMSDRIVE) dbg 'EXAMINE R0..R5,SP,PC'"
	@echo "  $(VMSDRIVE) dbg 'EXIT'"
	@echo ""
	@echo "Current PROG = $(PROG)  ->  source $(SRC)  ->  remote $(NAME_UC).MAR"

vms-up:
	@$(VMSDRIVE) start

vms-down:
	@$(VMSDRIVE) stop

vms-status:
	@$(VMSDRIVE) status

vms-push: vms-up
	@test -f $(SRC) || { echo "missing source: $(SRC)" >&2; exit 1; }
	@echo ">>> upload $(SRC) -> $(NAME_UC).MAR"
	@$(VMSFTP) put $(SRC) $(NAME_UC).MAR

vms-build: vms-push
	@echo ">>> MACRO/LIST/DEBUG $(NAME_UC)"
	@$(VMSDRIVE) cmd 'MACRO/LIST/DEBUG $(NAME_UC)'
	@echo ">>> LINK/DEBUG $(NAME_UC)"
	@$(VMSDRIVE) cmd 'LINK/DEBUG $(NAME_UC)'
	@$(MAKE) --no-print-directory vms-fetch-lis

# Release build -- no debugger stub. Required for any image that runs
# as a detached process (e.g. a print symbiont via INITIALIZE/QUEUE
# /PROCESSOR=...): a /DEBUG-linked image will try to attach the
# debugger at activation time, find no DBG$INPUT/DBG$OUTPUT, and the
# job controller reports %QMAN-E-SYMDEL with a -DEBUG-S- continuation
# line. Use this target for symbionts, ACPs, and detached servers.
vms-build-release: vms-push
	@echo ">>> MACRO/LIST $(NAME_UC)"
	@$(VMSDRIVE) cmd 'MACRO/LIST $(NAME_UC)'
	@echo ">>> LINK/NOTRACEBACK/NODEBUG $(NAME_UC)"
	@$(VMSDRIVE) cmd 'LINK/NOTRACEBACK/NODEBUG $(NAME_UC)'
	@$(MAKE) --no-print-directory vms-fetch-lis

vms-fetch-lis:
	@echo ">>> fetch $(NAME_UC).LIS -> $(LIS)"
	@$(VMSFTP) get '$(NAME_UC).LIS' $(LIS) >/dev/null
	@ls -l $(LIS)

vms-run: vms-build
	@echo ">>> RUN/NODEBUG $(NAME_UC)  (capturing to $(LOG))"
	@$(VMSDRIVE) cmd 'RUN/NODEBUG $(NAME_UC)' | tee $(LOG)
	@echo ">>> exit status:"
	@$(VMSDRIVE) cmd 'SHOW SYMBOL $$STATUS'

# Run an interactive program: wait for PROMPT, send INPUT, then for the DCL
# prompt. Optional OUTFILE is fetched back into the program's source dir.
#
#   make vms-run-input PROG=primes/primesio INPUT=100 \
#        PROMPT='generate: ' OUTFILE=PRIMES.TXT
vms-run-input: vms-build
	@test -n "$(INPUT)"  || { echo "set INPUT=...";  exit 1; }
	@test -n "$(PROMPT)" || { echo "set PROMPT='text appearing right before the cursor'"; exit 1; }
	@echo ">>> RUN/NODEBUG $(NAME_UC)  expect='$(PROMPT)'  input='$(INPUT)'  (-> $(LOG))"
	@( $(VMSDRIVE) cmd 'RUN/NODEBUG $(NAME_UC)' --expect '$(PROMPT)' --timeout 30; \
	   $(VMSDRIVE) cmd '$(INPUT)' --timeout 60 ) | tee $(LOG)
	@echo ">>> exit status:"
	@$(VMSDRIVE) cmd 'SHOW SYMBOL $$STATUS'
ifdef OUTFILE
	@echo ">>> fetch $(OUTFILE) -> $(OUT_DIR)$(shell echo $(OUTFILE) | tr '[:upper:]' '[:lower:]')"
	@$(VMSFTP) get '$(OUTFILE)' $(OUT_DIR)$(shell echo $(OUTFILE) | tr '[:upper:]' '[:lower:]') >/dev/null
	@ls -l $(OUT_DIR)$(shell echo $(OUTFILE) | tr '[:upper:]' '[:lower:]')
endif

vms-debug: vms-build
	@echo ">>> RUN/DEBUG $(NAME_UC)  (intro logged to $(LOG))"
	@$(VMSDRIVE) cmd 'RUN/DEBUG $(NAME_UC)' | tee $(LOG)
	@echo ""
	@echo "Now at DBG> prompt. Drive the debugger with:"
	@echo "  $(VMSDRIVE) dbg '<command>'"
	@echo "Common: TYPE n:m | STEP | EXAMINE R0..R5,PC | SET BREAK %LINE 49 | GO | EXIT"

vms-clean:
	@echo ">>> purge $(NAME_UC).*"
	@$(VMSDRIVE) cmd 'PURGE/KEEP=1 $(NAME_UC).*'

# ----------------------------------------------------------------------
# Multi-file image builds (currently used by SCAVE / Sorcerer's Cave)
#
# A multi-module program lives at src/macro32/<NAME>/ with one .MAR file
# per module and a sources.list giving link order, one BASENAME per line.
# All modules link into <NAME_UC>.EXE.  The default target SCAVE uses
# src/macro32/sorcerer/.
#
# On the VAX side, all SCAVE files live in a [.SCAVE] subdirectory of
# the daemon's default ([MSW.CLAUDE.SCAVE] in practice).  Each target
# does SET DEFAULT [.SCAVE] at the start and SET DEFAULT [-] at the end
# so other tools that assume [MSW.CLAUDE] (vms-build, vms-run for the
# single-file demos) keep working unchanged.  vmsftp uploads/downloads
# go via the `raw` subcommand with an explicit cd into [.SCAVE] so the
# DCL session and FTP session don't have to share state.
# ----------------------------------------------------------------------

SCAVE_DIR     := src/macro32/sorcerer
SCAVE_NAME    := SCAVE
SCAVE_SUBDIR  := SCAVE
SCAVE_SRCS    := $(shell awk 'NF && !/^\#/' $(SCAVE_DIR)/sources.list 2>/dev/null)
SCAVE_LINK    := $(shell awk 'NF && !/^\#/{print $$0".OBJ"}' $(SCAVE_DIR)/sources.list 2>/dev/null | paste -sd, -)
SCAVE_LIS_DIR := $(SCAVE_DIR)
SCAVE_LOG     := $(SCAVE_DIR)/scave.log

.PHONY: vms-scave-build vms-scave-build-release vms-scave-run vms-scave-debug \
        vms-scave-fetch-lis vms-scave-clean vms-scave-cd vms-scave-cd-back

# Helper: enter / leave the SCAVE subdir on the daemon side.
vms-scave-cd:
	@$(VMSDRIVE) cmd 'SET DEFAULT [.$(SCAVE_SUBDIR)]'

vms-scave-cd-back:
	@$(VMSDRIVE) cmd 'SET DEFAULT [-]'

#
# Host-side build is now a thin driver around MAKE.COM living on the
# VAX in [.SCAVE].  We push the .MAR sources + MAKE.COM in one FTP
# session, run @MAKE.COM via vmsdrive (one round-trip for the whole
# MACRO/LINK chain), then fetch listings in one FTP session.  This
# replaces the previous one-cmd-per-MACRO loop, which was slow and
# repeatedly tripped the daemon's prompt-detection.
#
# MAKE.COM uses ON ERROR THEN EXIT $STATUS so any failed MACRO halts
# the procedure before LINK runs.  See src/macro32/sorcerer/MAKE.COM
# for the canonical list of sources -- keep it in sync with
# sources.list.
#

# Build the script that vmsftp will execute: cd into [.SCAVE], then
# `put <local> <basename>.MAR` for every source plus MAKE.COM.
define SCAVE_PUSH_SCRIPT
ascii
cd [.$(SCAVE_SUBDIR)]
$(foreach s,$(SCAVE_SRCS),put $(SCAVE_DIR)/$(s).MAR $(s).MAR
)put $(SCAVE_DIR)/MAKE.COM MAKE.COM
put $(SCAVE_DIR)/SCAVEHLP.TXT SCAVEHLP.TXT
endef
export SCAVE_PUSH_SCRIPT

# Build the fetch script for listings.
define SCAVE_FETCH_SCRIPT
ascii
cd [.$(SCAVE_SUBDIR)]
$(foreach s,$(SCAVE_SRCS),get $(s).LIS $(SCAVE_LIS_DIR)/$(s).lis
)
endef
export SCAVE_FETCH_SCRIPT

vms-scave-build: vms-up
	@test -n "$(SCAVE_SRCS)" || { echo "no sources in $(SCAVE_DIR)/sources.list" >&2; exit 1; }
	@test -f $(SCAVE_DIR)/MAKE.COM || { echo "missing $(SCAVE_DIR)/MAKE.COM" >&2; exit 1; }
	@echo ">>> regenerate SCAVEHLP.TXT from help/*.md"
	@python3 tools/gen_help.py
	@echo ">>> upload sources + MAKE.COM + help text -> [.$(SCAVE_SUBDIR)]"
	@$(VMSFTP) raw "$$SCAVE_PUSH_SCRIPT" >/dev/null
	@echo ">>> SET DEFAULT [.$(SCAVE_SUBDIR)]"
	@$(VMSDRIVE) cmd 'SET DEFAULT [.$(SCAVE_SUBDIR)]'
	@echo ">>> @MAKE.COM"
	@$(VMSDRIVE) cmd '@MAKE.COM'
	@echo ">>> SET DEFAULT [-]"
	@$(VMSDRIVE) cmd 'SET DEFAULT [-]'
	@$(MAKE) --no-print-directory vms-scave-fetch-lis

vms-scave-build-release: vms-up vms-scave-cd
	@echo "release variant not yet ported to MAKE.COM driver -- TODO"
	@$(MAKE) --no-print-directory vms-scave-cd-back
	@false

vms-scave-fetch-lis:
	@echo ">>> fetch *.LIS -> $(SCAVE_LIS_DIR)/"
	@$(VMSFTP) raw "$$SCAVE_FETCH_SCRIPT" >/dev/null
	@ls -l $(SCAVE_LIS_DIR)/*.lis

vms-scave-run: vms-scave-build vms-scave-cd
	@echo ">>> RUN/NODEBUG $(SCAVE_NAME)  (capturing to $(SCAVE_LOG))"
	@$(VMSDRIVE) cmd 'RUN/NODEBUG $(SCAVE_NAME)' | tee $(SCAVE_LOG)
	@echo ">>> exit status:"
	@$(VMSDRIVE) cmd 'SHOW SYMBOL $$STATUS'
	@$(MAKE) --no-print-directory vms-scave-cd-back

vms-scave-debug: vms-scave-build vms-scave-cd
	@echo ">>> RUN/DEBUG $(SCAVE_NAME)  (intro logged to $(SCAVE_LOG))"
	@$(VMSDRIVE) cmd 'RUN/DEBUG $(SCAVE_NAME)' | tee $(SCAVE_LOG)
	@echo ""
	@echo "Now at DBG> prompt -- daemon stays in [.$(SCAVE_SUBDIR)] until"
	@echo "you 'make vms-scave-cd-back' (or run another scave target)."
	@echo "Drive the debugger with:"
	@echo "  $(VMSDRIVE) dbg '<command>'"

vms-scave-clean: vms-up vms-scave-cd
	@for s in $(SCAVE_SRCS); do \
	   echo ">>> purge $$s.*"; \
	   $(VMSDRIVE) cmd "PURGE/KEEP=1 $$s.*"; \
	 done
	@$(VMSDRIVE) cmd 'PURGE/KEEP=1 $(SCAVE_NAME).EXE'
	@$(MAKE) --no-print-directory vms-scave-cd-back
