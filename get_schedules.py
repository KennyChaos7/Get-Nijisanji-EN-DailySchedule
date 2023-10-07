#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import schedule
import time
import os
import json
# import math
import datetime
# import cv2
# import numpy as np
from PIL import Image, ImageFont, ImageDraw

class Liver:
    def __init__(self, name, headIcon, title, scheduleTime, streamThumbnail, streamUrl):
        self.name = name
        self.heabIcon = headIcon
        self.title = title
        self.scheduleTime = scheduleTime
        self.streamThumbnail = streamThumbnail
        self.streamUrl = streamUrl


path = os.getcwd()
imgFileName = path + "/schedules.jpg"
_fontType = './silver.ttf'
_liverList = []
_liveListTextSize = 0
reqUrl = 'https://dhiljqbdkw8vk.cloudfront.net/schedules'
reqParams = {
    
}
reqHeaders = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Content-Encoding': 'gzip',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

def get():
    response = requests.get(url = reqUrl, params = reqParams, headers = reqHeaders)
    if(response.status_code == 200):
        _array = json.loads(response.text)
        for _obj in _array: 
            _headIconJson = json.loads(json.dumps(_obj['StreamerThumbnails']))
            _scheduleArray = json.loads(json.dumps(_obj['Schedule']))
            _channelUrl = json.loads(json.dumps(_obj['ChannelUrl']))
            for _schedule in _scheduleArray:
                if 'ScheduledStartTime' in _schedule:
                    _videoId = json.loads(json.dumps(_schedule['VideoId']))
                    _scheduleThumbnails = json.loads(json.dumps(_schedule['ThumbnailDetails']))
                    _schedule['ScheduledStartTime'] = datetime.datetime.strptime(str(_schedule['ScheduledStartTime']),'%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=8)
                    scheduleDT = _schedule['ScheduledStartTime'].strftime('%Y-%m-%d')                
                    nowDT = datetime.datetime.today().strftime('%Y-%m-%d') 
                    if(scheduleDT == nowDT):
                        _liver = Liver(
                            name = str(_obj['StreamerName']).replace('【NIJISANJI EN】',''),
                            headIcon = _headIconJson['Url'],
                            title = _schedule['Title'],
                            scheduleTime = str(_schedule['ScheduledStartTime'].strftime('%H:%M')),
                            streamThumbnail = _scheduleThumbnails['Url'],
                            streamUrl = "https://youtube.com/watch?v=" + _videoId #_channelUrl + _videoId
                        )
                        # print(_liver.__dict__)
                        global _liverList
                        _liverList.append(_liver)
                        
                        global _liveListTextSize
                        _liveListTextSize = _liveListTextSize + 4 + len(_liver.name) + 8 + len(_liver.heabIcon) + 5 + len(_liver.title) + 12 + len(_liver.scheduleTime) + 15 + len(_liver.streamThumbnail)

                    _liverList.sort(key=takeSecond)

    else:
        print(response.text)        

def saveToJPG(margin = 15, backgroundRGB = [255,255,255], fontType = _fontType, fontRGB = [0,0,0]):

    textList, maxSingleText, allText = decodeText()
    # print(maxSingleText)
    size = tuple([1080, len(_liverList) * 85])
    backgroundRGB = tuple(backgroundRGB)
    fontRGB = tuple(fontRGB)

    image = Image.new('RGB', size, backgroundRGB) # 设置画布大小及背景色
    iwidth, iheight = image.size # 获取画布高宽

    # 计算字节数，GBK编码下汉字双字，英文单字。都转为双字计算
    size=len(maxSingleText.encode('utf-8'))/3
    # 计算字体大小，每两个字号按字节长度翻倍。
    fontSize = 30#math.ceil((iwidth-(margin*2))/size)
    # print(fontSize)
    
    font = ImageFont.truetype(fontType, fontSize) # 设置字体及字号
    draw = ImageDraw.Draw(image)
    
    fwidth, fheight = draw.textsize(allText, font) # 获取文字高宽
    owidth, oheight = font.getoffset(allText)

    fontx = (iwidth - fwidth - owidth) / 2
    # fonty = (iheight - fheight - oheight) / 4
    fonty = fontSize + margin * 2

    draw.text((iwidth / 3, margin), str(datetime.datetime.today().strftime('%Y - %m - %d')) + " - 今天直播人数 : " + str(len(_liverList)), fontRGB, font)
    for tmpText in textList:
        draw.text((fontx, fonty), tmpText, fontRGB, font)
        fonty += fontSize * 2 + margin
        # print(tmpText)
        
    image.save(imgFileName) # 保存图片        

def decodeText():
    textList = []
    maxSingleText = ""
    allText = ""
    _liverList.sort(key=takeSecond)
    for _liver in _liverList:
        # print(_liver.__dict__)
        tmpText = _liver.scheduleTime + " " + _liver.name + "\n      " + _liver.title + "\n"
        textList.append(tmpText)
        allText += tmpText
        if (len(maxSingleText) < len(tmpText)):
            maxSingleText = tmpText
    return textList, maxSingleText, allText

def takeSecond(elem):
    return elem.scheduleTime

def createHtml():
    h1 = str(datetime.datetime.today().strftime('%Y - %m - %d')) + " - 今天直播人数 : " + str(len(_liverList))
    html = """
    <h1 align="center">%s</h1>
    """%(h1)
    f = open('nijisan_en_daily.html','w')
    a_tag_list = []
    for _liver in _liverList:
        a_tag = """
        <h3 align="center">%s</h3>
        <h5 align="center">%s  <a href="%s">LINK</a>
        <br/>
        <img src="%s"/>
        </h5>
        """%(_liver.scheduleTime + "   " + _liver.name, _liver.title, _liver.streamUrl, _liver.streamThumbnail)
        html+=a_tag
    f.write(html)
    f.close()

def main():
    get()
    saveToJPG()
    createHtml()

if __name__ == '__main__':
    main()
#     schedule.every(12).hours.do(main)
#     print("start schedule task ....")
#     while True:
#         schedule.run_pending()  # 运行所有可以运行的任务
#         time.sleep(1)

