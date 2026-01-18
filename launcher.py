import subprocess
import sys
import os

os.chdir(r"d:\Program-item\GitHub-submit-folder\UselessBrowser")
python_path = r"d:\Program-item\GitHub-submit-folder\UselessBrowser\.venv\Scripts\python.exe"
script_path = r"d:\Program-item\GitHub-submit-folder\UselessBrowser\main.py"

subprocess.Popen([python_path, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
print("应用程序已启动!")
