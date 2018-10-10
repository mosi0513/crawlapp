
from start import Huafen
from config import *
from db import *
huafen = Huafen(appPackage, appActivity)
conn = MysqlClient()

class Schedule():

    #  向数据库中添加配置信息
    def add(self):
        print('请输入关键字')
        key = input()
        print('请输入最高价格')
        startprice = input()
        print('请输入最低价格')
        endprice = input()
        data = {
        'NAME' : key,
        'STARTPRICE' : startprice,
        'ENDPRICE' : endprice,
        'ID': key + startprice + endprice
        }
        conn.updata(config, data)
        print('继续添加请按1， 返回请按0')
        black = input()
        if black == '1':
            return self.add()
        elif black == '0':
            self.go()


    #  查询当前数据库中的配置项信息
    def query(self):
        self.que()
        print('返回请按0')
        black = input()
        if black == '0':
            self.go()
        elif black == '0':
            self.go()



    #  查询数据
    def que(self):
        print('---'*20)
        results = conn.rowcount(config)
        if results:
            for result in results:
                print(result[0]+ ' ' +  result[1]+ ' ' +  result[2]+ ' ' +  result[19])
            print('总共有%s条配置信息'%conn.count(config))
            print('---'*20)
        else:
            print('数据库中无数据， 添加数据请按0')
            black = input()
            if black == '0':
                self.add()


    #  删除数据
    def deld(self):
        self.que()
        print('请输入关键字进行删除')
        deld = input()
        conn.deld(config, deld)
        print('数据库中当前数据')
        self.que()
        print('继续删除请按1， 返回上一级请按0')
        going = input()
        if going == '1':
            return self.deld()
        elif going == '0':
            self.go()


    #  根据提示完成操作
    def go(self):
        print(' **请输入对应的序号来完成操作**\n 1.开启手机模拟操作(不含数据截获功能，返回上一级直接可同时开启模拟操作与数据截获)\n 2.查询所有配置信息\n 3.添加新的配置信息\n 4.删除配置信息\n 0.退出')
        keys = input()
        if keys == '1':#  开启程序
            huafen.action()
        elif keys == '3':#  添加配置信息
            self.add()
        elif keys == '2':#  查询所有的配置信息
            self.query()
        elif keys == '4':#  删除配置信息
            self.deld()
        elif keys == '0':#  修改某条信息
            print('已退出程序')
            exit()
        else:
            print('输入错误，请从新输入')
