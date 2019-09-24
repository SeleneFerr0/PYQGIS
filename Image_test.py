# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:40:12 2019

@author: SeleneFerro
"""

import random
from urllib.request import urlretrieve
import os

#download 300 images for tests
url = 'http://www.moguproxy.com/proxy/validateCode/createCode?time={}'
path = 'C:\\Users\\base7005\\Pictures\\test\\'

for i in range(1531878604000,1531878604300):
    urlretrieve(url.format(i), path + str(i)[-3:] + '.jpg')
    print('downloaded {} images'.format(str(i)[-3:]))
    
    
from PIL import Image
import os


origin_path = path
new_path = 'C:\\Users\\base7005\\Pictures\\clean_test\\'

#从100张图片中提取出字符样本
for image in os.listdir(origin_path)[:100]: 
    im = Image.open(origin_path+image)    
    width, height = im.size
    
    #获取图片中的颜色，返回列表[(counts, color)...]
    color_info = im.getcolors(width*height)
    #按照计数从大到小排列颜色，那么颜色计数最多的应该是背景，接下来排名2到6的则对应5个字符。
    sort_color = sorted(color_info, key=lambda x: x[0], reverse=True)    

    #根据颜色，提取出每一个字符，重新放置到一个新建的白色背景image对象上。每个image只放一个字符。
    char_dict = {}
    for i in range(1, 6):
        im2 = Image.new('RGB', im.size, (255, 255, 255))
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                if im.getpixel((x, y)) == sort_color[i][1]:
                    im2.putpixel((x, y), (0, 0, 0))  
                else:
                    im2.putpixel((x, y), (255, 255, 255))
        im2.save(new_path + str(i)+'-'+ image.replace('jpg','tif'))  
    print('finished{}'.format(image))
    
    

for image in os.listdir(new_path): 
    im2 = Image.open(new_path+image)
    char = pytesseract.image_to_string(im2, config='--psm 10')  # psm 10表示将图片识别成单个字符。
    print(char)
    
    

    