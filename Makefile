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
