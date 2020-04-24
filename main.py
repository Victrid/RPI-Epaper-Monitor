import sys
import os
from epdlib import epd2in13bc
import time
from PIL import Image, ImageDraw, ImageFont

epd = epd2in13bc.EPD()
epd.init()
epd.Clear()
time.sleep(1)

font20 = ImageFont.truetype('./Font.ttc', 20)
font18 = ImageFont.truetype('./Font.ttc', 18)

HBlackimage = Image.new('1', (epd.height, epd.width), 255)
HRYimage = Image.new('1', (epd.height, epd.width), 255)
drawblack = ImageDraw.Draw(HBlackimage)
drawry = ImageDraw.Draw(HRYimage)

drawblack.text((10, 0), '123456789012345678901234567890', font=font20, fill=0)
drawblack.text((10, 20), '123456789012345678901234567890', font=font20, fill=0)
drawblack.text((120, 0), u'微雪电子', font=font20, fill=0)
HBlackimage = HBlackimage.transpose(Image.ROTATE_180)
HRYimage = HRYimage.transpose(Image.ROTATE_180)
epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
time.sleep(2)
epd.sleep()
