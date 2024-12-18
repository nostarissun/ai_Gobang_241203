package org.example;
import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;



//0 无棋子
//1 黑棋
//2 白棋


public class Game {
    public static final int ALL_WIDTH = 650;
    public static final int ALL_HEIGHT = 500;
    public static final int cellsize = 30;
    public static final int begin_x = 20;
    public static final int begin_y = 20;
    public static final int end_x = 350;   //590
    public static final int end_y = 350;
    public static final int WIDTH = end_x - begin_x;
    public static final int HEIGHT = end_y - begin_y;
    public static final int x_cnt = WIDTH / cellsize;
    public static final int y_cnt = HEIGHT / cellsize;
    public static final int board_size_W = WIDTH / cellsize + 1;
    public static final int board_size_H = HEIGHT / cellsize + 1;
    public static int chess_board[][] = new int[board_size_H][board_size_W];
    // public static int cur_chess = 1;
    public void open(JFrame  root){
        // System.out.println(board_size_H * board_size_W);
        // JFrame jf = new JFrame("五子棋");
        // jf.setResizable(false);
        root.setLayout(new BorderLayout());
        Container element = root.getContentPane();
        
        for(int i = 0; i < board_size_H; i++)
        {
            for(int j = 0; j < board_size_W; j++)
            {
                chess_board[i][j] = 0;
            }
        }
       
        int difficulty = choose_difficulty(root);

        DrawChessBoard boardPanel = new DrawChessBoard();
        PlaceChess pc = new PlaceChess(chess_board, root, difficulty);
        


        element.add(boardPanel);
        element.add(pc);
        
        element.revalidate();
        element.repaint();

        root.setSize(ALL_WIDTH,ALL_HEIGHT);
        // root.setLocation(320,240);
        
        root.setVisible(true);
        root.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
       
    }


int choose_difficulty(JFrame root){
    // 创建面板以容纳按钮
    JPanel panel = new JPanel();
    JButton button1 = new JButton("入门");
    JButton button2 = new JButton("进阶");

    final int[] choice = {0}; // 使用数组来保存选择

    button1.addActionListener(new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
            choice[0] = 1;
            ((JDialog) SwingUtilities.getWindowAncestor((Component) e.getSource())).dispose(); // 关闭对话框
        }
    });

    button2.addActionListener(new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
            choice[0] = 2;
            ((JDialog) SwingUtilities.getWindowAncestor((Component) e.getSource())).dispose(); // 关闭对话框
        }
    });

    // 将按钮添加到面板
    panel.add(button1);
    panel.add(button2);

    // 创建并显示模态对话框
    JOptionPane.showOptionDialog(
        root,
        panel,
        "选择难度（默认为入门难度）",
        JOptionPane.DEFAULT_OPTION,
        JOptionPane.PLAIN_MESSAGE,
        null,
        new Object[]{},
        null
    );

    return choice[0];
}

}

class DrawChessBoard extends JPanel {
    DrawChessBoard(){
        setBackground(new Color(239, 226, 146));
    }
    @Override
    protected void paintComponent(Graphics g) {
   
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;

        // 设置绘制线条的属性
        g2d.setStroke(new BasicStroke(1));
        g2d.setColor(Color.BLACK);
      
        //画横线
        for(int i = 0; i <= Game.y_cnt; i++)
        {
            int x0 = Game.begin_x;
            int y0 = i * Game.cellsize + Game.begin_y;
            int x1 = Game.end_x;
            int y1 = y0;
            g2d.drawLine(x0, y0, x1, y1);
        }
        //画竖线
        for(int i = 0; i <= Game.x_cnt; i++)
        {
            int y0 = Game.begin_y;
            int x0 = i * Game.cellsize + Game.begin_x;
            int y1 = Game.end_y;
            int x1 = x0;
            g2d.drawLine(x0, y0, x1, y1);
        }
    }


}



class PlaceChess extends DrawChessBoard{
    int chess_board[][] = new int[Game.board_size_H][Game.board_size_W];
    int cur = 1;
    boolean gamerun = true;
    int right = -1;
    boolean legal = false;

    PlaceChess(int[][] cb, JFrame root, int difficulty){
        // super(cur);
            for(int i = 0; i < Game.board_size_H; i++){
                for(int j = 0; j < Game.board_size_W; j++){
                    this.chess_board[i][j] = cb[i][j];
                }
            }
            
                    
            
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) 
            {
                if (gamerun) 
                {
                    cur = 1;
                    right = MouseClick(e);
                    if(judge_win(cur, root))
                    {
                        gamerun = false;
                    }
                   
                    
                    
                    // else if(right != -1)
                    else if (gamerun && right != -1)
                    {

                        cur = 2;
                        if(difficulty == 2){
                            int r = -1, c = -1;
                            String serverName = "localhost";
                            int servePort = 12000;
                            byte[] buffer = new byte[1024];
                            int bytesRead = 0;
                            String modifiedSentence = "";
                            
                            try {
                                
                                Socket clientSocket = new Socket(serverName, servePort);
        
                                String sentence = String.valueOf(right) + ",";
                                for (int i = 0; i < Game.board_size_H; i++) {
                                    for (int j = 0; j < Game.board_size_W; j++) {
                                        sentence += chess_board[i][j];
                                        
                                    }
                                    System.out.println();
                                }
                                // for(int i = 0 ; i < Game.board_size_H; i++)
                                // {
                                //     for(int j = 0; j < Game.board_size_W; j++)
                                //     {
                                //         System.out.print(sentence.charAt(Game.board_size_W * i + j));
                                //     }
                                //     System.out.println();
                                // }
                                
        
                                
                                OutputStream outputStream = clientSocket.getOutputStream();
                                outputStream.write(sentence.getBytes());
        
                                
                                bytesRead = clientSocket.getInputStream().read(buffer);
                                modifiedSentence = new String(buffer, 0, bytesRead);
                                System.out.print(modifiedSentence);
                                clientSocket.close();
                                String[] newstr = modifiedSentence.split(",");
                                r = Integer.parseInt(newstr[0]);
                                c = Integer.parseInt(newstr[1]);
                                if (r == -1 || c == -1) {
                                    System.exit(0);
                                }
        
        
                                chess_board[r][c] = 2;
        
                                Graphics2D g2d = (Graphics2D) getGraphics();
                                g2d.setColor(Color.WHITE);
                                int cellSize = Game.cellsize;
                                
                                g2d.fillOval(c * cellSize - 10 + Game.begin_x, r * cellSize - 10 + Game.begin_y, 20, 20);
        
                            } catch (IOException a) {
                                a.printStackTrace();
                            }
                        }

                        else{
                            int pos[] = new int[2];
                            pos = new guess(chess_board).place_where();
                            // System.out.print("!!!!!!!!!!!!!");
                            chess_board[pos[1]][pos[0]] = 2;
        
                            Graphics2D g2d = (Graphics2D) getGraphics();
                            g2d.setColor(Color.WHITE);
                            int cellSize = Game.cellsize;
                            
                            g2d.fillOval(pos[0] * cellSize - 10 + Game.begin_x, pos[1] * cellSize - 10 + Game.begin_y, 20, 20);
                        }
                    }
                    
                    if(judge_win(cur, root))
                    {
                        gamerun = false;
                    }

                } 


            
            }
        });
    }

    private int MouseClick(MouseEvent e) {
        
        int real_xlocation[] = new int[Game.board_size_W];
        for(int i = 0; i < Game.board_size_W; i++){
            real_xlocation[i] = Game.begin_x + Game.cellsize * i;
        }

        int real_ylocation[] = new int[Game.board_size_H];
        for(int i = 0; i < Game.board_size_H; i++){
            real_ylocation[i] = Game.begin_y + Game.cellsize * i;
        }

        
        int real_x = -1, real_y = -1;

        
        real_x = e.getX();
        real_y = e.getY();

        if(real_x > Game.end_x + 20 || real_x < Game.begin_x - 20 || real_y > Game.end_y + 20 || real_y < Game.begin_y - 20){
            System.out.println("鼠标点击不合法");
            return -1;
        }

        real_x = get_min_location(real_xlocation, real_x, Game.board_size_W);
        real_y = get_min_location(real_ylocation, real_y, Game.board_size_H);
        
        // System.out.println(real_x);
        // System.out.println(real_y);

        int board_x = (real_x - Game.begin_x) / Game.cellsize;
        int board_y = (real_y - Game.begin_y) / Game.cellsize;
        // if(chess_board[x][y] != 0)return;
        if(chess_board[board_y][board_x] != 0) {
            System.out.println("已有棋子");   
            return -1;
        }
        Graphics2D g2d = (Graphics2D) getGraphics();
        g2d.setColor(Color.BLACK);
    
        // System.out.println("\n\n\n" + this.cur);
        chess_board[board_y][board_x] = 1;


        g2d.fillOval(real_x - 10, real_y - 10, 20, 20);
     
        return board_y * 12 + board_x;
    }

    int get_min_location(int []real, int cur, int size){
        int res = 1000;
        for(int i = 0; i < size; i++){
            if(Math.abs(cur - real[i]) < Math.abs(res - cur))
                res = real[i];
        }
        return res;
    }

    boolean judge_win(int chess, JFrame root){
        int dir[][] = new int[8][2];
           // 八个方向 顺时针         
        dir[0] = new int[]{0, -1};
        dir[1] = new int[]{1, -1};
        dir[2] = new int[]{1, 0};
        dir[3] = new int[]{1, 1};
        dir[4] = new int[]{0, 1};
        dir[5] = new int[]{-1, 1};
        dir[6] = new int[]{-1, 0};
        dir[7] = new int[]{-1, -1};

        boolean have = false;
        for(int i = 0; i < Game.board_size_H; i++)
        {
            for(int j = 0; j < Game.board_size_W; j++)
            {
                for(int k = 0; k < 8; k++)
                {
                    int dx = dir[k][0];
                    int dy = dir[k][1];
                    int cnt = 0;
                    for(int m = 0; m < 5; m++)
                    {
                        if(i + m * dy < Game.board_size_H && i + m * dy >= 0 && j + m * dx  < Game.board_size_W && j + m * dx >= 0){
                            if(chess_board[i + m * dy][j + m * dx] == chess){
                                cnt++;
                            }
                            else if(chess_board[i + m * dy][j + m * dx] == 0){
                                have = true;
                            }
                        }
                    }
                    if(cnt == 5){
                        if(cur == 1)
                        show_end(root, "恭喜你赢得了游戏！！！！！！");
                        // System.exit(0);
                        else show_end(root, "此局游戏已输！！");
                        return true;
                    }
                }
            }
        }
        if(have == false){
            show_end(root, "恭喜达成成就《平局》");
        }
        return false;
    }
    
    void show_end(JFrame root, String show){
        JDialog dialog = new JDialog();
        dialog.setTitle("游戏已结束");
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setSize(300, 150);
        dialog.setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());

        JLabel label = new JLabel(show);
        panel.add(label, BorderLayout.CENTER);

        JButton back = new JButton("返回主页");
        JButton again = new JButton("再来一把");
        back.setFont(new Font("宋体", Font.BOLD, 12));
        again.setFont(new Font("宋体", Font.BOLD, 12));


        JPanel buttonPanel = new JPanel();

        

        buttonPanel.add(back);
        buttonPanel.add(again);
        panel.add(buttonPanel, BorderLayout.SOUTH);
        dialog.add(panel);

        dialog.setVisible(true);
        back.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                Container element = root.getContentPane();
                element.removeAll();
                element.revalidate();
                element.repaint();
                Main.main_page(root, root.getContentPane());
                dialog.dispose();
            }
        });
        again.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                reset_game();
                repaint();
                gamerun = true;
                dialog.dispose();
            }
        });

    }

    
    void reset_game(){
        cur = 1;
        for(int i = 0; i < Game.board_size_H; i++)
        {
            for(int j = 0 ; j < Game.board_size_W; j++)
            {
                chess_board[i][j] = 0;
            }
        }
    }

}

class guess{
    static class Const {
        static final Map<Integer, Integer> STATUS = new HashMap<>();
        static {
            STATUS.put(0, 0);
            STATUS.put(1, 100);
            STATUS.put(2, 3000);
            STATUS.put(3, 10000);
            STATUS.put(4, 20000);
        }

        // 棋盘尺寸
        static final int BOARD_SIZE_W = 12; // 棋盘宽度
        static final int BOARD_SIZE_H = 12; // 棋盘高度

        // 八个方向，顺时针
        static final int[][] DIR = {
            {0, -1},  // 左
            {1, -1},  // 左下
            {1, 0},   // 下
            {1, 1},   // 右下
            {0, 1},   // 右
            {-1, 1},  // 右上
            {-1, 0},  // 上
            {-1, -1}  // 左上
        };
    }
    
    int[][] chess_board = new int[12][12];

    guess(int[][] ch){
        for(int i = 0; i < 12; i++){
            for(int j = 0; j < 12; j++){
                this.chess_board[i][j] = ch[i][j];
            }
        }
    }


    int get_evaluate(int x, int y){
        int enemy = judge(x, y, 1, 2);
        int friend = judge(x, y, 2, 1);
        return enemy + friend;
    }

    int judge(int x0, int y0, int enemy, int friend){
        int score = 0;
        int[] cnt = new int[Const.DIR.length];

        for (int d = 0; d < Const.DIR.length; d++) {
            int r = 0;
            int firstEmpty = -1;

            for (int chessCnt = 1; chessCnt <= 5; chessCnt++) {
                int y = y0 + Const.DIR[d][1] * chessCnt;
                int x = x0 + Const.DIR[d][0] * chessCnt;

                if (x >= Const.BOARD_SIZE_W || x < 0 || y >= Const.BOARD_SIZE_H || y < 0)
                    break;

                if (this.chess_board[y][x] == friend)
                    break;

                if (this.chess_board[y][x] == 0 && firstEmpty == -1)
                    firstEmpty = chessCnt;

                if (this.chess_board[y][x] == enemy && firstEmpty <= 2)
                    r++;
            }
            cnt[d] = r;
        }

        int maxCnt = 0;
        for (int i = 0; i < Const.DIR.length; i++) {
            maxCnt = Math.max(maxCnt, cnt[i]);
        }
        score += Const.STATUS.getOrDefault(Math.min(maxCnt, Collections.max(Const.STATUS.keySet())), 0); // 确保索引不超过数组长度
        return score;
    }
   
    public int[] place_where() {
        int[] pos = new int[2];
        int res = Integer.MIN_VALUE;

        int center_score = 20;
        for (int r = 0; r < Const.BOARD_SIZE_H; r++) {
            for (int c = 0; c < Const.BOARD_SIZE_W; c++) {
                if (this.chess_board[r][c]!= 0) {
                    // System.out.printf("%-5s", "0");
                    continue;
                }
                int center[] = new int[2];
                // center = get_center();
                center[0] = 6;
                center[1] = 6;
                int score = center_score - Math.abs(center[0] - r) - Math.abs(center[1] - c) + get_evaluate(c, r);
                // System.out.printf("%-5s", score);

                if (res < score) {
                    res = score;
                    
                    pos[0] = c;
                    pos[1] = r;
                    
                }
            }
            // System.out.println();
        }
        System.out.print(pos[0]);
        System.out.println(pos[1]);
        return pos;
    }


    int[] get_center(){
        int s[][] = new int[Const.BOARD_SIZE_H + 1][Const.BOARD_SIZE_W + 1];
        for (int i = 1; i <= Const.BOARD_SIZE_H; i++) {
            for (int j = 1; j <= Const.BOARD_SIZE_W; j++) {
                s[i][j] = s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1] + (this.chess_board[i - 1][j - 1] == 0 ? 0 : 1);
            }
        }
        int best[] = new int[2];
        int max_cnt = -1;
        for (int r = 0; r <= Const.BOARD_SIZE_H - Const.BOARD_SIZE_H / 2; r++) {
            for (int c = 0; c <= Const.BOARD_SIZE_W - Const.BOARD_SIZE_W / 2; c++) {
                // 计算 6x6 区域内的空格子数量
                int t = s[r + Const.BOARD_SIZE_H / 2][c + Const.BOARD_SIZE_W / 2]
                                - s[r + Const.BOARD_SIZE_H / 2][c]
                                - s[r][c + Const.BOARD_SIZE_W / 2]
                                + s[r][c];

                if (t > max_cnt) {
                    max_cnt = t;
                    best[0] = c;
                    best[1] = r;
                }
            }
        }
        return best;
    }
}


