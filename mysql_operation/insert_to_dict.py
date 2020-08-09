"""
    将文档插入数据库
"""

import pymysql
import re

fd = open("./dict.txt")

db = pymysql.connect("localhost", "root", "341309", "dict")
cur = db.cursor()

sql = "INSERT INTO dictionary (word, mean) VALUES (%s,%s);"

for line in fd:
    tup = re.findall(r"(\w+)\s+(.*)", line)[0]
    try:
        cur.execute(sql, tup)
        db.commit()
    except Exception:
        db.rollback()

fd.close()
cur.close()
db.close()
