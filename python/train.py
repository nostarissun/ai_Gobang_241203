# import torch
import tkinter as tk
from tkinter import messagebox

import random
# board_size = 20
# #torch.float32
# tensor = torch.zeros((1, board_size, board_size))

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
        for chess_cnt in range(0, 4):
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





# 进入主事件循环
window()
