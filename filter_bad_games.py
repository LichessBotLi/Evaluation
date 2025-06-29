import chess
import chess.engine
import chess.pgn

STOCKFISH = "./stockfish"          # installed via apt in workflow
BOOK      = "Optimus2502.bin"      # book file in repo root
OUTPGN    = "bad_games.pgn"
GAMES     = 50                     # how many games to play

def play_game():
    # Stockfish WITH book
    eng1 = chess.engine.SimpleEngine.popen_uci(STOCKFISH)
    eng1.configure({"OwnBook": "true", "BookFile": BOOK})

    # Stockfish WITHOUT book
    eng2 = chess.engine.SimpleEngine.popen_uci(STOCKFISH)
    eng2.configure({"OwnBook": "false"})

    board = chess.Board()
    game  = chess.pgn.Game()
    node  = game
    engines = [eng1, eng2]
    turn = 0

    while not board.is_game_over():
        result = engines[turn].play(board, chess.engine.Limit(time=0.05))
        board.push(result.move)
        node = node.add_variation(result.move)
        turn ^= 1  # switch

    # tidy up
    eng1.quit()
    eng2.quit()

    game.headers["Result"] = board.result()
    game.headers["White"]  = "BookSide"
    game.headers["Black"]  = "NoBook"
    return game if board.result() == "0-1" else None   # save only if book side (White) lost

def main():
    saved = 0
    with open(OUTPGN, "w") as f:
        for _ in range(GAMES):
            g = play_game()
            if g:
                f.write(str(g) + "\n\n")
                saved += 1
    print(f"Saved {saved} losing games caused by the book.")

if __name__ == "__main__":
    main()
