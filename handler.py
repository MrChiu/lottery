#!/Users/qiudong/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-

from tornado import gen, web
import logging as log
import json
from common import JsonCustomEncoder, DBTool

db = DBTool()

def find_persons(status, first_prize, second_prize):
    sql = 'select * from test where name = ? and age = ?'
    temp = db.query(sql, ['name', 12])
    for st in temp:
        print('ID:', st[0], '  Name:', st[1], '  Age:', st[2])


# 获取配置
class HomeConfig(web.RequestHandler):
    @gen.coroutine
    def get(self):
        log.info('获取配置')
        response = []
        self.write(json.dumps(response, cls=JsonCustomEncoder))


# 开始抽奖
class LotteryStart(web.RequestHandler):
    @gen.coroutine
    def get(self):
        log.info('开始抽奖')
        start_param = self.get_argument("start", default=0, strip=False)
        response = []
        self.write(json.dumps(response, cls=JsonCustomEncoder))


# 停止抽奖
class LotteryStop(web.RequestHandler):
    @gen.coroutine
    def get(self):
        log.info('停止抽奖')


        response = []
        self.write(json.dumps(response, cls=JsonCustomEncoder))


# 抽奖设置
class LotterySetting(web.RequestHandler):
    @gen.coroutine
    def get(self):
        log.info('抽奖设置')
        
