@echo off

polyglot_tolerant dump-book Optimus2502.bin white-moves.txt white
polyglot_tolerant dump-book Optimus2502.bin black-moves.txt black

call python convert-cerebellum.py

del white-moves.txt
del black-moves.txt
