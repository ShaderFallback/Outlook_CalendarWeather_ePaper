#=================BiliBili日出东水===================
#               o365日历获取测试Demo
#----------------------------------------------------

from O365 import Account
import datetime
import time
import os
from collections import OrderedDict


                    #这里填写客户端ID                       #API权限中的值(第一次生成时才能看到)
credentials = ('13e82fa6-d204-4c2a-8670-f388c84277bc', 'aVk8Q~IlcKijyfbSp0dedNgMqm~Eiy_jlzOjDa97')

#第一次运行,生成令牌时运行下面代码
#----------------------------------------------------
#account = Account(credentials)
#if account.authenticate(scopes=['basic', 'calendar_all']):
#    print('Authenticated! 验证成功!')
#----------------------------------------------------


#如想查看所有event属性,可以查看源代码,在976行开始,搜索所有的 @property
#https://github.com/O365/python-o365/blob/412d5b7dc521328ceb84a0086f1d89036bc09bd8/O365/calendar.py

def GetO365(maxCount):
    account = Account(credentials)
    schedule = account.schedule()
    #查询从今天开始一个月内的日历
    #也可以指定 datetime(2022, 5, 30)
    now_time = datetime.datetime.now()
    end_time = datetime.timedelta(days =30)
    range_time = (now_time + end_time).strftime('%Y-%m-%d')

    q = schedule.new_query('start').greater_equal(now_time)
    q.chain('and').on_attribute('end').less_equal(range_time)

    getSchedule = schedule.get_events(query=q, include_recurring=True) 
    
    scheduleDic = OrderedDict()
    scheduleCount = 0
    for event in getSchedule:
        #获取位置
        locationStr = str(event.location).split(",")[0].split(":")[1].replace("'","").replace(" ","")
        #获取时间
        dateTime = event.start
        #获取标题
        subjectStr = event.subject
        #获取正文
        bodyStr = str(event.body)
        startIndex = bodyStr.find("body")
        endIndex = bodyStr.find("/body")
        bodyProcessStr = bodyStr[startIndex+6:endIndex-1].replace("\n","")

        elemDic = OrderedDict()
        elemDic["location"] = locationStr
        elemDic["dateTime"] = dateTime
        elemDic["subjectStr"] = subjectStr
        elemDic["bodyStr"] = bodyProcessStr
        scheduleDic[scheduleCount] = elemDic
        scheduleCount+=1
        if scheduleCount >=maxCount:
            break
    return scheduleDic


while True:
    scheduleDic = GetO365(5)
    print("\n查询到日程数量: "+str(len(scheduleDic))+"\n")

    for x in scheduleDic:
        print("位置: "+ scheduleDic[x]["location"])
        t = scheduleDic[x]["dateTime"]
        print("时间: "+ str(t.month) +"月"+ str(t.day)+"日" + str(t.strftime('%H:%M')))
        print("标题: "+ scheduleDic[x]["subjectStr"])
        print("正文: "+ scheduleDic[x]["bodyStr"])
        print("\n---------------------\n")
    print("等待10秒后刷新")
    print("=======================================\n\n")
    time.sleep(10)


#新建日历事件
#创建一个新事件
#new_event = schedule.new_event()  
#new_event.subject = '这里写标题'
#new_event.location = '位置'
#时间
#new_event.start = dt.datetime(2022, 4, 18, 19, 45)
#设置重复
#new_event.recurrence.set_daily(1, end=dt.datetime(2022, 4, 19))
#提前提醒时间
#new_event.remind_before_minutes = 45 
#更新保存
#new_event.save() 

#发送邮件
#m = account.new_message()
#m.to.add('XXXXXXX@qq.com')
#m.subject = 'Testing!'
#m.body = "这里写正文"
#m.send()


