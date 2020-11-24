# -*- coding: utf-8 -*-

from common import DBTool

db = DBTool()

ob = [(3, 'name', '12')]
sql = 'insert into test (id, name, age) values (?,?,?)'
T = db.save(sql, ob)
if T:
    print('插入成功！')
else:
    print('插入失败！')
