"""
    dict项目 数据库处理
"""

import pymysql


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
        self.db = pymysql.connect(self.host,
                                  self.port,
                                  self.user,
                                  self.passwd,
                                  self.database,
                                  self.charset)

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

