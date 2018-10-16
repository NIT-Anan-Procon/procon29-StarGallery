# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 21:39:59 2018

@author: selva

マスク作成

"""
import cv2
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

#撮った写真のマスク画像を作成
def mask(grabcut):
 
    # 画像をグレースケール化
    img2_gray = cv2.cvtColor(grabcut, cv2.COLOR_BGR2GRAY)
 
    # マスク画像を生成するために二値化
    img_maskg = cv2.threshold(img2_gray, 0, 255, cv2.THRESH_BINARY_INV)[1]
 
    # マスク画像を生成する
    img_mask = cv2.merge((img_maskg, img_maskg, img_maskg))
 
    # マスク画像の白黒を反転
    img_maskn = cv2.bitwise_not(img_mask)
    
    # numpy.array -> PILに   
    pilImg = Image.fromarray(np.uint8(img_maskn))
    img = gau_mask(pilImg)
    return img

#マスク画像にガウシアンフィルタをかけ加工
def gau_mask(pilImg):
    
    #オリジナル画像の幅と高さを習得
    width,height = pilImg.size

    #四角のマスク画像作成    
    img2 = Image.new("L", (width, height), 0)
    
    #四角を書き込む
    draw = ImageDraw.Draw(img2)
    draw.rectangle((20, 20, width-20, height-20), 255)
    img2.paste(pilImg, (0, 0), img2)
    img1 = img2.filter(ImageFilter.GaussianBlur(10))

    return img1

