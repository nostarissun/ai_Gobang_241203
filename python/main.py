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


def best_pos():
    global chess_board
    pos = [0, 0]
    score = 0
    for y in range(const.board_size_H):
        for x in range(const.board_size_W):
            if chess_board[y][x] == 0:
                #尝试在当前位置下白棋
                chess_board[y][x] = 2
                new_score = dfs(1)
                chess_board[y][x] = 0
                if new_score >= score:
                    score = new_score
                    pos[0] = x
                    pos[1] = y
    return pos



def dfs(depth):
    global chess_board
    # print("第%d层"%depth)
    score = 0

    if game_over(2, 1):
        return 100000

    if depth == 0:
        # print("!!!!!!!!!!!!!!!!")
        return get_situation(2)

    enemy_y, enemy_x = place_where()
    chess_board[enemy_y][enemy_x] = 1
    # if game_over(1):
    #     return 0
    y, x = place_where()
    chess_board[y][x] = 2

    new_score = dfs(depth - 1)
    if new_score >= score:
        score = new_score
    chess_board[y][x] = 0


    chess_board[enemy_y][enemy_x] = 0
    return score


def game_over(friend: int, enemy: int):
    global chess_board
    vis = []
    for i in range(const.board_size_H):
        t = []
        for j in range(const.board_size_W):
            t.append(False)
        vis.append(t)

    for y0 in range(const.board_size_H):
        for x0 in range(const.board_size_W):
            if chess_board[y0][x0] == friend:
                for i in range(4):
                    cnt = 0
                    y1 = y0 + const.dir[i][1]
                    x1 = x0 + const.dir[i][0]
                    y2 = y0 + const.dir[i + 4][1]
                    x2 = x0 + const.dir[i + 4][0]
                    can1 = True
                    can2 = True
                while can1 == True or can2 == True and y1 < const.board_size_H and y2 <= y1 and y1 >= 0 and y2 >= 0 and x1 >= 0 and x2 >= 0 and x1 < const.board_size_W and x2 <= x1:
                    if cnt == 5:
                        break
                    if chess_board[y1][x1] == friend:
                        cnt += 1
                        vis[y1][x1] = True
                    elif chess_board[y1][x1] == enemy:
                        can1 = False
                    if chess_board[y2][x2] == enemy:
                        can2 = False
                    elif chess_board[y2][x2] == friend:
                        cnt += 1
                        vis[y2][x2] = True
    return  False


def get_situation(cur: int):
    global chess_board

    enemy = 0
    if cur == 1:
        enemy = 2
    else:
        enemy = 1


    vis = []
    for i in range(const.board_size_H):
        t = []
        for j in range(const.board_size_W):
            t.append(False)
        vis.append(t)

    enemy_score = 0
    friend_score = 0
    for y0 in range(const.board_size_H):
        for x0 in range(const.board_size_W):
            enemy_cnt = 0
            friend_cnt = 0
            if chess_board[y0][x0] != 0:
                for dir in const.dir:
                    if chess_board[y0][x0] == cur:
                        for k in range(6):
                            y = y0 + dir[1] * k
                            x = x0 + dir[0] * k
                            if y >= 0 and x >= 0 and y < const.board_size_H and x < const.board_size_W:
                                if vis[y][x] == True:
                                    break

                                if chess_board[y][x] == cur:
                                    friend_cnt += 1
                                    vis[y][x] = True
                                elif chess_board[y][x] == enemy:

                                    break
                                else:
                                    friend_cnt += 0.75
                                    vis[y][x] = True

                    elif chess_board[y0][x0] == enemy:
                        for k in range(6):
                            y = y0 + dir[1] * k
                            x = x0 + dir[0] * k
                            if y >= 0 and x >= 0 and y < const.board_size_H and x < const.board_size_W:
                                if vis[y][x] == True:
                                    break

                                if chess_board[y][x] == cur:
                                    friend_cnt += 1
                                    vis[y][x] = True
                                elif chess_board[y][x] == enemy:
                                    break
                                else:
                                    friend_cnt += 0.75
                                    vis[y][x] = True
            if enemy_cnt == 2:
                enemy_score += 10
            elif enemy_cnt == 3:
                enemy_score += 100
            elif enemy_cnt == 4:
                enemy_score += 1000

            if friend_cnt == 2:
                friend_score += 10
            elif friend_cnt == 3:
                friend_score += 100
            elif friend_cnt == 4:
                friend_score += 1000

    return friend_score - enemy_score








def get_evaluate(r : int,  c: int):
    #分别判断下在此处我方和敌方的得分
    #最大化我方得分，抢占敌方最优位置
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
                # print("%-5s" % "0", end = ' ')
                continue

            score = center_score - abs(const.CENTER_X - r) - abs(const.CENTER_Y - c) + get_evaluate(r, c)

            # print("%-5s" % score, end = ' ')

            if res < score:
                res = score
                pos = [r, c]
        # print()

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





        # num = [cnt % 15 + 5, cnt % 15 + 5]

        #先发y再发x
        num = best_pos()
        print(num)
        s = str(num[1]) + "," + str(num[0])
        # print(s)

        print("已处理" + str(cnt) + "条\n")
        cnt += 1
        if cnt > 999 :
            cnt = 999

        connectionsocket.send(s.encode())
        connectionsocket.close()



def main():
    handle_connection()

main()


