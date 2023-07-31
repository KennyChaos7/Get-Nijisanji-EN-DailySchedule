#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import schedule
import time
import os
import json
import math
# import cv2
# import numpy as np
from PIL import Image, ImageFont, ImageDraw

class Liver:
    def __init__(self, name, headIcon, title, scheduleTime, streamThumbnail):
        self.name = name
        self.heabIcon = headIcon
        self.title = title
        self.scheduleTime = scheduleTime
        self.streamThumbnail = streamThumbnail


path = os.getcwd()
imgFileName = path + "/schedules.jpg"
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
    response = requests.get(url=reqUrl, params=reqParams, headers=reqHeaders)
    if(response.status_code == 200):
        _array = json.loads(response.text)
        for _obj in _array: 
            _headIconJson = json.loads(json.dumps(_obj['StreamerThumbnails']))
            _scheduleArray = json.loads(json.dumps(_obj['Schedule']))
            _schedule = _scheduleArray[0]
            _scheduleThumbnails = json.loads(json.dumps(_schedule['ThumbnailDetails']))
            _headMedium = _headIconJson.get("Medium")
            _streamMediumThumbnail = json.loads(json.dumps(_scheduleThumbnails['Medium']))

            _liver = Liver(
                name = _obj['StreamerName'],
                headIcon = _headMedium['Url'],
                title = _schedule['Title'],
                scheduleTime = _schedule['ScheduledStartTime'],
                streamThumbnail = _streamMediumThumbnail['Url']
            )
            global _liverList
            _liverList.clear()
            _liverList.append(_liver)
            
            global _liveListTextSize
            _liveListTextSize += _liver.__dict__
        print(_liveListTextSize)   
    else:
        print(response.text)        


def CreatePic(size=[500,800],margin=50,backgroundRGB=[255,255,255],fontType=r'\\System\\Library\\Fonts\\AmericanTypewriter.ttc',fontRGB=[0,0,0]):

    

    size=tuple(size)
    backgroundRGB=tuple(backgroundRGB)
    fontRGB=tuple(fontRGB)

    image = Image.new('RGB', size, backgroundRGB) # 设置画布大小及背景色
    iwidth, iheight = image.size # 获取画布高宽

    # 计算字节数，GBK编码下汉字双字，英文单字。都转为双字计算
    size=len(_liveListTextSize.encode('gbk'))/2
    # 计算字体大小，每两个字号按字节长度翻倍。
    fontSize=math.ceil((iwidth-(margin*2))/size)

    font = ImageFont.truetype(fontType, fontSize) # 设置字体及字号
    draw = ImageDraw.Draw(image)

    fwidth, fheight = draw.textsize(_liveListTextSize, font) # 获取文字高宽
    owidth, oheight = font.getoffset(_liveListTextSize)

    fontx = (iwidth - fwidth - owidth) / 2
    fonty = (iheight - fheight - oheight) / 2

    # draw.text((fontx, fonty), text, fontRGB, font)

    image.save(imgFileName) # 保存图片        

def get_data_task():
    # print("start new round ....")
    get()
    # CreatePic()
    # print("finish this round ....")

get_data_task()
# schedule.every(10).seconds.do(get_data_task)
# schedule.every(15).minutes.do(get_data_task)
# schedule.every(12).hours.do(get_data_task)
# os.popen(openServer)
# print("start schedule task ....")
# while True:
#     schedule.run_pending()  # 运行所有可以运行的任务
#     time.sleep(1)

