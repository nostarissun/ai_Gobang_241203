import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import

class GoBang_Model(nn.Module):

    #模型初始化
    def __init__(self, board_size):
        super(GoBang_Model, self).__init__()
        self.board_size = board_size
        #第一个卷积层
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        #第一次增加非线性因素
        self.relu1 = nn.ReLU()
        #第一个池化层
        self.pool1 = nn.MaxPool2d(2)
        #第二个卷积层
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        #第二次增加非线性因素
        self.relu2 = nn.ReLU()
        #第二个池化层
        self.pool2 = nn.MaxPool2d(2)
        #第一个全连接层
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
                    for step in range(1, 5):
                        new_row = row - step * direction[0]
                        new_col = col - step * direction[1]
                        if 0 <= new_row < board_size and 0 <= new_col < board_size and board_state[0][new_row][new_col] == piece_color:
                            count += 1
                        else:
                            break
                    if count >= 5:
                        return True, piece_color

    if (board_state == 0).sum() == 0:  # 棋盘已满判断平局
        return True, None

    return False, None


def calculate_reward(result, chess):
    """
    根据棋局结果和执子方计算奖励
    :param result: 棋局结果（None表示未结束或平局，1表示黑棋胜，2表示白棋胜）
    :param piece_color: 执子方棋子颜色（如1表示黑棋，2表示白棋）
    :return: 奖励值
    """
    if result == chess:
        return 1
    elif result is None:
        return 0
    else:
        return -1
    

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



def self_play(model_black, model_white, board_size, num_games, learning_rate=0.001):
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
        board_state = torch.zeros((1, board_size, board_size))
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
                reward = calculate_reward(result, current_color)
                rewards_list.append(reward)
                if result == 1:
                    update_model(model_black, optimizer_black, board_states_list, actions_list, rewards_list)
                elif result == 2:
                    update_model(model_white, optimizer_white, board_states_list, actions_list, rewards_list)
            else:
                current_color = 3 - current_color  # 切换棋子颜色

    return model_black, model_white


if __name__ == "__main__":

    board_size = 20
    num_games = 1000
    learning_rate = 0.001

    # model_black_loaded_full = torch.load('model_black_full.pth')
    # model_white_loaded_full = torch.load('model_white_full.pth')
    #     #确保相同输入，相同输出
    # model_black_loaded_full.eval()
    # model_white_loaded_full.eval()
    
    model_black = GoBang_Model(board_size)
    model_white = GoBang_Model(board_size)

    model_black, model_white = self_play(model_black, model_white, board_size, num_games, learning_rate)


    torch.save(model_black, 'model_black_full.pth')
    torch.save(model_white, 'model_white_full.pth')


    
