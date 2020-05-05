#!/bin/python
############################
# The main displaying file #
############################
import sys
import os
import re
from epdlib import epd2in13bc
import time
from PIL import Image, ImageDraw, ImageFont
import socket
import unicodedata

def write(inpt):
    
    # fonts
    epd = epd2in13bc.EPD()
    epd.init()
    font20 = ImageFont.truetype('./cour.ttf', 20)  # 20*17
    font20C = ImageFont.truetype('./simsun.ttc', 20)  # 20*30
    font18 = ImageFont.truetype('./cour.ttf', 18)
    font10 = ImageFont.truetype('./cour.ttf', 12)
    sfont10 = ImageFont.truetype('./simsun.ttc', 12)
    # initiation
    
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)
    HRYimage = Image.new('1', (epd.height, epd.width), 255)
    HBlackimage.paste(Image.open('./pb.bmp'), (98, 22))
    HRYimage.paste(Image.open('./py.bmp'), (98, 22))

    # Words Display
    if inpt == '':
        drawblack = ImageDraw.Draw(HBlackimage)
        drawry = ImageDraw.Draw(HRYimage)
        drawry.rectangle((0, 22, 97, 71), fill=0)
    else:
        v1 = ''
        v2 = ''
        v3 = ''
        lv1 = 0
        lv2 = 0
        lv3 = 0
        for pt in inpt:
            if lv1+1+(unicodedata.east_asian_width(pt) in ('F', 'W', 'A')) <= 14:
                v1 += pt
                lv1 += 1+(unicodedata.east_asian_width(pt) in ('F', 'W', 'A'))
            elif lv2+1+(unicodedata.east_asian_width(pt) in ('F', 'W', 'A')) <= 14:
                lv1 += 14
                v2 += pt
                lv2 += 1+(unicodedata.east_asian_width(pt) in ('F', 'W', 'A'))
            elif lv3+1+(unicodedata.east_asian_width(pt) in ('F', 'W', 'A')) <= 14:
                lv2 += 14
                v3 += pt
                lv3 += 1+(unicodedata.east_asian_width(pt) in ('F', 'W', 'A'))
        if len(v2) == 0:
            HRYimage.paste(Image.open('./rm.bmp'), (81, 22))
            HRYimage.paste(Image.open('./lm.bmp'), (69-6*lv1+12, 22))
            drawblack = ImageDraw.Draw(HBlackimage)
            drawry = ImageDraw.Draw(HRYimage)
            # fill empty
            drawry.rectangle((0, 22, 68-6*lv1+12, 71), fill=0)
            # upper and down
            drawry.rectangle((69+12-6*lv1+12, 22, 80, 41), fill=0)
            drawry.rectangle((69+12-6*lv1+12, 69, 80, 70), fill=0)
            drawblack.text((74-6*lv1+12, 46), v1, font=sfont10, fill=0)
        else:
            HRYimage.paste(Image.open('./re.bmp'), (81, 22))
            HRYimage.paste(Image.open('./le.bmp'), (0, 22))
            drawblack = ImageDraw.Draw(HBlackimage)
            drawry = ImageDraw.Draw(HRYimage)
            drawry.rectangle((0, 22, 68-6*12, 71), fill=0)
            drawry.rectangle((69+12-6*12, 22, 80, 22), fill=0)
            drawry.rectangle((69+12-6*12, 69, 80, 70), fill=0)
            drawblack.text((4, 28), v1, font=sfont10, fill=0)
            drawblack.text((4, 40), v2, font=sfont10, fill=0)
            drawblack.text((4, 53), v3, font=sfont10, fill=0)

    # hostname and IP address
    hostname = socket.gethostname()
    IPAddr = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(
        ("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

    # title
    drawblack.text((15, 0), time.strftime(
        "%b.%d %a", time.localtime()), font=font18, fill=0)
    # # statics
    tmp = os.popen('vnstat -q --oneline').readlines()
    down = '0 KB'
    up = '0 KB'
    for i in tmp:
        z = i.split(';')
        down = z[3]
        up = z[4]

    drawblack.line((epd.height*0.8-3, 0, epd.height*0.8-3, 21), fill=0)
    drawblack.line((epd.height*0.67, 0, epd.height*0.67, 21), fill=0)
    drawblack.text((epd.height*0.8, 0), 'D'+down.split(' ')
                   [0][0:4]+down.split(' ')[1][0], font=font10, fill=0)
    drawry.rectangle((epd.height*0.8-2, 10, epd.height*0.8-2+6, 20), fill=0)
    drawry.text((epd.height*0.8, 10), 'U'+up.split(' ')
                [0][0:4]+up.split(' ')[1][0], font=font10, fill=255)
    drawblack.text((epd.height*0.8, 10), 'U'+up.split(' ')
                   [0][0:4]+up.split(' ')[1][0], font=font10, fill=0)
    drawblack.line((0, 21, epd.height, 21), fill=0)

    #

    tmp = os.popen('df -h').readlines()
    lvs = re.findall(r"\d+\.?\d*", tmp[1])
    pv = str(int(float(lvs[1])/float(lvs[0])*100))
    ps = float(lvs[1])/float(lvs[0])*360
    i = 0
    drawblack.rectangle((epd.height*0.8-3, 0, epd.height*0.67, 21), fill=0)
    while i < 9:
        drawry.arc((145+i, 1+i, 164-i, 20-i), ps, 360, fill=0)
        drawblack.arc((145+i, 1+i, 164-i, 20-i), 0, ps, fill=255)
        i = i+1
    drawblack.text((147, 4), pv, font=font10, fill=0)
    drawry.text((147, 4), pv, font=font10, fill=255)

    # down
    # ! to fix misoutput caused by heat
    # drawry.rectangle((0, 73, epd.height*0.7, epd.width), fill=0)
    drawblack.text((0, 72), hostname, font=font18, fill=0)
    drawry.text((0, 72), hostname, font=font18, fill=255)
    drawblack.text((0, 87), '@'+IPAddr, font=font18, fill=0)
    drawry.text((0, 87), '@'+IPAddr, font=font18, fill=255)
    drawblack.text((epd.height*0.7+3, 72), '  LAST', font=font10, fill=0)
    drawblack.text((epd.height*0.7+3, 80), ' UPDATE', font=font10, fill=0)
    drawblack.text((epd.height*0.7+3, 87), time.strftime(
        "%H:%M", time.localtime()), font=font18, fill=0)
    drawry.line((epd.height*0.7, 73, epd.height*0.7, epd.width), fill=0)
    drawblack.line((0, 72, epd.height, 72), fill=0)
    HBlackimage = HBlackimage.transpose(Image.ROTATE_180)
    HRYimage = HRYimage.transpose(Image.ROTATE_180)
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)
    epd.sleep()

def power_off():
    
    # fonts
    epd = epd2in13bc.EPD()
    epd.init()
    font20 = ImageFont.truetype('./cour.ttf', 20)  # 20*17
    font20C = ImageFont.truetype('./simsun.ttc', 20)  # 20*30
    font18 = ImageFont.truetype('./cour.ttf', 18)
    font10 = ImageFont.truetype('./cour.ttf', 12)
    sfont10 = ImageFont.truetype('./simsun.ttc', 12)
    # initiation
    
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)
    HRYimage = Image.new('1', (epd.height, epd.width), 255)
    HBlackimage.paste(Image.open('./power_off_bb.bmp'), (0, 22))
    HRYimage.paste(Image.open('./power_off_yy.bmp'), (0, 22))
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)

    # hostname and IP address
    hostname = socket.gethostname()
    IPAddr = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(
        ("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

    # title
    drawblack.text((15, 0), time.strftime(
        "%b.%d %a", time.localtime()), font=font18, fill=0)
    # # statics
    tmp = os.popen('vnstat -q --oneline').readlines()
    down = '0 KB'
    up = '0 KB'
    for i in tmp:
        z = i.split(';')
        down = z[3]
        up = z[4]

    drawblack.line((epd.height*0.8-3, 0, epd.height*0.8-3, 21), fill=0)
    drawblack.line((epd.height*0.67, 0, epd.height*0.67, 21), fill=0)
    drawblack.text((epd.height*0.8, 0), 'D'+down.split(' ')
                   [0][0:4]+down.split(' ')[1][0], font=font10, fill=0)
    drawry.rectangle((epd.height*0.8-2, 10, epd.height*0.8-2+6, 20), fill=0)
    drawry.text((epd.height*0.8, 10), 'U'+up.split(' ')
                [0][0:4]+up.split(' ')[1][0], font=font10, fill=255)
    drawblack.text((epd.height*0.8, 10), 'U'+up.split(' ')
                   [0][0:4]+up.split(' ')[1][0], font=font10, fill=0)
    drawblack.line((0, 21, epd.height, 21), fill=0)

    #

    tmp = os.popen('df -h').readlines()
    lvs = re.findall(r"\d+\.?\d*", tmp[1])
    pv = str(int(float(lvs[1])/float(lvs[0])*100))
    ps = float(lvs[1])/float(lvs[0])*360
    i = 0
    drawblack.rectangle((epd.height*0.8-3, 0, epd.height*0.67, 21), fill=0)
    while i < 9:
        drawry.arc((145+i, 1+i, 164-i, 20-i), ps, 360, fill=0)
        drawblack.arc((145+i, 1+i, 164-i, 20-i), 0, ps, fill=255)
        i = i+1
    drawblack.text((147, 4), pv, font=font10, fill=0)
    drawry.text((147, 4), pv, font=font10, fill=255)

    # down
    # ! to fix misoutput caused by heat
    # drawry.rectangle((0, 73, epd.height*0.7, epd.width), fill=0)
    drawblack.text((0, 72), hostname, font=font18, fill=0)
    drawry.text((0, 72), hostname, font=font18, fill=255)
    drawblack.text((0, 87), '@'+IPAddr, font=font18, fill=0)
    drawry.text((0, 87), '@'+IPAddr, font=font18, fill=255)
    drawblack.text((epd.height*0.7+3, 72), '  LAST', font=font10, fill=0)
    drawblack.text((epd.height*0.7+3, 80), ' UPDATE', font=font10, fill=0)
    drawblack.text((epd.height*0.7+3, 87), time.strftime(
        "%H:%M", time.localtime()), font=font18, fill=0)
    drawry.line((epd.height*0.7, 73, epd.height*0.7, epd.width), fill=0)
    drawblack.line((0, 72, epd.height, 72), fill=0)
    HBlackimage = HBlackimage.transpose(Image.ROTATE_180)
    HRYimage = HRYimage.transpose(Image.ROTATE_180)
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)
    epd.sleep()

if __name__ == "__main__":
    write('')
