import mcts_alphaZero as mcts
import socket
import policy_value_net_pytorch as pvn
from game import Game, Board

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
        length = 12 * 12
        if len(sentence) != length:
            print("接收到的数据长度不正确，请重新发送" + str(len(sentence)))
            print(sentence)
            # connectionsocket.send(error_message.encode())
            # connectionsocket.close()
            continue


        for i in range(12):
            for j in range(12):
                chess_board[i][j] = (int(sentence[12 * i + j]))
                print(chess_board[i][j], end='')
            print()
        print("!!!!!!!!!!!!!!!!!!!!!!!!")



        print("已处理" + str(cnt) + "条\n")
        cnt += 1
        if cnt > 999 :
            cnt = 999

        # num = [cnt % 15 + 5, cnt % 15 + 5]

        num = get_res()

        print(num)
        s = str(num // 12) + "," + str(num % 12)
        # print(s)

        #go y / x
        connectionsocket.send(s.encode())
        connectionsocket.close()


def get_res():
    board = Board(width=20,
                    height=20,
                    n_in_row=5)
    game = Game(board)
    net = pvn.PolicyValueNet(12, 12, './best_policy.model')
    mct = mcts.MCTSPlayer(net.policy_value_fn, 5, 400, 0)
    return mct.get_action(board)


handle_connection()