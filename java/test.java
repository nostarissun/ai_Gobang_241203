

// import java.io.BufferedReader;
// import java.io.IOException;
// import java.io.InputStreamReader;
// import java.io.OutputStream;
// import java.net.Socket;

// public class test {
//     public static void main(String args[]){
//         int[][] chess_board = new int[800/30][650/30];
//     int m = 800/30;
//     int n = 650/30;
    
//     for(int i = 0; i < m; i++){
//         for(int j = 0; j < n; j++){
//             chess_board[i][j] = 1;
//         }
//     }
//         String serverName = "172.17.226.23";
//         int servePort = 12000;
//         byte[] buffer = new byte[1024];
//         int bytesRead = 0;
//         String modifiedSentence = new String(buffer, 0, bytesRead);
//         try {
//             // 创建套接字并连接到服务器
//             Socket clientSocket = new Socket(serverName, servePort);

//             // 获取用户输入
//             String sentence = new String();
//             BufferedReader userInput = new BufferedReader(new InputStreamReader(System.in));
//             for(int i = 0; i < 800 / 30; i++)
//             {
//                 for(int j = 0; j < 650 / 30; j++)
//                 {
//                     sentence += chess_board[i][j];
//                 }
//             }
            

//             // 向服务器发送数据
//             OutputStream outputStream = clientSocket.getOutputStream();
//             outputStream.write(sentence.getBytes());

//             // 接收服务器返回的数据
//             bytesRead = clientSocket.getInputStream().read(buffer);
            

//             // 打印服务器返回的内容
//             // for(int i = 0; i < 800 / 30; i++)
//             // {
//             //     for(int j = 0; j < 650 / 30; j++)
//             //     {
//             //         chess_board[i][j] = Integer.parseInt(modifiedSentence.charAt(650 / 30 * i + j));
//             //     }
//             // }
            
//             // 关闭套接字
//             clientSocket.close();
//         } catch (IOException a) {
//             a.printStackTrace();
//         }
//             int x = Integer.parseInt(modifiedSentence, modifiedSentence.charAt(0));
//             int y = Integer.parseInt(modifiedSentence, modifiedSentence.charAt(1));
//          System.out.println(x);
//          System.out.println(y);       
//     }
    
// }
public class test {
    public static void main(String args[]){
        System.out.println(650/30);
        System.out.println(800/30);
    }
}