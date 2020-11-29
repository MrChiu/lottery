#!/Users/qiudong/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-

from tornado import gen, web
import logging as log
import json
from common import JsonCustomEncoder, DBTool
from model import Person, Config

db = DBTool()


# 查询参与抽奖的人员
def find_join_persons():
    sql = "SELECT p.E_NAME, p.C_NAME, p.URL from PERSON p left join PERSON_WIN pw on p.E_NAME == pw.E_NAME where pw.E_NAME is null"
    result = db.query(sql, [])
    persons = []
    for r in result:
        persons.append(Person(r[0], r[1], r[2]).__dict__)
    return persons


# 人员更新为中奖
def update_lucky_dog(name, win):
    sql = "UPDATE PERSON SET STATUS = 'S', WIN = ? WHERE NAME = ?"
    return db.save(sql, [(win, name)])


# 人员更新为指定抽一等奖
def update_appoint_prize1(name):
    sql = "UPDATE PERSON SET APPOINT_PRIZE1 = 'Y' WHERE NAME = ?"
    return db.save(sql, [(name,)])


# 人员更新为指定抽二等奖
def update_appoint_prize2(name):
    sql = "UPDATE PERSON SET APPOINT_PRIZE2 = 'Y' WHERE NAME = ?"
    return db.save(sql, [(name,)])


# 查询配置
def find_config_val(param_key):
    sql = 'SELECT * FROM CONFIG WHERE PARAM_KEY = ?'
    result = db.query(sql, [param_key])
    configs = []
    for r in result:
        configs.append(Config(r[0], r[1]))
    if configs:
        return configs[0].param_object
    else:
        return None


# 更新配置
def update_config_val(param_key, param_object):
    sql = 'UPDATE CONFIG SET PARAM_OBJECT = ? WHERE PARAM_KEY = ?'
    return db.save(sql, [(param_object, param_key)])


# 获取配置
class HomeConfig(web.RequestHandler):
    @gen.coroutine
    def get(self):
        log.info('获取配置')
        try:
            lottery_type_order = find_config_val('lottery_type_order')
            prize0_total_num = find_config_val('prize0_total_num')
            prize0_take_count = find_config_val('prize0_take_count')
            prize1_total_num = find_config_val('prize1_total_num')
            prize1_take_count = find_config_val('prize1_take_count')
            prize2_total_num = find_config_val('prize2_total_num')
            prize2_take_count = find_config_val('prize2_take_count')
            prize3_total_num = find_config_val('prize3_total_num')
            prize3_take_count = find_config_val('prize3_take_count')
            special_prize1_person = find_config_val('special_prize1_person')
            special_prize2_person = find_config_val('special_prize2_person')
            persons = find_join_persons()
            response = {
                'code':'0000',
                'desc':'交易成功',
                'lottery_type_order': lottery_type_order,
                'prize0_total_num': prize0_total_num,
                'prize0_take_count': prize0_take_count,
                'prize1_total_num': prize1_total_num,
                'prize1_take_count': prize1_take_count,
                'prize2_total_num': prize2_total_num,
                'prize2_take_count': prize2_take_count,
                'prize3_total_num': prize3_total_num,
                'prize3_take_count': prize3_take_count,
                'special_prize1_person': special_prize1_person,
                'special_prize2_person': special_prize2_person,
                'persons': persons
            }
        except Exception as e:
            log.error('HomeConfig ', e)
            response = {
                'code': '9999',
                'desc': '系统异常'
            }
        self.write(json.dumps(response, ensure_ascii=False, cls=JsonCustomEncoder))


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
        try:
            lottery_type_order = self.get_argument('lottery_type_order', default='s1,s2,3,2,1')
            prize1_total_num = self.get_argument('prize1_total_num', default=0)
            prize1_take_count = self.get_argument('prize1_take_count', default=0)
            prize2_total_num = self.get_argument('prize2_total_num', default=0)
            prize2_take_count = self.get_argument('prize2_take_count', default=0)
            prize3_total_num = self.get_argument('prize3_total_num', default=0)
            prize3_take_count = self.get_argument('prize3_take_count', default=0)
            special_prize1_person = self.get_argument('special_prize1_person')
            special_prize2_person = self.get_argument('special_prize2_person')
            update_config_val('lottery_type_order', lottery_type_order)
            update_config_val('prize1_total_num', prize1_total_num)
            update_config_val('prize1_take_count', prize1_take_count)
            update_config_val('prize2_total_num', prize2_total_num)
            update_config_val('prize2_take_count', prize2_take_count)
            update_config_val('prize3_total_num', prize3_total_num)
            update_config_val('prize3_take_count', prize3_take_count)
            update_config_val('special_prize1_person', special_prize1_person)
            update_config_val('special_prize2_person', special_prize2_person)
            response = {
                'code': '0000',
                'desc': '交易成功'
            }
        except Exception as e:
            log.error('LotterySetting ', e)
            response = {
                'code': '9999',
                'desc': '系统异常'
            }
        self.write(json.dumps(response, ensure_ascii=False, cls=JsonCustomEncoder))


# 重置设置
class Reset(web.RequestHandler):
    @gen.coroutine
    def get(self):
        log.info('重置设置')
        find_persons('S', )

