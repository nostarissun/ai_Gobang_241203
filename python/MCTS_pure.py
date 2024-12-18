import numpy as np
import copy
from operator import itemgetter


def rollout_policy_fn(board):
    '''随机生成每个位置的概率'''
    action_probs = np.random.rand(len(board.availables))
    return zip(board.availables, action_probs)


def policy_value_fn(board):
    '''均分概率'''

    action_probs = np.ones(len(board.availables))/len(board.availables)
    return zip(board.availables, action_probs), 0

'''节点的相关操作'''
class TreeNode(object):

    def __init__(self, parent, prior_p):
        self._parent = parent
        self._children = {}  
        self._n_visits = 0
        self._Q = 0
        self._u = 0
        self._P = prior_p

    def expand(self, action_priors):
        for action, prob in action_priors:
            if action not in self._children:
                self._children[action] = TreeNode(self, prob)

    def select(self, c_puct):
        '''选择uct价值最大的点'''
        return max(self._children.items(),
                   key = lambda act_node: act_node[1].get_value(c_puct))

    def update(self, leaf_value):

        self._n_visits += 1
        
        self._Q += 1.0*(leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):
        '''更新上面函数的自身节点和所有父节点'''

        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):
        '''返回UCT'''
        self._u = (c_puct * self._P *
                   np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def is_leaf(self):
        return self._children == {}

    def is_root(self):
        return self._parent is None

'''MCT的相关操作'''
class MCTS(object):

    def __init__(self, policy_value_fn, c_puct=5, n_playout=10000):

        self._root = TreeNode(None, 1.0)
        self._policy = policy_value_fn
        self._c_puct = c_puct
        self._n_playout = n_playout

    '''开始单次模拟'''
    def _playout(self, state):

        node = self._root
        while True:
            if node.is_leaf():
                break
            '''选择uct最大的动作'''
            action, node = node.select(self._c_puct)
            state.do_move(action)

        action_probs, _ = self._policy(state)
    
        end, winner = state.game_end()
        if not end:
            node.expand(action_probs)
 
        leaf_value = self._evaluate_rollout(state)

        node.update_recursive(-leaf_value)

    def _evaluate_rollout(self, state, limit=1000):
        '''核算到达叶子节点后，迅速估算一下从叶子节点出发的价值'''
        player = state.get_current_player()
        for i in range(limit):
            end, winner = state.game_end()
            if end:
                break
            action_probs = rollout_policy_fn(state)
            max_action = max(action_probs, key = itemgetter(1))[0]
            state.do_move(max_action)

        if winner == -1:  
            return 0
        else:
            return 1 if winner == player else -1

    def get_move(self, state):
        '''通过_n_playout次模拟确定，源头节点最佳动作即选择访问次数最多'''
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)
        return max(self._root._children.items(),
                   key = lambda act_node: act_node[1]._n_visits)[0]

    def update_with_move(self, last_move):
        '''更新MCT根节点'''
        if last_move in self._root._children:
            self._root = self._root._children[last_move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, 1.0)




class MCTSPlayer():
   
    def __init__(self, c_puct = 5, n_playout = 2000):
        self.mcts = MCTS(policy_value_fn, c_puct, n_playout)

    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, board):
        sensible_moves = board.availables

        if len(sensible_moves) > 0:
            move = self.mcts.get_move(board)
            self.mcts.update_with_move(-1)
            return move



