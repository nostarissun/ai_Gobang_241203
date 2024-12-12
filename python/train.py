# import torch
import tkinter as tk
from tkinter import messagebox
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random


board_size = 20
#torch.float32
tensor = torch.zeros((1, board_size, board_size))

chess_board = []
for i in range(20):
    t = []
    for j in range(20):
        t.append(0)
    chess_board.append(t)
dir = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
begin_x = 20
begin_y = 20
end_x = 590
end_y = 590
cell_size = 30
r = 10
status = {
    0: 0,
    1: 100,
    2: 3000,
    3: 10000,
    4: 20000,
    5: 20000
}

def window():

    
    # 创建主窗口
    root = tk.Tk()
    root.title("Tkinter 示例")
    
    # 设置窗口的初始大小
    root.geometry("650x650+300+300")  # 宽度x高度
    canvas = tk.Canvas(root, width=650, height=650)
    canvas.pack()

        # 绘制垂直线
    for i in range(20):
        new_x = begin_x + cell_size * i
        canvas.create_line(new_x, begin_y, new_x, end_y, fill="black")
    # 绘制水平线
    for i in range(20):
        new_y = begin_y + cell_size * i
        canvas.create_line(begin_x, new_y, end_x, new_y, fill="black")


    for y0 in range(20):
        for x0 in range(20):
            y = begin_y + y0 * cell_size
            x = begin_x + x0 * cell_size
            if chess_board[y0][x0] == 1:
                canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")
            elif chess_board[y0][x0] == 2:
                canvas.create_oval(x - r, y - r, x + r, y + r, fill="white")


    
    current_player = 1  # 标记当前下棋方，1为黑棋，2为白棋
    game_ended = False
    while not game_ended:
        x, y = place_where()
        chess_board[y][x] = current_player
        y = begin_y + cell_size * y
        x = begin_x + cell_size * x
        color = "black" if current_player == 1 else "white"
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)
        game_ended = game_over(current_player, root)
        if game_ended:
            break
        current_player = 2 if current_player == 1 else 1
        
    
    
    root.mainloop()

def pop_window(parent, cur):
    # 创建一个Toplevel窗口作为弹出窗口
    win = tk.Toplevel(parent)
    win.title("胜负情况")
    win.geometry("200x100")  # 设置弹出窗口的大小

    # 在弹出窗口中添加一个标签
    if cur == 1:
        label = tk.Label(win, text="黑棋胜利!!!")
    else:
        label = tk.Label(win, text = "白棋胜利!!!")
    label.pack(pady=20)


    # win.after(3000, win.destroy)


def game_over(cur: int, parent):
    for y in range(20):
        for x in range(20):
            if chess_board[y][x] == cur:
                for k in dir:
                    cnt = 0
                    for i in range(5):
                        y1 = y + k[1] * i
                        x1 = x + k[0] * i
                        if y1 < 0 or y1 >= 20 or x1 < 0 or x1 >= 20:  # 防止越界
                            break
                        if chess_board[y1][x1]!= cur:
                            break
                        cnt += 1
                    if cnt == 5:
                        pop_window(parent, cur)
                        return True
    return False




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

    for d in dir:
        r = 0
        first_empty = -1
        for chess_cnt in range(0, 5):
            y = y0 + d[1] * chess_cnt
            x = x0 + d[0] * chess_cnt
            if x >= 20 or x < 0 or y >= 20 or y < 0:
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
    score += status[max_cnt]
    return score




def compare_scores(item1, item2):
    """
    用于比较两个元组中第一个元素（得分）大小的函数
    返回值为：
    - 若 item1 的得分大于 item2 的得分，返回 1
    - 若 item1 的得分小于 item2 的得分，返回 -1
    - 若二者得分相等，返回 0
    """
    score1 = item1[0]
    score2 = item2[0]
    if score1 > score2:
        return 1
    elif score1 < score2:
        return -1
    return 0


def place_where():
    scores = []  # 用于存储每个空白位置的得分以及对应的坐标
    global chess_board
    center_score = 20

    for r in range(20):
        for c in range(20):
            if chess_board[r][c]!= 0:
                continue
            score = center_score - abs(10 - r) - abs(10 - c) + get_evaluate(r, c)
            scores.append((score, (c, r)))  # 将得分和坐标作为元组存入列表

    # 使用自定义的比较函数对scores列表进行排序，实现按照得分从高到低排序
    for i in range(len(scores) - 1):
        for j in range(len(scores) - i - 1):
            if compare_scores(scores[j], scores[j + 1]) < 0:
                scores[j], scores[j + 1] = scores[j + 1], scores[j]

    ten_scores = scores[:3]  # 取前十个得分最高的位置（如果不足十个则取全部）
    if len(ten_scores) == 0:
        return []  # 如果没有可落子的空白位置，返回空列表

    choice = random.randint(0, len(ten_scores) - 1)  # 随机选择一个索引
    return list(ten_scores[choice][1])  # 返回选中位置的坐标（转换为列表形式）












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
        self.fc1 = nn.Linear(64 * (board_size // 4) * (board_size // 4), 128)
        #第三次引入非线性因素
        self.relu3 = nn.ReLU()
        #第二个全连接层
        self.fc2 = nn.Linear(128, board_size * board_size)

    #前向传播
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)

        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        return x
    


def select_move(model, board_state, temperature=1.0):
    """
    根据模型输出的概率分布选择走法
    model: 五子棋模型
    board_state: 当前棋盘状态张量，形状为(1, board_size, board_size)
    temperature: 温度参数，用于控制采样的随机性，温度越高越随机，越低越偏向确定性选择
    :return: 走法坐标
    """
    with torch.no_grad():
        output = model(board_state)
        output = output.squeeze(0).flatten()  # 转换为一维概率向量
                # 创建一个掩码，排除已下棋的位置

        # 根据温度参数调整概率分布
        # 根据 temperature 参数的值来分情况处理走法选择的逻辑。temperature 参数用于控制选择走法的随机性程度，
        # 当它大于 0 时，采用一种基于概率采样的方式来选择走法，使得选择具有一定随机性，更有利于探索不同的走法可能性，
        # 尤其在训练早期探索更多不同走法对模型学习更全面的策略有帮助。
        if temperature > 0:
            # 在这里，先将 output 除以 temperature，temperature 的作用类似一个缩放因子，
            # 温度越高，经过 softmax 后得到的概率分布越 “平缓”，意味着各个位置被选中的概率相对更均匀，随机性就越大；温度越低，概率分布越 “尖锐”，
            # 模型认为最优的几个位置的概率就会占比极大，随机性就越小，更偏向于确定性地选择模型认为最好的走法。
            probs = torch.softmax(output / temperature, dim=0).cpu().numpy()
            move_index = np.random.choice(len(probs), p=probs)
        else:
            move_index = torch.argmax(output).item()

        row = move_index // model.board_size
        col = move_index % model.board_size

    return row, col
    
def update_board_state(board_state, move, chess):
    """
    根据走法更新棋盘状态张量
    param board_state: 当前棋盘状态张量
    param move: 走法坐标（行，列）
    chess: 棋子颜色（如1表示黑棋，2表示白棋）
    return: 更新后的棋盘状态张量
    """
    row, col = move
    board_state[0][row][col] = chess
    return board_state
    

def is_game_over(board_state, board_size):
    """
    判断五子棋棋局是否结束
    :param board_state: 棋盘状态张量
    :param board_size: 棋盘大小
    :return: 是否结束（True/False）以及获胜方（None表示未结束或平局，1表示黑棋胜，2表示白棋胜）
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for row in range(board_size):
        for col in range(board_size):
            if board_state[0][row][col]!= 0:
                piece_color = board_state[0][row][col]
                for direction in directions:
                    count = 1
                    for step in range(1, 5):
                        new_row = row + step * direction[0]
                        new_col = col + step * direction[1]
                        if 0 <= new_row < board_size and 0 <= new_col < board_size and board_state[0][new_row][new_col] == piece_color:
                            count += 1
                        else:
                            break
                    if count >= 5:
                        return True, piece_color

    if (board_state == 0).sum() == 0:  # 棋盘已满判断平局
        return True, None

    return False, None


def calculate_reward(result, chess, x):
    """
    根据棋局结果和执子方计算奖励
    result: 棋局结果（None表示未结束或平局，1表示黑棋胜，2表示白棋胜）
    piece_color: 执子方棋子颜色（如1表示黑棋，2表示白棋）
    return: 奖励值
    """
    if result == chess:
        return 1 * x
    elif result is None:
        return 0
    else:
        return -1 * x
    

def update_model(model, optimizer, board_states, actions, rewards):
    """
    根据奖励更新模型参数
    model: 五子棋模型
    optimizer: 优化器（如Adam等）
    board_states: 整个棋局过程中的棋盘状态张量列表
    actions: 整个棋局过程中的走法坐标列表
    rewards: 对应的奖励值列表
    :return:
    """
    optimizer.zero_grad()
    loss = 0
    for board_state, action, reward in zip(board_states, actions, rewards):
        output = model(board_state)
        row, col = action
        action_index = row * model.board_size + col
        target = torch.zeros_like(output).squeeze(0).flatten()
        target[action_index] = reward
        loss += ((output.squeeze(0).flatten() - target) ** 2).sum()

    loss.backward()
    optimizer.step()


#白棋
def play_with_gambling(model, board_size, learning_rate, num_games):
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for _ in range(num_games):
        board_state = torch.tensor(chess_board).reshape(1, 20, 20)
        game_over = False
        board_states_list = []
        actions_list = []
        rewards_list = []

        while not game_over:
            x, y = place_where()
            board_states_list.append(board_state.clone())
            actions_list.append([y, x])
            board_state = update_board_state(board_state, [y, x], 1)


            #确定走法
            move = select_move(model, board_state)
            #将每一步棋走动时的棋盘记录下来，并避免使用引用
            board_states_list.append(board_state.clone())
            #记录每一步的走法
            actions_list.append(move)            
            board_state = update_board_state(board_state, move, 2)


            game_over, result = is_game_over(board_state, board_size)

            #一局结束分配奖励
            if game_over:
                reward = calculate_reward(result, 2, 3)
                rewards_list.append(reward)
                if result == 2:
                    update_model(model, optimizer, board_states_list, actions_list, rewards_list)

    return model


def self_play(model_black, model_white, board_size, num_games, learning_rate):
    """
    执行自我博弈过程并更新模型
    model_black: 代表黑棋的模型
    model_white: 代表白棋的模型
    board_size: 棋盘大小
    num_games: 自我博弈的局数
    learning_rate: 学习率
    :return:
    """
    #创建 Adam 优化器
    #将模型中所有可学习的参数传递给优化器
    optimizer_black = optim.Adam(model_black.parameters(), lr=learning_rate)
    optimizer_white = optim.Adam(model_white.parameters(), lr=learning_rate)

    for _ in range(num_games):
        board_state = torch.tensor(chess_board).reshape(1, 20, 20)
        game_over = False
        current_color = 1  # 黑棋先下，用1表示
        board_states_list = []
        actions_list = []
        rewards_list = []

        while not game_over:

            #选择下旗方
            if current_color == 1:
                model = model_black
            else:
                model = model_white

            #确定走法
            move = select_move(model, board_state)
            #将每一步棋走动时的棋盘记录下来，并避免使用引用
            board_states_list.append(board_state.clone())
            #记录每一步的走法
            actions_list.append(move)

            board_state = update_board_state(board_state, move, current_color)
            game_over, result = is_game_over(board_state, board_size)


            #一局结束分配奖励
            if game_over:
                reward = calculate_reward(result, current_color, 1)
                rewards_list.append(reward)
                if result == 1:
                    update_model(model_black, optimizer_black, board_states_list, actions_list, rewards_list)
                elif result == 2:
                    update_model(model_white, optimizer_white, board_states_list, actions_list, rewards_list)
            else:
                current_color = 3 - current_color  # 切换棋子颜色

    return model_black, model_white


def main():

    board_size = 20
    num_games = 1000
    learning_rate = 0.001
    #每十轮与博弈算法进行一次对弈
    model_black = GoBang_Model(board_size)
    model_white = GoBang_Model(board_size)

    i = 0
    while i <= num_games:
        if i % 10 == 0:
            play_with_gambling(model_white, board_size, learning_rate, 1)
            i += 1
        else:
            model_black, model_white = self_play(model_black, model_white, board_size, 9, learning_rate)
            i += 9

    torch.save(model_black, 'model_black_full.pth')
    torch.save(model_white, 'model_white_full.pth')



main()
