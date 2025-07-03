@echo off
setlocal

REM ---- 1. white repertoire ----
call polyglot_tolerant -noini -ec cmd dump-book ^
     -bin Optimus2502.bin -color white -out white-moves.txt

REM ---- 2. black repertoire ----
call polyglot_tolerant -noini -ec cmd dump-book ^
     -bin Optimus2502.bin -color black -out black-moves.txt

REM ---- 3. turn the two dumps into PGN(s) ----
python convert-cerebellum.py

REM ---- 4. tidy up ----
del white-moves.txt
del black-moves.txt

endlocal
