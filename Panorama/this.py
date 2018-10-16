# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 09:58:59 2018

@author: selva
"""

import cv2
import numpy as np
import glob

import panorama

if __name__=="__main__":
    image_names = glob.glob("../a/*.jpg")

    images = []
    panorama1 = []
    for i in range(1,len(image_names)):
        print( "Loading " + str(image_names[i]))
        img = panorama.resize_image(cv2.imread(image_names[i],cv2.IMREAD_COLOR))
        images.append(panorama.Image(str(i), img))

    panorama1.append(panorama.Image(images[0].name, images[0].image))

    print("Your images have been loaded. Generating panorama starts ...")
    for i in range(0,len(images)-1):
        panorama1.append(panorama.Image(str(i+1),panorama.make_panorama(panorama1[i],images[i+1])))

    print("A panorama image is generated.")
    print(type(panorama1[-1].image))
    cv2.imwrite("panorama.png",panorama1[-1].image)