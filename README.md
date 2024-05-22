# Overview  
API which automatically posts images from a local pc into a miro board.  
### e.g. scanning a document  
![scan](https://github.com/billyshub/Miro-Scanner-API/assets/64965899/bfd40bba-3b95-4ded-9aef-58332eeb1850)  
### e.g. sending an image from third party tools  
![picture](https://github.com/billyshub/Miro-Scanner-API/assets/64965899/60afd1e7-88c6-4c90-8205-bd5afb59ed07)  
    
# Operation
1. Ensure you have developer access in your miro subscription and have generated a permanent bearer token.  
2. Create a config.ini file in root directory and define miro api bearer token and board url to upload to.  
```
[Tokens]
bearer_token = XXXXXXXXXXXXXXXXXXXXXXXXXXXX
miro_url = https://miro.com/app/board/YYYYYYYYYY/ 
```
2. Set the folder in which should be monitored for new images in the python file.  
```
def main():
    # Folder to scan for new files
    folder_paths = [os.getcwd(), r"XXXX\XXXX\XXXX"]
```
3. Run the python script.  
4. Miro will automatically launch with referenced board.  
5. Python script will run in the background and scan the specified folder for any new images.  
6. Once an image is detected in this folder, it will push the image via api to the selected miro board.  
7. Image locally will automatically be deleted.  
8. Python script will continue to montior for images.  

# Context of files
`miro.py` contains the api  
`new item.mp3` is the nosie played when a new item is found  
`run.bat` is a bat file to start the python script, used for desktop shortcus to start the script  
`config.ini` is hidden via .gitignore but cotains the api secrets  
