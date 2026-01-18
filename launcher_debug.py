import subprocess
import sys
import os
import traceback

os.chdir(r"d:\Program-item\GitHub-submit-folder\UselessBrowser")
python_path = r"d:\Program-item\GitHub-submit-folder\UselessBrowser\.venv\Scripts\python.exe"
script_path = r"d:\Program-item\GitHub-submit-folder\UselessBrowser\main.py"

try:
    process = subprocess.Popen(
        [python_path, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    print("应用程序已启动!")
    print(f"PID: {process.pid}")
except Exception as e:
    print(f"启动失败: {e}")
    traceback.print_exc()
