@echo off

call polyglot_tolerant dump-book -bin Optimus2502.bin -color white -out white-moves.txt
call polyglot_tolerant dump-book -bin Optimus2502.bin -color black -out black-moves.txt

call python convert-cerebellum.py

del white-moves.txt
del black-moves.txt
