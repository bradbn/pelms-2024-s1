#!/usr/bin/python
import tkinter as tk
import picamera
import time
import numpy as np
import cv2 as cv

from PIL import Image
from PIL import ImageTk

camera = picamera.PiCamera()
camera.resolution = (100,100)
camera.framerate = 24



#camera.start_preview()
time.sleep(5)
camera.capture('image.jpg')
#camera.stop_preview()

img = cv.imread('image.jpg')
cv.imshow('image', img)
cv.imshow('image2', img)

print(img.ndim)
print(img.shape)
print(img.dtype)

cv.waitKey()

