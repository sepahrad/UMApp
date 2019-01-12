import subprocess
import hashlib
import logger
import sys
import os
import requests
import tkinter as tk
from tkinter import messagebox
import json

def HDSerialFetcher():

    # wmic DISKDRIVE where 'MediaType like "Fixed%"' get SerialNumber
    try:
        CREATE_NO_WINDOW = 0x08000000
        hardDriver = subprocess.run(['wmic', 'DISKDRIVE', 'where', 'MediaType like "Fixed%"', 'get', 'SerialNumber'], shell=False, creationflags=CREATE_NO_WINDOW, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    except:
        logger.log.critical("Could not execute wmic.")
        messagebox.showerror("!خطا", ".خطا در اجرای برنامه لایسنس")
        sys.exit(1)

    hardDriverList = hardDriver.stdout
    hardDriverList = hardDriverList.split('\n')[1:len(hardDriverList)]
    hardDriverList = list(filter(None, hardDriverList))

    listHardDrive = []
    for key in hardDriverList:
        value=key.strip(' ')
        listHardDrive.append(value)

    hardDriverList=listHardDrive

    hdSerialNum = ""
    for key in hardDriverList:
        hdSerialNum = key + ':' + hdSerialNum

    return hdSerialNum

def SerialCreator(serialNum):
    
    privateSerialNum = serialNum + 'UCClient' + 'c1c75ca61f91ceb1f2f836780d7f7c08b2867e9d'
    hashSerialNum = hashlib.sha1(privateSerialNum.encode('utf-8')).hexdigest()

    return hashSerialNum

def SerialSaver(key):
    try:
        with open('uc.key', 'w') as f:
            f.write(key)
        return True
    except:
        logger.log.critical("Can't save key to uc.key")
        messagebox.showerror("!خطا", ".خطا در بارگذاری لایسنس")
        sys.exit(1)

def SerialLoader():
    try:
        with open('uc.key', 'r') as f:
            serialNum = f.read()
        return serialNum
    except:
        logger.log.critical("Can't load key from uc.key")
        messagebox.showerror("!خطا", ".خطا در بارگذاری لایسنس")
        sys.exit(1)

def SerialExists():
    if not ( os.path.isfile('uc.key') ) or ( os.path.getsize('uc.key') == 0 ):
        return False
    else:
        return True

def Licensing():

    root = tk.Tk()
    root.iconbitmap('assets/icon/icon.ico')
    root.title("نرم افزار مدیریت اثر انگشت")
    root.geometry("270x100")
    root.resizable(0, 0)
    tk.Label(root, text="شماره سریال:", padx=10, pady=10).grid(row=0, column=0, padx=5, pady=5)
    userEntry = tk.StringVar()
    entry = tk.Entry(root, textvariable=userEntry, width=25).grid(row=0, column=1)
    tk.Button(root, text="اعمال", width=10, command=lambda: ApplyLicense(userEntry)).grid(row=1, column=0, padx=5, pady=5)

    if SerialExists():
        if not SerialLoader() == SerialCreator(HDSerialFetcher()):
            messagebox.showerror("!خطا", ".شماره سریال نرم افزار نامعتبر می باشد\n.دوباره تلاش کنید")

    def ApplyLicense(serialNum):
        hdSerialNum = HDSerialFetcher()

        data = {'serialNum' : serialNum.get(), 'HDSerial' : hdSerialNum}
        
        try:
            result = requests.post('http://www.daftardaran.ir/ucserialnumber', data=data)
            if result.text == "True":
                SerialSaver(SerialCreator(HDSerialFetcher()))
                messagebox.showinfo("!موفق", ".سریال با موفقیت نصب شد\n.برنامه را مجددا اجرا کنید ")
                root.destroy()
            elif result.text == "False":
                messagebox.showerror("!خطا", ".سریال اشتباه است")
            elif result.text == "Locked":
                messagebox.showerror("!خطا", "سریال قبلا توسط دستگاه دیگری ثبت شده است.\n .با پشتیبانی تماس بگیرید")
            elif result.status_code != 200:
                messagebox.showerror("!خطا", "!خطا از سمت سرور\n.با پشتیبانی تماس بگیرید")
        except:
            messagebox.showerror("!خطا", ".عدم ارتباط با سرور")

    root.mainloop()

    