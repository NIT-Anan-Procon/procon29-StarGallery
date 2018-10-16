# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 16:21:54 2018

@author: selva
"""

import cv2 
import glob
from natsort import natsorted

#2枚の画像を合成する
def hu(img1,img2,i):
    
    stitcher = cv2.createStitcher(False) 
    foo = cv2.imread(img1) 
    bar = cv2.imread(img2) 
    result = stitcher.stitch((foo,bar)) 
    cv2.imwrite("../scene/res2/{}.jpg".format(i), result[1])
    
#一気に画像を合成す
def main():
    #ファイルの画像を参照
    files = glob.glob("../90/*.jpg")
    
    #空の配列を生成
    images = []
    
    for i in files:
        img = cv2.imread(i)
        """
        gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #二値化
        i1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY_INV)[1]
    """
        print("load",i)
        images.append(img)
    
    
    stitcher = cv2.createStitcher(True)  
    
    #パノラマ画像合成
    result = stitcher.stitch(images)
    
    cv2.imwrite("../result.jpg", result[1])

#二枚づつ画像を合成していき、ひとつのパノラマ画像にする
def Nimai():
    
    #ファイル画像の参照
    files = glob.glob("../scene_90/1/*.jpg")
    
    #ファイル保存名用の引数
    i=1
    
    #画像を二枚ずつ参照していき合成を行う
    for index,path in enumerate(files):        
        if index == int(len(files))-1:
            break
        
        hu(files[index],files[index+1],i)
        i+=1
            
    main()

def resize(path,index):
    # ファイル参照
    f_img=cv2.imread(path,cv2.IMREAD_COLOR)
    
    #画像の大きさ取得
    h,w = f_img.shape[:2]

    M = max(f_img.shape[:2])
    i = 2
    while True:
      if M/i < 1000:
          break
      i+=1
    size = (int(w/i),int(h/i))
    
    #リサイズ
    img = cv2.resize(f_img,size)
    
    cv2.imwrite("../tate_scene2/hsv/{}.jpg".format(index),img)
    #print("write",index)


if __name__=="__main__":
    
    files = natsorted(glob.glob("../tate_scene2/resize/*.jpg"))
    for index,path in enumerate(files):
        print(path)
        resize(path,index)

    #main()