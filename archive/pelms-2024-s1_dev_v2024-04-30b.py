#!/usr/bin/python
import tkinter as tk

import picamera2
import libcamera

import os
import shutil
import time
import numpy as np

import RPi.GPIO as GPIO


from PIL import Image
from PIL import ImageTk

# Global GPIO settings
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.output(7,GPIO.LOW)



# Global picamera 2 configuration
picam2 = picamera2.Picamera2()
#picam2_camera_config = picam2.create_preview_configuration(raw={'format': 'SBGGR12'})
picam2_camera_config = picam2.create_preview_configuration()
picam2.configure(picam2_camera_config)

# Global directories - create the, if they don't exist
pelms_dir = '/opt/pelms/'
img_viewer_dir = pelms_dir + 'images_viewer/'
img_measure_dir = pelms_dir + 'images_measure/'

os.makedirs(img_viewer_dir, exist_ok=True)

os.makedirs(img_measure_dir, exist_ok=True)
shutil.rmtree(img_measure_dir) 
os.makedirs(img_measure_dir)


'''class PelmsPicamera2Class(picamera2.Picamera2):
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self):
        super().__init__()

    def run_preview(self):
        preview_config = self.create_preview_configuration()
        self.configure(preview_config)
        self.start_preview(picamera2.Preview.QTGL, 
            x=50, y=115, width=480, height=220
        )
        self.start()
        time.sleep(5)
        self.stop_preview()

    def stop_preview(self):
        self.stop_preview()        
'''

class PelmsTkGuiClass(tk.Tk):
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self):
        """Initializes the instance based on spam preference.

        Args:
          likes_spam: Defines if instance exhibits this preference.
        """
        super().__init__()
        self.geometry('800x480')
        self.resizable(False, False)
        self.title_string = "Portable Electroluminescence Measurement System "
        self.title_string += "(pelms) v2023.s2"
        self.title(self.title_string)
        #self.attributes('-fullscreen', True)
        #self.pelms_camera = picamera2.Picamera2() #PelmsPicamera2Class()

        self.Frame_header = tk.Frame()
        self.Frame_header.configure(
            width=800, height=80,
            highlightbackground="black",
            highlightthickness=1
        )
        self.Frame_header.place(x=0,y=0)
        self.config_Frame_header()

        self.Frame_footer = tk.Frame()
        self.Frame_footer.configure(
            width=800, height=40,
            highlightbackground="black",
            highlightthickness=1
        )
        self.Frame_footer.place(x=0,y=440)
        self.config_Frame_footer()
        
        self.Frame_menu = tk.Frame()
        self.Frame_menu.configure(width=240, height=360,
            highlightbackground="black",
            highlightthickness=1
        )
        self.Frame_menu.place(x=560, y=80)
        self.config_Frame_menu()
        
        self.Frame_workspace = tk.Frame()
        self.Frame_workspace.configure(width=560, height=360,
            highlightbackground="black",
            highlightthickness=1
        )
        self.Frame_workspace.place(x=0, y=80)
        self.config_Frame_workspace('default')

        
    def config_Frame_header(self):
        label_title = tk.Label(self.Frame_header)
        label_title.configure(text=self.title_string, 
            font=('Helvetica', 15, 'bold')
        )
        label_title.place(relx=0.5, rely=0.5, anchor='center')
        
    def config_Frame_footer(self):
        label_footer = tk.Label(self.Frame_footer)
        label_footer.configure(text="footer frame", font=(8), fg='Grey')
        label_footer.place(relx=0.5, rely=0.5, anchor='center')
        
    def config_Frame_menu(self):
        label_menu_title = tk.Label(self.Frame_menu)
        label_menu_title.configure(text="PELMS Options", 
            font=('Helvetica', 11, 'bold')
        )
        label_menu_title.place(relx=0.5, rely=0.05, anchor="center")

        button_capture_EL_image = tk.Button(self.Frame_menu)
        button_capture_EL_image.configure(text="Main Page",
            command=lambda: self.config_Frame_workspace('main_page'),
            height=1, width=20, justify="right"
        )
        button_capture_EL_image.place(relx=0.5, rely=0.15, anchor="center")

        button_capture_EL_image = tk.Button(self.Frame_menu)
        button_capture_EL_image.configure(text="Capture EL Image ...",
            command=lambda: self.config_Frame_workspace('capture_EL_image'),
            height=1, width=20, justify="right"
        )
        button_capture_EL_image.place(relx=0.5, rely=0.25, anchor="center")

        button_run_EL_image_test = tk.Button(self.Frame_menu)
        button_run_EL_image_test.configure(text="Run EL Image Test ...", 
            command=lambda: self.config_Frame_workspace('run_EL_test'),
            height=1, width=20
        )
        button_run_EL_image_test.place(relx=0.5, rely=0.35, anchor="center")

        button_camera_viewer = tk.Button(self.Frame_menu)
        button_camera_viewer.configure(text="Camera Viewer ...",
            command=lambda: self.config_Frame_workspace('camera_viewer'),
            height=1, width=20
        )
        button_camera_viewer.place(relx=0.5, rely=0.45, anchor="center")

        button_settings = tk.Button(self.Frame_menu)
        button_settings.configure(text="Settings ...",
            command=lambda: self.config_Frame_workspace('settings'),
            height=1, width=20
        )
        button_settings.place(relx=0.5, rely=0.6, anchor="center")

        button_file_transfer = tk.Button(self.Frame_menu)
        button_file_transfer.configure(text="File Transfer ...",
            command=lambda: self.config_Frame_workspace('file_transfer'),
            height=1, width=20
        )
        button_file_transfer.place(relx=0.5, rely=0.7, anchor="center")

        button_quit = tk.Button(self.Frame_menu)
        button_quit.configure(text="Quit", command=self.command_quit,
            height=1, width=20
        )
        button_quit.place(relx=0.5, rely=0.9, anchor="center")

    def config_Frame_workspace(self, workspace_type):
        for widget in self.Frame_workspace.winfo_children():
            widget.destroy()

        label_workspace = tk.Label(self.Frame_workspace)
        label_workspace.place(relx=0.5, rely=0.5, anchor="center")

        if workspace_type == 'main_page':
            self.workspace_main_page_setup()
        elif workspace_type == 'capture_EL_image':
            self.workspace_capture_EL_image_page_setup()
        elif workspace_type == 'run_EL_test':
            self.workspace_run_EL_test_page_setup()
        elif workspace_type == 'camera_viewer':
            self.workspace_camera_viewer_page_setup()
        elif workspace_type == 'settings':
            self.workspace_settings_page_setup()
        elif workspace_type == 'file_transfer':
            self.workspace_file_transfer_setup()
        else:
            self.workspace_main_page_setup()
        


    def command_quit(self):
        self.destroy()

    #TODO
    def workspace_main_page_setup(self):
        file_transfer_button = tk.Button(self.Frame_workspace)
        file_transfer_button.configure(text="Main Page", 
            command=self.command_quit, height=1, width=20
        )
        file_transfer_button.place(relx=0.5, rely=0.9, anchor="center")

    #TODO
    def workspace_capture_EL_image_page_setup(self):
        file_transfer_button = tk.Button(self.Frame_workspace)
        file_transfer_button.configure(text="Capture EL Image", 
            command=self.command_quit, height=1, width=20
        )
        file_transfer_button.place(relx=0.5, rely=0.9, anchor="center")

    #TODO
    def workspace_run_EL_test_page_setup(self):
        file_transfer_button = tk.Button(self.Frame_workspace)
        file_transfer_button.configure(text="Run EL Test", 
            command=self.command_quit, height=1, width=20
        )
        file_transfer_button.place(relx=0.5, rely=0.9, anchor="center")

    #TODO
    def workspace_camera_viewer_page_setup(self):
        button_run_viewer = tk.Button(self.Frame_workspace)
        button_run_viewer.configure(text="Run Viewer", 
            command=self.command_run_viewer, height=1, width=8
        )
        button_run_viewer.place(relx=0.1, rely=0.9, anchor="center")
        
        button_capture_base_image = tk.Button(self.Frame_workspace)
        button_capture_base_image.configure(text="Capture Base Image", 
            command=self.command_capture_base_image, height=1, width=14
        )
        button_capture_base_image.place(relx=0.35, rely=0.9, anchor="center")

        button_capture_EL_image = tk.Button(self.Frame_workspace)
        button_capture_EL_image.configure(text="Capture EL Image", 
            command=self.command_capture_EL_image, height=1, width=14
        )
        button_capture_EL_image.place(relx=0.65, rely=0.9, anchor="center")

        button_stop_viewer = tk.Button(self.Frame_workspace)
        button_stop_viewer.configure(text="Stop Viewer", 
            command=self.command_stop_viewer, height=1, width=8
        )
        button_stop_viewer.place(relx=0.9, rely=0.9, anchor="center")


    def command_run_viewer(self):
        print('run viewer')
        picam2.start_preview(picamera2.Preview.QTGL, x=20, y=150, width=520, height=250)
        picam2.start()
        
    def command_capture_base_image(self):
        picam2.stop_preview()
        picam2.start_preview(picamera2.Preview.QTGL, x=20, y=150, width=520, height=250)
        picam2.start()
        img_timestamp = time.strftime("%Y%m%d%H%M%S")
        img_filepath = img_viewer_dir + "img_base." + img_timestamp + ".jpg"
        picam2.capture_file(img_filepath)
        time.sleep(1)
        print('capture base image: ' + img_filepath)

    def command_capture_EL_image(self):
        picam2.stop_preview()
        picam2.start_preview(picamera2.Preview.QTGL, x=20, y=150, width=520, height=250)
        picam2.start()
        img_timestamp = time.strftime("%Y%m%d%H%M%S")
        img_filepath = img_viewer_dir + "img_EL." + img_timestamp + ".jpg"
        GPIO.output(7,GPIO.HIGH)
        time.sleep(0.5)
        picam2.capture_file(img_filepath)
        time.sleep(1)
        GPIO.output(7,GPIO.LOW)
        print('capture EL image: ' + img_filepath)



    def command_stop_viewer(self):
        print('stop viewer')
        picam2.stop_preview()

    #TODO
    def workspace_settings_page_setup(self):
        file_transfer_button = tk.Button(self.Frame_workspace)
        file_transfer_button.configure(text="Settings", 
            command=self.command_quit, height=1, width=20
        )
        file_transfer_button.place(relx=0.5, rely=0.9, anchor="center")

    #TODO
    def workspace_file_transfer_setup(self):
        file_transfer_button = tk.Button(self.Frame_workspace)
        file_transfer_button.configure(text="File Transfer", 
            command=self.command_quit, height=1, width=20
        )
        file_transfer_button.place(relx=0.5, rely=0.9, anchor="center")



'''
def open():
    global my_image
    root.filename = filedialog.askopenfilename(initialdir="~/test/images", title="Select a File", filetypes=(("png files", "*.png"), ("jpeg files", "*.jpeg"),("all files", "*")))
    my_label = Label(root, text=root.filename).pack()
    my_image = ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label = Label(image=my_image).pack()
    return


my_btn = Button(root, text="Open File", command=open).pack()
'''

if __name__ == "__main__":
    pelms_main_window = PelmsTkGuiClass()
    pelms_main_window.mainloop()

    GPIO.cleanup()
