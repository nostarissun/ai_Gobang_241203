import random
import numpy as np
from collections import defaultdict, deque
from chess import Board, game

from MCTS import MCTSPlayer
from policy_value_net import PolicyValueNet  # Theano and Lasagne



class Train():
    def __init__(self, init_model = None):
 
        self.board_width = 6
        self.board_height = 6

        self.board = Board(self.board_width, self.board_height)
        self.game = game(self.board)

  
        self.learn_rate = 2e-3
        self.lr_multiplier = 1.0  
        self.temp = 1.0 
        self.n_playout = 400 
        self.c_puct = 5
        #总数据量上线
        self.buffer_size = 10000
        #每一次抽取的数据
        self.batch_size = 512  
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.play_batch_size = 1
        #每一组数据迭代次数
        self.epochs = 5  
        self.kl_targ = 0.02
        #每隔50次保存模型
        self.check_freq = 50
        #总迭代
        self.game_batch_num = 1500
        self.best_win_ratio = 0.0

        self.pure_mcts_playout_num = 1000
        if init_model:
            self.policy_value_net = PolicyValueNet(self.board_width,   self.board_height,   model_file = init_model)
        else:
        
            self.policy_value_net = PolicyValueNet(self.board_width,   self.board_height)

        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,  c_puct=self.c_puct,  n_playout=self.n_playout,  is_selfplay=1)

    def get_equi_data(self, play_data):
        '''同一个棋局，旋转后四次利用'''
        extend_data = []
        for state, mcts_prob, winner in play_data:
            for i in [1, 2, 3, 4]:
      
                equi_state = np.array([np.rot90(s, i) for s in state])
                equi_mcts_prob = np.rot90(np.flipud(
                    mcts_prob.reshape(self.board_height, self.board_width)), i)
                extend_data.append((equi_state, np.flipud(equi_mcts_prob).flatten(), winner))

                equi_state = np.array([np.fliplr(s) for s in equi_state])
                equi_mcts_prob = np.fliplr(equi_mcts_prob)
                extend_data.append((equi_state, np.flipud(equi_mcts_prob).flatten(), winner))
        return extend_data

    def collect_selfplay_data(self, n_games=1):

        for i in range(n_games):
            winner, play_data = self.game.self_play(self.mcts_player, temp = self.temp)
            play_data = list(play_data)[:]
            self.episode_len = len(play_data)
       
            play_data = self.get_equi_data(play_data)
            #将数据存入双端队列
            self.data_buffer.extend(play_data)

    def policy_update(self):
        
        mini_batch = random.sample(self.data_buffer, self.batch_size)
        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]

        old_probs, old_v = self.policy_value_net.policy_value(state_batch)
        for i in range(self.epochs):
            loss, entropy = self.policy_value_net.train_step(state_batch, mcts_probs_batch, winner_batch, self.learn_rate*self.lr_multiplier)
            new_probs, new_v = self.policy_value_net.policy_value(state_batch)
            kl = np.mean(np.sum(old_probs * (np.log(old_probs + 1e-10) - np.log(new_probs + 1e-10)), axis=1))
            if kl > self.kl_targ * 4: 
                break
   
        if kl > self.kl_targ * 2 and self.lr_multiplier > 0.1:
            self.lr_multiplier /= 1.5
        elif kl < self.kl_targ / 2 and self.lr_multiplier < 10:
            self.lr_multiplier *= 1.5

        explained_var_old = (1 - np.var(np.array(winner_batch) - old_v.flatten()) / np.var(np.array(winner_batch)))
        explained_var_new = (1 - np.var(np.array(winner_batch) - new_v.flatten()) / np.var(np.array(winner_batch)))
        print(("kl:{:.5f},"
               "lr_multiplier:{:.3f},"
               "loss:{},"
               "entropy:{},"
               "explained_var_old:{:.3f},"
               "explained_var_new:{:.3f}"
               ).format(kl,
                        self.lr_multiplier,
                        loss,
                        entropy,
                        explained_var_old,
                        explained_var_new))
        return loss, entropy

    def policy_evaluate(self, n_games=10):
        '''衡量模型进步与否'''
        current_mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn, c_puct=self.c_puct, n_playout=self.n_playout)

        
        #具体来说，defaultdict(int) 表示创建了一个字典对象，当你尝试访问其中不存在的键时，它会自动为这个键创建对应的值，并且这个值的初始类型由传入的工厂函数 int 决定，也就是初始化为整数 0。
        win_cnt = defaultdict(int)
        for i in range(n_games):
            winner = self.game.start_play(current_mcts_player, i % 2 + 1)
            win_cnt[winner] += 1
        #1是模型赢，2是输，-1是平局
        win_ratio = 1.0*(win_cnt[1] + 0.5*win_cnt[-1]) / n_games
        print("num_playouts:{}, win: {}, lose: {}, tie:{}".format(
                self.pure_mcts_playout_num,
                win_cnt[1], win_cnt[2], win_cnt[-1]))
        
        return win_ratio

    def run(self):
  
        try:
            for i in range(self.game_batch_num):
                self.collect_selfplay_data(self.play_batch_size)

                print("batch i:{}, episode_len:{}".format(i+1, self.episode_len))

                if len(self.data_buffer) > self.batch_size:
                    loss, entropy = self.policy_update()
 
                if (i+1) % self.check_freq == 0:
                    print("current self-play batch: {}".format(i+1))
                    win_ratio = self.policy_evaluate()
                    
                    self.policy_value_net.save_model('./current_policy.model')
                    
                    if win_ratio > self.best_win_ratio:
                        print("New best policy!!!!!!!!")
                        self.best_win_ratio = win_ratio
    
                        self.policy_value_net.save_model('./best_policy.model')
                        if (self.best_win_ratio == 1.0 and
                                self.pure_mcts_playout_num < 5000):
                            self.pure_mcts_playout_num += 1000
                            self.best_win_ratio = 0.0
        except KeyboardInterrupt:
            print('\n\rquit')





if __name__ == '__main__':
    training = Train()
    training.run()
