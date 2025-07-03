@echo off

:: Set dummy engine
set ENGINE_COMMAND=cmd.exe /c exit 0

:: Call PolyGlot Tolerant with dummy engine
call polyglot_tolerant dump-book -bin Optimus2502.bin -color white -out white-moves.txt
call polyglot_tolerant dump-book -bin Optimus2502.bin -color black -out black-moves.txt

:: Convert to PGN
call convert-cerebellum.py

:: Cleanup
del white-moves.txt
del black-moves.txt
