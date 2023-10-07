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
    def __init__(self, name, head_icon, title, schedule_time, stream_thumbnail, stream_url):
        self.name = name
        self.headIcon = head_icon
        self.title = title
        self.scheduleTime = schedule_time
        self.streamThumbnail = stream_thumbnail
        self.streamUrl = stream_url
    def __str__(self):
        return self.name + " - " + self.headIcon + " - " + self.title + " - " + self.scheduleTime + " - " + self.streamThumbnail + " - " + self.streamUrl


path = os.getcwd()
imgFileName = path + "/schedules.jpg"
_fontType = './silver.ttf'
_liver_list = list()
_live_list_text_size = 0
reqUrl = 'https://dhiljqbdkw8vk.cloudfront.net/schedules'
reqParams = {
    
}
reqHeaders = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Content-Encoding': 'gzip',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

def fun_get():
    response = requests.get(url = reqUrl, params = reqParams, headers = reqHeaders)
    global _liver_list, _live_list_text_size
    if response.status_code == 200:
        _array = json.loads(response.text)
        for _obj in _array: 
            _headIconJson = json.loads(json.dumps(_obj['StreamerThumbnails']))
            _scheduleArray = json.loads(json.dumps(_obj['Schedule']))
            _channelUrl = json.loads(json.dumps(_obj['ChannelUrl']))
            for _schedule in _scheduleArray:
                if 'ScheduledStartTime' in _schedule:
                    _videoId = json.loads(json.dumps(_schedule['VideoId']))
                    _scheduleThumbnails = json.loads(json.dumps(_schedule['ThumbnailDetails']))
                    _schedule['ScheduledStartTime'] = datetime.datetime.strptime(str(_schedule['ScheduledStartTime']),'%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours = 8)
                    schedule_datetime = _schedule['ScheduledStartTime'].strftime('%Y-%m-%d')
                    now_datetime = datetime.datetime.today().strftime('%Y-%m-%d')
                    if schedule_datetime == now_datetime:
                        _liver = Liver(
                            name = str(_obj['StreamerName']).replace('【NIJISANJI EN】',''),
                            head_icon= _headIconJson['Url'],
                            title = _schedule['Title'],
                            schedule_time= str(_schedule['ScheduledStartTime'].strftime('%H:%M')),
                            stream_thumbnail= _scheduleThumbnails['Url'],
                            stream_url="https://youtube.com/watch?v=" + _videoId #_channelUrl + _videoId
                        )
                        # print(_liver.__dict__)
                        _liver_list.append(_liver)

                        _live_list_text_size = _live_list_text_size + 4 + len(_liver.name) + 8 + len(_liver.headIcon) + 5 + len(_liver.title) + 12 + len(_liver.scheduleTime) + 15 + len(_liver.streamThumbnail)

                        _liver_list.sort(key = fun_take_second)

    else:
        print(response.text)
    return _liver_list

def fun_save_to_jpg(margin = 15, backgroundRGB = [255, 255, 255], fontType = _fontType, fontRGB = [0, 0, 0]):

    textList, maxSingleText, allText = fun_decode_text()
    # print(maxSingleText)
    size = tuple([1080, len(_liver_list) * 85])
    backgroundRGB = tuple(backgroundRGB)
    fontRGB = tuple(fontRGB)

    image = Image.new('RGB', size, backgroundRGB) # 设置画布大小及背景色
    iwidth, iheight = image.size # 获取画布高宽

    # 计算字节数，GBK编码下汉字双字，英文单字。都转为双字计算
    size = len(maxSingleText.encode('utf-8'))/3
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

    draw.text((iwidth / 3, margin), str(datetime.datetime.today().strftime('%Y - %m - %d')) + " - 今天直播人数 : " + str(len(_liver_list)), fontRGB, font)
    for tmpText in textList:
        draw.text((fontx, fonty), tmpText, fontRGB, font)
        fonty += fontSize * 2 + margin
        # print(tmpText)
        
    image.save(imgFileName) # 保存图片        

def fun_decode_text():
    text_list = []
    max_single_text = ""
    all_text = ""
    _liver_list.sort(key=fun_take_second)
    for _liver in _liver_list:
        # print(_liver.__dict__)
        tmp_text = _liver.scheduleTime + " " + _liver.name + "\n      " + _liver.title + "\n"
        text_list.append(tmp_text)
        all_text += tmp_text
        if len(max_single_text) < len(tmp_text):
            max_single_text = tmp_text
    return text_list, max_single_text, all_text

def fun_take_second(elem):
    return elem.scheduleTime

def fun_create_html():
    h1 = str(datetime.datetime.today().strftime('%Y - %m - %d')) + " - 今天直播人数 : " + str(len(_liver_list))
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <body align="center">
    <h1>%s</h1>
    """ % h1
    for _liver in _liver_list:
        a_tag = """
        <h2>%s</h2>
        <h3>%s</h3>  <br/>
        <a href="%s"><img src="%s" alt="%s"/> <br/>
        ⬆ CLICK LINK</a>
        <br/>
        """%(_liver.scheduleTime + "   " + _liver.name, _liver.title, _liver.streamUrl, _liver.streamThumbnail, _liver.name)
        html += a_tag
    html += "</body><html>"
    f = open('nijisan_en_daily.html', 'w')
    f.write(html)
    f.close()

def main():
    print(fun_get())
    fun_save_to_jpg()
    fun_create_html()

if __name__ == '__main__':
    main()
#     schedule.every(12).hours.do(main)
#     print("start schedule task ....")
#     while True:
#         schedule.run_pending()  # 运行所有可以运行的任务
#         time.sleep(1)

