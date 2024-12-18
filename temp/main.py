import mcts_alphaZero as mcts
import socket

# from game import Game, Board

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
        all = connectionsocket.recv(1024).decode()
        record = all.split(',')
        last_move = int(record[0])
        sentence = record[1]
        # 检查接收到的数据长度是否符合预期
        # length = 12 * 12
        # if len(sentence) != length:
        #     print("接收到的数据长度不正确，请重新发送" + str(len(sentence)))
        #     print(sentence)
        #     # connectionsocket.send(error_message.encode())
        #     # connectionsocket.close()
        #     continue
        
        chess_board = []
        for i in range(12):
            t = []
            for j in range(12):
                t.append(0)
            chess_board.append(t)
        
        for i in range(12):
            for j in range(12):
                chess_board[i][j] = (int(sentence[12 * i + j]))
                print(chess_board[i][j], end='')
            print()
        print("!!!!!!!!!!!!!!!!!!!!!!!!")

        board, available = chess_board_to_standard(chess_board)


        print("已处理" + str(cnt) + "条\n")
        cnt += 1
        if cnt > 999 :
            cnt = 999

        # num = [cnt % 15 + 5, cnt % 15 + 5]

        num = get_res(board, available,last_move)

        print(num)
        # s = str(num // 12) + "," + str(num % 12)
        # print(s)
        s = str(num)
        #go y / x
        connectionsocket.send(s.encode())
        connectionsocket.close()

def chess_board_to_standard(chess_board):
    res = {}
    availables = list(range(12 * 12))
    for i in range(12):
        for j in range(12):
            if chess_board[i][j] != 0:
                res[i * 12 + j] = chess_board[i][j]
                availables.remove(i * 12 + j)
    return res, availables

def get_res(board, available, last_move):

    
    mct = mcts.MCTSPlayer(board, available, last_move, 5, 400, 0)
    return mct.get_action(temp=1e-3, return_prob=0)


handle_connection()
# a = list(range(12 * 12))
# a.remove(12)
# print(get_res({12 : 1}, a, 12))