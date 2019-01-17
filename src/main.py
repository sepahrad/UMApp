import maingui
import logger
import serialmanager
import subprocess
import os
import sys

try:
    CREATE_NO_WINDOW = 0x08000000
    subprocess.run(['assets/exe/devcon.exe', 'enable', 'usb*'], shell=False, creationflags=CREATE_NO_WINDOW, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    logger.log.info("All devices enabled at main when program started.")
except:
    logger.log.critical("Could not execute devcon at main.")
    sys.exit(1)

if __name__ == "__main__":

    if serialmanager.SerialExists():
        if serialmanager.SerialLoader() == serialmanager.SerialCreator(serialmanager.HDSerialFetcher()):
            maingui.MainGui()
        else:
            serialmanager.Licensing()
    else:
        serialmanager.Licensing()

try:
    CREATE_NO_WINDOW = 0x08000000
    subprocess.run(['assets/exe/devcon.exe', 'enable', 'usb*'], shell=False, creationflags=CREATE_NO_WINDOW, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    logger.log.info("All devices enabled at main when program killed.")
except:
    logger.log.critical("Could not execute devcon at main.")
    sys.exit(1)