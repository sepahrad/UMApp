import subprocess
import json
import os
import logger
import sys
from tkinter import messagebox


def UsbDictFetcher():
    # Fetches the list of all USB devices:
    try:
        CREATE_NO_WINDOW = 0x08000000
        usbDevies = subprocess.run(['assets/exe/devcon.exe', 'hwids', 'usb*'], shell=False, creationflags=CREATE_NO_WINDOW, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    except:
        logger.log.critical("Could not execute devcon")
        messagebox.showerror("!خطا", ".خطا در اجرای برنامه اصلی")
        sys.exit(1)

    usbDevStdOut = usbDevies.stdout
    usbDevStdOut = usbDevStdOut.split('\n')
    usbDevStdOut = usbDevStdOut[0:len(usbDevStdOut) - 2]

    # Fetches the HWID of USB devices
    deviceList = []
    for i in usbDevStdOut:
        if not ' ' in i:
            deviceList.append(i)

    # Fetches the name of HWID
    usbDevDict = {}
    for key in deviceList:
        try:
            CREATE_NO_WINDOW = 0x08000000
            result = subprocess.run(['assets/exe/devcon.exe', 'hwids', "@" + key], shell=False, creationflags=CREATE_NO_WINDOW, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        except:
            logger.log.critical("Could not execute devcon")
            messagebox.showerror("!خطا", ".خطا در اجرای برنامه اصلی")
            sys.exit(1)
            
        usbDevNameStdOut = result.stdout
        usbDevNameStdOut = usbDevNameStdOut.split('\n')
        usbDevName = usbDevNameStdOut[1]
        usbDevName = usbDevName.split(':')
        usbDevName = usbDevName[len(usbDevName) - 1].lstrip()

        usbDevDict[key] = usbDevName
    
    return usbDevDict

def UsbListFetcher():
    dictUsb = UsbDictFetcher()
    usbList = []

    for key in dictUsb:
        usbList.append(key + " : " + dictUsb.get(key , "No Name"))

    return usbList

def UsbFileSaver(dictDev):
    try:
        with open('config/DevMap.json', 'w') as f:
            f.write(json.dumps(dictDev))
        return True
    except:
        logger.log.critical("Can't save settings to DevMap.json")
        return False

def UsbFileLoader():
    if not ( os.path.isfile('config/DevMap.json') ) or ( os.path.getsize('config/DevMap.json') == 0 ):
        UsbFileSaver({"SarDaftar": "None", "ArbabRojoo": "None"})

    dictDev = {}
    try:
        with open('config/DevMap.json', 'r') as f:
            dictDev = json.loads(f.read())
            return dictDev
    except:
        logger.log.critical("Could not load settings from DevMap.json")
        messagebox.showerror("!خطا", ".خطا در بارگذاری تنظیمات")
        sys.exit(1)

def executor(mode, address):
    try:
        CREATE_NO_WINDOW = 0x08000000
        devExec = subprocess.run(['assets/exe/devcon.exe', mode, "@" + address], shell=False, creationflags=CREATE_NO_WINDOW, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        logger.log.info(devExec.stdout)
    except:
        logger.log.critical("Could not execute devcon")
        messagebox.showerror("!خطا", ".خطا در اجرای برنامه اصلی")
        sys.exit(1)