# Overview:  
API which automatically posts images from a local pc into a miro board.  
### e.g. scanning a document  
![scan](https://github.com/billyshub/Miro-Scanner-API/assets/64965899/bfd40bba-3b95-4ded-9aef-58332eeb1850)  
### e.g. sending an image  
![picture](https://github.com/billyshub/Miro-Scanner-API/assets/64965899/60afd1e7-88c6-4c90-8205-bd5afb59ed07)  
    
# Operation:  
1. Set miro_input as a miro url and run the python script.
2. Miro will automatically launch with referenced board.
3. Python script will run in the background and scan the tempsend folder for images.
4. Once an image is detected in this folder, it will push the image via api to the selected miro board.
5. Image locally will automatically be deleted.  
6. Python script will continue to montior for images.
