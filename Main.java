static int find(String user, String pwd){
    //0表示没有该用户，-1表示密码不对，1表示找到
    int res = 0;
    return res;
}

static void change_pwd(String user, String new_pwd){

}

static void delete_user(String user){

}


static void registerNewUser(String user, String pwd) {

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

    return res;
}

static void insert_time(String user){
    //数据库时间使用String
    String time = get_cur_time();
    
}
