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

        self.tk_Frame_header = tk.Frame(width=800, height=120)
        self.tk_Frame_header.configure(highlightbackground="black")
        self.tk_Frame_header.configure(highlightthickness=1)
        self.tk_Frame_header.place(x=0,y=0)
        
        self.tk_Frame_footer = tk.Frame(width=800, height=60)
        self.tk_Frame_footer.configure(highlightbackground="black")
        self.tk_Frame_footer.configure(highlightthickness=1)
        self.tk_Frame_footer.place(x=0,y=420)
        
        self.tk_Frame_menu = tk.Frame(width=300, height=300)
        self.tk_Frame_menu.configure(highlightbackground="black")
        self.tk_Frame_menu.configure(highlightthickness=1)
        self.tk_Frame_menu.place(x=500, y=120)
        
        self.tk_Frame_workspace = tk.Frame(width=500, height=300)
        self.tk_Frame_workspace.configure(highlightbackground="black")
        self.tk_Frame_workspace.configure(highlightthickness=1)
        self.tk_Frame_workspace.place(x=0, y=120)

        self.config_tk_Frame_header()
        self.config_tk_Frame_footer()
        self.config_tk_Frame_menu()
        self.config_tk_Frame_workspace()

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
        tk_Frame_menu_label.configure(text="menu frame")
        tk_Frame_menu_label.place(relx=0.5, rely=0.5, anchor='center')
        
        menu_button_camera_settings = tk.Button(self.tk_Frame_menu)
        menu_button_camera_settings.configure(text="Camera Settings")
        menu_button_camera_settings.place(relx=0.1, rely=0.1, anchor="w")

        menu_button_camera_viewer = tk.Button(self.tk_Frame_menu)
        menu_button_camera_viewer.configure(text="Camera Viewer")
        menu_button_camera_viewer.place(relx=0.1, rely=0.2, anchor="w")

        menu_button_quit = tk.Button(self.tk_Frame_menu)
        menu_button_quit.configure(text="Quit")
        menu_button_quit.place(relx=0.1, rely=0.3, anchor="w")

    def config_tk_Frame_workspace(self):
        tk_Frame_workspace_label = tk.Label(self.tk_Frame_workspace)
        tk_Frame_workspace_label.configure(text="workspace frame")
        tk_Frame_workspace_label.place(relx=0.5, rely=0.5, anchor='center')




if __name__ == "__main__":
    pelms_main_window = PelmsTkGuiClass()
    pelms_main_window.mainloop()




