# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:17:06 2018

@author: selva
"""
import numpy as np
import cv2

#2点間の距離を求める
def get_Distance(img,p1,p2):
    p1_x = p1.shape[1]
    p2_x = p2.shape[1]
    
    #二つの特徴量の多い方に合わせる
    if p1_x < p2_x:
        flag = 0
    else:
        flag = 1
    p2 = np.reshape(p2,(p2_x, 1, -1))
    
    # Make matrix by copying elements
    m1 = np.tile(p1, (p2_x, 1, 1))
    m2 = np.tile(p2, (1,p1_x, 1))
    
    # Make vectors from p2 to p1
    mv = m1 - m2
    
    # Calculate square distances
    ms = np.sum(np.square(mv), axis=2)
    
    # Calculate distances
    md = np.sqrt(ms)
    
    #print("p1.shape =", p1_x)
    #print("p2.shape =", p2_x)
    #print("ms =", ms)
    #print("md =", md)
    
    #行で最小の値を求める
    index = np.argmin(md,axis=flag)
    p1_int = np.array(p1,dtype="int64")
    p2_int = np.array(p2,dtype="int64")

    dis_sum = 0
    for i,x in enumerate(index):
        if flag == 0:
            #print("p1{},p2{},distance:{}".format(p1[0,i],p2[x,0],md[x,i]))
            #cv2.line(img,(p1_int[0,i,0],p1_int[0,i,1]),(p2_int[x,0,0],p2_int[x,0,1]),(255,0,255),thickness = 2)
            dis_sum += md[x,i]
        else :
            #print("p1{},p2{},distance:{}".format(p1[0,x],p2[i,0],md[i,x]))
            cv2.line(img,(p1_int[0,x,0],p1_int[0,x,1]),(p2_int[i,0,0],p2_int[i,0,1]),(255,0,255),thickness = 2)
            #print((p1_int[0,x]))
            dis_sum += md[i,x]
    print(dis_sum)
    return img,dis_sum
if __name__=="__main__":
    p1 = np.array([[[1,0],[1,1],[1,2]]])
    
    p2 = np.array([[[2,1],[2,2],[2,0]]])

    get_Distance(p1,p2)