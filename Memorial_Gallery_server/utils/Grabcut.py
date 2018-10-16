# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 16:23:38 2018

@author: selva
前景抽出
"""

import numpy as np
import cv2

import Filter

def grabCut(file):
    img = Filter.resize(file)
    #thickness = 3           # brush thickness

    height, width = img.shape[:2] 
    
    img2 = img.copy()                       # a copy of original image
    img = Filter.edge(img2)
    
    mask = np.zeros(img.shape[:2], dtype=np.uint8) # mask initialized to PR_BG
    output = np.zeros(img.shape, np.uint8)           # output image to be shown
       
    # grabcut range
    rect = (50, 1, width-50, height)
    
    # input write rectangle

    bgdmodel = np.zeros((1, 65), np.float64)  # 前景モデル GMG
    fgdmodel = np.zeros((1, 65), np.float64)  # 背景モデル GMG
    cv2.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 5, cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask==1) + (mask==3), 255, 0).astype('uint8')
    output = cv2.bitwise_and(img2, img2, mask=mask2)
    return output

