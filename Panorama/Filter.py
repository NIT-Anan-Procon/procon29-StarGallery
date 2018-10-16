# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 00:42:21 2018

@author: selva
とりあえずエッジ強調
先鋭化した
"""

import cv2
import numpy as np

def resize(path):
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
    
    cv2.imwrite("./img/resize.png",img)
    return img


#先鋭化（4近傍）
def edge(image):
    # 入力画像 読み込み
    #image = cv2.imread(path,1)
    
    # カーネル 空間フィルタを適用して輪郭を強調する
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    

    dst2 = cv2.filter2D(image, -1, kernel)
    
    return dst2

#エッジ処理
def canny(image):
    
    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    edge2 = cv2.Canny(gray, 5, 60)

    # 結果を出力
    cv2.imwrite("output2.png", edge2)

#ガウシアンフィルタ　重み付き平均
def Gauss(image):
    # カーネル 空間フィルタ
    kernel = np.array([[1/24, 2/24, 1/24],
                       [2/24, 12/24, 2/24],
                       [1/24, 2/24, 1/24]])
    

    dst2 = cv2.filter2D(image, -1, kernel)

    return dst2
    
def display(dst):
    # 結果を出力
    #cv2.imwrite("output2.jpg", dst)
    cv2.imshow("this",dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__=="__main__":
    path ="./img/5.jpg"
    resize(path)
