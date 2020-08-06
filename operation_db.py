"""
    dict项目 数据库处理
"""

import pymysql
import hashlib
import time


class Database:
    def __init__(self, host="localhost",
                 port=3306,
                 user="root",
                 passwd="341309",
                 database="dict",
                 charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()

    def connect_db(self):
        """
            创建数据库连接
        :return:
        """
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    def create_cursor(self):
        """
            创建游标
        :return:
        """
        self.cursor = self.db.cursor()

    def close(self):
        """
            关闭数据库
        :return:
        """
        self.cursor.close()
        self.db.close()

    def register(self, name, password):
        """
            注册逻辑
        :param name: 用户名
        :param password: 密码
        :return: bool
        """

        # 查询数据库中是否该用户名
        select_sql = "SELECT * FROM user WHERE name = %s;"
        self.cursor.execute(select_sql, name)

        if self.cursor.fetchone():
            return False

        # 加密
        hash = hashlib.md5((name + "the-salt").encode())
        hash.update(password.encode())

        # 将用户名,密码存入数据库中
        insert_sql = "INSERT INTO user (name, passwd) VALUES (%s,%s);"

        try:
            self.cursor.execute(insert_sql, [name, hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self, name, password):
        """
            登陆
        :param name: 用户名
        :param password: 密码
        :return: bool
        """

        hash = hashlib.md5((name + "the-salt").encode())
        hash.update(password.encode())

        select_sql = "SELECT * FROM user WHERE name=%s and passwd=%s"
        self.cursor.execute(select_sql, [name, hash.hexdigest()])

        if self.cursor.fetchone():
            return True
        else:
            return False

    def insert_history(self, name, word):
        """
            插入历史记录
        :param name: 所登陆的用户
        :param word: 所查询的单词
        :return:
        """

        insert_sql = "INSERT INTO history (name,word,time) VALUES (%s,%s,%s);"

        try:
            self.cursor.execute(insert_sql, [name, word, time.ctime()])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def do_query(self, word):
        """
            查询单词
        :param word: 所查询的单词
        :return:
        """
        select_sql = "SELECT mean FROM dictionary WHERE word=%s;"
        self.cursor.execute(select_sql, word)

        mean = self.cursor.fetchone()
        if mean:
            return mean[0]
