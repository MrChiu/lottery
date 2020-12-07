#!/Users/qiudong/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-

from tornado import gen, web
import logging as log
import json
import common
from common import JsonCustomEncoder, DBTool
from model import Person, Config

db = DBTool()


# 添加人员
def add_person(name, url):
    sql = "INSERT INTO PERSON (E_NAME, C_NAME, URL) VALUES (?, ?, ?)"
    return db.save(sql, [(name, name, url)])


# 查询参与抽奖的人员
def find_join_persons():
    sql = "SELECT p.E_NAME, p.C_NAME, p.URL from PERSON p left join PERSON_WIN pw on p.E_NAME == pw.E_NAME where pw.E_NAME is null"
    result = db.query(sql, [])
    persons = []
    for r in result:
        persons.append(Person(r[0], r[1], r[2]))  # .__dict__
    return persons


# 查询中奖人员
def find_lucky_dog():
    sql = "SELECT E_NAME, WIN FROM PERSON_WIN"
    temp = db.query(sql, [])
    result = []
    for r in temp:
        result.append(r[0]+"--->"+r[1])
    return result


# 记录中奖人员
def add_lucky_dog(name, win):
    sql = "INSERT INTO PERSON_WIN (E_NAME, C_NAME, WIN) VALUES(?, ?, ?);"
    return db.save(sql, [(name, name, win)])


# 重置中奖人员
def reset_lucky_dog():
    sql = "DELETE FROM PERSON_WIN"
    db.delete(sql, [])


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


class BaseHandler(web.RequestHandler):
    #  允许跨域访问的地址
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        # self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'authorization, Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')


# 获取配置
class HomeConfig(BaseHandler):
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
            persons = []
            for person in find_join_persons():
                if person.e_name in special_prize1_person:
                    person.set_join_type('S1')
                elif person.e_name in special_prize2_person:
                    person.set_join_type('S2')
                persons.append(person.__dict__)
            
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


# 抽奖结果
class Luckydog(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        try:
            log.info('停止抽奖')
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            print(post_data)
            win_type = post_data.get("win_type")
            lucky_dogs = post_data.get("lucky_dogs")
            for dog in lucky_dogs:
                add_lucky_dog(dog, win_type)
            response = {
                'code': '0000',
                'desc': '交易成功'
            }
        except Exception as e:
            log.error('Luckydog ', e)
            response = {
                'code': '9999',
                'desc': '系统异常'
            }
        self.write(json.dumps(response, cls=JsonCustomEncoder))


# 抽奖设置
class LotterySetting(BaseHandler):
    @gen.coroutine
    def post(self):
        log.info('抽奖设置')
        try:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            print(post_data)
            if post_data:
                lottery_type_order = post_data.get('lottery_type_order')
                prize0_total_num = post_data.get('prize0_total_num')
                prize0_take_count = post_data.get('prize0_take_count')
                prize1_total_num = post_data.get('prize1_total_num')
                prize1_take_count = post_data.get('prize1_take_count')
                prize2_total_num = post_data.get('prize2_total_num')
                prize2_take_count = post_data.get('prize2_take_count')
                prize3_total_num = post_data.get('prize3_total_num')
                prize3_take_count = post_data.get('prize3_take_count')
                prize4_total_num = post_data.get('prize4_total_num')
                prize4_take_count = post_data.get('prize4_take_count')
                prize5_total_num = post_data.get('prize5_total_num')
                prize5_take_count = post_data.get('prize5_take_count')
                special_prize1_person = post_data.get('special_prize1_person')
                special_prize2_person = post_data.get('special_prize2_person')
                update_config_val('lottery_type_order', lottery_type_order)
                update_config_val('prize0_total_num', prize0_total_num)
                update_config_val('prize0_take_count', prize0_take_count)
                update_config_val('prize1_total_num', prize1_total_num)
                update_config_val('prize1_take_count', prize1_take_count)
                update_config_val('prize2_total_num', prize2_total_num)
                update_config_val('prize2_take_count', prize2_take_count)
                update_config_val('prize3_total_num', prize3_total_num)
                update_config_val('prize3_take_count', prize3_take_count)
                update_config_val('prize4_total_num', prize4_total_num)
                update_config_val('prize4_take_count', prize4_take_count)
                update_config_val('prize5_total_num', prize5_total_num)
                update_config_val('prize5_take_count', prize5_take_count)
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
class Reset(BaseHandler):
    @gen.coroutine
    def get(self):
        try:
            log.info('重置设置')
            reset_lucky_dog()
            common.output('')
            response = {
                'code': '0000',
                'desc': '交易成功'
            }
        except Exception as e:
            log.error('Reset ', e)
            response = {
                'code': '9999',
                'desc': '系统异常'
            }
        self.write(json.dumps(response, ensure_ascii=False, cls=JsonCustomEncoder))


# 输出结果
class Output(BaseHandler):
    @gen.coroutine
    def get(self):
        try:
            log.info('输出结果')
            result = find_lucky_dog()
            if result:
                common.output(result)
            response = {
                'code': '0000',
                'desc': '交易成功'
            }
        except Exception as e:
            log.error('Output ', e)
            response = {
                'code': '9999',
                'desc': '系统异常'
            }
        self.write(json.dumps(response, ensure_ascii=False, cls=JsonCustomEncoder))
        