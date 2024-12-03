import const 
import main


# //0 无棋子
# //1 黑棋
# //2 白棋


chess_board = main.chess_board
#return max_score (x, y)
def get_score() -> int:

    def calculate(x, y):
        for dx in range()

    res_x = None
    res_y = None
    res_score = -'inf'
    for x in range(const.X):
        for y in range(const.Y):
            t = calculate(x, y)
            if t > res_score:
                res_x = x
                res_y = y
                res_score = t
    return res_score, res_x, res_y

def main():
    print()










main()