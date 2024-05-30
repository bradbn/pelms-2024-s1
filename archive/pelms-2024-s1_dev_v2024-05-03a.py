#!/usr/bin/python
""" PELMS-2024-S1 Camera Algorithm System Raspberry Pi GUI.

This is the GUI used for the Camera Algorithm Sub-system of the 
Portable Electronic Measurement System (v2024 S1).  The GUI is written 
in python and runs on a Raspberry Pi that interfaces with:
    - the Raspberry Pi camera via the camera interface, and
    - and RF Link via the GPIO pins.

Typical usage example:

    pelms_gui
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
picam2_camera_config = picam2.create_preview_configuration()
picam2.configure(picam2_camera_config)


"""Global directories configuration

The global directories used by the GUI are primarily used to store intermediate 
image files.

IMG_VIEWER_DIR  is the directory used for storing images captured using the 
                Raspberry Pi camera in a "preview" mode.

IMG_MEASURE_DIR is the directory used for storing intermediate images used for 
                processing this directory is destoryed and recreated everytime 
                the application is run.
"""
PELMS_DIR = '/opt/pelms/'
IMG_VIEWER_DIR = PELMS_DIR + 'images_viewer/'
IMG_MEASURE_DIR = PELMS_DIR + 'images_measure/'

os.makedirs(IMG_VIEWER_DIR, exist_ok=True)
os.makedirs(IMG_MEASURE_DIR, exist_ok=True)
shutil.rmtree(IMG_MEASURE_DIR)
os.makedirs(IMG_MEASURE_DIR)


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
            highlightbackground="black",
            highlightthickness=1
        )
        self.frame_workspace.place(x=0, y=80)
        self.config_frame_workspace('default')


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
            font=('Helvetica', 15, 'bold')
        )
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
        """Configure the frame menu.

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
        # Menu Option:      Main Page
        # Button:           button_main_page    
        # Workpace Config:  config_frame_workspace('main_page')
        button_main_page = tk.Button(self.frame_menu)
        button_main_page.configure(text="Main Page",
            command=lambda: self.config_frame_workspace('main_page'),
            height=1, width=20, justify="right"
        )
        button_main_page.place(relx=0.5, rely=0.15, anchor="center")

        # Menu Option:      Camera Viewer
        # Button:           button_camera_viewer 
        # Workpace Config:  config_frame_workspace('camera_viewer')
        button_camera_viewer = tk.Button(self.frame_menu)
        button_camera_viewer.configure(text="Camera Viewer",
            command=lambda: self.config_frame_workspace('camera_viewer'), 
            height=1, width=20)
        button_camera_viewer.place(relx=0.5, rely=0.25, anchor="center")

        # Menu Option:      EL Measure
        # Button:           button_el_measure 
        # Workpace Config:  config_frame_workspace('el_measure')
        button_el_measure = tk.Button(self.frame_menu)
        button_el_measure.configure(text="EL Measure",
            command=lambda: self.config_frame_workspace('el_measure'), height=1,
            width=20)
        button_el_measure.place(relx=0.5, rely=0.35, anchor="center")

        # Menu Option:      Settings
        # Button:           button_settings 
        # Workpace Config:  config_frame_workspace('settings')
        button_settings = tk.Button(self.frame_menu)
        button_settings.configure(text="Settings", height=1, width=20,
            command=lambda: self.config_frame_workspace('settings'))
        button_settings.place(relx=0.5, rely=0.6, anchor="center")

        # Menu Option:      File Transfer
        # Button:           button_file_transfer 
        # Workpace Config:  config_frame_workspace('file_transfer')
        button_file_transfer = tk.Button(self.frame_menu)
        button_file_transfer.configure(text="File Transfer", height=1, width=20,
            command=lambda: self.config_frame_workspace('file_transfer'))
        button_file_transfer.place(relx=0.5, rely=0.7, anchor="center")

        # Menu Option:      Quit
        # Button:           button_quit 
        # Workpace Config:  N/A call cmd_quit
        button_quit = tk.Button(self.frame_menu)
        button_quit.configure(text="Quit", command=self.command_quit,
            height=1, width=20)
        button_quit.place(relx=0.5, rely=0.9, anchor="center")


    def config_frame_workspace(self, workspace_type):
        """Configure the frame workspace.

        Configure the frame_workspace 560x360 side section of the Tkinter GUI 
        which is where the "work" of the GUI is displayed which maybe things 
        such as images or setting or text output etc.

        Args:
            workspace_type  - this is the type space and depends on the menu 
                            option selected.  Dependinf on the workspace_type
                            given the appropriate workspace_page_setup function 
                            will be called.

        Returns:
            None
        
        Raises:
            None
        """
        for widget in self.frame_workspace.winfo_children():
            widget.destroy()

        label_workspace = tk.Label(self.frame_workspace)
        label_workspace.place(relx=0.5, rely=0.5, anchor="center")

        label_workspace_title = tk.Label(self.frame_menu)
        label_workspace_title.configure(text="Main Page", 
            font=('Helvetica', 11, 'bold'))
        label_workspace_title.place(relx=0.5, rely=0.05, anchor="center")

        if workspace_type == 'main_page':
            label_workspace_title.config(text="    Main Page    ")
            self.workspace_main_page_setup()
        elif workspace_type == 'camera_viewer':
            label_workspace_title.configure(text="Camera Viewer")
            self.workspace_camera_viewer_page_setup()
        elif workspace_type == 'el_measure':
            label_workspace_title.configure(text="   EL Measure   ")
            self.workspace_el_measure_page_setup()
        elif workspace_type == 'settings':
            label_workspace_title.configure(text="      Settings      ")
            self.workspace_settings_page_setup()
        elif workspace_type == 'file_transfer':
            label_workspace_title.configure(text="  File Transfer  ")
            self.workspace_file_transfer_setup()
        else:
            label_workspace_title.config(text="    Main Page    ")
            self.workspace_main_page_setup()


    """ Main Page functions """
    def workspace_main_page_setup(self):
        file_transfer_button = tk.Button(self.frame_workspace)
        file_transfer_button.configure(text="Main Page", 
            command=self.command_quit, height=1, width=20)
        file_transfer_button.place(relx=0.5, rely=0.9, anchor="center")


    """ Camera Viewer functions """
    def workspace_camera_viewer_page_setup(self):
        """Camera Viewer workspace page setup.

        Setup the Camera Viewer workspace with the following buttons and 
        commands:

            button_run_viewer       cmd_run_viewer
            button_capture_VL_img   cmd_capture_VL_img
            button_capture_EL_img   cmd_capture_EL_img

        Args:
            None

        Returns:
            None
        
        Raises:
            None
        """
        # Run Viewer button
        button_run_viewer = tk.Button(self.frame_workspace)
        button_run_viewer.configure(text="Run Viewer",
            command=self.cmd_run_viewer, height=1, width=8)
        button_run_viewer.place(relx=0.1, rely=0.95, anchor="center")

        # Run Viewer button
        button_capture_VL_img = tk.Button(self.frame_workspace)
        button_capture_VL_img.configure(text="Capture VL Image",
            command=self.cmd_capture_VL_img, height=1, width=14)
        button_capture_VL_img.place(relx=0.35, rely=0.95, anchor="center")

        # Run Viewer button
        button_capture_EL_img = tk.Button(self.frame_workspace)
        button_capture_EL_img.configure(text="Capture EL Image",
            command=self.cmd_capture_EL_img, height=1, width=14)
        button_capture_EL_img.place(relx=0.65, rely=0.95, anchor="center")

        # Run Viewer button
        button_stop_viewer = tk.Button(self.frame_workspace)
        button_stop_viewer.configure(text="Stop Viewer",
            command=self.command_stop_viewer, height=1, width=8)
        button_stop_viewer.place(relx=0.9, rely=0.95, anchor="center")

    def cmd_run_viewer(self):
        print('run viewer')
        picam2.start_preview(picamera2.Preview.QTGL, x=20, y=125, width=520, 
            height=270)
        picam2.start()

    def cmd_capture_VL_img(self):
        picam2.stop_preview()
        picam2.start_preview(picamera2.Preview.QTGL, x=20, y=125, width=520, 
            height=270)
        picam2.start()
        img_timestamp = time.strftime("%Y%m%d%H%M%S")
        img_filepath = IMG_VIEWER_DIR + "img_VL." + img_timestamp + ".tif"
        picam2.capture_file(img_filepath)
        time.sleep(1)
        print('capture base image: ' + img_filepath)

    def cmd_capture_EL_img(self):
        picam2.stop_preview()
        picam2.start_preview(picamera2.Preview.QTGL, x=20, y=125, width=520, 
            height=270)
        picam2.start()
        img_timestamp = time.strftime("%Y%m%d%H%M%S")
        img_filepath = IMG_VIEWER_DIR + "img_EL." + img_timestamp + ".jpg"
        GPIO.output(7,GPIO.HIGH)
        time.sleep(0.5)
        picam2.capture_file(img_filepath)
        time.sleep(1)
        GPIO.output(7,GPIO.LOW)
        print('capture EL image: ' + img_filepath)


    def command_stop_viewer(self):
        print('stop viewer')
        picam2.stop_preview()


    def command_quit(self):
        self.destroy()


    #TODO
    def workspace_el_measure_page_setup(self):
        el_measure_button = tk.Button(self.frame_workspace)
        el_measure_button.configure(text="EL Measuremnt",
            command=self.command_quit, height=1, width=20)
        el_measure_button.place(relx=0.5, rely=0.9,
            anchor="center")
            
    def command_run_el_measure(self):
        picam2.stop_preview()
        
        # for the number of iterations
        # Setup the camera
        # Capture the image
        # Write the tif files
        


    #TODO
    def workspace_settings_page_setup(self):
        file_transfer_button = tk.Button(self.frame_workspace)
        file_transfer_button.configure(text="Settings",
            command=self.command_quit, height=1, width=20
        )
        file_transfer_button.place(relx=0.5, rely=0.9, anchor="center")




    """ File Tansfer functions """
    src_dir = IMG_VIEWER_DIR
    src_file = IMG_VIEWER_DIR
    dst_dir = "/media/portableel"
    #src_file_img = ImageTk.PhotoImage(Image.new("RGB", (60, 60),'lightgray'))
    #src_file_img = ImageTk.PhotoImage(Image.open("/opt/pelms/images_viewer/img_EL.20240501155719.jpg"))
    #PIL_img = Image.open('/opt/pelms/images_viewer/test.jpg')
    #PIL_img = PIL_img.resize((60,60))
    
    def workspace_file_transfer_setup(self):
        src_file_img = ImageTk.PhotoImage(Image.new(mode="RGB", size=(150,150)))
        src_file_img_label = tk.Label(self.frame_workspace, image=src_file_img)   

        src_dir_label = tk.Label(self.frame_workspace, text="Source Directory:")
        src_dir_val = tk.Label(self.frame_workspace, text=self.src_dir, 
            background="white", highlightbackground="black", 
            highlightthickness=0.5)
        src_dir_update_button = tk.Button(self.frame_workspace)
        src_dir_update_button.configure(text="Change", height=1, width=6,
            command=lambda: self.cmd_file_transfer_update_path('src_dir', 
            src_dir_val, src_file_img_label))
        src_dir_label.place(relx=0.02, rely=0.05, anchor="w")
        src_dir_val.place(relx=0.02, rely=0.12, anchor="w")
        src_dir_update_button.place(relx=0.85, rely=0.05, anchor="w")

        src_file_label = tk.Label(self.frame_workspace, text = "Source File:")
        src_file_val = tk.Label(self.frame_workspace, text=self.src_file,
            background="white", highlightbackground="black", 
            highlightthickness=0.5)
        src_file_update_button = tk.Button(self.frame_workspace)
        src_file_update_button.configure(text="Change", height=1, width=6,
            command=lambda: self.cmd_file_transfer_update_path('src_file', 
            src_file_val, src_file_img_label))
        src_file_label.place(relx=0.02, rely=0.20, anchor="w")
        src_file_val.place(relx=0.02, rely=0.27, anchor="w")
        src_file_update_button.place(relx=0.85, rely=0.20, anchor="w")

        dst_dir_label = tk.Label(self.frame_workspace, text = "Dest Directory:")
        dst_dir_val = tk.Label(self.frame_workspace, text=self.dst_dir,
            background="white", highlightbackground="black", 
            highlightthickness=0.5)
        dst_dir_update_button = tk.Button(self.frame_workspace)
        dst_dir_update_button.configure(text="Change", height=1, width=6,
            command=lambda: self.cmd_file_transfer_update_path('dst_dir', 
            dst_dir_val, src_file_img_label))
        dst_dir_label.place(relx=0.02, rely=0.80, anchor="w")
        dst_dir_val.place(relx=0.02, rely=0.85, anchor="w")
        dst_dir_update_button.place(relx=0.85, rely=0.80, anchor="w")

        src_file_img_label.place(relx=0.05,rely=0.32).pack()

        return
        


    def cmd_file_transfer_update_path(self, path_type, val_label, img_label):
        if path_type == 'src_dir':
            path_string = filedialog.askdirectory(initialdir=self.src_dir)
        elif path_type == 'src_file':
            path_string = filedialog.askopenfilename(initialdir=self.src_file)
            val_label.config(text=path_string)
            src_img_full = Image.open(path_string)
            src_img_resize = src_img_full.resize((150,150))
            src_img = ImageTk.PhotoImage(src_img_resize)
            img_label.config(image=src_img).place(relx=0.05,rely=0.32).pack()
        elif path_type == 'dst_dir':
            path_string = filedialog.askdirectory(initialdir=self.dst_dir)
    
        val_label.config(text=path_string)
        return


if __name__ == "__main__":
    pelms_main_window = PelmsTkGuiClass()
    pelms_main_window.mainloop()
    GPIO.cleanup()
