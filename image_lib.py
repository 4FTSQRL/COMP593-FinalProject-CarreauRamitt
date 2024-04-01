'''
Library of useful functions for working with images.
'''
# Import statements
    # Requests
import requests
    # ctypes
import ctypes
# Import apod_api
import apod_api
import apod_desktop
# Import base64
import base64

def main():
    # TODO: Add code to test the functions in this module
    date = apod_desktop.get_apod_date()
    info = apod_api.get_apod_info(date)
    url = apod_api.get_apod_image_url(info)
    bind = download_image(url)
    save_image_file(bind, "APODPic.jpg")
    set_desktop_background_image(bind)
    return

def download_image(image_url):
    """Downloads an image from a specified URL.

    DOES NOT SAVE THE IMAGE FILE TO DISK.

    Args:
        image_url (str): URL of image

    Returns:
        binData (bytes): Binary image data, if succcessful. None, if unsuccessful.
    """
    # TODO: Complete function body
    # Get the requests for the url
    resp = requests.get(image_url)
    
    # Check if it succeeded
    if resp.status_code == requests.codes.ok:
        # Get the binary data
        binData = resp.content
        # Return the binary data
        return binData
    
    # Check if failed
    else:
        # Return none
        return None

def save_image_file(image_data, image_path):
    """Saves image data as a file on disk.
    
    DOES NOT DOWNLOAD THE IMAGE.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        bool: True, if succcessful. False, if unsuccessful
    """
    # TODO: Complete function body
    # Open the file
    with open(image_path, "wb") as f:
        # Write
        f.write(image_data)
        # Return true
        return True
    # Return false if failed
    return False

def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        bytes: True, if succcessful. False, if unsuccessful        
    """
    # TODO: Complete function body
    # Try and except
    try:
        # Set the desktop background pic
        ctypes.windll.user32.SystemParametersInfo(20, 0, image_path, 0)
        # Return true
        return True
    # Except Statement
    except:
        return False

def scale_image(image_size, max_size=(800, 600)):
    """Calculates the dimensions of an image scaled to a maximum width
    and/or height while maintaining the aspect ratio  

    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height) 
        max_size (tuple[int, int], optional): Maximum image size in pixels (width, height). Defaults to (800, 600).

    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height)
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    # NOTE: This function is only needed to support the APOD viewer GUI
    resize_ratio = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_size = (int(image_size[0] * resize_ratio), int(image_size[1] * resize_ratio))
    return new_size

if __name__ == '__main__':
    main()