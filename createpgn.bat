@echo off

REM White book dump
call polyglot_tolerant polyglot.ini dump-book -bin Optimus2502.bin -color white -out white-moves.txt

REM Black book dump
call polyglot_tolerant polyglot.ini dump-book -bin Optimus2502.bin -color black -out black-moves.txt

REM Convert to PGNs
call convert-cerebellum.py

REM Cleanup
del white-moves.txt
del black-moves.txt
