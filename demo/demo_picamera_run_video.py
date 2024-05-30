#!/usr/bin/python
import tkinter as tk
import picamera
import time
import numpy as np

from PIL import Image
from PIL import ImageTk


class PELMS_Run_Video_Tk_Class(tk.Tk):
    
    global picamera_iso
    global picamera_resolution
    global picamera_shutter_speed 
    global picamera_exposure_speed
    global picamera_framerate
    
    global rgb_disp_image
    

    def __init__(self):
        super().__init__()
        self.geometry('800x480')
        self.resizable(False, False)
        self.title("Portable Electroluminescence Measurement System (pelms) v2023.s2")
        cdself.attributes('-fullscreen', True)
        self.createWidgets()

    def createWidgets(self):

        self.tk_Button_run_video = tk.Button(self, text="Run Video", command=self.command_run_video)
        self.tk_Button_run_video.grid(column=2, row=5)

        self.tk_Button_quit = tk.Button(self, text="Quit", command=self.command_quit)
        self.tk_Button_quit.grid(column=2, row=7)

        #self.rgb_disp_image = np.zeros((512,304,3), dtype=np.uint8)
        #rgb_disp_PhotoImage =  ImageTk.PhotoImage(image=Image.fromarray(self.rgb_disp_image))
        #self.tk_Label_rgb_disp_image = tk.Label(self, rgb_disp_PhotoImage)
        #self.tk_Label_rgb_disp_image.pack()


    def command_run_video(self):
        with picamera.PiCamera() as rpicamera:
            rpicamera.resolution = (500, 300)
            rpicamera.start_preview(fullscreen=False, window=(6, 133, 500,300))
            time.sleep(10)
            rpicamera.stop_preview()
            rpicamera.capture(rgb_disp_image, format='rgb')


    def command_quit(self):
        self.destroy()

            

if __name__ == "__main__":
    pelms_main_window = PELMS_Run_Video_Tk_Class()
    pelms_main_window.mainloop()
