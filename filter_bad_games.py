import chess
import chess.engine
import chess.pgn
import os

STOCKFISH = "./stockfish"
BOOK = "./Optimus2502.bin"
OUTPGN = "bad_games.pgn"

def play_game():
    board = chess.Board()
    game = chess.pgn.Game()
    node = game

    engine1 = chess.engine.SimpleEngine.popen_uci([STOCKFISH, f"option.UseBook=true", f"option.BookFile={BOOK}"])
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
    game.headers["White"] = "BookSide"
    game.headers["Black"] = "NoBook"
    return game if result == "0-1" else None  # Book side lost

def main():
    with open(OUTPGN, "w") as f:
        for _ in range(50):  # Try 50 games
            game = play_game()
            if game:
                f.write(str(game) + "\n\n")
                print("Saved a bad game.")

if __name__ == "__main__":
    main()
