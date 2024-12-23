import numpy as np
import copy
import policy_value_net_pytorch as pvn

def softmax(x):
    """
    先将x整体缩小，避免指数运算溢出
    转化为概率分布
    """
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs


class TreeNode(object):
    """
    MCTS关于每一个结点的一些操作
    """
    def __init__(self, parent, prior_p):
        """
        记录当前节点的相关信息
        """
        self._parent = parent
        self._children = {}  
        self._n_visits = 0
        self._Q = 0
        self._u = 0
        self._P = prior_p

    def expand(self, action_priors):
        '''
        生成新的子节点,传入各个动作及概率
        '''
        for action, prob in action_priors:
            if action not in self._children:
                self._children[action] = TreeNode(self, prob)

    def select(self, c_puct):
        return max(self._children.items(),
                   key=lambda act_node: act_node[1].get_value(c_puct))

    def update(self, leaf_value):

        self._n_visits += 1

        self._Q += 1.0*(leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):

        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):
        """
        计算当前节点的探索价值，通过系数调节先验概率权重，开平方避免次数过大，作商以减少频繁访问同一个节点，增强探索性
        """

        self._u = (c_puct * self._P *
                   np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def is_leaf(self):

        return self._children == {}

    def is_root(self):
        return self._parent is None


class MCTS(object):


    def __init__(self, board, availables, last_move, c_puct=5, n_playout=10000):
        """
        policy_value_fn: 
        n_playout: 模拟次数
        c_puct: 用来控制依赖先验概率的程度
        """
        self.board = board
        self.availables = availables
        self.last_move = last_move
        self._root = TreeNode(None, 1.0)
        # self._policy = policy_value_fn
        self._c_puct = c_puct
        self._n_playout = n_playout
      

    def _playout(self, state, availables):
        """
        从‘根’节点开始，直接遍历到叶子节点，代表当前情况下的游戏状态为结束
        """
        node = self._root
        while(1):
            if node.is_leaf():
                print("shi")
                break
            action, node = node.select(self._c_puct)
            print(action)
            if action in state:
                continue
            self.do_move(action, state, availables) 
            

        
        net = pvn.PolicyValueNet(state, availables, self.last_move, 12, 12, './best_policy.model')
        
        action_probs, leaf_value = net.policy_value_fn(state, availables)
        
        
        end, winner = self.is_end(state)
        if not end:
            node.expand(action_probs)
        else:
          
            if winner == -1: 
                leaf_value = 0.0
            else:
                leaf_value = (
                    1.0 if winner == 2 else -1.0  #这里
                )


        node.update_recursive(-leaf_value)

    def do_move(self, action, state, availables):
        '''默认ai移动白棋'''
        state[action] = 2
        availables.remove(action)


    def is_end(self, states):

        width = 12
        height = 12
      
        n = 5

        moved = list(set(range(width * height)) - set(self.availables))
        if len(moved) < 5 *2-1:
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
        
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1
        
    def get_move_probs(self, state, temp=1e-3):

        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            availables_copy = copy.deepcopy(self.availables)
            self._playout(state_copy, availables_copy)
        #获取所有的动作极其概率
        act_visits = [(act, node._n_visits)
                      for act, node in self._root._children.items()]
        #解包，将二者分离
        acts, visits = zip(*act_visits)
        #1e-10避免出现零，temp温度参数
        act_probs = softmax(1.0/temp * np.log(np.array(visits) + 1e-10))

        return acts, act_probs

    def update_with_move(self, last_move):

        if last_move in self._root._children:
            self._root = self._root._children[last_move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, 1.0)




class MCTSPlayer(object):

    '''ai玩家：使用MCTS进行决策'''
    def __init__(self, board, available, last_move, c_puct=5, n_playout=2000, is_selfplay=0):
        self.board = board
        self.availables = available
        self.last_move = last_move
        #创建一颗MCTS树
        self.mcts = MCTS(self.board, self.availables, self.last_move, c_puct, n_playout)
        self._is_selfplay = is_selfplay


    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, temp=1e-3, return_prob=0):
         #保存可移动的位置
        sensible_moves = self.availables  
        #记录动作概率
        move_probs = np.zeros(12 * 12)
        if len(sensible_moves) > 0:
            acts, probs = self.mcts.get_move_probs(self.board, temp)
            move_probs[list(acts)] = probs
            #概率转权重，随机避免局部最优
            move = np.random.choice(acts, p=probs)
            # move = np.max(acts)
            self.mcts.update_with_move(-1)


            if return_prob:
                return move, move_probs
            else:
                return move







