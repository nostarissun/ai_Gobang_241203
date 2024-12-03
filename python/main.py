import ai
import const
#下白棋
#黑棋是1， 白棋是2

chess_board = []

def read_chess_board():
    
    with open("C:/Users/联想/Desktop/ai五子棋课设/chess_board_info.txt", 'r') as file:
        
        for line in file:
            t = []
            for char in line:
                if char != '\n':  
                    if char == '.':
                        t.append(0)
                    elif char == 'B':
                        t.append(1)
                    elif char == 'W':
                        t.append(2)
            chess_board.append(t)

def put_to_java():
    with open("C:/Users/联想/Desktop/ai五子棋课设/chess_board_info.txt", 'w') as file:
        for r in chess_board:
            s = ""
            for num in r:
                if num == 0:
                    s += '.'
                elif num == 1:
                    s += 'B'
                elif num == 2:
                    s += 'W' 

            file.write(s + '\n')



def get_evaluate(x : int, y : int) -> int:
    
    cnt2 = [0] * 8
    cnt1 = [0] * 8
    idx = 0
    for dir in const.DIR:
        for i in range(1, max(const.X, const.Y)):
            x1 = x + dir[0] * i
            y1 = y + dir[1] * i
            
            if(x1 > const.X or x1 < 0 or y1 > const.Y or y1 < 0):
                break
            if(chess_board[x1][y1] == 1 or chess_board[x1][y1] == 0):
                if(chess_board[x1][y1] == 1):
                    cnt1[idx] += 1
                    idx += 1
                break
            if chess_board[x1][y1] == 2:
                cnt2[idx] += 1
                break;    
    
    res = 0
    for i in range(4):
        t1 = cnt1[i] + cnt1[i + 4]
        t2 = cnt2[i] + cnt2[i + 4]
        res = max(res, const.status[t2][t1])
        
    
    return  res


def place_where() -> int:
    pos = []
    res = 0
    for x in const.X:
        for y in const.Y:
            if chess_board[x][y] != 0:
                continue
            if res <= get_evaluate(x, y):
                res = get_evaluate(x, y)
                pos = [x, y]
    return pos

def place_chess():
    pos = place_where()
    chess_board[pos[0]][pos[1]] = 2

def main():
    read_chess_board()




    put_to_java()



main()