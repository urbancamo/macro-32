$!
$! MAKE.COM -- single-shot SCAVE build script.  Invoked from the host
$! Makefile via:
$!
$!     $(VMSDRIVE) cmd 'SET DEFAULT [.SCAVE]'
$!     $(VMSDRIVE) cmd '@MAKE.COM'
$!     $(VMSDRIVE) cmd 'SET DEFAULT [-]'
$!
$! Caller is responsible for setting the working directory to
$! [.SCAVE] before invoking; we don't change it here so the procedure
$! can also be run by hand from inside the directory.
$!
$! On error any MACRO returns a non-success $STATUS.  ON ERROR aborts
$! the procedure so we don't link a half-assembled image.
$!
$! Sources in link order match src/macro32/sorcerer/sources.list.
$! When you edit sources.list, mirror the change here.
$!
$ ON ERROR THEN EXIT $STATUS
$ WRITE SYS$OUTPUT "-- SCAVE build (default: ", F$ENVIRONMENT("DEFAULT"), ") --"
$ MACRO/DEBUG/LIST MAIN.MAR
$ MACRO/DEBUG/LIST SETUP.MAR
$ MACRO/DEBUG/LIST MAP.MAR
$ MACRO/DEBUG/LIST VIEW.MAR
$ MACRO/DEBUG/LIST HELP.MAR
$ MACRO/DEBUG/LIST CHAMBER.MAR
$ MACRO/DEBUG/LIST STRANGER.MAR
$ MACRO/DEBUG/LIST FIGHT.MAR
$ MACRO/DEBUG/LIST SPECIAL.MAR
$ MACRO/DEBUG/LIST ARTIFACT.MAR
$ MACRO/DEBUG/LIST SCORE.MAR
$ MACRO/DEBUG/LIST UI.MAR
$ MACRO/DEBUG/LIST RNG.MAR
$ MACRO/DEBUG/LIST DATA.MAR
$ MACRO/DEBUG/LIST STATE.MAR
$ MACRO/DEBUG/LIST ENGINE.MAR
$ MACRO/DEBUG/LIST SCCONF.MAR
$ WRITE SYS$OUTPUT "-- LINK SCAVE --"
$ LINK/DEBUG/EXEC=SCAVE.EXE -
        MAIN.OBJ,SETUP.OBJ,MAP.OBJ,VIEW.OBJ,HELP.OBJ,CHAMBER.OBJ, -
        STRANGER.OBJ,FIGHT.OBJ,SPECIAL.OBJ,ARTIFACT.OBJ,SCORE.OBJ, -
        UI.OBJ,RNG.OBJ,DATA.OBJ,STATE.OBJ,ENGINE.OBJ
$ WRITE SYS$OUTPUT "-- LINK SCCONF --"
$ LINK/DEBUG/EXEC=SCCONF.EXE -
        SCCONF.OBJ,ENGINE.OBJ,SETUP.OBJ,UI.OBJ,RNG.OBJ,DATA.OBJ,STATE.OBJ
$ WRITE SYS$OUTPUT "-- DONE --"
