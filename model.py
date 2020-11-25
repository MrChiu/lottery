# -*- coding: utf-8 -*-


# 人员信息
class Person(object):

    def __init__(self):
        # 姓名
        self.name = None
        # 头像
        self.pic = None
        # 中奖状态(I:未中奖 s:已中奖)
        self.status = None
        # 一等奖优先标记 Y
        self.first_prize = None
        # 二等奖优先标记 Y
        self.second_prize = None

    def init(self, name, pic, status, first_prize, second_prize):
        self.name = name
        self.pic = pic
        self.status = status
        self.first_prize = first_prize
        self.second_prize = second_prize


# 配置信息
# param_key: param_object
# 抽奖顺序(默认) lottery_type_order: s1(special 1等奖),s2(special 2等奖),3(3等奖),2(2等奖),1(1等奖)
# 抽奖配置 prize1_total_num prize1_take_count prize2_total_num prize2_take_count prize3_total_num prize3_take_count
class Config(object):
    def __init__(self, param_key, param_object):
        self.param_key = param_key
        self.param_object = param_object

    def __str__(self) :
        return 'param_key:' + self.param_key + ',' + 'param_object:' + self.param_object
