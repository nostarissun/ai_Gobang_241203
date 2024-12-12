import const
import socket


class GoBang_Model(nn.Module):

    #模型初始化
    def __init__(self, board_size):
        super(GoBang_Model, self).__init__()
        self.board_size = board_size
        #第一个卷积层输入1通道，输出32通道，卷积核大小为3，填充大小1
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        #第一次增加非线性因素
        self.relu1 = nn.ReLU()
        #第一个池化层使用2x2的池化核，步长为2
        self.pool1 = nn.MaxPool2d(2)
        #第二个卷积层
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        #第二次增加非线性因素
        self.relu2 = nn.ReLU()
        #第二个池化层
        self.pool2 = nn.MaxPool2d(2)
        #第一个全连接层
        #输出特征数量设置为 128，两个池化层//4
        # print(board_size)
        # print("fc1:", 64 * (board_size // 4) * (board_size // 4))
        self.fc1 = nn.Linear(64 * (board_size // 4) * (board_size // 4), 128)
        #第三次引入非线性因素
        self.relu3 = nn.ReLU()
        #第二个全连接层
        self.fc2 = nn.Linear(128, board_size * board_size)

    #前向传播
    def forward(self, x):
        # print("Input shape:", x.shape)  # 打印输入形状
        x = self.conv1(x)
        # print("After conv1:", x.shape)  # 打印第一个卷积层后的形状
        x = self.relu1(x)
        x = self.pool1(x)
        # print("After pool1:", x.shape)  # 打印第一个池化层后的形状
        x = self.conv2(x)
        # print("After conv2:", x.shape)  # 打印第二个卷积层后的形状
        x = self.relu2(x)
        x = self.pool2(x)
        # print("After pool2:", x.shape)  # 打印第二个池化层后的形状
        x = x.view(1, -1)
        # print("After flatten:", x.shape)  # 打印展平后的形状
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        return x
    


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
