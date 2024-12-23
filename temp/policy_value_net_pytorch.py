import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np


def set_learning_rate(optimizer, lr):
    '''设置学习率'''
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


class Net(nn.Module):
    def __init__(self, board_width, board_height):
        super(Net, self).__init__()

        self.last_move = -1

        self.board_width = board_width
        self.board_height = board_height
        '''公共卷积层：棋盘数据
        输入通道数 分别记录我方棋局，敌方棋盘数据，上一步的移动情况，是不是我方回合
        输出通道数
        卷积核大小
        填充参数'''
        self.conv1 = nn.Conv2d(4, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)

        '''动作策略卷积层'''
        self.act_conv1 = nn.Conv2d(128, 4, kernel_size=1)
        '''全连接层'''
        self.act_fc1 = nn.Linear(4 * board_width * board_height,
                                 board_width*board_height)
        
        '''价值评估卷积层'''
        self.val_conv1 = nn.Conv2d(128, 2, kernel_size=1)
        '''全连接层'''
        self.val_fc1 = nn.Linear(2 * board_width * board_height, 64)
        self.val_fc2 = nn.Linear(64, 1)

    def forward(self, state_input):

        #添加线性修正单元
        x = F.relu(self.conv1(state_input))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
       
        x_act = F.relu(self.act_conv1(x))
        #重塑张量形状
        x_act = x_act.view(-1, 4 * self.board_width * self.board_height)
        #将动作概率转化为对数形式，避免积过大
        x_act = F.log_softmax(self.act_fc1(x_act))
        
        x_val = F.relu(self.val_conv1(x))
        x_val = x_val.view(-1, 2 * self.board_width * self.board_height)
        x_val = F.relu(self.val_fc1(x_val))
        #将数据压缩至（-1，1）
        x_val = F.tanh(self.val_fc2(x_val))
        return x_act, x_val


class PolicyValueNet():
   
    def __init__(self, board, availables, last_move, board_width, board_height, model_file=None, use_gpu=False):
        self.use_gpu = use_gpu
        self.board_width = board_width
        self.board_height = board_height
        #设置l2正则化系数，防止过拟合
        self.l2_const = 1e-4  
        self.board = board
        self.availables = availables
        self.last_move = last_move
        if self.use_gpu:
            self.policy_value_net = Net(board_width, board_height).cuda()
        else:
            self.policy_value_net = Net(board_width, board_height)
            #采用adam优化器
        self.optimizer = optim.Adam(self.policy_value_net.parameters(), weight_decay=self.l2_const)

        if model_file:
            net_params = torch.load(model_file)
            self.policy_value_net.load_state_dict(net_params)

    def policy_value(self, state_batch):
        if self.use_gpu:
            state_batch = Variable(torch.FloatTensor(state_batch).cuda())
            log_act_probs, value = self.policy_value_net(state_batch)
            act_probs = np.exp(log_act_probs.data.cpu().numpy())
            return act_probs, value.data.cpu().numpy()
        else:
            state_batch = Variable(torch.FloatTensor(state_batch))
            log_act_probs, value = self.policy_value_net(state_batch)
            act_probs = np.exp(log_act_probs.data.numpy())
            return act_probs, value.data.numpy()



    def get_current_state(self):

        width = self.board_width
        height = self.board_height
        state = np.zeros((4, width, height))
        if self.board:
            moves, players = np.array(list(zip(*self.board.items())))
            move_curr = moves[players == 2]
            move_oppo = moves[players != 1]
            state[0][move_curr // width,
                            move_curr % height] = 1.0
            state[1][move_oppo // width,
                            move_oppo % height] = 1.0
            
            state[2][self.last_move // width,
                            self.last_move % height] = 1.0
        if len(self.board) % 2 == 0:
            state[3][:, :] = 1.0  
        return state




    def policy_value_fn(self, board, availables):

        legal_positions = availables
        #先转化成四维数组并确保内存存储连续，以转化成张量
        current_state = np.ascontiguousarray(self.get_current_state().reshape(-1, 4, self.board_width, self.board_height))
        if self.use_gpu:
            log_act_probs, value = self.policy_value_net(Variable(torch.from_numpy(current_state)).cuda().float())
            act_probs = np.exp(log_act_probs.data.cpu().numpy().flatten())
            value = value.data.cpu().numpy()[0][0]
        else:
            log_act_probs, value = self.policy_value_net(Variable(torch.from_numpy(current_state)).float())
            act_probs = np.exp(log_act_probs.data.numpy().flatten())
            value = value.data.numpy()[0][0]

        act_probs = zip(legal_positions, act_probs[legal_positions])
        return act_probs, value


