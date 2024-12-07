import const
import socket


# 下白棋
# 黑棋是1， 白棋是2
# chess_board = [[0] * const.board_size_W] * const.board_size_W
chess_board = []
for i in range(const.board_size_H):
    t = []
    for j in range(const.board_size_W):
        t.append(0)
    chess_board.append(t)



def get_evaluate(r: int, c: int) -> int:
    global chess_board
    cnt2 = [0, 0, 0, 0, 0, 0 ,0, 0]
    cnt1 = [0, 0, 0, 0, 0, 0 ,0, 0]
    idx = 0
    for dir in const.dir:
        for i in range(1, 9):
            r1 = r + dir[1] * i
            c1 = c + dir[0] * i

            if c1 >= const.board_size_W or c1 < 0 or r1 >= const.board_size_H or r1 < 0 :
                break
            # if not (0 <= r1 < len(chess_board) and 0 <= c1 < len(chess_board[0])):
            #     print(x1)
            #     print(y1)
            #     exit(0)
            if chess_board[r1][c1] == 1 or chess_board[r1][c1] == 0 :
                if chess_board[r1][c1] == 1 :
                    cnt1[idx] += 1
                break
            if chess_board[r1][c1] == 2:
                cnt2[idx] += 1
        
        idx += 1

    res = 0
    for i in range(4):
        t1 = cnt1[i] + cnt1[i + 4]
        t2 = cnt2[i] + cnt2[i + 4]
        res = max(res, const.status[t2][t1])

    return res


def place_where():
    pos = []
    res = float('-inf')
    global chess_board


    # for i in range(const.board_size_H):
    #     for j in range(const.board_size_W):
    #         print(chess_board[i][j], end='')
    #     print()
    # print("!!!!!!!!!!!!!!!!!!!!!!!!")

    for r in range(const.board_size_H):
        for c in range(const.board_size_W):
            if chess_board[r][c] == 0 and res < get_evaluate(r, c):
                res = get_evaluate(r, c)
                pos = [r, c]
            # if chess_board[r][c] == 0:
            #     return [r, c]
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


