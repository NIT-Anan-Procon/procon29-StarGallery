# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:26:10 2018

@author: selva
"""
import cv2
import numpy as np
import glob
import time

from natsort import natsorted

import Get_Euclidean_Distance as Euclidean

def denoising(index,path):
    # 読み込み
    img = cv2.imread(path)
    # hsv変換
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV_FULL)
    
    # hsv閾値
    lower = np.array([0,0,100])
    upper = np.array([255,100,255])
    
    """
    # hsv分離
    channels = cv2.split(hsv_img)
    # channel連結
    img_channels_hsv = cv2.hconcat([channels[i] for i in range(3)])
    """    
    
    # hsv範囲指定
    hsv_white = cv2.inRange(hsv_img,lower,upper)
    #dst = search_White(hsv_white)
    # Mask
    res_white = cv2.bitwise_and(img,img, mask= hsv_white)
    #"""
    #白を探す
    dst = search_White(res_white)
    #特徴量の中心点を求める
    tmp = get_CenterPoint(dst)
    #重なっている場所の点を抽出
    pt = get_overlaypoint(img,tmp,index,res_white)
    """
    #出力
    for i in range(len(pt[0])):
        print("#{} X:{} Y:{}".format(i,pt[1,i],pt[0,i]))
        
        cv2.rectangle(res_white, (int(pt[1,i]-5),int(pt[0,i]-5)), (int(pt[1,i]+5),int(pt[0,i]+5)), (255, 255, 0),thickness = 1)
    """
    #配列の形を変える [[x1,x2],[y1,y2]] → [[x1,y1],[x2,y2]]
    #dst_point = np.dstack([pt[1,:],pt[0,:]])
    """
    # Window表示
    cv2.namedWindow("hsv",cv2.WINDOW_AUTOSIZE)
    
    cv2.imshow("hsv",res_white)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    #cv2.imwrite("../tate_scene2/{}.jpg".format(index),hsv_white)
    return res_white,pt

def search_White(src):
    # Detect White
    white = 200
    dst = np.array(np.where(src >= white),dtype='float64')
    return dst

#中心点を求める
def get_CenterPoint(src):
    #同じ配列の大きさの零行列を生成
    tmp = np.zeros_like(src[[0,1],:])
    
    #配列の番号
    index = 0
    #足した数
    count = 1
    
    tmp_x = 0
    tmp_y = 0
    
    for i in range(len(src[0])):
        tmp_x += src[1,i]
        tmp_y += src[0,i]
        
        if i+1 == len(src[0]):
            tmp[1,index] = tmp_x/count
            tmp[0,index] = tmp_y/count
            break
        
        #隣の要素の差を調べる
        elif abs(src[1,i]-src[1,i+1]) <= 10.0 and abs(src[0,i]-src[0,i+1]) <= 10.0:
            count += 1

        else:
            #平均を求める
            tmp[1,index] = tmp_x/count
            tmp[0,index] = tmp_y/count
            tmp_x = 0
            tmp_y = 0
            index += 1
            count = 1
    #0の要素の列を削除
    tmp = np.delete(tmp,np.where(tmp==0)[1],axis=1)
    return tmp

#抽出点の選別,四角を描画
def get_overlaypoint(img,tmp,index,res_white):
    h,w = img.shape[:2]
    
    #画像の重なっている範囲
    overlap = 2.5

    h_over = h/overlap
    w_over= w/overlap
    #一枚目 右側から1/3程度の範囲
    if index == 1:
        print("座標指定範囲:{}\nW:{}~{}\nH:0~{}".format(1,2*w_over,w,h))
        #座標選別
        tmp = np.delete(tmp,np.where(tmp[1] < 2*w_over),axis=1)
        cv2.line(res_white,(int(w-w_over),0),(int(w-w_over),h),(0,0,255),thickness = 1)
    
    #二枚目　左側から1/3程度の範囲
    elif index == 2:
        print("座標指定範囲:{}\nW:0~{}\nH:{}".format(index,w_over,h))
        tmp = np.delete(tmp,np.where(tmp[1]>w_over),axis=1)
        cv2.line(res_white,(int(w_over),0),(int(w_over),h),(0,0,255),thickness = 1)

    #1枚目　上の1/3重なる範囲の抽出
    elif index == 3:
        print("座標指定範囲:{}\nW:0~{}\nH:0~{}".format(index,w,h_over))
        tmp = np.delete(tmp,np.where(tmp[0]>h_over),axis=1)
        cv2.line(res_white,(0,int(h_over)),(w,int(h_over)),(0,0,255),thickness = 2)

    #二枚目　下の1/3重なる範囲
    elif index == 4:
        print("座標指定範囲:{}\nW:0~{}\nH:{}~{}".format(index,w,h-h_over,h))
        tmp = np.delete(tmp,np.where(tmp[0]<h-h_over),axis=1)
        cv2.line(res_white,(0,int(h-h_over)),(w,int(h-h_over)),(0,0,255),thickness = 2)
        tmp = np.array([tmp[0,:]-(h-h_over),tmp[1,:]],dtype = "float64")
        
    return tmp
        
    
def display(img1,img2):
    
    cv2.namedWindow("1",cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("1",cv2.WINDOW_AUTOSIZE)
    cv2.imshow("1",img1)
    cv2.imshow("2",img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    """
    files = natsorted(glob.glob("../tate_scene2/*.jpg"))

    for index,path in enumerate(files):
        print(path)
        denoising(index,path)
    """ 
    img = cv2.imread("../tate_scene2/resize/0.jpg")
    h,w = img.shape[:2]
    front,pt = denoising(3,"../tate_scene2/resize/0.jpg")
    #print(time.time()-start)
    back,pt2 = denoising(4,"../tate_scene2/resize/1.jpg")
    
    for i in range(len(pt2[0])):
        print("#{} X:{} Y:{}".format(i,pt2[1,i],pt2[0,i]))
        cv2.rectangle(front, (int(pt2[1,i]-5),int(pt2[0,i]-5+70)), (int(pt2[1,i]+5),int(pt2[0,i]+5+70)), (255, 255, 0),thickness = 1)
    
    for i in range(len(pt[0])):
        print("#{} X:{} Y:{}".format(i,pt[1,i],pt[0,i]))
        cv2.rectangle(front, (int(pt[1,i]-5),int(pt[0,i]-5)), (int(pt[1,i]+5),int(pt[0,i]+5)), (0, 255, 255),thickness = 1)
    
    dst = np.dstack([pt[1,:],pt[0,:]])
    dst2 = np.dstack([pt2[1,:],pt2[0,:]+70])
    img,dis = Euclidean.get_Distance(front,dst,dst2)
    
    print(dis)
    """        
    dis_min = 100000
    min_x=0
    min_y=0
    
    for y in range(int(h/2.5)):
        for x in range(int(w/2.5)):
            dst2 = np.dstack([pt2[1,:]-x,pt2[0,:]-y])
            dis = Euclidean.get_Distance(dst,dst2)
            #print(x,y,dis)
            if dis_min >= dis:
                dis_min = dis

                print("距離：{},\nずらした座標,w:{},h:{}".format(dis,x,y))
    
    """
    # Window表示
    cv2.namedWindow("res",cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
    cv2.imshow("res",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    