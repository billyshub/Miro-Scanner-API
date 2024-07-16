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
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self):
        # Initialize pygame mixer for playing sounds
        pygame.mixer.init()
        # Load the mp3 file for playback
        self.mp3_file = os.path.join(os.getcwd(), "new item.mp3")
        # Read configuration and set up session
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.bearer_token = self.config['Tokens']['bearer_token']
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.bearer_token}'})
        self.boardcode = self.config['Tokens']['miro_url'].rsplit('/', 2)[1]
        self.url = f"https://api.miro.com/v2/boards/{self.boardcode}/images"
        self.payload = {
            "data": {
                "title": "title for the image",
                "position": {"x": 100, "y": 200, "origin": "center"},
                "geometry": {"width": 100, "height": 100, "rotation": 0}
            }
        }

    def on_created(self, event):
        # Check if the event corresponds to a new file creation in a directory
        if event.is_directory or not event.src_path.lower().endswith(".jpg"):
            return
        threading.Thread(target=self.process_file, args=(event.src_path,)).start()

    def process_file(self, file_path):
        print("New JPG file was detected:", file_path)

        # Retry opening the file with a short delay in case of PermissionError
        max_retries = 3
        for _ in range(max_retries):
            try:
                # Read the file content and store it in a variable
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                break
            except PermissionError:
                time.sleep(0.1)  # Adjust the delay as needed
        else:
            print(f"Failed to open the file: {file_path}")
            return

        # Create a tuple containing the file content and metadata needed for the API request
        files = [('resource', (os.path.basename(file_path), file_content, 'image/jpg'))]
        start_time = time.time()
        
        try:
            response = self.session.post(self.url, json=self.payload, files=files, timeout=5)
            response.raise_for_status()  # Ensure we catch HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return

        print(f"Request time: {time.time() - start_time} seconds")
        print(response.text)

        # Verify the image was imported successfully
        if "type" in response.json() and response.json()["type"] == "image":
            # Delete the image after a successful import
            self.del_image(file_path)

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
            print(f"Failed to delete image: {str(e)}")

def add_watch_folder(observer, event_handler, folder_path):
    observer.schedule(event_handler, folder_path, recursive=False)

def main():
    # Folder to scan for new files
    folder_paths = [os.getcwd(), r"..\VCBportable\VCBconfig\tempsend"]

    # Create the main application window
    root = tk.Tk()

    # Obtain the miro board url
    config = configparser.ConfigParser()
    config.read('config.ini')
    global miro_input
    miro_input = config['Tokens']['miro_url']

    # Close the main application window
    root.destroy()

    # Open miro then open the board input
    os.startfile(os.getenv('LOCALAPPDATA') + r'\Programs\RealtimeBoard\Miro.exe')
    urlsplit = miro_input.split('://')[1]  # Extract everything after '://'
    time.sleep(5)  # Give os time to load miro before opening board url
    os.system(f'start "" miroapp://{urlsplit}')  # Access board url

    event_handler = FileHandler()

    # Add watch folders
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
