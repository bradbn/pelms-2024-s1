#!/usr/bin/python
""" PELMS-2024-S1 Camera Algorithm System Raspberry Pi GUI.
This is the thin GUI used for the Camera Algorithm Sub-system of the 
Portable Electronic Measurement System (v2024 S1).  The GUI is written 
in python and runs on a Raspberry Pi that interfaces with:
    - the Raspberry Pi camera via the camera interface, and
    - the RF Link via the GPIO pins.

Typical usage example:

    pelms_thin_gui
"""
import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import OptionMenu
from tkinter import StringVar
import numpy as np
import picamera2
import libcamera
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageTk
import cv2

""" Global GPIO configuration
The GPIO module is used to connect with the RF Link hardware.  Pin 7 is 
currently used to send a HIGH or LOW signal to the RF Link to transmit to the 
Current Regulator Sub-system.
"""
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.output(7,GPIO.LOW)


""" Global picamera2 configuration
The picamera2() module is used to connect to the Raspberry Pi camera.
"""
picam2 = picamera2.Picamera2()
picam2_camera_preview_config = picam2.create_preview_configuration(
    transform=libcamera.Transform(hflip=1, vflip=1))
picam2.configure(picam2_camera_preview_config)


"""Global directories configuration
The global directories used by the GUI are primarily used to store intermediate 
image files.

PELMS_DIR       is the directory location of the pelms directory containing
                the bin directory and supporting directories and files.
IMG_DATA_DIR    is the directory used for storing images captured using the 
                Raspberry Pi camera.
"""
PELMS_DIR = '/opt/pelms/'
IMG_DATA_DIR = PELMS_DIR + 'data/images/'
os.makedirs(IMG_DATA_DIR, exist_ok=True)


""" Tkinter classes and function.
The GUI is a Tkinter-based gui - the following section contains the Tkinter 
classes and function used.
"""
class PelmsTkGuiClass(tk.Tk):
    """ PELMS Tkinter GUI Class
    This class contains the Tkinter layout for the PELMS GUI and the
    functions called.  The GUI will be an 800x480 pixel GUI with the following 
    sections:
        frame_header - 800x80 pixel top section
        frame_footer - 800x40 pixel bottom section

    Attributes:
        None
    """
    def __init__(self):
        """Initialise the PELMS Tkinter GUI.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
        """
        super().__init__()
        self.geometry('800x480')
        self.resizable(False, False)
        self.title_string = "Portable Electroluminescence "
        self.title_string += "Measurement System "
        self.title_string += "(PELMS) GUI v2024.s1"
        self.title(self.title_string)
        self.attributes('-fullscreen', True)

        # frame_header is the 800x80 top section of the Tkinter GUI
        # containing the title of the GUI and the version.
        self.frame_header = tk.Frame()
        self.frame_header.configure(
            width=800, height=80,
            highlightbackground="black",
            highlightthickness=1
        )
        self.frame_header.place(x=0,y=0)
        self.config_frame_header()

        # frame_footer is the 800x40 bottom section of the Tkinter GUI.
        self.frame_footer = tk.Frame()
        self.frame_footer.configure(
            width=800, height=40,
            highlightbackground="black",
            highlightthickness=1
        )
        self.frame_footer.place(x=0,y=440)
        self.config_frame_footer()

        # frame_menu is the 240 x 360 side section of the Tkinter GUI which
        # contains the menu options for the GUI.
        self.frame_menu = tk.Frame()
        self.frame_menu.configure(width=240, height=360,
            highlightbackground="black",
            highlightthickness=1
        )
        self.frame_menu.place(x=560, y=80)
        self.config_frame_menu()

        # frame_workspace is the 560 x 360 section of the Tkinter GUI which
        # is where the "work" of the GUI is displayed which maybe thing such
        # as images or setting or text output etc.
        self.frame_workspace = tk.Frame()
        self.frame_workspace.configure(width=560, height=360,
            highlightbackground="black", highlightthickness=1 )
        self.frame_workspace.place(x=0, y=80)
        #self.config_frame_workspace('default')


        """ GLobal tKinter GUI EL Measurement configuration
        The global tKinter GUI EL Measurement parameters are useable in all 
        tKinter frames.

        NUM_IMG_PAIR - the number of image pairs to measure with
        KEEP_PAIR_FILES_FLAG - flag to keep intermediate file images
        CAM_RES - camera resolution of raspberry picamera image
        CAM_EXP_MS - camera exposure time in ms
        
        # Setup Global EL Measurement variables:
        NUM_IMG_PAIR = tk.StringVar(self)
        KEEP_PAIR_FILES_FLAG = tk.StringVar(self)
        CAM_RES = tk.StringVar(self)
        CAM_EXP_MS = tk.StringVar(self)

        # Initialise Global EL Measurement variables:
        NUM_IMG_PAIR.set("5")
        KEEP_PAIR_FILES_FLAG.set("N")
        CAM_RES.set("2028x1520")
        CAM_EXP_MS.set("1000")"""



    def config_frame_header(self):
        """Configure the frame header.
        Configure the frame_header 800x80 top section of the Tkinter GUI
        containing the title_string.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            None
        """
        label_title = tk.Label(self.frame_header)
        label_title.configure(text=self.title_string, 
            font=('Helvetica', 15, 'bold'))
        label_title.place(relx=0.5, rely=0.5, anchor='center')


    def config_frame_footer(self):
        """Configure the frame footer.
        Configure the frame_footer 800x40 bottom section of the Tkinter GUI.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            None
        """
        label_footer = tk.Label(self.frame_footer)
        label_footer.place(relx=0.5, rely=0.5, anchor='center')

    def config_frame_menu(self):
        """ Configure the frame menu.
        Configure the frame_menu 240x360 side section of the Tkinter GUI.  The
        menu contains options - which have buttons and call function to 
        configure the workspace.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            None
        """
        
        """ GLobal tKinter GUI EL Measurement configuration
        The global tKinter GUI EL Measurement parameters are useable in all 
        tKinter frames.

        NUM_IMG_PAIR - the number of image pairs to measure with
        KEEP_PAIR_FILES_FLAG - flag to keep intermediate file images
        CAM_RES - camera resolution of raspberry picamera image
        CAM_EXP_MS - camera exposure time in ms
        """
        
        # Setup Global EL Measurement variables:
        NUM_IMG_PAIR = tk.StringVar(self)
        KEEP_PAIR_FILES_FLAG = tk.StringVar(self)
        CAM_RES = tk.StringVar(self)
        CAM_EXP_MS = tk.StringVar(self)

        # Initialise Global EL Measurement variables:
        NUM_IMG_PAIR.set("5")
        KEEP_PAIR_FILES_FLAG.set("N")
        CAM_RES.set("2028x1520")
        CAM_EXP_MS.set("1000")


        # Menu Option:      Camera Resolution
        # Label:            label_cam_res 
        # Workspace Config: N/A
        label_cam_res = tk.Label(self.frame_menu)
        label_cam_res.configure(text="Cam Res:")
        label_cam_res.place(relx=0.02, rely=0.1, anchor="w")
        opt_menu_cam_res = tk.OptionMenu(self.frame_menu, 
            CAM_RES, "2028x1520", "4056x3040")
        opt_menu_cam_res.place(relx = 0.5, rely=0.1, anchor="w")


        # Menu Option:      Camera Exposure
        # Label:            label_cam_exp 
        # Workspace Config: N/A
        label_cam_exp = tk.Label(self.frame_menu)
        label_cam_exp.configure(text="Cam Exp (ms):")
        label_cam_exp.place(relx=0.02, rely=0.2, anchor="w")
        opt_menu_cam_exp = tk.OptionMenu(self.frame_menu, 
            CAM_EXP_MS, "100", "500", "1000", "5000")
        opt_menu_cam_exp.place(relx = 0.5, rely=0.2, anchor="w")

        # Menu Option:      Num Image Pair
        # Label:            label_num_img_pair 
        # Workspace Config: N/A
        label_num_img_pair = tk.Label(self.frame_menu)
        label_num_img_pair.configure(text="No. Img Pair:")
        label_num_img_pair.place(relx=0.02, rely=0.3, anchor="w")
        opt_menu_num_img_pair = tk.OptionMenu(self.frame_menu, 
            NUM_IMG_PAIR, "1", "2", "5", "10", "20", "50")
        opt_menu_num_img_pair.place(relx = 0.5, rely=0.3, anchor="w")

        # Menu Option:      Keep Image Pair Flag
        # Label:            label_keep_img_pair 
        # Workspace Config: N/A
        label_keep_img_pair = tk.Label(self.frame_menu)
        label_keep_img_pair.configure(text="Keep Img Pair:")
        label_keep_img_pair.place(relx=0.02, rely=0.4, anchor="w")
        opt_menu_keep_img_pair = tk.OptionMenu(self.frame_menu, 
            KEEP_PAIR_FILES_FLAG, "Y", "N")
        opt_menu_keep_img_pair.place(relx = 0.5, rely=0.4, anchor="w")


        # Menu Option:      Camera Preview
        # Button:           button_camera_viewer 
        # Workspace Config: config_frame_workspace('camera_preview')
        button_camera_preview = tk.Button(self.frame_menu)
        button_camera_preview.configure(text="Camera Preview",
            #command=lambda: self.config_frame_workspace('camera_preview'), 
            height=2, width=20)
        button_camera_preview.place(relx=0.5, rely=0.64, anchor="center")

        # Menu Option:      EL Measure
        # Button:           button_el_measure 
        # Workspace Config: config_frame_workspace('el_measure')
        button_el_measure = tk.Button(self.frame_menu)
        button_el_measure.configure(text="EL Measure",
            #command=lambda: self.config_frame_workspace('el_measure'), 
            height=2, width=20)
        button_el_measure.place(relx=0.5, rely=0.78, anchor="center")

        # Menu Option:      Quit
        # Button:           button_quit 
        # Workspace Config: N/A call cmd_quit
        button_quit = tk.Button(self.frame_menu)
        button_quit.configure(text="Quit", command=self.command_quit,
            height=2, width=20)
        button_quit.place(relx=0.5, rely=0.92, anchor="center")


    """ Quit functions """
    def command_quit(self):
        """ Quit command
        Quits the application by destroying all tKinter windows.

        Args:
            None

        Returns:
            None
        
        Raises:
            None
        """
        self.destroy()



if __name__ == "__main__" :
    pelms_main_window = PelmsTkGuiClass()
    pelms_main_window.mainloop()
    GPIO.cleanup()

