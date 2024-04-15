from tkinter import *
from tkinter import ttk
#import apod_desktop
#import cytpe
import ctypes
# pillow
from PIL import Image, ImageTk

# Initialize the image cache
#apod_desktop.init_apod_cache()

# TODO: Create the GUI
root = Tk()
root.title("APOD Viewer")


#Creating frames for the GUI


#frame for image (top frame)
root.columnconfigure(0,weight=2)
root.columnconfigure(1,weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)
    
    
image_frame = ttk.Frame(root)

image_frame.grid(row=0, column=0, columnspan=2)

#top fram widget


#frame for title and date (middle frame)
# middle_frame = LabelFrame(root, text="") #This will need to be pulled from the API
# middle_frame.grid(row=1, column=0)

#frame for cached image and set button (bottom left frame)
bottom_left_frame = LabelFrame(root, text="View Cached Image")
bottom_left_frame.grid(row=1, column=0)

#frame for date entry and get download image button (bottom right frame)
bottom_right_frame = LabelFrame(root, text="Get More Images")
bottom_right_frame.grid(row=1, column=1)

# TODO: Set Icon
iconID = 'COMP593.APODViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(iconID)
root.iconbitmap('nasa.ico')

# TODO: Set default picture
openIMG = Image.open("moonwalking.jpg")
img = ImageTk.PhotoImage(openIMG)
# Add it to the label
imgLbl = Label(image_frame, image=img)
imgLbl.grid()

# TODO: Select Image Label
selImgLbl = Label(bottom_left_frame, text="Select Image:")
selImgLbl.grid()
# TODO: Select Image drop down
selImgcmbx = ttk.Combobox(bottom_left_frame)
selImgcmbx.grid()
# TODO: Set as Desktop button
setDskBtn = Button(bottom_left_frame, text="Set as Desktop")
setDskBtn.grid(row=1,column=1, padx=10)

# TODO: Select Date Label
selDateLbl = Label(bottom_right_frame, text="Select Date:")
selDateLbl.grid()
# TODO: Download Image Button
dwnldImgBtn = Button(bottom_right_frame, text="Download Image")
dwnldImgBtn.grid(row=1, column=1, pady=10)
root.mainloop()