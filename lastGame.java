import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
//0 无棋子
//1 黑棋
//2 白棋

public class Game {
    public static final int X = 800;
    public static final int Y = 650;
    public static void main(String args[]){
        JFrame jf = new JFrame("五子棋");
        Container contain = jf.getContentPane();
        
        // 绘制棋盘
        DrawChessBoard boardPanel = new DrawChessBoard();
        int cur = 1;
        int chess_board[][] = new int[30][30];
        PlaceChess pc = new PlaceChess(chess_board, cur);
        contain.add(boardPanel);
        contain.add(pc);

        
        
        
        jf.setSize(X,Y);
        jf.setLocation(320,240);
        
        jf.setVisible(true);
        jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
    }
   
}
class DrawChessBoard extends JPanel {
    DrawChessBoard(){
        
        
        // setBackground(Color.);
        setBackground(new Color(239, 226, 146));
    }
    @Override
    protected void paintComponent(Graphics g) {
   
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;

        // 设置绘制线条的属性
        g2d.setStroke(new BasicStroke(1));
        g2d.setColor(Color.BLACK);
        int cellSize = 30;
        int x_cnt = 800 / cellSize;
        int y_cnt = 650 / cellSize;

        for(int i = 0; i < y_cnt; i++)
        {
            int x0 = 0;
            int y0 = i * cellSize;
            int x1 = 800;
            int y1 = i * cellSize;
            g2d.drawLine(x0, y0, x1, y1);
        }

        for(int i = 0; i < x_cnt; i++)
        {
            int y0 = 0;
            int x0 = i * cellSize;
            int y1 = 650;
            int x1 = i * cellSize;
            g2d.drawLine(x0, y0, x1, y1);
        }
    }
}
class PlaceChess extends DrawChessBoard{
    int chess_board[][] = new int[30][30];
    int cur;
    PlaceChess(int[][] cb, int cur){
        this.cur = cur;
        
        for(int i = 0; i < 30; i++){
            for(int j = 0; j < 30; j++){
                this.chess_board[i][j] = chess_board[i][j];
            }
        }

        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                MouseClick(e);
            }
        });
    }
    private void MouseClick(MouseEvent e) {
        int x = e.getX();
        int y = e.getY();
        int a[] = new int[30];
        for(int i = 0; i < 800 / 30; i++){
            a[i] = 30 * i;
        }
        x = get_min_location(a, x, 800 / 30);
        for(int i = 0; i < 650 / 30; i++){
            a[i] = 30 * i;
        }
        y = get_min_location(a, y, 650 / 30);
        
        // if(chess_board[x][y] != 0)return;

        Graphics2D g2d = (Graphics2D) getGraphics();
        if(this.cur == 1)
        g2d.setColor(Color.BLACK);
        else if(this.cur == 2)
        g2d.setColor(Color.WHITE);

        // System.out.println("\n\n\n" + this.cur);
        if(chess_board[x / 30][y / 30] != 0)return;
        chess_board[x / 30][y / 30] = this.cur;
        
        


        g2d.fillOval(x - 10, y - 10, 20, 20);

        judge_win(this.cur);
        put_to_ai(chess_board);
        // System.out.println("\n\n\n" + this.cur);
        
        
    }
    int get_min_location(int []a, int cur, int size){
        int res = 1000;
        for(int i = 0; i < size; i++){
            if(Math.abs(cur - a[i]) < Math.abs(res - cur))
                res = a[i];
        }
        return res;
    }

    void judge_win(int chess){
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


        for(int i = 0; i < 30; i++)
        {
            for(int j = 0; j < 30; j++)
            {
                for(int k = 0; k < 8; k++)
                {
                    int dx = dir[k][0];
                    int dy = dir[k][1];
                    int cnt = 0;
                    for(int m = 0; m < 5; m++)
                    {
                        if(i + m * dx < 30 && i + m * dx >= 0 && j + m * dy  < 30 && j + m * dy >= 0 && chess_board[i + m * dx][j + m * dy] == chess)cnt++;
                    }
                    if(cnt == 5){
                        show_win();
                        // System.exit(0);
                    }
                }
            }
        }
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
    void put_to_ai(int a[][]) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter("../chess_board_info.txt"))) {
            for (int i = 0; i < 30; i++) {
                for (int j = 0; j < 30; j++) {
                    if (a[j][i] == 0) {
                        bw.write('.');
                    } else if (a[j][i] == 1) {
                        bw.write('B');
                    } else if (a[j][i] == 2) {
                        bw.write('W');
                    }
                }
                bw.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}