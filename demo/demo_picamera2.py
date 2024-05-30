from tkinter import *
from tkinter import messagebox
from picamera2 import Picamera2, Preview
from libcamera import controls
import time
import sys
import importlib.metadata

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.start()

root = Tk()
root.title(sys.argv[0])
root.geometry("550x450")
# center on screen
root.eval('tk::PlaceWindow . center')

label_picam_ver = Label(root,
                        text="picamera2 ver: " + importlib.metadata.version('picamera2'),
                        anchor="e",
                        )
label_picam_ver.pack(fill = "x", padx=(10, 10), pady=10)

labelframe = LabelFrame(root, text="Click button to capture image")
labelframe.pack(fill = "both", expand = "yes")

def capture_button_CallBack():
    print("- Capture image -")
    timeStamp = time.strftime("%Y%m%d-%H%M%S")
    targetPath="img_"+timeStamp+".jpg"
    picam2.capture_file(targetPath)
    print("image save:", targetPath)
    print("----------------------------------------------------")
    time.sleep(1)
    print("- Capture image -")
    timeStamp = time.strftime("%Y%m%d-%H%M%S")
    targetPath="img_"+timeStamp+".jpg"
    picam2.capture_file(targetPath)
    print("image save:", targetPath)
    print("----------------------------------------------------")

capture_button = Button(labelframe, text ="Capture", command = capture_button_CallBack)
capture_button.pack()

stop_preview_button = Button(labelframe, text ="Stop Preview", command = picam2.stop_preview)
stop_preview_button.pack()

start_preview_button = Button(labelframe, text ="Start Preview", command = picam2.start_preview)
start_preview_button.pack()

#def AF_button_tpggled():
#    if AF_button.config('relief')[-1] == 'sunken':
#        AF_button.config(relief='raised')
#        picam2.set_controls({"AfMode": controls.AfModeEnum.Manual})
#    else:
#        AF_button.config(relief='sunken')
#        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#        
#    print(picam2.controls.AfMode)
#    
#AF_button = Button(labelframe, text="Continuous Focus", relief="sunken", command=AF_button_tpggled)
#AF_button.pack()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        
        # if preview window cloased before,
        # will raise RuntimeError of No preview specified.
        try:
            picam2.stop_preview()
        except RuntimeError as e:
            print(e)
        root.destroy()
        
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

