package org.example;



import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;



import java.io.IOException;


import java.io.OutputStream;

import java.net.Socket;





//0 无棋子
//1 黑棋
//2 白棋


public class Game {
    public static final int ALL_WIDTH = 800;
    public static final int ALL_HEIGHT = 650;
    public static final int cellsize = 30;
    public static final int begin_x = 20;
    public static final int begin_y = 20;
    public static final int end_x = 590;
    public static final int end_y = 590;
    public static final int WIDTH = end_x - begin_x;
    public static final int HEIGHT = end_y - begin_y;
    public static final int x_cnt = WIDTH / cellsize;
    public static final int y_cnt = HEIGHT / cellsize;
    public static final int board_size_W = WIDTH / cellsize + 1;
    public static final int board_size_H = HEIGHT / cellsize + 1;
    public static int chess_board[][] = new int[board_size_H][board_size_W];
    // public static int cur_chess = 1;
    public void open(){
        // System.out.println(board_size_H * board_size_W);
        JFrame jf = new JFrame("五子棋");
        Container contain = jf.getContentPane();
        
        for(int i = 0; i < board_size_H; i++)
        {
            for(int j = 0; j < board_size_W; j++)
            {
                chess_board[i][j] = 0;
            }
        }
        DrawChessBoard boardPanel = new DrawChessBoard();
        
        
 

        PlaceChess pc = new PlaceChess(chess_board);
        


        contain.add(boardPanel);
        contain.add(pc);

        
        
        
        jf.setSize(ALL_WIDTH,ALL_HEIGHT);
        jf.setLocation(320,240);
        
        jf.setVisible(true);
        jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
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

     // 创建一个线程池，用于执行各种异步和多线程任务
    

    PlaceChess(int[][] cb){
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
                if (gamerun && cur == 1) 
                {
                      MouseClick(e);
                } 

                else if (gamerun && cur == 2) {
                 
                  
                        int r = -1, c = -1;
                        String serverName = "localhost";
                        int servePort = 12000;
                        byte[] buffer = new byte[1024];
                        int bytesRead = 0;
                        String modifiedSentence = "";

                        try {
                            
                            Socket clientSocket = new Socket(serverName, servePort);

                            String sentence = "";
                            for (int i = 0; i < Game.board_size_H; i++) {
                                for (int j = 0; j < Game.board_size_W; j++) {
                                    sentence += chess_board[i][j];
                                    
                                }
                                System.out.println();
                            }
                            for(int i = 0 ; i < Game.board_size_H; i++)
                            {
                                for(int j = 0; j < Game.board_size_W; j++)
                                {
                                    System.out.print(sentence.charAt(Game.board_size_W * i + j));
                                }
                                System.out.println();
                            }
                            

                           
                            OutputStream outputStream = clientSocket.getOutputStream();
                            outputStream.write(sentence.getBytes());

                            
                            bytesRead = clientSocket.getInputStream().read(buffer);
                            modifiedSentence = new String(buffer, 0, bytesRead);

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
                                
                                // (real_x - Game.begin_x) / Game.cellsize = t
                                g2d.fillOval(c * cellSize - 10 + Game.begin_x, r * cellSize - 10 + Game.begin_y, 20, 20);
    
                                if (judge_win(cur)) {
                                    gamerun = false;
                                }
                                System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!" + c + r);


                        } catch (IOException a) {
                            a.printStackTrace();
                        }

                
                }
                cur = cur % 2 + 1;
            }
        });
    }

    private void MouseClick(MouseEvent e) {
        
        int real_xlocation[] = new int[Game.board_size_W];
        for(int i = 0; i < Game.board_size_W; i++){
            real_xlocation[i] = Game.begin_x + Game.cellsize * i;
        }

        int real_ylocation[] = new int[Game.board_size_H];
        for(int i = 0; i < Game.board_size_H; i++){
            real_ylocation[i] = Game.begin_y + Game.cellsize * i;
        }

        if(judge_win(cur)){
            gamerun = false;
            return;
        }
        
        int real_x = -1, real_y = -1;

        
        real_x = e.getX();
        real_y = e.getY();

        if(real_x > Game.end_x || real_x < Game.begin_x || real_y > Game.end_y || real_y < Game.begin_y){
            System.out.println("鼠标点击不合法");
            return ;
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
            return;
        }
        Graphics2D g2d = (Graphics2D) getGraphics();
        g2d.setColor(Color.BLACK);
    
        // System.out.println("\n\n\n" + this.cur);
        chess_board[board_y][board_x] = 1;


        g2d.fillOval(real_x - 10, real_y - 10, 20, 20);
        
        if(judge_win(cur))
        {
            gamerun = false;
        }
     
        return;
        // put_to_ai(chess_board);
        // System.out.println("\n\n\n" + this.cur);
        
        // cur = cur % 2 + 1;
    }

    int get_min_location(int []real, int cur, int size){
        int res = 1000;
        for(int i = 0; i < size; i++){
            if(Math.abs(cur - real[i]) < Math.abs(res - cur))
                res = real[i];
        }
        return res;
    }

    boolean judge_win(int chess){
        // System.out.println("!!!!!!!!!!!!!!!");
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
                        if(i + m * dx < Game.board_size_H && i + m * dx >= 0 && j + m * dy  < Game.board_size_W && j + m * dy >= 0 && chess_board[i + m * dx][j + m * dy] == chess)cnt++;
                    }
                    if(cnt == 5){
                        if(cur == 1)
                        show_win();
                        // System.exit(0);
                        else show_lose();
                        return true;
                    }
                }
            }
        }
        return false;
    }
    void show_win(){
        JDialog dialog = new JDialog();
        dialog.setTitle("THE FINAL RESULT:");
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setSize(300, 150);

        dialog.setLocationRelativeTo(null);// 居中

        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());

        JLabel label = new JLabel("YOU WIN THE GAME!!!");
        panel.add(label, BorderLayout.CENTER);

        dialog.add(panel);
        dialog.setVisible(true);
    }

    void show_lose(){
        JDialog dialog = new JDialog();
        dialog.setTitle("THE FINAL RESULT:");
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setSize(300, 150);

        dialog.setLocationRelativeTo(null);// 居中

        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());

        JLabel label = new JLabel("YOU LOSE THE GAME!!!");
        panel.add(label, BorderLayout.CENTER);

        dialog.add(panel);
        dialog.setVisible(true);
    }
}







    //     if(cur == 2 && gamerun){
    //         