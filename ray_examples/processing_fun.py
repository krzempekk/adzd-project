import re
import io
import chess.pgn
import numpy as np

from collections import defaultdict


def filter_out_games(games, filters):
    filltered_games = []

    for key, value in filters.items():
        for game in games:
            if key in game.headers and game.headers[key] == value:
                filltered_games.append(game)
    return filltered_games
    

def process(file_path, filters={}, aggregate=""):
    games = []
    pgn = []
    with open(file_path) as input:
        for line in input:
            if line == '\n':
                games.append(chess.pgn.read_game(io.StringIO('\n'.join(pgn))))
                pgn = []
            else:
                pgn.append(line)                

    games = filter_out_games(games, filters)

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
    process('output/0.txt', aggregate='move_dist', filters={'Result': '0-1'})
