#!/usr/bin/python
""" PELMS-2024-S1 Camera Algorithm System Raspberry Pi GUI.
This is the GUI used for the Camera Algorithm Sub-system of the 
Portable Electronic Measurement System (v2024 S1).  The GUI is written 
in python and runs on a Raspberry Pi that interfaces with:
    - the Raspberry Pi camera via the camera interface, and
    - the RF Link via the GPIO pins.

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
picam2_camera_preview_config = picam2.create_preview_configuration(
    transform=libcamera.Transform(hflip=1, vflip=1))
picam2.configure(picam2_camera_preview_config)



"""Global directories configuration
The global directories used by the GUI are primarily used to store intermediate 
image files.

IMG_DATA_DIR  is the directory used for storing images captured using the 
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
        #self.attributes('-fullscreen', True)

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
        # Menu Option:      Camera Viewer
        # Button:           button_camera_viewer 
        # Workpace Config:  config_frame_workspace('camera_viewer')
        button_camera_viewer = tk.Button(self.frame_menu)
        button_camera_viewer.configure(text="Camera Viewer",
            command=lambda: self.config_frame_workspace('camera_viewer'), 
            height=1, width=20)
        button_camera_viewer.place(relx=0.5, rely=0.15, anchor="center")

        # Menu Option:      EL Measure
        # Button:           button_el_measure 
        # Workpace Config:  config_frame_workspace('el_measure')
        button_el_measure = tk.Button(self.frame_menu)
        button_el_measure.configure(text="EL Measure",
            command=lambda: self.config_frame_workspace('el_measure'), 
            height=1, width=20)
        button_el_measure.place(relx=0.5, rely=0.25, anchor="center")

        # Menu Option:      File Transfer
        # Button:           button_file_transfer 
        # Workpace Config:  config_frame_workspace('file_transfer')
        button_file_transfer = tk.Button(self.frame_menu)
        button_file_transfer.configure(text="File Transfer", height=1, 
            width=20,
            command=lambda: self.config_frame_workspace('file_transfer'))
        button_file_transfer.place(relx=0.5, rely=0.35, anchor="center")

        # Menu Option:      Quit
        # Button:           button_quit 
        # Workpace Config:  N/A call cmd_quit
        button_quit = tk.Button(self.frame_menu)
        button_quit.configure(text="Quit", command=self.command_quit,
            height=1, width=20)
        button_quit.place(relx=0.5, rely=0.85, anchor="center")


    def config_frame_workspace(self, workspace_type):
        """ Configure the frame workspace.
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

        if workspace_type == 'camera_viewer':
            label_workspace_title.configure(text="Camera Viewer")
            self.workspace_camera_viewer_page_setup()
        elif workspace_type == 'el_measure':
            label_workspace_title.configure(text="   EL Measure   ")
            self.workspace_el_measure_page_setup()
        elif workspace_type == 'file_transfer':
            label_workspace_title.configure(text="  File Transfer  ")
            self.workspace_file_transfer_setup()
        else:
            label_workspace_title.configure(text="Camera Viewer")
            self.workspace_camera_viewer_page_setup()


    """ Camera Viewer functions """
    def workspace_camera_viewer_page_setup(self):
        """ Camera Viewer workspace page setup.
        Setup the Camera Viewer workspace with the following options:
            - Run Viewer        i.e. Run the camera preview
            - Capture VL image  i.e. Take a VL (Visible Light) image    
            - Capture EL image  i.e. Take a EL (Electroluminesence) image
            - Stop Viewer       i.e. Stop the camera preview
        
        (A VL image is simply a normal image captured by the camera, an EL
         image is taken when a GPIO pin is raised that should trigger a current
         regulator to inject current into a Solar Panel that will generate
         EL light.)

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
            command=lambda: self.cmd_camera_viewer('run_viewer'), height=1, 
                width=8)
        button_run_viewer.place(relx=0.1, rely=0.95, anchor="center")

        # Capture VL Image button
        button_capture_VL_img = tk.Button(self.frame_workspace)
        button_capture_VL_img.configure(text="Capture VL Image",
            command=lambda: self.cmd_camera_viewer('VL_img'), height=1, 
                width=14)
        button_capture_VL_img.place(relx=0.35, rely=0.95, anchor="center")

        # Capture EL Image button
        button_capture_EL_img = tk.Button(self.frame_workspace)
        button_capture_EL_img.configure(text="Capture EL Image",
            command=lambda: self.cmd_camera_viewer('EL_img'), height=1, 
                width=14)
        button_capture_EL_img.place(relx=0.65, rely=0.95, anchor="center")

        # Stop Viewer button
        button_stop_viewer = tk.Button(self.frame_workspace)
        button_stop_viewer.configure(text="Stop Viewer",
            command=lambda: self.cmd_camera_viewer('stop_viewer'), height=1, 
                width=8)
        button_stop_viewer.place(relx=0.9, rely=0.95, anchor="center")

        # Preview background:
        preview_background_label = tk.Label(self.frame_workspace)
        preview_background_label.config(background="black")
        preview_background_label.place(x=19, y=35, width=520, height=280)
        preview_bg_dict = preview_background_label.place_info()
        print(preview_bg_dict['x'])

    def cmd_camera_viewer(self, cmd_type):
        """ Camera Viewer commands.
        Runs the camera viewer commands that are called by the camera viewer
        buttons.  Depending on the cmd_type passed through the function will do
        one of the following:
            Run the camera viewer
            Capture a VL (Visible Light) image
            Capture an EL (Electroluminescence) image
            Stop the camera viewer

        Args:
            cmd_type    Determines what commands are run is one of the 
                        following: 
                        ['run_viewer', 'VL_img', 'EL_img', 'stop_viewer']

        Returns:
            None
        
        Raises:
            None
        """
        if cmd_type == 'run_viewer':
            if picam2.started == True:
                picam2.stop_preview()
                picam2.stop()
                time.sleep(0.5)

            picam2.start_preview(picamera2.Preview.QTGL, x=20, y=125, width=520, 
                height=270)
            picam2.start()

        if cmd_type == 'VL_img':
            if picam2.started == True:
                picam2.stop_preview()
                picam2.stop()
                time.sleep(0.5)

            picam2.start_preview(picamera2.Preview.QTGL, x=20, y=125, width=520, 
                height=270)
            picam2.start()

            img_timestamp = time.strftime("%Y%m%d%H%M%S")
            img_filepath = IMG_DATA_DIR + img_timestamp + "-preview_VL" + ".tif"
            picam2.capture_file(img_filepath)
            time.sleep(1)

        if cmd_type == 'EL_img':
            if picam2.started == True:
                print("EL_img: Stopping Picam")
                picam2.stop_preview()
                picam2.stop()
                time.sleep(0.5)

            time.sleep(1)
            picam2.start_preview(picamera2.Preview.QTGL, x=20, y=125, width=520, 
                height=270)
            picam2.start()
            img_timestamp = time.strftime("%Y%m%d%H%M%S")
            img_filepath = IMG_DATA_DIR + img_timestamp + "-preview_EL" + ".tif"
            GPIO.output(7,GPIO.HIGH)
            time.sleep(0.5)
            picam2.capture_file(img_filepath)
            time.sleep(0.5)
            GPIO.output(7,GPIO.LOW)

        if cmd_type == 'stop_viewer':
            if picam2.started == True:
                picam2.stop_preview()
                picam2.stop()
                time.sleep(0.25)

        return






    #TODO
    """ EL Measurement functions and variables """

    elm_status = "preview_camera_mode"
        
    def workspace_el_measure_page_setup(self):
        """ EL Measure workspace page setup.
        Setup the workspace with the following options:
            - Image Pair Count  i.e. Number of pairs used in EL Measurment
            - Keep Pair Files   i.e. Keep pair files used in EL Measurement    
            - Camera Resolution i.e. Pixel Resolution of camera 
            - Stop Viewer       i.e. Stop the camera preview
        
        (A VL image is simply a normal image captured by the camera, an EL
         image is taken when a GPIO pin is raised that should trigger a current
         regulator to inject current into a Solar Panel that will generate
         EL light.)

        Args:
            None

        Returns:
            None
        
        Raises:
            None
        """

        self.elm_img_num_pair = tk.StringVar(self)#"50"
        self.elm_img_num_pair.set("5")
        self.elm_keep_pair_files = StringVar(self)
        self.elm_keep_pair_files.set("N")
        self.elm_camera_res = StringVar(self)
        self.elm_camera_res.set("(2028x1520)")

        elm_status_label = tk.Label(self.frame_workspace, text="Status: ")
        elm_status_val = tk.Label(self.frame_workspace, text=self.elm_status)

        elm_img_num_pair_label = tk.Label(self.frame_workspace, 
            text="Image Pair Count: ")    
        elm_img_num_pair_optmenu = tk.OptionMenu(self.frame_workspace, 
            self.elm_img_num_pair, "1", "2", "5", "10", "20", "50", "80", 
            "100")
        
        elm_keep_pair_files_label = tk.Label(self.frame_workspace, 
            text="Keep Pair Files: ")    
        elm_keep_pair_files_optmenu = tk.OptionMenu(self.frame_workspace, 
            self.elm_keep_pair_files, "Y", "N")


        elm_camera_res_label = tk.Label(self.frame_workspace, 
            text="Camera Resolution: ")    
        elm_camera_res_optmenu = tk.OptionMenu(self.frame_workspace, 
            self.elm_camera_res, "(2028x1520)", "(4056x3040)")

        elm_img_num_pair_label.place(relx=0.05, rely=0.04)  
        elm_img_num_pair_optmenu.place(relx=0.30, rely=0.02)        
        elm_keep_pair_files_label.place(relx=0.05, rely=0.14)    
        elm_keep_pair_files_optmenu.place(relx=0.30, rely=0.12)
        elm_camera_res_label.place(relx=0.05, rely=0.24)    
        elm_camera_res_optmenu.place(relx=0.30, rely=0.22)

        elm_status_label.place(relx=0.3, rely=0.9, anchor="w")
        elm_status_val.place(relx=0.4, rely=0.9, anchor="w")

        elm_run_button = tk.Button(self.frame_workspace)
        elm_run_button.config(text="Run EL Measurement",
            command=lambda: self.command_run_elm(elm_status_val, 
                self.elm_img_num_pair.get(), self.elm_keep_pair_files.get(), 
                self.elm_camera_res.get()))
        elm_run_button.config(height=4, width=25)
        elm_run_button.place(relx=0.55, rely=0.05)


            
    def command_run_elm(self, status_val, num_pair, keep_pair_files, cam_res):

        print("elm_status:         " + self.elm_status)
        print("elm_img_num_pair: " + num_pair)
    
        print('---- preview config ----')
        print(picam2.camera_config['use_case'])
        print(picam2.camera_config['raw'])
        print('----------------------')

        # Stop the camera
        if picam2.started == True:
            picam2.stop_preview()
            picam2.stop()
    
        # Build the still config, load it and start the camera
        if cam_res == "(2028x1520)":
            picam2_camera_raw_config = picam2.create_preview_configuration(
                transform=libcamera.Transform(hflip=1, vflip=1), 
                raw={'format': 'SRGGB12'})
        else:
            picam2_camera_raw_config = picam2.create_still_configuration(
                transform=libcamera.Transform(hflip=1, vflip=1), 
                raw={'format': 'SRGGB12'})
        
        picam2.configure(picam2_camera_raw_config)
        try: 
            picam2.start()
        except:
            print('Camera Start Fail')
            self.elm_status = "camera_start_fail"
            status_val.configure(text=self.elm_status)
            status_val.update()
            return

        # Check the config
        print('---- still config ----')
        print(picam2.camera_config['use_case'])
        print(picam2.camera_config['raw'])
        print('----------------------')

        # Update the status
        self.elm_status = "still_camera_mode"
        status_val.configure(text=self.elm_status)
        status_val.update()

        # Create the file_prefix containing timestamp and measure info 
        img_timestamp = time.strftime("%Y%m%d%H%M%S")
        img_file_prefix = IMG_DATA_DIR + img_timestamp + "-ELM"
 
        # Create a VL and EL image for each pair
        for pair_index in range(int(num_pair)):

            # Update the status
            self.elm_status = "Measuring - Image Capture Pair: " \
                            + str(pair_index)
            status_val.configure(text=self.elm_status)
            status_val.update()
            # Update the VL and EL filenames
            index_str = "-" + "{:03d}".format(pair_index)
            num_pair_str = "-" + "{:02d}".format(int(num_pair))

            img_VL_file = img_file_prefix + index_str + num_pair_str + "-VL.tif"
            img_EL_file = img_file_prefix + index_str + num_pair_str + "-EL.tif"
            img_IR_file = img_file_prefix + index_str + num_pair_str + "-IR.tif"

            # Capture the VL image:
            # Get a raw Bayer frame with 12-bit values packed into 16-bits.
            # Convert Bayer 12-bit array to RGB 16-bit an write to file by
            # doing the following steps:
            #   - Convert to 12-bit value to 16-bit by shifting 4 bits
            #   - Convert from Bayer format to RGB format    
            img_VL_Bayer_12bit = picam2.capture_array("raw").view(np.uint16)
            img_VL_Bayer_16bit = img_VL_Bayer_12bit * 16
            img_VL_RGB_16bit = cv2.cvtColor(img_VL_Bayer_16bit, 
                cv2.COLOR_BAYER_RG2RGB)

            if keep_pair_files == 'Y':
                cv2.imwrite(img_VL_file, img_VL_RGB_16bit)
            
            # Capture the EL image:
            # Turn on the EL signal
            GPIO.output(7,GPIO.HIGH)
            time.sleep(0.5)
            # Get a raw Bayer frame with 12-bit values packed into 16-bits.
            # Convert Bayer 12-bit array to RGB 16-bit an write to file.
            img_EL_Bayer_12bit = picam2.capture_array("raw").view(np.uint16)            
            img_EL_Bayer_16bit = img_EL_Bayer_12bit * 16
            img_EL_RGB_16bit = cv2.cvtColor(img_EL_Bayer_16bit, 
                cv2.COLOR_BAYER_RG2RGB)

            if keep_pair_files == 'Y':
                cv2.imwrite(img_EL_file, img_EL_RGB_16bit)
            # Turn off the EL signal
            GPIO.output(7,GPIO.LOW)
            time.sleep(0.5)

            # Generate the IR image:
            # Subtract the visual light (VL) image from the 
            # electroluminescence (EL) image to leave behind only the 
            # infrared (IR) image.
            img_IR_RGB_16bit = img_EL_RGB_16bit - img_VL_RGB_16bit
            
            if keep_pair_files == 'Y':
                # Write to file
                cv2.imwrite(img_IR_file, img_IR_RGB_16bit)

            # Sum the 16-bit IR images in 32 float format:
            if pair_index == 0:
                sum_IR_RGB_32float = img_IR_RGB_16bit.astype(np.float32)
            else:
                sum_IR_RGB_32float = sum_IR_RGB_32float \
                    + img_IR_RGB_16bit.astype(np.float32)

        # Find the min and max values of the sum of the IR images:
        min_val = np.min(sum_IR_RGB_32float)
        max_val = np.max(sum_IR_RGB_32float)
        print("min_val: " + str(min_val))
        print("max_val: " + str(max_val))

        # Convert the image to a uint16 full scale image.
        dfs_IR_RGB_32float = sum_IR_RGB_32float / max_val * (2**16 - 1)
        dfs_IR_RGB_16bit = dfs_IR_RGB_32float.astype(np.uint16)

        min_val = np.min(dfs_IR_RGB_16bit)
        max_val = np.max(dfs_IR_RGB_16bit)
        print("min_val: " + str(min_val))
        print("max_val: " + str(max_val))

        # Convert from RGB 16-bit to GRAY 16-bit and write to file.
        dfs_IR_GRAY_16bit = cv2.cvtColor(dfs_IR_RGB_16bit, cv2.COLOR_RGB2GRAY)

        dfs_IR_RGB_file = img_file_prefix + num_pair_str + "-DFS-IR-RGB.tif"
        dfs_IR_GRAY_file = img_file_prefix + num_pair_str + "-DFS-IR-GRAY.png"

        cv2.imwrite(dfs_IR_RGB_file, dfs_IR_RGB_16bit)
        cv2.imwrite(dfs_IR_GRAY_file, dfs_IR_GRAY_16bit)

        # Stop the camera and re-configure it to the original preview.
        if cam_res == "(2028x1520)":
            picam2.stop_preview()
        picam2.stop()
        time.sleep(2)
        picam2.configure(picam2_camera_preview_config)
        picam2.start()

        # Update the status
        self.elm_status = "preview_camera_mode"
        status_val.configure(text=self.elm_status)
        status_val.update()

        return





    """ File Transfer functions """
    """ File Transfer class variables
    There are 3 class variables are defined for use in the File Transfer 
    functions - which are the source directory, source file and destination 
    directory.
    """
    src_dir = IMG_DATA_DIR
    src_file = IMG_DATA_DIR
    dst_dir = "/media/portableel"
    
    def workspace_file_transfer_setup(self):
        """ File Transfer workspace page setup..
        Setup the File Transfer workspace with the following options:
            - Source Directory      i.e. Display/Change source dir path.
            - Source File           i.e. Display/Change source file path.    
            - Destination Directory i.e. Display/Change dest dir path.
            - Transfer Directory    i.e. Copy source dir to dest dir.
            - Transfer File         i.e. Copy source file to dest dir.

        Args:
            None

        Returns:
            None
        
        Raises:
            None
        """
        # Initialise src_file_img i.e. image of the source file
        src_file_img = ImageTk.PhotoImage(Image.new(mode="RGB", size=(150,150)))
        src_file_img_label = tk.Label(self.frame_workspace)
        src_file_img_label.place(relx=0.05, rely=0.55)
        src_file_img_label.config(image=src_file_img)
        src_file_img_label.image = src_file_img
        
        # Source Directory display and buttons
        src_dir_label = tk.Label(self.frame_workspace, text="Source Directory:")
        src_dir_val = tk.Label(self.frame_workspace, text=self.src_dir, 
            background="white", highlightbackground="black", 
            highlightthickness=0.5)
        src_dir_update_button = tk.Button(self.frame_workspace)
        src_dir_update_button.configure(text="Change", height=1, width=6,
            command=lambda: self.cmd_file_transfer_update_path('src_dir', 
            src_dir_val, src_file_img_label))
        src_dir_label.place(relx=0.02, rely=0.03, anchor="w")
        src_dir_val.place(relx=0.02, rely=0.10, anchor="w")
        src_dir_update_button.place(relx=0.85, rely=0.05, anchor="w")

        # Source File display and buttons
        src_file_label = tk.Label(self.frame_workspace, text = "Source File:")
        src_file_val = tk.Label(self.frame_workspace, text=self.src_file,
            background="white", highlightbackground="black", 
            highlightthickness=0.5)
        src_file_update_button = tk.Button(self.frame_workspace)
        src_file_update_button.configure(text="Change", height=1, width=6,
            command=lambda: self.cmd_file_transfer_update_path('src_file', 
            src_file_val, src_file_img_label))
        src_file_label.place(relx=0.02, rely=0.18, anchor="w")
        src_file_val.place(relx=0.02, rely=0.25, anchor="w")
        src_file_update_button.place(relx=0.85, rely=0.20, anchor="w")

        # Destination Directory display and buttons
        dst_dir_label = tk.Label(self.frame_workspace, text = "Dest Directory:")
        dst_dir_val = tk.Label(self.frame_workspace, text=self.dst_dir,
            background="white", highlightbackground="black", 
            highlightthickness=0.5)
        dst_dir_update_button = tk.Button(self.frame_workspace)
        dst_dir_update_button.configure(text="Change", height=1, width=6,
            command=lambda: self.cmd_file_transfer_update_path('dst_dir', 
            dst_dir_val, src_file_img_label))
        dst_dir_label.place(relx=0.02, rely=0.33, anchor="w")
        dst_dir_val.place(relx=0.02, rely=0.40, anchor="w")
        dst_dir_update_button.place(relx=0.85, rely=0.35, anchor="w")

        # Source Directory Transfer button
        src_dir_transfer_button = tk.Button(self.frame_workspace)
        src_dir_transfer_button.configure(text="Transfer Source Dir", 
            command=lambda: self.cmd_file_transfer('dir'), height=2, width=20)
        src_dir_transfer_button.place(relx=0.55, rely=0.6, anchor="w")

        # Source File Transfer button
        src_file_transfer_button = tk.Button(self.frame_workspace)
        src_file_transfer_button.configure(text="Transfer Source File", 
            command=lambda: self.cmd_file_transfer('file'), height=2, width=20)
        src_file_transfer_button.place(relx=0.55, rely=0.8, anchor="w")

        # Place the image of the source file and label
        src_file_img_txt_label = tk.Label(self.frame_workspace, 
            text="Source File Image Preview:")
        src_file_img_txt_label.place(relx=0.015, rely=0.55, anchor="w")
        
        return
        

    def cmd_file_transfer_update_path(self, path_type, val_label, img_label):
        """ Transfer File update path commands.
        These command update the paths for the:
            - Source Directory      i.e. Display/Change source dir path.
            - Source File           i.e. Display/Change source file path.    
            - Destination Directory i.e. Display/Change dest dir path.
        
        Args:
            path_type   specifies the path_type to change one of:
                        'src_dir', 'src_file', 'dst_dir'
            val_label   specifies the label that will nedd tobe updated to 
                        update the path in the tKinter GUI
            img_label   specifies the label with the image for the source file

        Returns:
            None
        
        Raises:
            None
        """        
        if path_type == 'src_dir':
            path_string = filedialog.askdirectory(initialdir=self.src_dir)
            self.src_dir = path_string
        elif path_type == 'src_file':
            path_string = filedialog.askopenfilename(initialdir=self.src_dir)
            self.src_file = path_string
            val_label.config(text=path_string)
            src_img_full = Image.open(path_string)
            src_img_resize = src_img_full.resize((150,150))
            src_img = ImageTk.PhotoImage(src_img_resize)
            img_label.config(image=src_img)
            img_label.image = src_img
        elif path_type == 'dst_dir':
            path_string = filedialog.askdirectory(initialdir=self.dst_dir)
            self.dst_dir = path_string

        val_label.config(text=path_string)
        
        return
    
    def cmd_file_transfer(self, copy_type):
        """ Transfer File commands
        This command perform one of two file transfers depending on the 
        copy_type:
            - cp src_file dst_dir       i.e. File copy from source file to dest 
                                        dir.
            - cp -R src_dir dst_dir     i.e. Dir copy from source dir to dest 
                                        dir.    
        
        Args:
            copy_type   specifies the copy_type to change one of:
                        'file', 'dir'

        Returns:
            None
        
        Raises:
            None
        """        
        if copy_type == 'file':
            copy_cmd = "cp " + self.src_file + " " + self.dst_dir
        elif copy_type == 'dir':
            copy_cmd = "cp -R " + self.src_dir + " " + self.dst_dir
        
        print(copy_cmd)
        os.system(copy_cmd)
        
        return


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


if __name__ == "__main__":
    pelms_main_window = PelmsTkGuiClass()
    pelms_main_window.mainloop()
    GPIO.cleanup()
