#=================BiliBili日出东水===================
#                   墨水屏天气台历
#----------------------------------------------------
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath + "/lib")

import epd7in5
import epdconfig
import time
from PIL import Image,ImageDraw,ImageFont,ImageChops
import traceback
import datetime
import requests
import logging
from O365 import Account
from collections import OrderedDict
import re

fontSize16 = ImageFont.truetype(rootPath + '/lib/字体.ttf', 16)
fontSize20 = ImageFont.truetype(rootPath + '/lib/字体.ttf', 20)
fontSize25 = ImageFont.truetype(rootPath + '/lib/字体.ttf', 25)
fontSize30 = ImageFont.truetype(rootPath + '/lib/字体.ttf', 30)
fontSize50 = ImageFont.truetype(rootPath + '/lib/字体.ttf', 50)
fontSize70 = ImageFont.truetype(rootPath + '/lib/字体.ttf', 70)

oilStrTime = ""
weekStr = ""
oilStrWeek = ""
countUpdate_1 = False
countUpdate_2 = False
countUpdate_3 = False
countUpdate_4 = False
SwitchDay = True
tempArray = ["---"]*23

def GetO365(maxCount):
                    #这里填写客户端ID                       #API权限中的密码(第一次生成时才能看到)
    credentials = ('44322eca5-007c-4e3358cta-e8bicd8g010d', 'W3-7Q~lqRJBLGXnJGy3qCJfusaRXAyzwcaH.o')
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

def GetTime():
    return(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"   ")
#获取天气
def GetTemp():
    try:                                                                     # 连接超时,6秒，下载文件超时,7秒
        r = requests.get('http://t.weather.itboy.net/api/weather/city/101280701',timeout=(6,7)) 
        r.encoding = 'utf-8'
        tempList = [
        (r.json()['cityInfo']['city']),             #城市0
        (r.json()['data']['shidu']),                #湿度1
        (r.json()['data']['forecast'][0]['low']),   #今日低温2
        (r.json()['data']['forecast'][0]['high']),  #今日高温3
        (r.json()['data']['forecast'][0]['type']),  #今日天气4
        (r.json()['data']['forecast'][0]['fx']),    #今日风向5
        (r.json()['data']['forecast'][0]['fl']),    #今日风级6

        (r.json()['data']['forecast'][1]['low']),   #明日低温7
        (r.json()['data']['forecast'][1]['high']),  #明日高温8
        (r.json()['data']['forecast'][1]['type']),  #明日天气9
        (r.json()['data']['forecast'][1]['fx']),    #明日风向10
        (r.json()['data']['forecast'][1]['fl']),    #明日风级11

        (r.json()['data']['forecast'][2]['low']),   #后日低温12
        (r.json()['data']['forecast'][2]['high']),  #后日高温13
        (r.json()['data']['forecast'][2]['type']),  #后日天气14
        (r.json()['data']['forecast'][2]['fx']),    #后日风向15
        (r.json()['data']['forecast'][2]['fl']),    #后日风级16

        (r.json()['data']['forecast'][3]['low']),   #大后日低温17
        (r.json()['data']['forecast'][3]['high']),  #大后日高温18
        (r.json()['data']['forecast'][3]['type']),  #大后日天气19
        (r.json()['data']['forecast'][3]['fx']),    #大后日风向20
        (r.json()['data']['forecast'][3]['fl']),    #大后日风级21

        (r.json()['cityInfo']['updateTime'])        #更新时间22
        ]
    except:
        tempList = ["---"]*23
        return tempList
    else:
        return tempList

def UpdateWeatherIcon(tempType):  #匹配天气类型图标
    if(tempType == "大雨"  or tempType == "中到大雨"):
        return "大雨.bmp"
    elif(tempType == "暴雨"  or tempType == "大暴雨" or 
        tempType == "特大暴雨" or tempType == "大到暴雨" or
        tempType == "暴雨到大暴雨" or tempType == "大暴雨到特大暴雨"):
        return "暴雨.bmp"
    elif(tempType == "沙尘暴" or tempType == "浮尘" or
        tempType == "扬沙" or tempType == "强沙尘暴" or
        tempType == "雾霾"):
        return "沙尘暴.bmp"
    elif(tempType == "--"):
        return "无天气类型.bmp"
    return (tempType + ".bmp")

def TodayWeek(nowWeek):
    if nowWeek == "0":
        return"星期天"
    elif nowWeek =="1":
        return"星期一"
    elif nowWeek =="2":
        return"星期二"
    elif nowWeek =="3":
        return"星期三"
    elif nowWeek =="4":
        return"星期四"
    elif nowWeek =="5":
        return"星期五"
    elif nowWeek =="6":
        return"星期六"

def UpdateData():
    global tempArray
    tempArray = GetTemp()
    return tempArray

def UpdateTemp(timeUpdate):
    global oilStrWeek
    global tempArray
    global countUpdate_1
    global countUpdate_2
    global countUpdate_3
    global countUpdate_4
    strtime2 = timeUpdate.strftime('%H:%M')   #时间
    strtime4 = timeUpdate.strftime('%w')      #星期
    strtime5 = timeUpdate.strftime('%H')      #小时
    
    if(strtime4 != oilStrWeek):  #每天重置更新天气
        oilStrWeek = strtime4
        countUpdate_1 = True
        countUpdate_2 = True
        countUpdate_3 = True
        countUpdate_4 = True
        tempArray = UpdateData()
        epd.Clear()
        print(GetTime()+'Reset Update..', flush=True)

    # 天气API 只有这几个点会更新,减少无用请求
    intTime = int(strtime5)

    if(countUpdate_1 and  intTime == 7):
        tempArray = UpdateData()
        countUpdate_1 = False
        print(GetTime() + 'UpdateWeather', flush=True)
    elif(countUpdate_2 and intTime == 11):
        tempArray = UpdateData()
        countUpdate_2 = False
        print(GetTime() + 'UpdateWeather', flush=True)
    elif(countUpdate_3 and intTime == 16):
        tempArray = UpdateData()
        countUpdate_3 = False
        print(GetTime() + 'UpdateWeather', flush=True)
    elif(countUpdate_4 and intTime == 21 ):
        tempArray = UpdateData()
        countUpdate_4 = False
        print(GetTime() + 'UpdateWeather', flush=True)

def ReplaceLowTemp(lowTemp):
    temp_L = lowTemp.replace("低温","")
    temp_L = temp_L.replace("℃","")
    temp_L = temp_L.replace(" ","")
    return temp_L

def ReplaceHeightTemp(heighTemp):
    temp_H = heighTemp.replace("高温","")
    temp_H = temp_H.replace("℃","")
    temp_H = temp_H.replace(" ","")
    return temp_H

#348 - 640 像素 居中显示
#居中显示的方法 一个字宽度30像素 例如重479像素开始 多加一个字 少空 15 个像素
def AlignCenter(string,scale,startPixel):
    charsCount = 0
    for s in string:
        charsCount += 1
    charsCount *= scale/2
    charsCount = startPixel - charsCount
    return charsCount

def StrLenCur(text):
    #字母和数字占位与汉字间距不同 
    #2个约等于一个汉字,当包含数字或字母时放宽显示数量
    allStrLen = len(text)
    numberLen = len("".join([x for x in text if x.isdigit()]))
    letterLen = len("".join(re.findall(r'[A-Za-z]',text)))
    sumLen = (numberLen + letterLen)
    characterLen =  allStrLen - sumLen
    calculateLen = characterLen + int(sumLen/3)
    tempLen = (int)(sumLen/3) + 12
    if(calculateLen >= 12):
        return text[0:tempLen]+"..."
    else:
        return text

def DrawHorizontalDar(draw,Himage,timeUpdate):
    strtime = timeUpdate.strftime('%Y-%m-%d') #年月日
    strtime2 = timeUpdate.strftime('%H:%M')   #时间
    strtimeW = timeUpdate.strftime('%w') #星期

    #显示星期
    draw.text((20, 15), TodayWeek(strtimeW), font = fontSize30, fill = 0)
    #显示时间   
    draw.text((128, 8), strtime2, font = fontSize50, fill = 0)
    #显示年月日
    draw.text((20, 55), strtime, font = fontSize16, fill = 0)
    #显示城市
    #draw.text((220, 55), tempArray[0], font = fontSize16, fill = 0)
    #天气图标
    tempTypeIcon = Image.open(rootPath + "/pic/weatherType/" + UpdateWeatherIcon(tempArray[4]))
    Himage.paste(tempTypeIcon,(280,18))
    #今日天气
    draw.text((330,18),tempArray[4], font = fontSize25, fill = 0)
    #温度
    todayTemp = ReplaceLowTemp(tempArray[2])+"-"+ReplaceHeightTemp(tempArray[3]) +" 度"
    draw.text((450,55),todayTemp, font = fontSize16, fill = 0)
    #温度图标
    TempIcon = Image.open(rootPath + "/pic/temp.png")
    Himage.paste(TempIcon,(450,15))
    #显示湿度
    draw.text((545,55),"湿度: "+ tempArray[1], font = fontSize16, fill = 0)
    #湿度图标
    tmoistureIcon = Image.open(rootPath + "/pic/moisture.png")
    Himage.paste(tmoistureIcon,(545,15))
    #风力
    windTemp = tempArray[5] + tempArray[6]
    draw.text((330,55),windTemp, font = fontSize16, fill = 0)

def DrawSchedule(draw,timeUpdate):
    print(GetTime()+'Get Schedule Date...', flush=True)
    scheduleDic = GetO365(6)
    for x in range(0,len(scheduleDic)):
        t = scheduleDic[x]["dateTime"]
        subjectStr = scheduleDic[x]["subjectStr"]
        bodyStr = scheduleDic[x]["bodyStr"]
        #黑方框标记今日
        fillColor = 0
        if(int(t.day) == int(timeUpdate.strftime('%d'))):
            draw.rectangle((5, 95 + x*50, 80, 135 + x*50), fill = "black")
            fillColor = 255
        draw.text((10,100 + x*50),str(t.month) +"月"+ str(t.day)+"日", font = fontSize16, fill = fillColor)
        draw.text((10,115 + x*50),str(t.strftime('%H:%M')), font = fontSize16, fill = fillColor)
        #日程标题
        draw.text((90,95 + x*50),StrLenCur(str(subjectStr)), font = fontSize25, fill = 0)
        #draw.text((15,80 + x*100),bodyStr, font = fontSize16, fill = 0)
    print(GetTime()+'Schedule Done!', flush=True)

def WeatherStrSwitch(index):
    if index == 0:
        return"明天"
    elif index == 1:
        return"后天"
    elif index == 2:
        return"大后天"

def WeatherSwitch(index):
    if index == 0:
        return 4
    elif index == 1:
        return 9
    elif index == 2:
        return 14

def DrawWeather(draw):
    for x in range(0,3):
        draw.text((430,90 + x *100),WeatherStrSwitch(x), font = fontSize16, fill = 0)
        strWeather = tempArray[WeatherSwitch(x)]
        #图标
        pathIcon = UpdateWeatherIcon(strWeather)
        tempTypeIcon = Image.open(rootPath + "/pic/weatherType/" + pathIcon)
        Himage.paste(tempTypeIcon,(454,112 + x*100))
        #天气
        draw.text((510,120 + x *100),strWeather, font = fontSize20, fill = 0)
        #温度
        forecastTemp = ReplaceLowTemp(tempArray[WeatherSwitch(x)-2])+"-"+ReplaceHeightTemp(tempArray[WeatherSwitch(x)-1]) +" 度"
        draw.text((500,145 + x *100),forecastTemp, font = fontSize20, fill = 0)
        #风力
        windTemp = tempArray[WeatherSwitch(x)+1] + tempArray[WeatherSwitch(x)+2]
        draw.text((555,90 + x *100),windTemp, font = fontSize16, fill = 0)

UpdateData()

#刷新循环
while (True):
    print(GetTime()+'Epd7in5 Init...', flush=True)
    epd = epd7in5.EPD()
    epd.init()

    timeUpdate = datetime.datetime.now()
    
    #更新天气
    UpdateTemp(timeUpdate)
    print(GetTime()+'Weather Update Done !', flush=True)
    #时间
    strtime2 = timeUpdate.strftime('%H:%M')
    #小时
    strtime5 = timeUpdate.strftime('%H')      
    intTime = int(strtime5)
    #新建空白图片
    Himage = Image.new('1', (epd.width, epd.height), 128)
    draw = ImageDraw.Draw(Himage)

    #显示背景
    bmp = Image.open(rootPath + '/pic/bg.png')
    Himage.paste(bmp,(0,0))

    #绘制水平栏
    DrawHorizontalDar(draw,Himage,timeUpdate)

    #绘制日程
    DrawSchedule(draw,timeUpdate)

    #绘制天气预报
    DrawWeather(draw)

    #画线(x开始值，y开始值，x结束值，y结束值)
    #draw.rectangle((280, 90, 280, 290), fill = 0)

    #刷新屏幕
    print(GetTime() + 'Update Screen...', flush=True)
    #反向图片
    #Himage = ImageChops.invert(Himage)
    epd.display(epd.getbuffer(Himage))
    #屏幕休眠
    print(GetTime() + 'Screen Sleep...', flush=True)
    epd.sleep()
    print(GetTime() + 'Time.sleep...', flush=True)
    
    if(intTime >= 1 and intTime <= 6): #2点～6点 每小时刷新一次
        time.sleep(3600)
    else:
        time.sleep(600)
