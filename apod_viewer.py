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
image_frame = ttk.Frame(root)
image_frame.grid(row=0, column=0, padx=20, pady=20)
#top fram widget


#frame for title and date (middle frame)
middle_frame = LabelFrame(root, text="", padx=10, pady=10) #This will need to be pulled from the API
middle_frame.grid(row=1, column=0, padx=10, pady=10)

#frame for cached image and set button (bottom left frame)
bottom_left_frame = LabelFrame(root, text="View Cached Image", padx=10, pady=10)
bottom_left_frame.grid(row=2, column=0, padx=10, pady=10)

#frame for date entry and get download image button (bottom right frame)
bottom_right_frame = LabelFrame(root, text="Get More Images", padx=10, pady=10)
bottom_right_frame.grid(row=2, column=1, padx=10, pady=10)

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
root.mainloop()