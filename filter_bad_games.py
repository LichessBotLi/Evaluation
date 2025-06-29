import chess
import chess.engine
import chess.pgn

STOCKFISH = "./stockfish"          # installed via apt
POLYGLOT  = "./polyglot"           # downloaded in workflow
BOOK      = "./Optimus2502.bin"    # keep in repo root
OUTPGN    = "bad_games.pgn"

def play_game():
    board = chess.Board()
    game  = chess.pgn.Game()
    node  = game

    # Engine 1 = Stockfish with Optimus book via Polyglot
    engine1_cmd = [POLYGLOT, "-e", STOCKFISH, "-b", BOOK]
    engine1 = chess.engine.SimpleEngine.popen_uci(engine1_cmd)

    # Engine 2 = plain Stockfish (no book)
    engine2 = chess.engine.SimpleEngine.popen_uci(STOCKFISH)

    engines = [engine1, engine2]
    turn = 0

    while not board.is_game_over():
        result = engines[turn].play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        node = node.add_variation(result.move)
        turn ^= 1

    engine1.quit()
    engine2.quit()

    result = board.result()
    game.headers["Result"] = result
    game.headers["White"]  = "BookSide"
    game.headers["Black"]  = "NoBook"
    return game if result == "0-1" else None   # save only if book side loses

def main():
    saved = 0
    with open(OUTPGN, "w") as f:
        for _ in range(50):          # play 50 games
            g = play_game()
            if g:
                f.write(str(g) + "\n\n")
                saved += 1
    print(f"Bad games saved: {saved}")

if __name__ == "__main__":
    main()
