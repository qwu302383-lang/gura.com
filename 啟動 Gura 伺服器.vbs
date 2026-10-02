Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\ella2\OneDrive\桌面\吳奕璿的"
WshShell.Run """C:\Users\ella2\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe"" run_server.py --open-browser", 0, False
