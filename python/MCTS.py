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
        # If it is not root, this node's parent should be updated first.
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

    def __str__(self):
        return "MCTS"


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
                '''0.75*probs：这部分将原始的动作概率列表 probs 中的每个概率值都乘以 0.75。其目的是保留大部分（这里是 75% 的权重）基于 MCTS 搜索得到的原始概率信息，
                体现了对已有搜索经验和评估结果的一定依赖，使得选择的动作依然在一定程度上倾向于那些过往模拟搜索认为比较好的动作。
                0.25*np.random.dirichlet(0.3*np.ones(len(probs)))：
                np.random.dirichlet(0.3*np.ones(len(probs)))：这是生成狄利克雷噪声的关键部分。
                np.random.dirichlet 函数用于生成符合狄利克雷分布的随机向量，其参数 0.3*np.ones(len(probs)) 表示狄利克雷分布的浓度参数（concentration parameter）。
                这里创建了一个长度与可用动作数量（即 len(probs)）相同的向量，每个元素都是 0.3，以此作为狄利克雷分布的参数。
                生成的随机向量的每个元素都在 (0, 1) 区间内，且所有元素之和为 1，这个随机向量就代表了一种随机的概率分布情况，也就是所谓的狄利克雷噪声。
                通过添加这种噪声，可以为每个可用动作引入一定的随机性，鼓励探索那些原本按照纯 MCTS 搜索可能概率较低、不太会被选择，但实际上可能具有潜在价值的动作，避免模型陷入局部最优策略。
                前面乘以 0.25 则是确定了狄利克雷噪声在最终混合概率中所占的权重，即给这个随机的概率分布赋予了 25% 的权重，与前面 0.75*probs 中的 75% 权重相结合，共同构成了最终用于选择动作的混合概率。'''
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
        # else:
        #     print("WARNING: the board is full")
    '''__str__ 是一个特殊方法（也被称为 “魔术方法” 或 “双下划线方法”），它定义了一个类的实例对象被转换为字符串时的表示形式。
当你使用 print() 函数打印该类的实例，或者通过 str() 函数将实例对象转换为字符串时，就会调用这个 __str__ 方法来获取相应的字符串表示内容。'''
    def __str__(self):
        return "MCTS {}".format(self.player)
