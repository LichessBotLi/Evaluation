import chess
import chess.engine
import chess.pgn
import asyncio

BOOK = "Optimus2502.bin"
STOCKFISH = "./stockfish"

async def play_game():
    eng1 = await chess.engine.popen_uci(STOCKFISH)
    eng2 = await chess.engine.popen_uci(STOCKFISH)

    # SFBook uses the Polyglot book
    await eng1.configure({"OwnBook": "true", "BookFile": BOOK})
    await eng2.configure({"OwnBook": "false"})

    board = chess.Board()
    game = chess.pgn.Game()
    game.headers["White"] = "SFBook"
    game.headers["Black"] = "SF"

    node = game

    while not board.is_game_over():
        move = None
        if board.turn == chess.WHITE:
            result = await eng1.play(board, chess.engine.Limit(time=0.1))
        else:
            result = await eng2.play(board, chess.engine.Limit(time=0.1))
        move = result.move
        board.push(move)
        node = node.add_variation(move)

    game.headers["Result"] = board.result()

    await eng1.quit()
    await eng2.quit()

    return game

def save_game(game, filename):
    with open(filename, "a") as f:
        print(game, file=f, end="\n\n")

def main():
    games_to_play = 2  # Change to desired number
    all_games = []
    bad_games = []

    for _ in range(games_to_play):
        game = asyncio.run(play_game())
        save_game(game, "all_games.pgn")
        result = game.headers["Result"]
        if (game.headers["White"] == "SFBook" and result == "0-1") or \
           (game.headers["Black"] == "SFBook" and result == "1-0"):
            save_game(game, "bad_games.pgn")

if __name__ == "__main__":
    main()
