#!/bin/python
#########
# Clear #
#########
import sys
import os
from epdlib import epd2in13bc
import time
from PIL import Image, ImageDraw, ImageFont
import socket
epd = epd2in13bc.EPD()
time.sleep(1)
epd.init()
time.sleep(1)
epd.Clear()
time.sleep(1)
epd.sleep()
