# -*- coding: utf-8 -*-

import sqlite3
import logging as log
import json
import datetime
from decimal import Decimal


# db工具
class DBTool(object):
    def __init__(self):
        """
        初始化函数，创建数据库连接
        """
        self.conn = sqlite3.connect('lottery.db')
        self.dbcur = self.conn.cursor()
        

    def table(self, sql):
        try:
            self.dbcur.execute(sql)
        except Exception as e:
            log.error('table error: ', e)
        finally:
            self.conn.commit()
            self.conn.close()


    def save(self, sql, ob):
        """
        数据库的插入、修改函数
        :param sql: 传入的SQL语句
        :param ob: 传入数据
        :return: 返回操作数据库状态
        """
        try:
            self.dbcur.executemany(sql, ob)
            i = self.conn.total_changes
            if i > 0:
                return True
            else:
                return False
        except Exception as e:
            log.error('save error: ', e)
            return False
        finally:
            self.conn.commit()


    def delete(self, sql, ob):
        """
        操作数据库数据删除的函数
        :param sql: 传入的SQL语句
        :param ob: 传入数据
        :return: 返回操作数据库状态
        """
        try:
            self.dbcur.execute(sql, ob)
            i = self.conn.total_changes
            if i > 0:
                return True
            else:
                return False
        except Exception as e:
            log.error('delete error: ', e)
            return False
        finally:
            self.conn.commit()


    def query(self, sql, ob):
        """
        数据库数据查询
        :param sql: 传入的SQL语句
        :param ob: 传入数据
        :return: 返回操作数据库状态
        """
        try:
            return self.dbcur.execute(sql, ob)
        except Exception as e:
            log.error('query error: ', e)
            return []
        

    def close(self):
        """
        关闭数据库相关连接的函数
        :return:
        """
        self.dbcur.close()
        self.conn.close()


# 序列化
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(Decimal(obj).quantize(Decimal('0.0000')))
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def output(result):
    temp = []
    for r in result:
        r = r+'\n'
        temp.append(r)
    f = open('result.txt', 'w')
    f.writelines(temp)
    f.close()
