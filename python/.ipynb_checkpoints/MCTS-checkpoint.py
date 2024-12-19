import numpy as np
import copy


def to_probs(x):
    """
    先将x整体缩小，避免指数运算溢出
    转化为概率分布
    """
    p = np.exp(x - np.max(x))
    p /= np.sum(p)
    return p


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

    def new_child(self, action_priors):
        '''
        生成新的子节点,传入各个动作及概率
        '''
        for action, prob in action_priors:
            if action not in self._children:
                self._children[action] = TreeNode(self, prob)

    def select(self, c_puct):
        """
        选择新节点
        """
        mv = float('inf')
        best_act_node = None
        for act, node in self._children.items():
            new_v = node.get_value(c_puct)
            if new_v > mv:
                mv = new_v
                best_act_node = (act, node)
        return best_act_node
    
    def get_value(self, c_puct):
        """
        计算当前节点的探索价值，通过系数调节先验概率权重，开平方避免次数过大，作商以减少频繁访问同一个节点，增强探索性
        """
        self._u = (c_puct * self._P *
                    np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def update(self, leaf_value):
        '''
        移动平均原理：
        移动平均的基本思想是在不断获取新的数据时，通过合理的加权计算，
        使得估计值能够逐渐 “跟上” 数据的变化趋势，同时又不会因为单次新数据的波动而产生过大的偏差，能够平滑地反映整体的平均水平
'''
        
     
        self._n_visits += 1

        self._Q += 1.0*(leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):
        """
        递归更新所有父节点的Q
        """
     
        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)



    def is_leaf(self):
        return self._children == {}

    def is_root(self):
        return self._parent is None


class MCTS(object):


    def __init__(self, policy_value_fn, c_puct=5, n_playout=10000):
        """
        policy_value_fn: 
        n_playout: 模拟次数
        c_puct: 用来控制依赖先验概率的程度
        """
        self._root = TreeNode(None, 1.0)
        self._policy = policy_value_fn
        self._c_puct = c_puct
        self._n_playout = n_playout

    def _playout(self, state):
        """
        从‘根’节点开始，直接遍历到叶子节点，代表当前情况下的游戏状态为结束
        """
        node = self._root
        while(1):
            if node.is_leaf():
                break
        
            action, node = node.select(self._c_puct)
            state.do_move(action)

        
        action_probs, leaf_value = self._policy(state)
        end, winner = state.game_end()
        if not end:
            node.expand(action_probs)
        else:

            if winner == -1:  # tie
                leaf_value = 0.0
            else:
                leaf_value = (
                    1.0 if winner == state.get_current_player() else -1.0
                )

        node.update_recursive(-leaf_value)

    def get_move_probs(self, state, temp=1e-3):
        """

        """
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)


        act_visits = [(act, node._n_visits)
                      for act, node in self._root._children.items()]
        acts, visits = zip(*act_visits)
        act_probs = to_probs(1.0 / temp * np.log(np.array(visits) + 1e-10))

        return acts, act_probs

    def update_with_move(self, last_move):

        if last_move in self._root._children:
            self._root = self._root._children[last_move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, 1.0)




class MCTSPlayer(object):
    '''ai玩家：使用MCTS进行决策'''

    def __init__(self, policy_value_function,
                 c_puct=5, n_playout=2000, is_selfplay=0):
        
        #创建一颗MCTS树
        self.mcts = MCTS(policy_value_function, c_puct, n_playout)
        self._is_selfplay = is_selfplay

    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, board, temp=1e-3, return_prob=0):
        #保存可移动的位置
        can_moves_pos = board.availables
        #记录动作概率
        move_probs = np.zeros(board.width * board.height)

        if len(can_moves_pos) > 0:
            acts, probs = self.mcts.get_move_probs(board, temp)
            #将可用动作和对应概率整合成一个变量
            move_probs[list(acts)] = probs
            if self._is_selfplay:
                '''加入狄利克雷噪声，增加随机性，避免过拟合'''
                move = np.random.choice(
                    acts,
                    p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                )

                self.mcts.update_with_move(move)
            else:

                move = np.random.choice(acts, p=probs)
                self.mcts.update_with_move(-1)

            if return_prob:
                return move, move_probs
            else:
                return move

