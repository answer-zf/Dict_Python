"""
    客户端
"""

from socket import *
from getpass import getpass

HOST = "127.0.0.1"
PORT = 12016
ADDR = (HOST, PORT)

# 创建套接字
sock_fd = socket()
sock_fd.connect(ADDR)


def do_query(name):
    """
        查询单词
    :param name: 用户名
    :return:
    """

    while True:
        word = input("word: ")

        if word == "##":
            break

        if " " in word:
            print("Word Can't Have Space")
            continue

        query_msg = "Q %s %s" % (name, word)
        sock_fd.send(query_msg.encode())

        response_msg = sock_fd.recv(2048).decode()
        print(response_msg)


def login(name):
    """
        登陆 / 注册成功进入二级页面
    :param name:用户名
    :return:
    """
    while True:

        print("""
        ============== Query Dictionary ==============

            1. Query Word    2. History    3. Exit

        ==============================================\n
        """)

        str_cmd = input("PL. Command Number:")

        if str_cmd == "1":
            do_query(name)
        elif str_cmd == "2":
            pass
        elif str_cmd == "3":
            print("Bye ...")
            return
        else:
            print("Command error, pl. input again...")


def do_login():
    """
        登陆
    :return:
    """

    name = input("user name: ")
    password = getpass()

    login_msg = "L %s %s" % (name, password)
    sock_fd.send(login_msg.encode())

    response_msg = sock_fd.recv(128).decode()

    if response_msg == "OK":
        print("Login Success !")
        login(name)
    else:
        print("Login Failed !")


def do_register():
    """
        注册
    :return:
    """

    while True:

        str_name = input("user name: ")
        str_password = getpass()  # 隐藏输入内容
        str_password_again = getpass("Again: ")

        if " " in str_name or " " in str_password:
            print("Name or Password Can't Have Space")
            continue

        if str_password != str_password_again:
            print("Inconsistent Passwords")
            continue

        # 发送请求
        register_msg = "R %s %s" % (str_name, str_password)
        sock_fd.send(register_msg.encode())

        # 收到响应
        response_msg = sock_fd.recv(128).decode()

        if response_msg == "OK":
            print("Register Success!")
            login(str_name)
        else:
            print("Register Failed!")
        return


def main():
    """
        客户端主程序
    :return:
    """

    while True:

        print("""
        ============= Welcome Dictionary =============
        
              1. Login    2. Register    3. Exit
        
        ==============================================\n
        """)

        str_cmd = input("PL. Command Number:")

        if str_cmd == "1":
            do_login()
        elif str_cmd == "2":
            do_register()
        elif str_cmd == "3":
            sock_fd.send(b"E")
            print("Thanks..")
            return
        else:
            print("Command error, pl. input again...")


if __name__ == '__main__':
    main()
