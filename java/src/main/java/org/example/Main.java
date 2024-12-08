package org.example;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;




public class Main {
    public static final int X = 800;
    public static final int Y = 650;
    public static void main(String args[]){
        JFrame jf = new JFrame("五子棋");
        Container contain = jf.getContentPane();
        
        
        jf.setSize(X,Y);
        jf.setLocation(320,240);
        

        main_page(jf, contain);
        
        

        jf.setVisible(true);
        jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

    }
public static void open_game(JFrame win, Container contain){
    Game game = new Game();
    game.open(win);

}
    public static void main_page(JFrame windows, Container contain){
        
        windows.setLayout(null); // 设置布局管理器为null

        JLabel main_label = new JLabel("五子棋AI对战");
        main_label.setFont(new Font("SansSerif", Font.BOLD, 18));
        main_label.setBounds(X / 2 - 70, 0, 200, 30); // 设置标签的位置和大小
        contain.add(main_label);

        
        JButton button1 = new JButton("游客登录");
        JButton button2 = new JButton("登录");
        JButton button3 = new JButton("注册");
        JButton button4 = new JButton("退出游戏");
        button1.setFont(new Font("SansSerif", Font.BOLD, 16));
        button2.setFont(new Font("SansSerif", Font.BOLD, 16));
        button3.setFont(new Font("SansSerif", Font.BOLD, 16));
        button4.setFont(new Font("SansSerif", Font.BOLD, 16));
        button1.setBounds(X / 2 - 70, Y / 3, 100, 30);
        button2.setBounds(X / 2 - 70, Y / 3 + 30 + 50, 100, 30);
        button3.setBounds(X / 2 - 70, Y / 3 + 110 + 50, 100, 30);
        button4.setBounds(X / 2 - 70, Y / 3 + 190 + 50, 100, 30);
        // ImageIcon icon1 = new ImageIcon("C://Users//联想//Desktop//ai五子棋课设//label.png"); // 替换为实际图标路径
        // button1.setIcon(icon1);
//         button1.setHorizontalTextPosition(SwingConstants.CENTER);
// button1.setVerticalTextPosition(SwingConstants.BOTTOM);


        windows.add(button1);
        windows.add(button2);
        windows.add(button3);
        windows.add(button4);

        button4.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                int result = JOptionPane.showConfirmDialog(windows, "确定要退出游戏吗？", "退出确认", JOptionPane.YES_NO_OPTION);
                if (result == JOptionPane.YES_OPTION) {
                    System.exit(0); // 用户确认退出
                }
            }
        });
        button1.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                open_game(windows, contain);
            }
        });
        button2.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                    login(windows, contain);    
                    open_game(windows, contain);
            }
        });

        button3.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                    login(windows, contain);    
            }
        });

    }

    public static void register(JFrame windows, Container contain){
        
            JDialog get_info = new JDialog(windows, true);
            get_info.setSize(X / 2, Y / 2 - 180);


            get_info.getContentPane().setLayout(new BoxLayout(get_info.getContentPane(), BoxLayout.Y_AXIS));
            // 创建输入组件
            JLabel account = new JLabel("账号:");
            JLabel pwd = new JLabel("密码:");
            JTextField get_account = new JTextField(20);
            JTextField get_pwd = new JTextField(20);
            JButton ok = new JButton("确认");
            get_info.add(account);
            get_info.add(get_account);
            get_info.add(pwd);
            get_info.add(get_pwd);
            get_info.add(ok);


            
            get_info.setLocationRelativeTo(windows); // 将对话框居中于父窗口
            

            ok.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e){
                        String user = get_account.getText();
                        String password = get_pwd.getText();
                        int result = JOptionPane.showConfirmDialog(get_info, "账号: " + user + "\n密码: " + password + "\n确认登录？", "登录确认", JOptionPane.YES_NO_OPTION);
                        if (result == JOptionPane.YES_OPTION) {
                            get_info.dispose();  // 用户确认退出
                        }
                    }   
                
            });
            get_info.setVisible(true);
            get_info.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
         
    
    }

    public static void login(JFrame windows, Container contain){
        
            JDialog get_info = new JDialog(windows, true);
            get_info.setSize(X / 2, Y / 2 - 180);


            get_info.getContentPane().setLayout(new BoxLayout(get_info.getContentPane(), BoxLayout.Y_AXIS));
            // 创建输入组件
            JLabel account = new JLabel("账号:");
            JLabel pwd = new JLabel("密码:");
            JTextField get_account = new JTextField(20);
            JTextField get_pwd = new JTextField(20);
            JButton ok = new JButton("确认");
            get_info.add(account);
            get_info.add(get_account);
            get_info.add(pwd);
            get_info.add(get_pwd);
            get_info.add(ok);


            
            get_info.setLocationRelativeTo(windows); // 将对话框居中于父窗口
            

            ok.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e){
                        String user = get_account.getText();
                        String password = get_pwd.getText();
                        int result = JOptionPane.showConfirmDialog(get_info, "账号: " + user + "\n密码: " + password + "\n确认登录？", "登录确认", JOptionPane.YES_NO_OPTION);
                        if (result == JOptionPane.YES_OPTION) {
                            get_info.dispose();  // 用户确认退出
                        }
                    }   
                
            });
            get_info.setVisible(true);
            get_info.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
         
    }

}
