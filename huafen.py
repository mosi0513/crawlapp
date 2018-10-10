

from mitmproxy import ctx
import json
from db import MysqlClient
from config import *
import re
import time
import smtplib
from email.mime.text import MIMEText
conn = MysqlClient()
import time



def response(flow):
    url = 'https://api.huafer.cc/api/v1/schizo'
    if flow.request.url.startswith(url):
        text = flow.response.text
        result = json.loads(text)
        if result.get('obj') and result.get('obj').get('items'):
            items = result.get('obj').get('items')
            second = 0
            for x in items:
                second +=1
                if second <=3:
                    if x.get('item') and x.get('counts') and x.get('user'):
                        info1 = x.get('item')
                        info2 = x.get('counts')
                        info3 = x.get('user')
                        sellers = {}
                        stuff_data = {}
                        sellers['STUFFID'] = info1.get('goodsId') # 宝贝id
                        sellers['ADDRESS'] = None #  卖家地址
                        sellers['SELLERNAME'] = info3.get('userName') #  卖家名称
                        sellers['SELLERICON'] = info3.get('avatarUrl') #  卖家头像
                        sellers['SELLERSHOPURL'] = None# 卖家连接
                        sellers['SELLERTYPE'] = '普通卖家' # 卖家类型  黑名单／普通卖家／vip
                        sellers['SELLERTYPEREASON'] = None#  变更原因
                        sellers['ID'] = info3.get('userId')#  主键   程序生成唯一值
                        sellers['CREATE_BY'] = 'python'#  创建者  默认写python
                        sellers['UPDATE_BY'] = 'python'#更新者  默认python
                        sellers['DEL_FLAG'] = '0'# 逻辑删除标记  默认0
                        stuff_data['STUFFID'] = info1.get('goodsId')#  宝贝D
                        stuff_data['ALERT'] = info1.get('brand') + '|' + info1.get('name')#  宝贝名称
                        stuff_data['PRICE'] = info1.get('price') # 价格
                        stuff_data['DESCINFO'] = info1.get('content') #  宝贝介绍
                        stuff_data['IMAGEURL'] = info1.get('goodsImgs')[0] # 图片链接
                        stuff_data['STUFFURL'] = 'https://i.huafer.cc/g/' + str(info1.get('goodsId')) # 宝贝链接
                        stuff_data['SELLERNAME'] = info3.get('userName')# 卖家名称
                        stuff_data['SELLERSHOPURL'] = 'https://i.huafer.cc/u/' + str(info3.get('userId'))# 卖家店铺
                        stuff_data['SELLERICON'] = info3.get('avatarUrl')# 卖家头像
                        stuff_data['MSGCOUNT'] = info2.get('collection')# 点赞数量
                        stuff_data['CUST3'] = '普通卖家'
                        stuff_data['CUST6'] = '花粉儿'


                        username = sellers.get('SELLERNAME')
                        stuffid =  stuff_data.get('STUFFID')
                        stuffprice = stuff_data.get('PRICE')
                        stuffname = stuff_data.get('ALERT')


                        #  判断是否黑名单
                        if conn.query_username(seller, username):
                            print('-'*60)
                            print('卖家已存在， 正在判断卖家类型...')
                            blacklist = conn.query_blacklist(seller, username)
                            if blacklist:
                                print('-'*60)
                                print('该卖家是*黑名单*卖家， 忽略邮件提醒， 爬取数据储存至数据库...')
                                stuff_data['UPDATE_DATE'] = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                                conn.updata(stuff, stuff_data)
                            else:
                                print('无卖家类型信息')


                        else:
                            print('-'*60)
                            print('该卖家是非黑名单类型，开始判断数据是否已有...')
                            if conn.query_id(stuff, stuffid):
                                print('-'*60)
                                print('数据库中存在此商品ID, 正在判断价格是否发生变化...')
                                if conn.query_price(stuff, stuffid, stuffprice):
                                    print('-'*60)
                                    print('价格无变化...')
                                else:


                                    """
                                    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                                    XXXXXXXX  修改邮件发送标题内容（新品上架）XXXXXX
                                    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                                    """

                                    print('-'*60)
                                    print('价格发生变化...')
                                    text1 = '详细内容...'
                                    text2 = '标题...'
                                    send_mail(text1, text2)
                                    stuff_data['UPDATE_DATE'] = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                                    sellers['UPDATE_DATE'] = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                                    conn.updata(seller, sellers)
                                    conn.updata(stuff, stuff_data)


                            else:
                                print('-'*60)
                                print('ID不存在，正在查询数据库中是否有此配置信息...')

                                """
                                XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                                XXXXXXXX  修改邮件发送标题内容（新品上架）XXX
                                XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                                """


                                results = conn.rowcount(config)
                                for result in results:
                                    key = re.search(result[0], stuffname ,re.I)
                                    if key is not None and int(stuffprice) >= int(result[1]) and int(stuffprice) <= int(result[2]):
                                        print('-'*60)
                                        print('配置信息存在， 保存至数据库...')
                                        name = result[0]
                                        stuff_data['CUST5'] = name
                                        stuff_data['CREATE_DATE'] = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                                        sellers['CREATE_DATE'] = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                                        #print(stuff_data)
                                        #print(sellers)
                                        text1 = '详细内容13231321'
                                        text2 = '标题信息'
                                        send_mail(text1, text2)
                                        conn.insert(stuff, stuff_data)
                                        conn.insert(seller, sellers)

                                    else:
                                        print('-'*60)
                                        print('此条不满足配置条件， 正在判断下一条')



#  发送邮件
def send_mail(text1, text2):
    email_host = EMAILHOST
    email_user = EMAILUSER
    email_pwd = EMAILPASSWORD
    maillist = EMAILLIST
    me = email_user
    msg = MIMEText(text1)
    msg['Subject'] = text2
    msg['From'] = me
    msg['To'] = ", ".join(maillist)
    smtp = smtplib.SMTP(email_host, port=25)
    smtp.login(email_user, email_pwd)
    smtp.sendmail(me, maillist, msg.as_string())
    smtp.quit()
    print('-'*60)
    print('邮件发送成功')
