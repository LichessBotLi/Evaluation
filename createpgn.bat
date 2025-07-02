@echo off

REM --- dump the book lines ------------------------------------
polyglot_tolerant dump-book -bin Optimus2502.bin -color white -out white-moves.txt
polyglot_tolerant dump-book -bin Optimus2502.bin -color black -out black-moves.txt

REM --- convert to PGN ----------------------------------------
python convert-cerebellum.py

del white-moves.txt
del black-moves.txt
