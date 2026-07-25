import subprocess
import os

directory = "/Drive-D/04-Projects/New_Projects/Web_Projects/notepad/"
os.chdir(directory)
subprocess.call(
    [". {}/.venv/bin/activate && flask run -p 5002".format(directory)], shell=True
)
