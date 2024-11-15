import subprocess
import os

params = ["python", f"{os.path.dirname(__file__)}\\test1.py"]
proc = subprocess.Popen(params, env=os.environ.copy(), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, bufsize=1)
while (line := proc.stdout.readline()) != "":
    print(line)