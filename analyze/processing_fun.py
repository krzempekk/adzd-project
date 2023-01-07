import io
import json
import itertools
import chess.pgn
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict


def filter_result(game, result):
    return "Result" in game.headers and game.headers["Result"] == result


def filter_time_le(game, value):
    if "TimeControl" not in game.headers or game.headers["TimeControl"] == '-':
        return False
    
    time_control, _ = game.headers["TimeControl"].split("+")
    time_control = int(time_control)
    if value >= time_control:
        return True
    return False


def filter_time_ge(game, value):
    if "TimeControl" not in game.headers or game.headers["TimeControl"] == '-':
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
    

def process_games(games=[], filters=None, aggregate=""):
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


def all_experiments(games):
    with open('analyze/experiments.json') as experiments:
        experiments_setup = json.load(experiments)
        counter = 0
        for setup in experiments_setup:
            result = process_games(games=games, **setup)
            plt.clf()
            if setup['aggregate'] == 'wins':
                print(setup['filters'], result)
            elif setup['aggregate'] == 'move_dist':
                plt.bar(result.keys(), result.values(), color='g')
                plt.title(setup['filters'])
                plt.savefig(f'docs/results/{counter}.png')
            elif setup['aggregate'] == 'heatmap':
                heatmap = np.sum(result, axis=0).reshape((8, 8))
                heatmap = heatmap / heatmap.max()

                plt.imshow(heatmap, cmap='hot', interpolation='nearest')
                plt.xticks(range(8), ['%c' % x for x in range(65, 65 + 8)])
                plt.yticks(range(8), range(8, 0, -1))

                plt.title(f"Heatmap {setup['filters']}")

                plt.colorbar()

                plt.savefig(f'docs/results/{counter}.png')
            counter += 1


def heatmap(games):
    result = process_games(games=games, aggregate='heatmap')
    figures = ["pawn", "knight", "bishop", "rook", "queen", "king"]

    for i, figure in enumerate(figures):
        plt.clf()
        heatmap = result[6+i].reshape((8, 8))

        heatmap = heatmap / heatmap.max()
        plt.imshow(heatmap, cmap='hot', interpolation='nearest')

        plt.xticks(range(8), ['%c' % x for x in range(65, 65 + 8)])
        plt.yticks(range(8), range(8, 0, -1))
        plt.title(f"Heatmap {figure}")
        plt.colorbar()
        plt.savefig(f'docs/results/black_{figure}.png')


if __name__ == '__main__':
    input_file = 'lichess_db_standard_rated_2015-12.pgn'

    games = []
    pgn = []
    counter = 0
    parity = 1
    with open(input_file) as input:
        for line in input:
            if line == '\n':
                parity *= -1
                if parity == -1:
                    continue
                games.append(chess.pgn.read_game(io.StringIO('\n'.join(pgn))))
                counter += 1
                if counter % 100_00 == 0:
                    print(counter)
                if counter % 1000 == 0:
                    break
                pgn = []
            else:
                pgn.append(line)

    # all_experiments(games)
    heatmap(games)
