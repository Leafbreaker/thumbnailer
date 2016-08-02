import os
import subprocess

pathToDirectory = subprocess.check_output('echo %cd%\\', shell=True).strip()
print pathToDirectory

for root, dirs , files in os.walk(pathToDirectory, topdown=False):
        for name in dirs:
            print name