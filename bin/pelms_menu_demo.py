#!/usr/bin/python
import tkinter as tk

#import picamera
import time
import numpy as np

from PIL import Image
from PIL import ImageTk

class PelmsTkGuiClass(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('800x480')
        self.resizable(False, False)
        self.title("Portable Electroluminescence Measurement System (pelms) v2023.s2")
        #self.attributes('-fullscreen', True)

        self.tk_Frame_header = tk.Frame(width=800, height=80)
        self.tk_Frame_header.configure(highlightbackground="black")
        self.tk_Frame_header.configure(highlightthickness=1)
        self.tk_Frame_header.place(x=0,y=0)
        
        self.tk_Frame_footer = tk.Frame(width=800, height=40)
        self.tk_Frame_footer.configure(highlightbackground="black")
        self.tk_Frame_footer.configure(highlightthickness=1)
        self.tk_Frame_footer.place(x=0,y=440)
        
        self.tk_Frame_menu = tk.Frame(width=240, height=360)
        self.tk_Frame_menu.configure(highlightbackground="black")
        self.tk_Frame_menu.configure(highlightthickness=1)
        self.tk_Frame_menu.place(x=560, y=80)
        
        self.tk_Frame_workspace = tk.Frame(width=560, height=360)
        self.tk_Frame_workspace.configure(highlightbackground="black")
        self.tk_Frame_workspace.configure(highlightthickness=1)
        self.tk_Frame_workspace.place(x=0, y=80)

        self.config_tk_Frame_header()
        self.config_tk_Frame_footer()
        self.config_tk_Frame_menu()
        self.config_tk_Frame_workspace('default')

    def config_tk_Frame_header(self):
        tk_Frame_header_label = tk.Label(self.tk_Frame_header)
        tk_Frame_header_label.configure(text="header frame")
        tk_Frame_header_label.place(relx=0.5, rely=0.5, anchor='center')
        
    def config_tk_Frame_footer(self):
        tk_Frame_footer_label = tk.Label(self.tk_Frame_footer)
        tk_Frame_footer_label.configure(text="footer frame")
        tk_Frame_footer_label.place(relx=0.5, rely=0.5, anchor='center')
        
    def config_tk_Frame_menu(self):
        tk_Frame_menu_label = tk.Label(self.tk_Frame_menu)
        tk_Frame_menu_label.configure(text="PELMS Options", font='bold')
        tk_Frame_menu_label.place(relx=0.5, rely=0.1, anchor="center")
        
        menu_button_capture_EL_image = tk.Button(self.tk_Frame_menu)
        menu_button_capture_EL_image.configure(text="Capture EL Image ...")
        menu_button_capture_EL_image.configure(command=lambda: self.config_tk_Frame_workspace('capture_EL_image'))
        menu_button_capture_EL_image.configure(height=1, width=20, justify="right")
        menu_button_capture_EL_image.place(relx=0.5, rely=0.25, anchor="center")

        menu_button_run_EL_image_test = tk.Button(self.tk_Frame_menu)
        menu_button_run_EL_image_test.configure(text="Run EL Image Test ...")
        menu_button_run_EL_image_test.configure(command=lambda: self.config_tk_Frame_workspace('run_EL_test'))
        menu_button_run_EL_image_test.configure(height=1, width=20)
        menu_button_run_EL_image_test.place(relx=0.5, rely=0.35, anchor="center")

        menu_button_camera_viewer = tk.Button(self.tk_Frame_menu)
        menu_button_camera_viewer.configure(text="Camera Viewer ...")
        menu_button_camera_viewer.configure(command=lambda: self.config_tk_Frame_workspace('camera_viewer'))
        menu_button_camera_viewer.configure(height=1, width=20)
        menu_button_camera_viewer.place(relx=0.5, rely=0.45, anchor="center")

        menu_button_settings = tk.Button(self.tk_Frame_menu)
        menu_button_settings.configure(text="Settings ...")
        menu_button_settings.configure(command=lambda: self.config_tk_Frame_workspace('settings'))
        menu_button_settings.configure(height=1, width=20)
        menu_button_settings.place(relx=0.5, rely=0.6, anchor="center")

        menu_button_file_transfer = tk.Button(self.tk_Frame_menu)
        menu_button_file_transfer.configure(text="File Transfer ...")
        menu_button_file_transfer.configure(command=lambda: self.config_tk_Frame_workspace('file_transfer'))
        menu_button_file_transfer.configure(height=1, width=20)
        menu_button_file_transfer.place(relx=0.5, rely=0.7, anchor="center")

        menu_button_quit = tk.Button(self.tk_Frame_menu)
        menu_button_quit.configure(text="Quit", command=self.command_quit)
        menu_button_quit.configure(height=1, width=20)
        menu_button_quit.place(relx=0.5, rely=0.9, anchor="center")

    def config_tk_Frame_workspace(self, workspace_type):
        tk_Frame_workspace_label = tk.Label(self.tk_Frame_workspace)

        if workspace_type == 'main_page':
            tk_Frame_workspace_label.configure(text="workspace frame - main page     ")
        elif workspace_type == 'capture_EL_image':
            tk_Frame_workspace_label.configure(text="workspace frame - capture EL    ")
        elif workspace_type == 'run_EL_test':
            tk_Frame_workspace_label.configure(text="workspace frame - run EL test   ")
        elif workspace_type == 'camera_viewer':
            tk_Frame_workspace_label.configure(text="workspace frame - camera view   ")
        elif workspace_type == 'settings':
            tk_Frame_workspace_label.configure(text="workspace frame - settings      ")
        elif workspace_type == 'file_transfer':
            tk_Frame_workspace_label.configure(text="workspace frame - file transfer ")
        else:
            tk_Frame_workspace_label.configure(text="workspace frame                 ")
        
        tk_Frame_workspace_label.place(relx=0.5, rely=0.5, anchor="center")


    def command_quit(self):
        self.destroy()


if __name__ == "__main__":
    pelms_main_window = PelmsTkGuiClass()
    pelms_main_window.mainloop()




