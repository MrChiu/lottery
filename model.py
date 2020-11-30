# -*- coding: utf-8 -*-


# 人员信息
class Person(object):
    def __init__(self, e_name, c_name, url):
        # 姓名
        self.e_name = e_name
        self.c_name = c_name
        # 头像
        self.url = url
        # 参与类型 N:普通  S1: 优先1等奖   S2:优先2等奖
        self.join_type = 'N'

    def set_join_type(self, join_type):
        self.join_type = join_type



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
