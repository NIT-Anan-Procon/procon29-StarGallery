# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 14:50:51 2018

@author: selva
YC分離、
それぞれの色調でノイズ除去


"""

import cv2
import Filter
import numpy as np 

# 画像１
img1 = cv2.imread("17_hsv_mask.jpg")
# 画像２
img2 = cv2.imread("18_hsv_mask.jpg")

# 画像をグレースケール化
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#ノイズ除去
i1 = cv2.fastNlMeansDenoising(gray1,None,1,7,21)
i2 = cv2.fastNlMeansDenoising(gray2,None,1,7,21)

# 二値化
i1 = cv2.threshold(i1, 64, 255, cv2.THRESH_BINARY_INV)[1]
i2 = cv2.threshold(i2, 64, 255, cv2.THRESH_BINARY_INV)[1]
"""
img11 = Filter.edge(i1)
img22 = Filter.edge(i2)
"""
# A-KAZE検出器の生成
akaze = cv2.AKAZE_create()                                

# 特徴量の検出と特徴量ベクトルの計算
kp1, des1 = akaze.detectAndCompute(img1, None)
kp2, des2 = akaze.detectAndCompute(img2, None)

# Brute-Force Matcher生成+
matcher = cv2.BFMatcher()

# 特徴量ベクトル同士をBrute-Force＆KNNでマッチング
matches = matcher.knnMatch(des1, des2, k=2)

# データを間引きする
ratio = 1
good = []
without =[]

for m, n in matches:
    if m.distance < ratio * n.distance:
        good.append([m])
        without.append(m)

# 対応する特徴点同士を描画
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good[:1000], None, flags=2)
"""
#特徴点の座標取得
img1_pt = [list(map(int, kp2[m.queryIdx].pt)) for m in without]
img2_pt = [list(map(int, kp2[m.trainIdx].pt)) for m in without]

pt1 = np.float32(img1_pt).reshape(-1,1,2)
pt2 = np.float32(img2_pt).reshape(-1,1,2)

#ホモグラフィ計算
H,Hstatus = cv2.findHomography(pt1,pt2,cv2.RANSAC,5.0)

w1,h1 = img2.shape[:2]
w2,h2 = img1.shape[:2]

# Get the canvas dimesions
img1_dims = np.float32([ [0,0], [0,w1], [h1, w1], [h1,0] ]).reshape(-1,1,2)
img2_dims_temp = np.float32([ [0,0], [0,w2], [h2, w2], [h2,0] ]).reshape(-1,1,2)


# Get relative perspective of second image
img2_dims = cv2.perspectiveTransform(img2_dims_temp, H)

	# Resulting dimensions
result_dims = np.concatenate( (img1_dims, img2_dims), axis = 0)

	# Getting images together
	# Calculate dimensions of match points
[x_min, y_min] = np.int32(result_dims.min(axis=0).ravel() - 0.5)
[x_max, y_max] = np.int32(result_dims.max(axis=0).ravel() + 0.5)
	
	# Create output array after affine transformation 
transform_dist = [-x_min,-y_min]
transform_array = np.array([[1, 0, transform_dist[0]], 
								[0, 1, transform_dist[1]], 
								[0,0,1]]) 

	# Warp images to get the resulting image
result_img = cv2.warpPerspective(img2, transform_array.dot(H), 
									(x_max-x_min, y_max-y_min))
result_img[transform_dist[1]:w1+transform_dist[1], transform_dist[0]:h1+transform_dist[0]]
"""

# 画像表示
cv2.imshow('img',img3)

#cv2.imwrite("../this.jpg",result_img)
# キー押下で終了
cv2.waitKey(0)
cv2.destroyAllWindows()