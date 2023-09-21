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
        self.title_string = "Portable Electroluminescence Measurement System "
        self.title_string += "(pelms) v2023.s2"
        self.title(self.title_string)
        self.attributes('-fullscreen', True)

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
        file_transfer_button = tk.Button(self.Frame_workspace)
        file_transfer_button.configure(text="Camera Viewer", 
            command=self.command_quit, height=1, width=20
        )
        file_transfer_button.place(relx=0.5, rely=0.9, anchor="center")

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




