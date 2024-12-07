
ALL_WIDTH = 800;
ALL_HEIGHT = 650;
cellsize = 30;
begin_x = 20;
begin_y = 20;
end_x = 590;
end_y = 590;
WIDTH = end_x - begin_x;
HEIGHT = end_y - begin_y;
x_cnt = WIDTH // cellsize;
y_cnt = HEIGHT // cellsize;
board_size_W = WIDTH // cellsize + 1;
board_size_H = HEIGHT // cellsize + 1;


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
    },
    0 : {
        0 : 0,
        1 : 0,
        2 : 0
    }
}