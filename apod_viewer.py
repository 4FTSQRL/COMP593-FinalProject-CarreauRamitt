# Import apod_desktop   
import apod_desktop

from tkinter import *
from tkinter import ttk
import ctypes
# pillow
from PIL import Image, ImageTk
# tkcalendar
from tkcalendar import Calendar


# Initialize the image cache
apod_desktop.init_apod_cache()

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

#top frame widget


#frame for title and date (middle frame)
# middle_frame = LabelFrame(root, text="") #This will need to be pulled from the API
# middle_frame.grid(row=1, column=0)

#frame for cached image and set button (bottom left frame)
bottom_left_frame = LabelFrame(root, text="View Cached Image")
bottom_left_frame.grid(row=1, column=0, padx=10)

#frame for date entry and get download image button (bottom right frame)
bottom_right_frame = LabelFrame(root, text="Get More Images")
bottom_right_frame.grid(row=1, column=1, padx=10)

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
selImgcmbx.grid(padx=(10,3))
# TODO: Set as Desktop button
setDskBtn = Button(bottom_left_frame, text="Set as Desktop")
setDskBtn.grid(row=1,column=1, padx=10, pady=3)

# TODO: Select Date Label
selDateLbl = Label(bottom_right_frame, text="Select Date:")
selDateLbl.grid()

# TODO: Calendar Date Picker combobox
cal = Calendar(bottom_right_frame, selectmode = 'day', year=1995, month=6, day=16)
cal.grid(padx=(10,3))

#Create dropdown menu that calendar will populate
date = cal.get_date()
print(date)

#create event for date selection
def get_date():
    date = cal.get_date()
    print(date)
    return date

#show image preview in top frame when date is selected
def show_image():
    date = get_date()
    apod_info = apod_desktop.get_apod_info(date)
    image_url = apod_info["url"]
    image_data = apod_desktop.get_apod_image(image_url)
    apod_desktop.save_image_file(image_data, "apod.jpg")
    openIMG = Image.open("apod.jpg")
    img = ImageTk.PhotoImage(openIMG)
    imgLbl = Label(image_frame, image=img)
    imgLbl.grid()
    return img

# TODO: Download Image Button
dwnldImgBtn = Button(bottom_right_frame, text="Download Image")
dwnldImgBtn.grid(row=1, column=1, pady=10)


root.mainloop()