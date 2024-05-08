# Requirements
# pygame==2.5.0
# Requests==2.31.0
# watchdog==3.0.0

import tkinter as tk
import os
import time
import requests
import pygame
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self):
        # Initialize pygame mixer for playing sounds
        pygame.mixer.init()
        # Load the mp3 file for playback
        self.mp3_file = os.getcwd() + "/new item.mp3"

    def on_created(self, event):
        # Check if the event corresponds to a new file creation in a directory
        if event.is_directory:
            return
        # Check if the created file has a .jpg extension
        if event.src_path.lower().endswith(".jpg"):
            print("New JPG file was detected:", event.src_path)

            # strip board ID from regular board URL and convert to API URL
            self.boardcode = miro_input.rsplit('/', 2)[1] 
            url = "https://api.miro.com/v2/boards/" + self.boardcode + "/images"
            
            payload = {"data": {
                "title": "title for the image",
                "position": {
                    "x": 100,
                    "y": 200,
                    "origin": "center"
                },
                "geometry": {
                    "width": 100,
                    "height": 100,
                    "rotation": 0
                }
            }}

            # Retry opening the file with a short delay in case of PermissionError
            max_retries = 3
            retries = 0
            while retries < max_retries:
                try:
                    # Read the file content and store it in a variable
                    with open(event.src_path, 'rb') as file:
                        file_content = file.read()
                    break
                except PermissionError:
                    retries += 1
                    time.sleep(0.1)  # Adjust the delay as needed

            # If the file is still locked after retries, give up on processing it
            if retries == max_retries:
                print(f"Failed to open the file: {event.src_path}")
                return

            #store miro api bearer token in a separate ini file
            config = configparser.ConfigParser()
            config.read('config.ini')

            bearer_token = config['Tokens']['bearer_token']
            
            headers = {
                'Authorization': f'Bearer {bearer_token}',
            }  # token for miro dev app

            # Create a tuple containing the file content and metadata needed for the API request
            files = [('resource', (os.path.basename(event.src_path), file_content, 'image/jpg'))]
            global response
            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print(response.text)

        # Verify the image was imported successfully
        if "type" in response.json() and response.json()["type"] == "image":
            # Delete the image after a successful import
            self.del_image(event.src_path)

        # Play the mp3 file upon successful import with a delay
        time.sleep(2)  # Adjust the delay as needed
        self.play_mp3()

    def play_mp3(self):
        try:
            pygame.mixer.music.load(self.mp3_file)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Failed to play the mp3 file: {str(e)}")

    def del_image(self, image_path):
        image_name = os.path.basename(image_path)

        try:
            # Delete the original file after uploading
            os.remove(image_path)
            print(f"Scanned Image uploaded successfully")
        except Exception as e:
            print(f"VCB Image uploaded sucessfully")

def add_watch_folder(observer, event_handler, folder_path):
    observer.schedule(event_handler, folder_path, recursive=False)

def main():
    # Folder to scan for new files
    folder_paths = [os.getcwd(), r"..\VCBportable\VCBconfig\tempsend"]

    # Create the main application window
    root = tk.Tk()

    # Obtain the miro board url
    global miro_input
    miro_input = 'https://miro.com/app/board/uXjVNUiYfUw=/'

    # Close the main application window
    root.destroy()

    #open miro then open the board input
    os.startfile(os.getenv('LOCALAPPDATA') + r'\Programs\RealtimeBoard\Miro.exe')
    urlsplit = miro_input.split('://')[1]  # Extract everything after '://'
    time.sleep(5) #give os time to load miro before opening board url
    os.system(f'start "" miroapp://{urlsplit}')  # Access board url

    event_handler = FileHandler()

    # add watch folders
    observer = Observer()

    for folder_path in folder_paths:
        add_watch_folder(observer, event_handler, folder_path)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()