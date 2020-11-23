#!/Users/qiudong/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-

from tornado import gen, web
import datetime
import common

# 首页handler
class HomeHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        price_1d_s = common.select(
            "SELECT pd.CODE,  MAX(pd.`DATE`) DATE FROM PRICE_1D pd GROUP BY pd.CODE ")
        price_60m_s = common.select(
            "SELECT pm.CODE,  MAX(pm.`DATE`) DATE FROM PRICE_60M pm  GROUP BY pm.CODE ")

        total = 0
        success = 0
        for item in price_1d_s:
            total=total+1
            if item['DATE'] == datetime.datetime.today().date():
                success=success+1
        for item in price_60m_s:
            total = total+1
            if item['DATE'].date() == datetime.datetime.today().date():
                success = success+1
        percent1 = '%.2f' % (success*100/total)
        self.render(
            "index.html", percent1=percent1, price_1d_s=price_1d_s, price_60m_s=price_60m_s, leftMenu=stock_web_dic.GetLeftMenu(self.request.uri))

# 数据同步
class DatasyncHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        print('--------')
