from picamera2 import Picamera2
import numpy as np
import cv2

# start picamera2
picam2 = Picamera2()
config = picam2.create_still_configuration(raw={'format': 'SBGGR12'})
picam2.configure(config)
picam2.start()

# grab a RAW frame
raw = picam2.capture_array("raw").view(np.uint16)
# convert to 16 bit
raw = raw * 16
# resize image for showing
result2 = cv2.resize(raw, dsize=(800,600), interpolation=cv2.INTER_CUBIC)
cv2.imshow('Output',result2)
# debayer 
colour = cv2.cvtColor(raw, cv2.COLOR_BAYER_BG2RGB)
# resize image for showing
resultc = cv2.resize(colour, dsize=(800,600), interpolation=cv2.INTER_CUBIC)
cv2.imshow('Colour',resultc)
# save both images as TIF
cv2.imwrite("R.tif",raw)
cv2.imwrite("C.tif",colour)
cv2.waitKey()