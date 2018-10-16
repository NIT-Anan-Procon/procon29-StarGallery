# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 14:37:32 2018

@author: selva
合成
"""

from PIL import Image
import cv2
import datetime

def synthesis(grabcut, scene, mask):
    #背景画像
    im1 = Image.open(scene)
    #貼り付ける画像
    img_cv = cv2.cvtColor(grabcut, cv2.COLOR_BGR2RGB)
    im2 = Image.fromarray(img_cv)
    
    mask = mask.convert("L")
    
    im1.paste(im2, (0, 300), mask)
    now = datetime.datetime.now()
    path = "{0:%Y}_{0:%m%d}_{0:%H%M}.png".format(now)
    im1.save("./composed_images/" + path, quality=95)
    return path
