
from uiautomator import device as d
import time
import os
import sys
from db import *
from config import *
conn = MysqlClient()
nums = 0
sys.setrecursionlimit(1000000)




class Huafen():
    def __init__(self, appPackage, appActivity):
        self.appPackage = appPackage
        self.appActivity = appActivity
        self.kill_app = 'adb shell am force-stop {appPackage}'.format(appPackage=appPackage)
        self.start_app = 'adb shell am start -n {appPackage}/{appActivity}'.format(appPackage=appPackage, appActivity=appActivity)


    def run(self, name, price1,price2):
        os.system(self.kill_app)
        print ('kill apk')
        os.system(self.start_app)
        time.sleep(5)
        print ('start apk')
        d(text=u"搜索你想要的宝贝").click()
        time.sleep(2)
        d(resourceId="com.huapu.huafen:id/etSearch").set_text(name)
        time.sleep(2)
        d.click(1000, 1845)
        time.sleep(2)
        d(resourceId="com.huapu.huafen:id/tvName", text=u"时间").click()
        time.sleep(2)
        d(resourceId="com.huapu.huafen:id/tvTitleBarRight").click()
        time.sleep(2)
        d(resourceId="com.huapu.huafen:id/etPriceLow").set_text(price1)
        time.sleep(2)
        d(resourceId="com.huapu.huafen:id/etPriceHigh").set_text(price2)
        time.sleep(2)
        d(resourceId="com.huapu.huafen:id/tvBtnConfirm").click()
        #d.swipe(527, 1803, 535, 273, 2)# 模拟向上滑动
        #d.press("back") 返回


    # 开启程序， 从数据库传入参数
    def action(self):
        global nums
        succ = 0
        while True:
            try:
                results = conn.rowcount(config)
                for result in results:
                    self.run(result[0], result[1], result[2])
                    print(time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())))
                    succ +=1
                    print('成功爬取%s次'%succ)

            except:
                nums +=1
                print('失败%s次'%nums)
                print(time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())))


if __name__ == '__main__':
    schedule = Huafen('com.huapu.huafen', '.activity.SplashActivity')
    schedule.action()
