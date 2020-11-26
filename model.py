# -*- coding: utf-8 -*-


# 人员信息
class Person(object):
    def __init__(self, name, pic, status, win):
        # 姓名
        self.name = name
        # 头像
        self.pic = pic
        # 状态(I:未中奖 S:已中奖)
        self.status = status
        # 中奖(1,2,3)
        self.win = win


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
