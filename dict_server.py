"""
    服务端
"""

from socket import *
from multiprocessing import Process
import signal
import sys

from operation_db import *

HOST = "0.0.0.0"
PORT = 12016
ADDR = (HOST, PORT)


def do_login(conn_fd, db, data):
    """
        登陆
    :param conn_fd: 连接套接字
    :param db: 数据库连接对象
    :param data: 登陆信息
    :return:
    """

    tmp = data.split(" ")
    name = tmp[1]
    password = tmp[2]

    if db.login(name, password):
        conn_fd.send(b"OK")
    else:
        conn_fd.send(b"FAIL")


def do_register(conn_fd, db, data):
    """
        注册逻辑
    :param conn_fd: 连接套接字
    :param db: 数据库连接对象
    :param data: 注册信息
    :return:
    """

    tmp = data.split(" ")
    name = tmp[1]
    password = tmp[2]

    if db.register(name, password):
        conn_fd.send(b"OK")
    else:
        conn_fd.send(b"FAIL")


def do_query(conn_fd, db, data):
    """
        查询单词
    :param conn_fd: 连接套接字
    :param db: 数据库连接对象
    :param data: 注册信息
    :return:
    """

    tmp = data.split(" ")
    name = tmp[1]
    word = tmp[2]

    # 插入历史纪录
    db.insert_history(name, word)
    # 查单词
    mean = db.do_query(word)
    if not mean:
        conn_fd.send(b"The World Was Not Found")
    else:
        mean_msg = "%s : %s" % (word, mean)
        conn_fd.send(mean_msg.encode())


def do_request(conn_fd, db):
    """
        处理请求
    :param conn_fd: 连接套接字
    :param db: 数据库连接对象
    :return:
    """

    # 生成游标 db.cursor()
    db.create_cursor()

    while True:
        request_msg = conn_fd.recv(1024).decode()
        print(conn_fd.getpeername(), ":", request_msg)

        if not request_msg or request_msg[0] == "E":
            conn_fd.close()
            sys.exit("Client Exit")
        elif request_msg[0] == "L":
            do_login(conn_fd, db, request_msg)
        elif request_msg[0] == "R":
            do_register(conn_fd, db, request_msg)
        elif request_msg[0] == "Q":
            do_query(conn_fd, db, request_msg)


def main():
    """
        服务器主程序
    :return:
    """

    # 创建数据库连接对象
    db = Database()

    # 创建套接字
    sock_fd = socket()
    sock_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock_fd.bind(ADDR)
    sock_fd.listen(3)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    print("listen 12016....")

    while True:
        # 等待客户端连接
        try:
            conn_fd, addr = sock_fd.accept()
            print("connect ...", addr)
        except KeyboardInterrupt:
            sock_fd.close()
            db.close()
            sys.exit("server exit...")
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        p = Process(target=do_request, args=(conn_fd, db))
        p.daemon = True  # 子进程随父进程退出而退出
        p.start()


if __name__ == '__main__':
    main()
