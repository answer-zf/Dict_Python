## 电子辞典

### 技术

-   编码：Python

-   通信：TCP

-   并发：多进程

-   数据库：MySQL

### 数据库

1.  用户表结构： 

    -   id: int primary key auto_increment
    -   name: varchar(32) not null
    -   passwd:varchar(32) not null

2.  历史纪录表结构：

    -   id: int primary key auto_increment
    -   name: varchar(32) not null
    -   word: varchar(32) not null
    -   time: varchar(64) not null
    
3.  字典表结构：

    -   id: int primary key auto_increment
    -   word: varchar(32) not null
    -   explain: text
    
#### 步骤：

`create database dict charset=utf8;`

1.  user
    
    -   `create table user(id int primary key auto_increment, name varchar(32) not null, passwd varchar(128) not null);`

2.  history

    -   `create table history(id int primary key auto_increment, name varchar(32) not null, word varchar(32) not null, time varchar(64) not null);`
    
    
3.  dictionary
    
    -   `create table dictionary(id int primary key auto_increment, word varchar(32), mean text);`
    
### 功能：

1.  网络模型

    -   请求协议：
    
        -   注册： R name password
        -   登陆： L name password
        -   退出:  E
        -   查单词:  Q name word

2.  登陆注册

3.  查单词

4.  历史记录
