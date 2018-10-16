#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 22:19:09 2018

@author: kojimanaoki
"""

import cv2
import numpy as np
import glob

def transform(img, synimg):
    
    height , width = img.shape[:2]
    synhei , synwid = synimg.shape[:2]
    
    print("img    y "+str(height))
    print("img    x "+str(width))
    print("synimg y "+str(synhei))
    print("synimg x "+str(synwid))
    
    
    ratio_img = width / height
    ratio = 5/3
    
    
    #黒との境界
    block = [0,0,0]
    
    yborder = 0 
    h = int(synhei / 2) 
    for y in range(0,h):
        #print(synimg[y, synwid-1])
        if not np.allclose(synimg[y,synwid-1],block):
            yborder = y-1
            #print("border y "+str(yborder))
            #print(synimg[yborder, synwid-1])
            break
    
    xborder = 0
    for x in range(0,synwid,1):
        #print(synimg[yborder, synwid-x-1])
        if not np.allclose(synimg[yborder,synwid-x-1],block):
            xborder = x
            #print("border x "+str(xborder))
            #print(synimg[yborder,xborder])
            break

    #座標
    bepoint1 = [0,0] #左上
    bepoint2 = [0,synhei] #左下
    bepoint3 = [synwid-width,yborder+height] #右下
    bepoint4 = [synwid-width,yborder] #右上
    afpoint1 = [0,0]
    afpoint2 = [0,height]
    afpoint3 = [synwid-width,height] #xに割合
    afpoint4 = [synwid-width,0] #xに割合
    #afpoint1 = [0,yborder]
    #afpoint2 = [0,yborder+height]
    #afpoint3 = [synwid-width,yborder+height]
    #afpoint4 = [synwid-width,yborder]
    
    #トリミング
    pts_mask1 = np.array(((0,0),(synwid-width,yborder),(synwid,yborder)))
    pts_mask2 = np.array(((0,synhei),(synwid-width,yborder+height),(synwid,yborder+height)))
    synimg = trimming(synimg,pts_mask1,pts_mask2)
    
    #ホモグラフィティ変換行列
    dst = []    
    pts1 = np.float32([bepoint3,bepoint4,bepoint1,bepoint2])
    pts2 = np.float32([afpoint3,afpoint4,afpoint1,afpoint2])
    #pts3 = np.float32([[],[],afpoint4,afpoint3])
    #pts4 = np.float32()
    #cv2.imwrite("../synimg.png",synimg)
    
    """
    synimg1 = synimg.copy()
    cv2.line(synimg,(0,0),(synwid-width,yborder+height),(0,255,0),1)
    cv2.line(synimg,(0,synhei),(synwid-width,yborder),(255,0,0),1)
    cv2.imwrite("../result/trans_sample2_before.png",synimg)
    
    cv2.line(synimg1,(0,yborder),(synwid-width,yborder+height),(0,255,0),1)
    cv2.line(synimg1,(0,yborder+height),(synwid-width,yborder),(255,0,0),1)
    cv2.imwrite("../result/trans_sample2_after.png",synimg1)
    """
    #変換実行
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(synimg,M,(synwid+width+width+100+100+100,synhei+height))
    
    
    height1 , width1 = dst.shape[:2]
    #pts3 = np.float32([[],[],afpoint4,afpoint3])
    #pts4 = np.float32()

    print(height1)
    print(width1)
    #dst = dst[0:0,synwid:yborder+height]
    
    #cv2.line(dst,(0,0),(width,height),(0,255,0),1)
    #cv2.line(dst,(0,height),(width,0),(255,0,0),1)

    
    cv2.imwrite("../result/trans_sample2.png",dst)  
    """
    for y in range(0,h):
        print(dst[synhei-y, synwid-1])
        if not np.allclose(dst[synhei-y,synwid-1],block):
            yborder = y-1
            print("border y "+str(yborder))
            print(dst[synhei-yborder, synwid-1])
            break
    """

def trimming(img,pts1,pts2):
    
    mask = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)
    cv2.fillPoly(thresh,[pts1],(0,0,0))
    cv2.fillPoly(thresh,[pts2],(0,0,0))
    cv2.imwrite("../result/trans_sample2_triangle.png",thresh)
    trim_img = cv2.bitwise_and(img,img,mask=thresh)
    #cv2.imwrite("../result/trans_sample2_triangle.png",trim_img)

    return trim_img


if __name__=="__main__":

    path = "../folder/IMG_1027.JPG"
    synpath = "../result/res2728.jpg"
    
    img = cv2.imread(path)
    synimg = cv2.imread(synpath)

    transform(img, synimg)   