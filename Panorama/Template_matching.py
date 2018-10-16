# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 13:57:31 2018

@author: selva
"""

import cv2
import numpy as np

def template():
    #画像をグレースケールで読み込む
    img = cv2.imread("../tate_scene2/resize/1.jpg", 0)
    temp = cv2.imread("../tate_scene2/tmp/0.jpg", 0)
    
    #マッチングテンプレートを実行
    #比較方法はcv2.TM_CCOEFF_NORMEDを選択
    result = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)
    
    #検出結果から検出領域の位置を取得
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    w, h = temp.shape[::-1]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    #検出領域を四角で囲んで保存
    result = cv2.imread("../tate_scene2/resize/1.jpg")
    cv2.rectangle(result,top_left, bottom_right, (255, 0, 0), 2)
    print(max_val)
    cv2.namedWindow("hsv",cv2.WINDOW_AUTOSIZE)
    cv2.imshow("hsv",result)
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def rotate():
    # 画像読み込み
    img = cv2.imread("../scene/res3_tmp/tmp1_0.jpg")
    h, w = img.shape[:2]
    size = (w, h)
    
    # 回転角の指定
    angle = -20
    angle_rad = angle/180.0*np.pi
    
    # 回転後の画像サイズを計算
    w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
    h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
    size_rot = (w_rot, h_rot)
    
    # 元画像の中心を軸に回転する
    center = (w/2, h/2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    
    # 平行移動を加える (rotation + translation)
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] -w/2 + w_rot/2
    affine_matrix[1][2] = affine_matrix[1][2] -h/2 + h_rot/2
    
    img_rot = cv2.warpAffine(img, affine_matrix, size_rot, flags=cv2.INTER_CUBIC)
    
    cv2.imshow("img_rot", img_rot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=="__main__":
    template()