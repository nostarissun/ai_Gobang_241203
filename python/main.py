import const
import socket


# 下白棋
# 黑棋是1， 白棋是2
# chess_board = [[0] * const.board_size_W] * const.board_size_W
chess_board = []
for init_chess_board in range(const.board_size_H):
    t = []
    for j in range(const.board_size_W):
        t.append(0)
    chess_board.append(t)



# def get_evaluate(r: int, c: int) -> int:
#     global chess_board
#     cnt2 = [0, 0, 0, 0, 0, 0 ,0, 0]
#     cnt1 = [0, 0, 0, 0, 0, 0 ,0, 0]
#     idx = 0
#     for dir in const.dir:
#         for i in range(1, 9):
#             r1 = r + dir[1] * i
#             c1 = c + dir[0] * i
#
#             if c1 >= const.board_size_W or c1 < 0 or r1 >= const.board_size_H or r1 < 0 :
#                 break
#             if chess_board[r1][c1] == 1 or chess_board[r1][c1] == 0 :
#                 if chess_board[r1][c1] == 1 :
#                     cnt1[idx] += 1
#                 continue
#             if chess_board[r1][c1] == 2:
#                 cnt2[idx] += 1
#
#         idx += 1
#
#     res = 0
#     for i in range(4):
#         t1 = cnt1[i] + cnt1[i + 4]
#         t2 = cnt2[i] + cnt2[i + 4]
#         if t2 in const.status and t1 in const.status[t2]:
#             # if t1 in const.status_enemy and t2 in const.status[t1]:
#                 # res = max(res, const.status[t2][t1] + const.status_enemy[t1][t2])
#                 # res = max(res, const.status[t2][t1] + another_score(c, r, 1, 2))
#
#
#     return res

# #统计对手在该位置的得分情况
# def another_score(c: int, r: int, enemy: int, friend: int):
#     score = 0
#     global chess_board
#     cnt = [0, 0, 0, 0, 0, 0, 0, 0]
#     idx = 0
#     for dir in const.dir:
#         for i in range(1, 9):
#             r1 = r + dir[1] * i
#             c1 = c + dir[0] * i
#             if c1 >= const.board_size_W or c1 < 0 or r1 >= const.board_size_H or r1 < 0:
#                 break
#
#
#             if chess_board[r1][c1] == enemy:
#                 cnt[idx] += 1
#             elif chess_board[r1][c1] == friend:
#                 continue
#             elif chess_board[r1][c1] == 2:
#                 t1 = c + dir[0] * (i + 1)
#                 t2 = r + dir[1] * (i + 1)
#                 if t1 >= const.board_size_W or t1 < 0 or t2 >= const.board_size_H or t2 < 0:
#                     continue
#                 if chess_board[r1][c1] == friend:
#                     continue
#                 cnt[idx] += 1
#
#         idx += 1
#     t = 0
#     for i in range(4):
#         t = max(t, cnt[i] + cnt[i + 4])
#     if t == 1:
#         return 100
#     elif t == 2:
#         return 2000
#     elif t == 3:
#         return 8000
#     elif t >= 4:
#         return 10000
#     else:
#         10


def get_evaluate(r : int,  c: int):

    enemy = judge(r, c, 1, 2)
    friend = judge(r, c, 2, 1)
    score = enemy + friend
    return score

def judge(y0: int, x0: int, enemy: int, friend: int):
    score = 0
    global chess_board
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

def place_where():
    pos = []
    res = float('-inf')
    global chess_board
    center_score = 20
    for r in range(const.board_size_H):
        for c in range(const.board_size_W):
            if chess_board[r][c] != 0:
                print("%-5s" % "0", end = ' ')
                continue

            score = center_score - abs(const.CENTER_X - r) - abs(const.CENTER_Y - c) + get_evaluate(r, c)

            print("%-5s" % score, end = ' ')

            if res < score:
                res = score
                pos = [r, c]
        print()

    return pos


def handle_connection():
    global chess_board
    serveport = 12000
  
    servesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servesocket.bind(('', serveport))
    servesocket.listen(1)
    print("运行中...\n")
    cnt = 1
    while True:
        connectionsocket, addr = servesocket.accept()
        sentence = connectionsocket.recv(1024).decode()

        # 检查接收到的数据长度是否符合预期
        length = const.board_size_W * const.board_size_H
        if len(sentence) != length:
            print("接收到的数据长度不正确，请重新发送" + str(len(sentence)))
            print(sentence)
            # connectionsocket.send(error_message.encode())
            # connectionsocket.close()
            continue


        for i in range(const.board_size_H):
            for j in range(const.board_size_W):
                chess_board[i][j] = (int(sentence[const.board_size_W * i + j]))
                print(chess_board[i][j], end='')
            print()
        print("!!!!!!!!!!!!!!!!!!!!!!!!")



        print("已处理" + str(cnt) + "条\n")
        cnt += 1
        if cnt > 999 :
            cnt = 999

        # num = [cnt % 15 + 5, cnt % 15 + 5]

        num = place_where()
        print(num)
        s = str(num[0]) + "," + str(num[1])
        # print(s)
        connectionsocket.send(s.encode())
        connectionsocket.close()



def main():
    handle_connection()

main()


