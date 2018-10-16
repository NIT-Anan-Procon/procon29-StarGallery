# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 17:48:05 2018

@author: selva
"""
import numpy as np
import cv2
from glob import glob
import matplotlib.pyplot as plt

def main():

    square_size = 28.0      # 正方形のサイズ
    pattern_size = (9,6)  # 模様のサイズ
    pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    obj_points = []
    img_points = []

    for fn in glob("../chess_board/ok/*.jpg"):
        # 画像の取得
        im = cv2.imread(fn, 0)
        print ("loading..." , fn)
        # チェスボードのコーナーを検出
        found, corner = cv2.findChessboardCorners(im, pattern_size)
        # コーナーがあれば
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(im, corner, (5,5), (-1,-1), term)
        # コーナーがない場合のエラー処理
        if not found:
            print ('chessboard not found')
            continue
        img_points.append(corner.reshape(-1, 2))
        obj_points.append(pattern_points)

    # 内部パラメータを計算
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points,img_points,(im.shape[1],im.shape[0]),None,None)
    # 計算結果を表示
    print ("reprojection error:\n ", ret)
    print ("camera matrix:\n", mtx)
    print ("distortion:\n ", dist.ravel())
    print ("rvecs:\n ", rvecs[0].shape)
    print ("tvecs:\n ", tvecs[0].shape)
    
    img = cv2.imread('../chess_board/DSC00651.jpg')
    
    new_cammat = cv2.getOptimalNewCameraMatrix(mtx, dist, (img.shape[1], img.shape[0]), 1)[0]
    map_ = cv2.initUndistortRectifyMap(mtx, dist, np.eye(3), new_cammat, (img.shape[1], img.shape[0]), cv2.CV_32FC1)
    img_und = cv2.remap(img, map_[0], map_[1], cv2.INTER_AREA)
    
    cv2.imshow("this",img_und)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()