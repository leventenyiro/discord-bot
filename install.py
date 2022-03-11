import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

with open('requirements.txt') as f:
    lines = [line.rstrip('\n') for line in f]
    for module in lines:
        install(module)
