'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
# Import statements
import requests
import json
from apod_desktop import get_apod_date

# Constants
# APOD's URL
APOD_URL = 'https://api.nasa.gov/planetary/apod'
# API Key
API_KEY = 'U7HLRY5ArCpjWIorpQN3fx4INNzCpVXkuNv4jYgw'

# Main Function
def main():
    # TODO: Add code to test the functions in this module.
    
    # Get the date for the APOD
    date = get_apod_date()
    
    # Get the APOD info
    get_apod_info(date)
    


def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    # TODO: Complete the function body
    # Hint: The APOD API uses query string parameters: https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
    # Hint: Set the 'thumbs' parameter to True so the info returned for video APODs will include URL of the video thumbnail image 
    
    # Set parameters
    params = {'date': apod_date, 'thumbs': True, 'api_key': API_KEY}
    
    # Resp message
    respMsg = requests.get(APOD_URL, params=params)
    
    # Update user
    print(f"Getting {apod_date} APOD information from NASA...", end="")
    
    # Check if successful
    if respMsg.status_code == requests.codes.ok:
        # Tell user it was a success
        print(f"success")
        
        # Convert to a dictionary
        dictAPOD = json.loads(respMsg.content)
        
        # Get title and print it
        title = dictAPOD["title"].title()
        
        print(f"APOD Title: {title}")

        # Return dictionary
        return dictAPOD
    
    # Else statement
    else:
        # Tell user it was a failure
        print(f"failure")
        
        # Notify user what the reason was
        print(f"{respMsg.status_code} {respMsg.reason} {respMsg.text}")
    
        # Return None
        return None

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """

    # Check if the APOD is an image

    date = get_apod_date()  
    apod_info_dict = get_apod_info(date)
    # If it is an image, get the URL of the high definition image
    if apod_info_dict['media_type'] == 'image':
        return apod_info_dict['hdurl']
    # If it is a video, get the URL of the video thumbnail
    else:
        return apod_info_dict['thumbnail_url']
    

if __name__ == '__main__':
    main()