import chess
import chess.polyglot
import chess.pgn
import pathlib
import sys

# Path to the Polyglot book and output PGN
BIN = pathlib.Path("Optimus2502.bin")
PGN = pathlib.Path("Optimus2502.pgn")
MAX_DEPTH = 12  # Max number of half-moves per PGN (6 full moves)

# Check if book exists
if not BIN.is_file():
    sys.exit(f"❌ {BIN} not found in repo root.")

# Open book and PGN output
with chess.polyglot.open_reader(str(BIN)) as reader, PGN.open("w", encoding="utf-8") as out:
    root = chess.Board()
    stack = [(root, [])]  # (board position, list of moves)

    while stack:
        board, line = stack.pop()

        # Emit PGN if we reach max depth or a node with no book moves
        if len(line) >= MAX_DEPTH or not list(reader.find_all(board)):
            game = chess.pgn.Game()
            node = game
            for mv in line:
                node = node.add_variation(mv)
            print(game, file=out, end="\n\n")
            continue

        # Traverse further by pushing all book continuations
        for entry in list(reader.find_all(board))[::-1]:  # Reverse to preserve move order
            mv = entry.move
            board.push(mv)
            stack.append((board.copy(stack=False), line + [mv]))
            board.pop()

print(f"✅ Wrote PGNs (up to {MAX_DEPTH} plies) to {PGN}")
