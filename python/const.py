CELL_SIZE = 30
WIDTH = 800
HEIGHT = 650
MAX_SCORE = 10000
X = int(WIDTH / CELL_SIZE)
Y = int(HEIGHT / CELL_SIZE)

dir = []      
    # 八个方向 顺时针         
dir.append([0, -1]);
dir.append([1, -1]);
dir.append([1, 0]);
dir.append([1, 1]);
dir.append([0, 1]);
dir.append([-1, 1]);
dir.append([-1, 0]);
dir.append([-1, -1]);

status = {
    5:{
        0: 100000,
        1: 100000,
        2: 100000
    },
    4:{
        0: 10000,
        1: 2000,
        2: 100
    },
    3:{
        0: 2000,
        1: 100,
        2: 10
    },
    2:{
        0: 100, 
        1 : 10,
        2: 5
    },
    1 :{
        0: 10,
        1 : 5,
        2: 0
    }
}