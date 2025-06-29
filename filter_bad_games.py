import chess.pgn

def play_game():
    with open("all_games.pgn", "r") as pgn:
        game = chess.pgn.read_game(pgn)
        while game:
            result = game.headers.get("Result")
            white = game.headers.get("White")
            black = game.headers.get("Black")

            # SFBook loses if:
            if (white == "SFBook" and result == "0-1") or (black == "SFBook" and result == "1-0"):
                yield game

            game = chess.pgn.read_game(pgn)

def main():
    with open("bad_games.pgn", "w") as out:
        for bad_game in play_game():
            print(bad_game, file=out, end="\n\n")

if __name__ == "__main__":
    main()
