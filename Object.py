# -*- coding: utf-8 -*-


# 人员信息
class Person(object):

    def __init__(self):
        # 手机号
        self.mobile = None
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

    def init(self, mobile, name, pic, status, first_prize, second_prize):
        self.mobile = mobile
        self.name = name
        self.pic = pic
        self.status = status
        self.first_prize = first_prize
        self.second_prize = second_prize


# 配置信息
# param_key: param_object
# 抽奖顺序(默认) order: s1(special 1等奖),s2(special 2等奖),3(3等奖),2(2等奖),1(1等奖)
# 抽奖配置 prize1:k,m,n  prize2:k,m,n  prize3:k,m,n
class Config(object):
    def __init__(self):
        self.param_key = None
        self.param_object = None
