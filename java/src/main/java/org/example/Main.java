package org.example;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;
import java.awt.event.ActionEvent;




public class Main {
    public static final int X = 650;
    public static final int Y = 500;
    public static void main(String args[]){
        JFrame jf = new JFrame("五子棋");
        Container contain = jf.getContentPane();
        jf.setResizable(false);  //锁死大小
        
        jf.setSize(X,Y);
        // jf.setLocation();
        jf.setLocationRelativeTo(null);

        main_page(jf, contain);
        
        

        jf.setVisible(true);
        jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

    }
public static void open_game(JFrame win, Container contain){
    Game game = new Game();
    
    Container element = win.getContentPane();
    element.removeAll();
    element.revalidate();
    element.repaint();
    game.open(win);
}
    public static void main_page(JFrame windows, Container contain){
        
        windows.setLayout(null); // 设置布局管理器为null

        JLabel main_label = new JLabel("五子棋AI对战");
        main_label.setFont(new Font("SansSerif", Font.BOLD, 18));
        main_label.setBounds(X / 2 - 70, 0, 200, 30); // 设置标签的位置和大小
        

        
        JButton button1 = new JButton("游客登录");
        JButton button2 = new JButton("登录");
        JButton button3 = new JButton("注册");
        JButton button4 = new JButton("退出游戏");
        JButton button5 = new JButton("注销");
        JButton button6 = new JButton("修改密码");
        button1.setFont(new Font("SansSerif", Font.BOLD, 16));
        button2.setFont(new Font("SansSerif", Font.BOLD, 16));
        button3.setFont(new Font("SansSerif", Font.BOLD, 16));
        button4.setFont(new Font("SansSerif", Font.BOLD, 16));
        button5.setFont(new Font("SansSerif", Font.BOLD, 12));
        button6.setFont(new Font("SansSerif", Font.BOLD, 12));
        
        button1.setBounds(X / 2 - 70, Y / 3, 100, 30);
        button2.setBounds(X / 2 - 70, Y / 3 + 30 + 50, 100, 30);
        button3.setBounds(X / 2 - 70, Y / 3 + 110 + 50, 100, 30);
        button4.setBounds(X / 2 - 70, Y / 3 + 190 + 50, 100, 30);
        button5.setBounds(X - 100, Y / 3 + 190 + 50, 70, 20);
        button6.setBounds(X - 100, Y / 3 + 190, 85, 20);
    

        windows.add(button1);
        windows.add(button2);
        windows.add(button3);
        windows.add(button4);
        windows.add(button5);
        windows.add(button6);

        contain.add(main_label);



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
              
            }
        });

        button3.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                    register(windows, contain);    
                 
            }
        });
        button4.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                int result = JOptionPane.showConfirmDialog(windows, "确定要退出游戏吗？", "退出确认", JOptionPane.YES_NO_OPTION);
                if (result == JOptionPane.YES_OPTION) {
                    System.exit(0); // 用户确认退出
                }
            }
        });
        button5.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                delete(windows);
            }
        });
        button6.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                change(windows);
            }
        });

    }

    public static void register(JFrame windows, Container contain){
    
            JDialog get_info = new JDialog(windows, true);
            get_info.setSize(X / 2, Y / 2);


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
                        int result = JOptionPane.showConfirmDialog(get_info, "账号: " + user + "\n密码: " + password + "\n确认注册？", "注册信息确认", JOptionPane.YES_NO_OPTION);
                        if (result == JOptionPane.YES_OPTION) {
                            // System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
                            System.out.println(user);
                            System.out.println(password);
                            // if(find(user, password) == 1){
                            //     show("用户已存在，请重试");
                            // }
                            // else{
                                show("注册成功");
                
                                registerNewUser(user, password);
                                open_game(windows, contain);
                            // }
                            get_info.dispose();  // 用户确认退出
                        }
                    }   
                
            });
            get_info.setVisible(true);
            get_info.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
    


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
            if(find(get_account.getText(), get_pwd.getText()) == 0){
                show("用户不存在，请注册");
            }
            else if (find(get_account.getText(), get_pwd.getText()) == -1){
                show("密码错误，请重试");
            }
            else{
                String t = querylast_time(get_account.getText());
                show("登陆成功\n上次登录时间:" + t);
                open_game(windows, contain);
            }
         
    }
    
    public static void delete(JFrame windows){
        JDialog get_info = new JDialog(windows, true);
        get_info.setSize(X / 2, Y / 2);


        get_info.getContentPane().setLayout(new BoxLayout(get_info.getContentPane(), BoxLayout.Y_AXIS));
        // 创建输入组件
        JLabel account = new JLabel("账号:");
        JLabel pwd = new JLabel("密码:");
        JTextField get_account = new JTextField(20);
        JTextField get_pwd = new JTextField(20);
        JButton ok = new JButton("确认注销");
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
                    int result = JOptionPane.showConfirmDialog(get_info, "账号: " + user + "\n密码: " + password + "\n确认注销？", "注销确认", JOptionPane.YES_NO_OPTION);
                    if (result == JOptionPane.YES_OPTION) {
                        get_info.dispose();  // 用户确认退出
                    }
                }   
            
        });
        get_info.setVisible(true);
        get_info.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        if(find(get_account.getText(), get_pwd.getText()) == -1){
            show("密码错误，请重试");
        }
        else if (find(get_account.getText(), get_pwd.getText()) == 0){
            show("用户不存在，无法注销");
        }
        else{
            delete_data_base(get_account.getText());
            show("注销成功");
        }
    }
    
    public static void change(JFrame windows){
        JDialog get_info = new JDialog(windows, true);
        get_info.setSize(X / 2, Y / 2);


        get_info.getContentPane().setLayout(new BoxLayout(get_info.getContentPane(), BoxLayout.Y_AXIS));
        // 创建输入组件
        JLabel account = new JLabel("账号:");
        JLabel pwd = new JLabel("旧密码:");
        JLabel newpwd = new JLabel("新密码");
        JTextField get_account = new JTextField(20);
        JTextField get_pwd = new JTextField(20);
        JTextField get_newpwd = new JTextField(20);
        JButton ok = new JButton("确认修改");
        get_info.add(account);
        get_info.add(get_account);
        get_info.add(pwd);
        get_info.add(get_pwd);
        get_info.add(newpwd);
        get_info.add(get_newpwd);
        get_info.add(ok);


        
        get_info.setLocationRelativeTo(windows); // 将对话框居中于父窗口
        

        ok.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e){
                    String user = get_account.getText();
                    String password = get_pwd.getText();
                    int result = JOptionPane.showConfirmDialog(get_info, "账号: " + user + "\n新密码: " + password + "\n确认修改？", "修改确认", JOptionPane.YES_NO_OPTION);
                    if (result == JOptionPane.YES_OPTION) {
                        get_info.setVisible(true);
                        get_info.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
                        if(find(get_account.getText(), get_pwd.getText()) == -1){
                            show("旧密码错误，请重试");
                
                        }
                        else if(find(get_account.getText(), get_pwd.getText()) == 0){
                            show("用户不存在");
                        }
                        else{
                            change_datebase(get_account.getText(), get_newpwd.getText());
                            show("修改成功");
                        }
                        get_info.dispose();  // 用户确认退出
                    }
                }   
            
        });

    }

    static void show(String text){
        JDialog dialog = new JDialog();
        // dialog.setTitle("游戏已结束");
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setSize(300, 150);
        dialog.setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());

        JLabel label = new JLabel(text);
        panel.add(label, BorderLayout.CENTER);

        // JButton back = new JButton("返回主页");
        // JButton again = new JButton("再来一把");
        // back.setFont(new Font("宋体", Font.BOLD, 12));
        // again.setFont(new Font("宋体", Font.BOLD, 12));


        // JPanel buttonPanel = new JPanel();

        

        // buttonPanel.add(back);
        // buttonPanel.add(again);
        // panel.add(buttonPanel, BorderLayout.SOUTH);
        dialog.add(panel);

        dialog.setVisible(true);
    }

    static int find(String user, String pwd){
        //0表示没有该用户，-1表示密码不对，1表示找到
        int res = 0;
        try (Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/us", "root", "123456")) {
            try (Statement statement = connection.createStatement()) {
                String sql = "SELECT * FROM user WHERE identify = '" + user + "'";
                try (ResultSet resultSet = statement.executeQuery(sql)) {
                    if (resultSet.next()) {
                        if (pwd.equals(resultSet.getString("password"))) {
                            res = 1;
                        } else {
                            res = -1;
                        }
                    }
                }
            }
        } catch (SQLException e) {
            System.out.println("查找用户时数据库操作出现问题");
            e.printStackTrace();
        }
        return res;
    }

    static void change_datebase(String user, String pwd){
           try (Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/us", "root", "123456")) {
            String sql = "UPDATE user SET password =? WHERE identify =?";
            try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
                preparedStatement.setString(1, pwd);
                preparedStatement.setString(2, user);
                int rowsAffected = preparedStatement.executeUpdate();
                if (rowsAffected > 0) {
                    System.out.println("密码修改成功");
                } else {
                    System.out.println("未找到对应用户，密码修改失败");
                }
            }
        } catch (SQLException e) {
            System.out.println("修改密码时数据库操作出现问题");
            e.printStackTrace();
        }
    }

    static void delete_data_base(String user){
        try (Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/us", "root", "123456")) {
            String sql = "DELETE FROM user WHERE identify =?";
            try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
                preparedStatement.setString(1, user);
                int rowsAffected = preparedStatement.executeUpdate();
                if (rowsAffected > 0) {
                    System.out.println("用户记录删除成功");
                } else {
                    System.out.println("未找到对应用户，删除操作失败");
                }
            }
        } catch (SQLException e) {
            System.out.println("删除用户记录时数据库操作出现问题");
            e.printStackTrace();
        }
    }


    // static void registerNewUser(String user, String pwd) {

    //     try (Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/us", "root", "123456")){
    //         String sql1 = "INSERT INTO user (identify, password) VALUES (?,?)";
    //         System.out.println("!!!!!!!!!!!!!!!!!!!");
    //         try (PreparedStatement queryStatement = connection.prepareStatement(sql1)){
    //             queryStatement.setString(1, user);
    //             queryStatement.setString(2, pwd);
    //             queryStatement.executeUpdate();
    //         }
    //     } catch (SQLException e) {
    //         System.out.println("注册用户时执行更新语句失败");
    //         e.printStackTrace();
    //     }



        
        
    // }
    static void registerNewUser(String identify, String password) {
        String sql = "INSERT INTO user (identify, password) VALUES (?,?)";
        try (Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/us", "root", "123456");
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, identify);
            statement.setString(2, password);
            int result = statement.executeUpdate();
            System.out.println("插入成功，受影响的行数: " + result);
        } catch (SQLException e) {
            System.out.println("注册用户时执行更新语句失败");
            e.printStackTrace();
        }
    }


    static String get_cur_time(){
        LocalDateTime currentDateTime = LocalDateTime.now();
        // 定义日期时间格式，这里采用常见的"yyyy-MM-dd HH:mm:ss"格式
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String formattedDateTime = currentDateTime.format(formatter);
        return formattedDateTime;
    }

    static String querylast_time(String identify) {
        String res = "";
        try (Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/us", "root", "123456")) {
            String sql = "SELECT time FROM game WHERE identify =?";
            try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
                preparedStatement.setString(1, identify);
                try (ResultSet resultSet = preparedStatement.executeQuery()) {
                    if (resultSet.next()) {
                        res = resultSet.getString("time");
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return res;
    }
    
    static void insert_time(String user){
        String time = get_cur_time();
        try (Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/us", "root", "123456")) {
            // 先查询是否存在该user记录
            String querySql = "SELECT COUNT(*) FROM game WHERE user =?";
            try (PreparedStatement queryStatement = connection.prepareStatement(querySql)) {
                queryStatement.setString(1, user);
                try (java.sql.ResultSet resultSet = queryStatement.executeQuery()) {
                    resultSet.next();
                    int count = resultSet.getInt(1);
                    if (count > 0) {
                        // 如果存在，则更新time字段
                        String updateSql = "UPDATE game SET time =? WHERE user =?";
                        try (PreparedStatement updateStatement = connection.prepareStatement(updateSql)) {
                            updateStatement.setString(1, time);
                            updateStatement.setString(2, user);
                            updateStatement.executeUpdate();
                        }
                    } else {
                        // 如果不存在，则插入新记录
                        String insertSql = "INSERT INTO game (user, time) VALUES (?,?)";
                        try (PreparedStatement insertStatement = connection.prepareStatement(insertSql)) {
                            insertStatement.setString(1, user);
                            insertStatement.setString(2, time);
                            insertStatement.executeUpdate();
                        }
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

}
