import io
import json
import chess.pgn
import numpy as np

from collections import defaultdict


def filter_result(game, result):
    return "Result" in game.headers and game.headers["Result"] == result


def filter_time_le(game, value):
    if "TimeControl" not in game.headers:
        return False
    
    time_control, _ = game.headers["TimeControl"].split("+")
    time_control = int(time_control)
    if value >= time_control:
        return True
    return False


def filter_time_ge(game, value):
    if "TimeControl" not in game.headers:
        return False
    
    time_control, _ = game.headers["TimeControl"].split("+")
    time_control = int(time_control)
    if value <= time_control:
        return True
    return False


def filter_elo_ge(game, value):
    if "WhiteElo" not in game.headers or "BlackElo" not in game.headers:
        return False
    
    white_elo = int(game.headers["WhiteElo"])
    black_elo = int(game.headers["BlackElo"])
    if white_elo >= value and black_elo >= value:
        return True
    return False


def filter_elo_le(game, value):
    if "WhiteElo" not in game.headers or "BlackElo" not in game.headers:
        return False
    
    white_elo = int(game.headers["WhiteElo"])
    black_elo = int(game.headers["BlackElo"])
    if white_elo <= value and black_elo <= value:
        return True
    return False


def filter_out_games(games, filters):
    # Available filters and possible values:
    #   "result": "1-0"/"0-1"/"1/2-1/2"
    #   "time_le": <time in sec> (filters out games with greater time control)
    #   "time_ge": <time in sec> (filters out games with lower time control)
    #   "elo_le": <value> (filters out games with players above provided elo)
    #   "elo_ge": <value> (filters out games with players below provided elo)

    filter_functions = {
        "result": filter_result,
        "time_le": filter_time_le,
        "time_ge": filter_time_ge,
        "elo_le": filter_elo_le,
        "elo_ge": filter_elo_ge
    }

    filtered_games = []

    for game in games:
        for key, value in filters.items():
            if not filter_functions[key](game, value):
                break
        else:
            filtered_games.append(game)
    return filtered_games
    

def process_file(file_path, filters=None, aggregate=""):
    games = []
    pgn = []
    with open(file_path) as input:
        for line in input:
            if line == '\n':
                games.append(chess.pgn.read_game(io.StringIO('\n'.join(pgn))))
                pgn = []
            else:
                pgn.append(line)                

    games = filter_out_games(games, filters) if filters is not None else games

    if aggregate == 'heatmap':
        heatmap = np.zeros((12, 64))

        for game in games:
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
                piece = board.piece_at(move.to_square)
                heatmap[piece.piece_type - 1 + 6*piece.color][move.to_square] += 1

        return heatmap

    if aggregate == 'wins':
        wins = np.zeros(3)

        for game in games:
            if game.headers['Result'] == '1-0':
                wins[0] += 1
            elif game.headers['Result'] == '0-1':
                wins[2] += 1
            else:
                wins[1] += 1
        return wins
    
    if aggregate == 'move_dist':
        distribution = defaultdict(int)

        for game in games:
            distribution[sum(1 for e in game.mainline_moves())] += 1
        
        return distribution


if __name__ == '__main__':
    # heatmap = process_file(
    #     'processed_input_0/0.txt', 
    #     aggregate='heatmap', 
    #     filters={
    #         "result": "1-0",
    #         "elo_ge": 1000,
    #         "time_ge": 180
    #     }
    # )

    input_file = 'processed_input_0/0.txt'

    with open('analyze/experiments.json') as experiments:
        experiments_setup = json.load(experiments)

        for setup in experiments_setup:
            result = process_file(input_file, **setup)

    # print(heatmap)
    # np.savetxt('output_1/heatmap_0.txt', heatmap)
