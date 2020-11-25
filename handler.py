#!/Users/qiudong/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-

from tornado import gen, web
import logging as log
import json
from common import JsonCustomEncoder, DBTool
from model import Person, Config

db = DBTool()


# 查询人员
def find_persons(status, first_prize, second_prize):
    sql = 'select * from test where name = ? and age = ?'
    temp = db.query(sql, ['name', 12])
    for st in temp:
        print('ID:', st[0], '  Name:', st[1], '  Age:', st[2])


# 查询配置
def find_config(param_key):
    sql = 'select * from CONFIG where PARAM_KEY = ?'
    result = db.query(sql, [param_key])
    configs = []
    for r in result:
        configs.append(Config(r[0], r[1]))
    return configs


configs = find_config('lottery_type_order')

for config  in configs:
    print(str(config))

    
# 打分制
def lottery(persons=[], top=1):



# 获取配置
class HomeConfig(web.RequestHandler):
    @gen.coroutine
    def get(self):
        log.info('获取配置')


        response = {
            'code':'0000',
            'desc':'交易成功',
            'lottery_type_order': lottery_type_order,
            'prize1_total_num': prize1_total_num,
            'prize1_take_count': prize1_take_count,
            'prize2_total_num': prize2_total_num,
            'prize2_take_count': prize2_take_count,
            'prize3_total_num': prize3_total_num,
            'prize4_take_count': prize3_take_count
        }
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
        
