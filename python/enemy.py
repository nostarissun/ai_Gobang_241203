import const
import numpy as np
def get_evaluate(r : int,  c: int, chess_board):

    enemy = judge(r, c, 1, 2, chess_board)
    friend = judge(r, c, 2, 1, chess_board)
    score = enemy + friend
    return score

def judge(y0: int, x0: int, enemy: int, friend: int, chess_board):
    score = 0
    cnt = []

    for dir in const.dir:
        r = 0
        first_empty = -1
        for chess_cnt in range(1, 6):
            y = y0 + dir[1] * chess_cnt
            x = x0 + dir[0] * chess_cnt
            if x >= const.board_size_W or x < 0 or y >= const.board_size_H or y < 0:
                break
            if chess_board[y][x] == friend:
                break
            if chess_board[y][x] == 0 and first_empty == -1:
                first_empty = chess_cnt

            if chess_board[y][x] == enemy and first_empty <= 2:
                r += 1
        cnt.append(r)
    max_cnt = 0
    for i in range(0, 4):
        max_cnt = max(max_cnt, cnt[i] + cnt[i + 4])
    score += const.status[max_cnt]
    return score

def place_where(chess_board):
    pos = []
    res = float('-inf')

    center_score = 20
    for r in range(const.board_size_H):
        for c in range(const.board_size_W):
            if chess_board[r][c] != 0:
                print("%-5s" % "0", end = ' ')
                continue

            score = center_score - abs(const.CENTER_X - r) - abs(const.CENTER_Y - c) + get_evaluate(r, c, chess_board)

            print("%-5s" % score, end = ' ')

            if res < score:
                res = score
                pos = [r, c]
        print()

    return pos