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
import subprocess
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
    transform=libcamera.Transform(hflip=1, vflip=1), raw={'format': 'SRGGB12'})
picam2_camera_still_config = picam2.create_still_configuration(
    transform=libcamera.Transform(hflip=1, vflip=1), raw={'format': 'SRGGB12'})



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

        # frame_workspace is the 560 x 360 section of the Tkinter GUI which
        # is where the "work" of the GUI is displayed which maybe thing such
        # as images or setting or text output etc.
        self.frame_workspace = tk.Frame()
        self.frame_workspace.configure(width=560, height=360,
            highlightbackground="black", highlightthickness=1 )
        self.frame_workspace.place(x=0, y=80)
        self.wks_img = ImageTk.PhotoImage(Image.new(mode="RGB", size=(406,304)))
        self.wks_txt = "Blank Image"      
        self.label_array = self.config_frame_workspace(self.wks_img, self.wks_txt)
        self.label_wks_img = self.label_array[0]
        self.label_wks_txt = self.label_array[1]

        # frame_menu is the 240 x 360 side section of the Tkinter GUI which
        # contains the menu options for the GUI.
        self.frame_menu = tk.Frame()
        self.frame_menu.configure(width=240, height=360,
            highlightbackground="black",
            highlightthickness=1
        )
        self.frame_menu.place(x=560, y=80)
        self.config_frame_menu()



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


    def config_frame_workspace(self, wks_img, wks_txt):
        """ Configure the frame workspace.
        Configure the frame_workspace 560x360 side section of the Tkinter GUI 
        which is where the "work" of the GUI is displayed which maybe things 
        such as images or setting or text output etc.

        Args:
            wks_img  - this is the workspace image to be displayed.

            wks_txt - this is the workspace text to be displayed
            
        Returns:
            None
        
        Raises:
            None
        """
        for widget in self.frame_workspace.winfo_children():
            widget.destroy()
       
        label_wks_img = tk.Label(self.frame_workspace)
        label_wks_img.config(image=wks_img)
        label_wks_img.place(relx=0.5, rely=0.45, anchor="center")

        label_wks_txt = tk.Label(self.frame_workspace)
        label_wks_txt.config(text=wks_txt)
        label_wks_txt.place(relx=0.5, rely=0.95, anchor="center")

        return [label_wks_img, label_wks_txt]

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
            CAM_EXP_MS, "10", "20", "40", "60", "80", "100", "500", "1000", "5000")
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
        # Button:           button_camera_preview 
        # Workspace Config: config_frame_workspace('camera_preview')
        button_camera_preview = tk.Button(self.frame_menu)
        button_camera_preview.configure(text="Camera Preview",
            command=lambda: self.camera_preview(), height=2, width=20)
        button_camera_preview.place(relx=0.5, rely=0.64, anchor="center")

        # Menu Option:      EL Measure
        # Button:           button_el_measure 
        # Workspace Config: config_frame_workspace('el_measure')
        button_el_measure = tk.Button(self.frame_menu)
        button_el_measure.configure(text="EL Measure",
            command=lambda: self.el_measure(NUM_IMG_PAIR, KEEP_PAIR_FILES_FLAG, 
                CAM_RES, CAM_EXP_MS), height=2, width=20)
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


    """ Camera Preview function """
    def camera_preview(self):
        """ Camera Preview
        Quits the application by destroying all tKinter windows.

        Args:
            None

        Returns:
            None
        
        Raises:
            None
        """
        self.wks_img = ImageTk.PhotoImage(Image.new(mode="RGB", size=(406,304)))
        self.wks_txt = "Camera Preview Image" + time.asctime()
        self.label_wks_img.config(image=self.wks_img)   
        self.label_wks_txt.config(text=self.wks_txt)

        #picam2.stop()
        #picam2.configure(picam2_camera_preview_config)
        #picam2.start()            
        #time.sleep(1)

        try:
            picam2.stop()
            picam2.configure(picam2_camera_preview_config)
            
            picam2.start()
            img_preview_BAY_12b = picam2.capture_array("raw").view(np.uint16)
            
            img_preview_BAY_16b = img_preview_BAY_12b*(2**4)
            img_preview_RGB_16b = cv2.cvtColor(img_preview_BAY_16b, 
                cv2.COLOR_BAYER_RG2RGB)
            #cv2.imwrite('test.png', img_preview_RGB_16b)
            #img_PIL_full = Image.open('test.png')
            img_PIL_full = Image.fromarray(img_preview_RGB_16b)
            img_PIL_resize = img_PIL_full.resize((406, 304))
            
            self.wks_img = ImageTk.PhotoImage(img_PIL_resize)            
            self.wks_txt = "Preview Camera PASS: " + time.asctime()
            self.label_wks_txt.config(text=self.wks_txt)
            self.label_wks_img.config(image=self.wks_img)

            picam2.stop()

        except:
            self.wks_txt = "Preview Camera FAIL: " + time.asctime()
            self.label_wks_txt.config(text=self.wks_txt)

        '''
        except:
            temp_cmd = "/usr/bin/vcgencmd measure_temp"
            temp_res = subprocess.run([temp_cmd], shell=True, capture_output=True, text=True)
            temp_txt = temp_res.stdout

            self.wks_txt = "Camera Fail" + time.asctime() + temp_txt
            self.label_wks_txt.config(text=self.wks_txt)
        '''

        return


    """ EL Measurement function """
    def el_measure(self, NUM_IMG_PAIR, KEEP_PAIR_FILES_FLAG, CAM_RES, CAM_EXP_MS):
        """ EL Measurement
        Performs teh EL MEasuremnt.

        Args:
            None

        Returns:
            None
        
        Raises:
            None
        """
        self.wks_img = ImageTk.PhotoImage(Image.new(mode="RGB", size=(406,304)))
        self.wks_txt = "EL Measurement" + time.asctime()
        self.label_wks_img.config(image=self.wks_img)   
        self.label_wks_txt.config(text=self.wks_txt)

        # Set the EL MEasurement variables
        num_img_pair = int(NUM_IMG_PAIR.get())
        keep_pair_files_flag = KEEP_PAIR_FILES_FLAG.get()
        cam_res = CAM_RES.get()
        cam_exp_ms = int(CAM_EXP_MS.get())

        print("EL MEasurement: num_img_pair: " + str(num_img_pair))
        print("EL Measurement: keep_pair_files_flag: " + keep_pair_files_flag) 
        print("EL Measurement: cam_res: " + cam_res) 
        print("EL Measurement: cam_exp_ms: " + str(cam_exp_ms)) 

        # Set the camera pixel resolution.
        # Full 4056x3040 resoltion uses the still configuration.
        # Preview 2028x1520 resolution uses the preview configuration.
        picam2.stop()
        if cam_res == "4056x3040":
            picam2.configure(picam2_camera_still_config)
            print("EL Measurement: Cam Res: 4056x3040")
        else:
            picam2.configure(picam2_camera_preview_config)
            print("EL Measurement: Cam Res: 2028x1520")
        picam2.start()

        # Set the camera exposure time.
        try:
            def_exp_ms = picam2.controls.__getattribute__('ExposureTime')
        except:
            def_exp_ms = "NOT SET"
        
        picam2.set_controls({"ExposureTime": cam_exp_ms, "AnalogueGain": 1.0})
        #set_exp_ms = picam2.controls.__getattribute__('ExposureTime')
        #print("EL Measurement: def_exp_ms: " + str(def_exp_ms))
        #print("EL Measurement: set_exp_ms: " + str(set_exp_ms))

        # Capture num_img_pair images.
        # Capture a pair of raw images one dark one light and generate an IR
        # image for each.  If the keep_pair_files_flag is Y then write the 
        # files to disk.
        img_timestamp = time.strftime("%y%m%d-%H%M%S")
        num_img_pair_str = "{:02d}".format(num_img_pair)
        cam_exp_ms_str = "{:05d}".format(cam_exp_ms)

        img_file_prefix = img_timestamp
        img_file_prefix = img_file_prefix + "_" + num_img_pair_str 
        img_file_prefix = img_file_prefix + "_" + cam_exp_ms_str
        print("EL Measurement: img_file_prefix: " + str(img_file_prefix))

        for pair_index in range(num_img_pair):

            pair_index_str = "{:02d}".format(pair_index)
            bri_img_str = pair_index_str + "BRI"
            drk_img_str = pair_index_str + "DRK"
            dif_img_str = pair_index_str + "DIF"
            print("EL Measurement: bri_img_str: " + str(bri_img_str))
            print("EL Measurement: drk_img_str: " + str(drk_img_str))
            print("EL Measurement: dif_img_str: " + str(dif_img_str))

            # Capture the dark image:
            try:
                img_drk_BAY_12b = picam2.capture_array("raw").view(np.uint16)
                self.wks_txt = "EL Measurement: GOOD - " + str(drk_img_str)
                self.label_wks_txt.config(text=self.wks_txt)

            except:
                self.wks_txt = "EL Measurement: FAIL - " + str(drk_img_str)
                self.label_wks_txt.config(text=self.wks_txt)
                continue

            img_drk_BAY_16b = img_drk_BAY_12b * (2**4)
            img_drk_RGB_16b = cv2.cvtColor(img_drk_BAY_16b, 
                cv2.COLOR_BAYER_RG2RGB)
            cv2.imwrite('test.tif', img_drk_RGB_16b)
            img_PIL_full = Image.open('test.tif')
            #img_PIL_full = Image.fromarray(img_drk_RGB_16b)
            img_PIL_resize = img_PIL_full.resize((406, 304))            
            self.wks_img = ImageTk.PhotoImage(img_PIL_resize)            
            self.label_wks_img.config(image=self.wks_img)

            time.sleep(0.5)
            self.label_wks_txt.update()
            self.label_wks_img.update()


            # Capture the bright image:
            GPIO.output(7, GPIO.HIGH)
            time.sleep(0.5)
            try:
                img_bri_BAY_12b = picam2.capture_array("raw").view(np.uint16)
                self.wks_txt = "EL Measurement: GOOD - " + str(bri_img_str)
                self.label_wks_txt.config(text=self.wks_txt)
            except:
                self.wks_txt = "EL Measurement: FAIL - " + str(bri_img_str)
                self.label_wks_txt.config(text=self.wks_txt)
                continue
            GPIO.output(7, GPIO.LOW)

            img_bri_BAY_16b = img_bri_BAY_12b*16
            img_bri_RGB_16b = cv2.cvtColor(img_bri_BAY_16b, 
                cv2.COLOR_BAYER_RG2RGB)
            #cv2.imwrite('test.png', img_bri_RGB_16b)
            #img_PIL_full = Image.open('test.png')
            #img_PIL_resize = img_PIL_full.resize((406, 304))            
            #self.wks_img = ImageTk.PhotoImage(img_PIL_resize)            
            #self.label_wks_img.config(image=self.wks_img)

            time.sleep(0.5)
            self.label_wks_txt.update()

            # Create the difference image:
            img_dif_RGB_16b = img_bri_RGB_16b - img_drk_RGB_16b

            # Write the image to file if keep images is set:
            if keep_pair_files_flag == "Y":

                bri_img_file    = IMG_DATA_DIR + img_file_prefix \
                                + "-" + bri_img_str + "-RGB16.tif"
                drk_img_file    = IMG_DATA_DIR + img_file_prefix \
                                + "-" + drk_img_str + "-RGB16.tif"
                dif_img_file    = IMG_DATA_DIR + img_file_prefix \
                                + "-" + dif_img_str + "-RGB16.tif"
        
                cv2.imwrite(drk_img_file, img_drk_RGB_16b)
                cv2.imwrite(bri_img_file, img_bri_RGB_16b)
                cv2.imwrite(dif_img_file, img_dif_RGB_16b)

            # Sum the 16-bit dif images as 32 float format:
            if pair_index == 0:
                sum_img_dif_RGB_32f = img_dif_RGB_16b.astype(np.float32)
            else:
                sum_img_dif_RGB_32f += img_dif_RGB_16b.astype(np.float32)

        # Find the min and max values of the sum of the dif images:
        min_val = np.min(sum_img_dif_RGB_32f)
        max_val = np.max(sum_img_dif_RGB_32f)
        print("EL Measurement: min_val: " + str(min_val))
        print("EL Measurement: max_val: " + str(max_val))

        # Convert from image to a uint16 full scale image.
        fs_img_dif_RGB_32f = sum_img_dif_RGB_32f - min_val     # set min to 0
        fs_img_dif_RGB_32f = fs_img_dif_RGB_32f / max_val      # scale to 1
        fs_img_dif_RGB_32f = fs_img_dif_RGB_32f * (2**16 - 1)  # scale to 2^16
        fs_img_dif_RGB_16b = fs_img_dif_RGB_32f.astype(np.uint16)

        # Write to file.
        fs_img_dif_RGB_16b_file = "/home/portableel/Desktop/" + img_file_prefix + ".tif"
        cv2.imwrite(fs_img_dif_RGB_16b_file, fs_img_dif_RGB_16b)
        return






if __name__ == "__main__" :
    pelms_main_window = PelmsTkGuiClass()
    pelms_main_window.mainloop()
    GPIO.cleanup()

