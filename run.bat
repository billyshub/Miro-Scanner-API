@echo off
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
"%LocalAppData%\Programs\Python\Python312\python.exe" ".\miro.py"
exit