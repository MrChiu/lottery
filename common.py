#!/Users/qiudong/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-

import pymysql
import logging

MYSQL_HOST = "localhost" 
MYSQL_USER = "root"
MYSQL_PWD = "abcde"
MYSQL_DB = "stock"

MYSQL_CONN_URL = "mysql+pymysql://" + MYSQL_USER + ":" + MYSQL_PWD + \
    "@" + MYSQL_HOST + ":3306/" + MYSQL_DB

class DB(object):
    def __init__(self, host=MYSQL_HOST, port=3306, db=MYSQL_DB, user=MYSQL_USER, passwd=MYSQL_PWD, charset="utf8mb4"):
        # 创建数据库连接
        self.dbconn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建字典型游标(返回的数据是字典类型)
        self.dbcur = self.dbconn.cursor(cursor=pymysql.cursors.DictCursor)

    # __enter__() 和 __exit__() 是with关键字调用的必须方法
    # with本质上就是调用对象的enter和exit方法
    def __enter__(self):
        # 返回游标
        return self.dbcur

    def __exit__(self, exc_type, exc_value, exc_trace):
        # 提交事务
        self.dbconn.commit()
        # 关闭游标
        self.dbcur.close()
        # 关闭数据库连接
        self.dbconn.close()    


# 插入数据。
def save(sql, params=()):
    with DB() as db:
        logging.info("save sql: %s", sql)
        try:
            db.execute(sql, params)
        except Exception as e:
            logging.error("error : %s", e)


# 查询数据
def select(sql, params=()):
    with DB() as db:
        logging.info("select sql: %s", sql)
        try:
            db.execute(sql, params)
        except Exception as e:
            logging.error("error : %s", e)
        result = db.fetchall()
        if len(result) > 0:
            return result
        else:
            return None

# 查询数据
def select_one(sql, params=()):
    with DB() as db:
        logging.info("select sql: %s", sql)
        try:
            db.execute(sql, params)
        except Exception as e:
            logging.error("error : %s", e)
        result = db.fetchone()
        return result


# 计算数量
def select_count(sql, params=()):
    with DB() as db:
        logging.info("select count sql: %s" + sql)
        try:
            db.execute(sql, params)
        except Exception as e:
            logging.error("error : %s", e)
        result = db.fetchall()
        # 只有一个数组中的第一个数据
        if len(result) == 1:
            return int(result[0][0])
        else:
            return 0

# 删除数据
def delete(sql, params=()):
    with DB() as db:
        logging.info("delete sql: %s", sql)
        try:
            db.execute(sql, params)
        except Exception as e:
            logging.error("error : %s", e)
            
