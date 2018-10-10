
import pymysql
from config import *
class MysqlClient(object):

    def __init__(self, host=HOST, port=MSQLPORT, user=MSQLUSER, password=MSQLPASSWORD, db=DB):

        self.db = pymysql.connect(host=host, user=user, password=password, port=port, db=db, charset='utf8')
        self.cursor = self.db.cursor()



    #  插入数据
    def insert(self, table, data):
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table,keys=keys,values=values)
        #try:
        if self.cursor.execute(sql, tuple(data.values())):
            self.db.commit()
            if table == 'T_STUFF':
                print('商品信息保存到数据库成功')
            elif table == 'T_CONFIG':
                print('配置信息添加到数据库成功')
            elif table == 'T_SELLER':
                print('卖家信息添加到数据库成功')
        else:
            if table == 'T_STUFF':
                print('*商品信息保存到数据库失败*')
            elif table == 'T_CONFIG':
                print('*配置信息添加到数据库失败*')
            elif table == 'T_SELLER':
                print('*卖家信息添加到数据库失败*')



    #  存在则不操作， 不存在则插入
    def updata(self, table, data):
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '.format(table=table,keys=keys,values=values)
        update = ','.join(["{key} = %s".format(key=key) for key in data])
        sql += update
        if self.cursor.execute(sql, tuple(data.values()) * 2):
            self.db.commit()
            if table == 'T_STUFF':
                print('商品信息更新到数据库成功')
            elif table == 'T_CONFIG':
                print('配置信息更新到数据库成功')
            elif table == 'T_SELLER':
                print('卖家信息更新到数据库成功')
        else:
            if table == 'T_STUFF':
                print('*商品信息更新到数据库失败*')
            elif table == 'T_CONFIG':
                print('*配置信息更新到数据库失败*')
            elif table == 'T_SELLER':
                print('*卖家信息更新到数据库失败*')

    #  返回所有的数量
    def count(self, table, data=None):
        sql = "select * from {table}".format(table=table)
        self.cursor.execute(sql)
        return self.cursor.rowcount


    #  返回所有数据库查询的数据
    def rowcount(self, table, data=None):
        sql = "select * from {table}".format(table=table)
        self.cursor.execute(sql)
        return self.cursor.fetchall()




    #  查询宝贝id
    def query_id(self, table, id):
        sql = "select * from %s where  STUFFID = %s"%(table,id)
        if self.cursor.execute(sql):
            return True
        else:
            return False


    # 查询宝贝价格与id
    def query_price(self, table, id, price):
        sql = "select * from %s where  STUFFID=%s and PRICE=%s"%(table,id,price)
        if self.cursor.execute(sql):
            return True
        else:
            return False

    #  查询是否黑名单
    def query_blacklist(self, table, sellername):
        sellertype = '黑名单'
        sql = "select * from %s where SELLERNAME='%s' and SELLERTYPE='%s'"%(table, sellername, sellertype)
        if self.cursor.execute(sql):
            return True
        else:
            return False

    #  查询用户
    def query_username(self, table, sellername):
        sql = "select * from %s where SELLERNAME='%s'"%(table, sellername)
        if self.cursor.execute(sql):
            return True
        else:
            return False


    #  删除数据
    def deld(self, table, condition):
        sql = "DELETE FROM {table} where {field} like %s".format(table=table,field='NAME')
        if self.cursor.execute(sql, (condition,)):
            self.db.commit()
            print('删除成功')
