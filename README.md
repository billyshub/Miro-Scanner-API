Overview:  
API which automatically posts images from a local pc into a miro board.  
e.g. scanning a document  
[.gif]  
e.g. sending an image  
[.gif]  

Operation:  
Set miro_input as a miro url and run the python script.  
Miro will automatically launch with referenced board.  
Python script will run in the background and scan the tempsend folder for images.  
Once an image is detected in this folder, it will push the image via api to the selected miro board.  
Image locally will automatically be deleted.
Python script will continue to montiro for images.