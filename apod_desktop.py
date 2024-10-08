""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
  
Students: Elicia Ramitt, Jesse Carreau
"""

# Import Statements
    # date from datetime
from datetime import date

    # os
import os
    
    # image_lib
import image_lib

    #argv
from sys import argv

    # Import SQLite
import sqlite3

    # Import regex
import re
    # Get apod info url
import apod_api

    # requests
import requests

    # Hashlib
import hashlib
# Full paths of the image cache folder and database
# - The image cache directory is a subdirectory of the specified parent directory.
# - The image cache database is a sqlite database located in the image cache directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')
image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()

    # Initialize the image cache
    init_apod_cache()
    
    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)
    
    # Get the information for the APOD from the DB
    apod_info = apod_api.get_apod_info(apod_date)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(determine_apod_file_path(apod_info['title'], apod_info['url']))
        
    # test get all titles
    get_all_apod_titles()

def get_apod_date():
    """Gets the APOD date
    s
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    today_date = date.today()
    apod_start_date = date(1995, 6, 16)  
    # get date from command line
    if len(argv) > 1:
        apod_date = argv[1]
        #if date is provided, validate it
        if apod_date is not None:
            try:
                # try to convert the date to a date object
                apod_date = date.fromisoformat(apod_date)
        
                   #check if date is prior to june 16th 1995, and if it is, use today's date
                if apod_date < apod_start_date or apod_date > today_date:
           
                     print("The APOD date must be between June 16th 1995, and today. Today's date will be used instead.")
                     apod_date = today_date
                
            except ValueError:
                # if invalid date, use today's date
                print("Invalid date. Please provide a date in the format YYYY-MM-DD. Today's date will be used instead.")
                apod_date = today_date
    
                exit()
    # Set apod_date to today's date
    else:
        apod_date = today_date
    return apod_date
     

def init_apod_cache():
    """Initializes the image cache by:
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    """
    # TODO: Create the image cache directory if it does not already exist
    # Tell user where it is
    print(f"Image cache directory: {image_cache_dir}")
    # Check if it exists
    if not os.path.exists(image_cache_dir):
        # Create image cache directory
        os.makedirs(image_cache_dir)
        # Tell user the script is creating the directory
        print(f"Image cache directory created.")
    # Else let user know
    else:
        print(f"Image cache directory exists.")
        
    # TODO: Create the DB if it does not already exist
    # Tell user where it is
    print(f"Image cache DB: {image_cache_db}")
    # Check if it exists
    if not os.path.isfile(image_cache_db):
        # Creating database update foer user
        print("Image cache DB created.")
        # Create the database
        con = sqlite3.connect(image_cache_db)
        cur = con.cursor()
        # query
        query = """
        CREATE TABLE IF NOT EXISTS apod
        (
            id  INTEGER PRIMARY KEY,
            title   TEXT NOT NULL,
            explanation TEXT NOT NULL,
            file_path   TEXT NOT NULL,
            sha256  TEXT NOT NULL
        )
        """
        # Excute
        cur.execute(query)
        # Close it up
        con.close()
    # If it already exists tell user
    else:
        print(f"Image cache DB exists.")
    return

def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())
    # TODO: Download the APOD information from the NASA API
 
 
    # Get the info
    apod_info = apod_api.get_apod_info(apod_date)
    # Hint: Use a function from image_lib.py 
    apod_image = image_lib.download_image(apod_api.get_apod_image_url(apod_info))

    # GET message
    respMsg = requests.get(apod_api.get_apod_image_url(apod_info))
    
    # Check if download was successful
    if respMsg.status_code == requests.codes.ok:
        # Extract binary data
        content = respMsg.content
        # Hash
        hashValue = hashlib.sha256(content).hexdigest()
    # Hint: Use the get_apod_id_from_db() function below
    # Compare the hash value
    apod_id = get_apod_id_from_db(hashValue)
    # If the APOD does not exist in the cache, add it
    if apod_id == 0:
        #Use the determine_apod_file_path() function below to determine the image file path
        image_path = determine_apod_file_path(apod_info['title'], apod_info['url'])
        # Add APOD to Cache
        apod_id = add_apod_to_db(apod_info['title'], apod_info['explanation'], image_path, hashValue)
        #Use a function from image_lib.py to save the image file
        image_lib.save_image_file(apod_image, image_path)


        # Hint: Use the add_apod_to_db() function below
        add_apod_to_cache(apod_date)
        
        return apod_id
    
    # If apod exists
    elif apod_id != 0:
        # Return the id
        return apod_id
    return 0

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful. Zero, if unsuccessful       
    """


    # Connect to the database
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()

    # Insert the APOD information into the DB
    cur.execute("INSERT INTO apod (title, explanation, file_path, sha256) VALUES (?, ?, ?, ?)", (title, explanation, file_path, sha256))
    # Commit the changes
    con.commit()

    return 0 

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
   
    # Connect to the database
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    # Get the record ID of the APOD in the cache
    cur.execute("SELECT id FROM apod WHERE sha256 = ?", (image_sha256,))
    # Fetch the record ID
    apod_id = cur.fetchone()
    # Close the connection
    con.close()
    # Return the record ID
    if apod_id is not None:
        return apod_id[0]  
    
    else:
        return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # regex pattern
    regex_pattern = r"[^a-zA-Z0-9\s]"

    #Strip down and reassamble to create file name/path

    #file extension
    file_extension = image_url.split('.')[-1]

    #file name
    file_name = image_title.strip().replace(" ", "_")

    #use regex to remove unwanted characters
    file_name = re.sub(regex_pattern, "", file_name)
 
    #full path
    file_path = os.path.join(image_cache_dir, f"{file_name}.{file_extension}")


    return file_path
    

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    #connect and cursor
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    #query 

    """Get_apod_info_query = {
        'title': 'Title',
        'explanation': 'Explanation',
        'file_path': 'File Path',
        'sha256': 'SHA-256'
    }"""
    Get_apod_info_query = """
    CREATE TABLE IF NOT EXISTS apod
    (
        id      INTEGER PRIMARY KEY,
        title   TEXT NOT NULL,
        explanation TEXT NOT NULL,
        file_path   TEXT NOT NULL,
        sha256  TEXT NOT NULL
    )
    """
    #execute the query
    cur.execute(Get_apod_info_query)

    # fetch the APOD information
    apod_info = cur.fetchall()

    #close the connection
    con.close()

    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # get list of all titles in image cache 
    # Connect to the database
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    # Get the titles
    cur.execute("SELECT title FROM apod")
    # Fetch the titles
    titles = cur.fetchall()
    # Close the connection
    con.close()
    
    # Return Statement
    return titles


if __name__ == '__main__':
    main()