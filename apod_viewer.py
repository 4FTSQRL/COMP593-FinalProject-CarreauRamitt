from tkinter import *
from tkinter import ttk
#import apod_desktop

# Initialize the image cache
#apod_desktop.init_apod_cache()

# TODO: Create the GUI
root = Tk()
root.title("APOD Viewer")
root.geometry('600x400')

#Creating frames for the GUI


#frame for image (top frame)
image_frame = ttk.Frame(root)
image_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="N")\
#top fram widget


#frame for title and date (middle frame)
middle_frame = LabelFrame(root, text="", padx=10, pady=10) #This will need to be pulled from the API
middle_frame.grid(row=0, column=2, padx=10, pady=10)

#frame for cached image and set button (bottom left frame)
bottom_left_frame = LabelFrame(root, text="View Cached Image", padx=10, pady=10)
bottom_left_frame.grid(row=1, column=0, padx=10, pady=10)

#frame for date entry and get download image button (bottom right frame)
bottom_right_frame = LabelFrame(root, text="Get More Images", padx=10, pady=10)
bottom_right_frame.grid(row=1, column=1, padx=10, pady=10)



root.mainloop()