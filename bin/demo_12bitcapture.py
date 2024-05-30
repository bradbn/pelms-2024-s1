#!/usr/bin/python
from picamera2 import Picamera2
import numpy as np
import cv2

picam2 = Picamera2()
config = picam2.create_still_configuration(raw={'format': 'SBGGR12'})
picam2.configure(config)
picam2.start()

raw = picam2.capture_array("raw").view(np.uint16)

raw = raw * 16

