import time
import tkinter as tk
from tkinter import messagebox
import core

class MainGui:
    def __init__(self):
        self.__root = None
        self.__frame = None
        self.__btnSarDaftar = None
        self.__btnArbabRojoo = None
        self.__lblSeconds = None
        self.__varSarDaftar = None
        self.__varArbabRojoo = None
        self.__lblApplyDev = None

        self.__InitMainGui().__Binder().StartGui()

    def __InitMainGui(self):
        self.__root = tk.Tk()
        self.__root.iconbitmap('assets/icon/icon.ico')
        self.__root.title("نرم افزار مدیریت اثر انگشت")
        self.__root.geometry("250x125")
        self.__root.resizable(0, 0)

        self.__frame = tk.Frame(self.__root)
        self.__frame.pack(fill=tk.BOTH, expand=True)
        self.__frame.pack_propagate(0)

        self.__btnSarDaftar = tk.Button(self.__frame, width=25, text="سر دفتر", fg="black", bg="gray")
        self.__btnSarDaftar.pack(padx=10, pady=5)

        self.__btnArbabRojoo = tk.Button(self.__frame, width=25, name="btnArbabRojoo", text="ارباب رجوع", fg="black", bg="gray")
        self.__btnArbabRojoo.pack(padx=10, pady=5)

        self.__lblSeconds = tk.Label(self.__frame)
        self.__lblSeconds.pack(padx=10, pady=5)

        topMenu = tk.Menu(self.__root)
        self.__root.config(menu=topMenu)
        settingMenu = tk.Menu(topMenu, tearoff=0)
        topMenu.add_cascade(label="فایل", menu=settingMenu)
        
        settingMenu.add_command(label="تنظیمات", command=self.__InitSettingGui)
        settingMenu.add_command(label="درباره ما", command=self.__AboutUs)
        settingMenu.add_command(label="خروج", command=self.__root.destroy)

        return self

    def __InitSettingGui(self):
        root = tk.Tk()
        root.iconbitmap('assets/icon/icon.ico')
        root.title("تنظیمات")
        root.geometry("550x140")
        root.resizable(0, 0)
        
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.pack_propagate(0)
        
        lblSarDaftar = tk.Label(frame, text="دستگاه اثر انگشت سر دفتر")
        lblSarDaftar.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        lblArbabRojoo = tk.Label(frame, text="دستگاه اثر انگشت ارباب رجوع")
        lblArbabRojoo.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        dictDev = core.UsbFileLoader()
        usbList = core.UsbListFetcher()
        usbDict = core.UsbDictFetcher()

        self.__varSarDaftar = tk.StringVar(frame)

        if dictDev["SarDaftar"] == "None":
            self.__varSarDaftar.set(dictDev["SarDaftar"])
        else:
            self.__varSarDaftar.set(dictDev["SarDaftar"] + " : " + usbDict.get(dictDev["SarDaftar"], "Not Exists!"))

        omSarDaftar = tk.OptionMenu(frame, self.__varSarDaftar, "None", *usbList)
        omSarDaftar.grid(row=0, column=1, sticky="w")

        self.__varArbabRojoo = tk.StringVar(frame)

        if dictDev["ArbabRojoo"] == "None":
            self.__varArbabRojoo.set(dictDev["ArbabRojoo"])
        else:
            self.__varArbabRojoo.set(dictDev["ArbabRojoo"] + " : " + usbDict.get(dictDev["ArbabRojoo"], "Not Exists!"))

        omArbabRojoo = tk.OptionMenu(frame, self.__varArbabRojoo, "None", *usbList)
        omArbabRojoo.grid(row=1, column=1, sticky="w")

        btnApply = tk.Button(frame, text="اعمال", width=10, command=self.__DevApply)
        btnApply.grid(row=2, column=0, padx=10, sticky="w")

        self.__lblApplyDev = tk.Label(frame)
        self.__lblApplyDev.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        root.mainloop()

    def __DevApply(self):
        
        if self.__varSarDaftar.get() == "None":
            sdDevAdd = "None"
        else:
            sdDevAdd = self.__varSarDaftar.get().split(':')[0].rstrip()

        if self.__varArbabRojoo.get() == "None":
            arDevAdd = "None"
        else:
            arDevAdd = self.__varArbabRojoo.get().split(':')[0].rstrip()

        dictDev = {}
        dictDev["SarDaftar"] = sdDevAdd
        dictDev["ArbabRojoo"] = arDevAdd

        result = core.UsbFileSaver(dictDev)
        if result:
            self.__lblApplyDev.config(text=".تنظیمات با موفقیت اعمال شد")
        else:
            self.__lblApplyDev.config(text="!خطا در اعمال تنظیمات")

    def __ChangeUsb(self, event, caller):
        devDict = core.UsbFileLoader()
        
        if ( devDict["SarDaftar"] == "None" ) or ( devDict["ArbabRojoo"] == "None" ):
            messagebox.showerror("!خطا", ".کلید ها تنظیم نشده اند")
        else:
            self.__lblSeconds.pack()

            if caller == "btnSarDaftar":
                self.__btnSarDaftar.config(bg="green")
                self.__btnArbabRojoo.config(bg="gray")
                self.__btnSarDaftar.config(state="disabled")
                self.__btnArbabRojoo.config(state="disabled")
                core.executor("disable", devDict["ArbabRojoo"])
                core.executor("enable", devDict["SarDaftar"])

            elif caller == "btnArbabRojoo":
                self.__btnSarDaftar.config(bg="gray")
                self.__btnArbabRojoo.config(bg="green")
                self.__btnArbabRojoo.config(state="disabled")
                self.__btnSarDaftar.config(state="disabled")
                core.executor("disable", devDict["SarDaftar"])
                core.executor("enable", devDict["ArbabRojoo"])

            counter=4
            def count_down(counter):
                if counter > 0:
                    self.__lblSeconds.config(text="Wait for: " + str(counter))
                    counter = counter - 1
                    self.__lblSeconds.after(1000, lambda: count_down(counter))
                else:
                    self.__btnArbabRojoo.config(state="normal")
                    self.__btnSarDaftar.config(state="normal")
                    self.__lblSeconds.pack_forget()
            count_down(counter)

    def __AboutUs(self):
        root = tk.Tk()
        root.iconbitmap('assets/icon/icon.ico')
        root.title("درباره ما")
        root.resizable(0, 0)
        
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.pack_propagate(0)

        explanation = """
        نرم افزار مدیریت اثر انگشت دفترداران
        نسخه: 0.9
        www.daftardaran.ir :وب سایت
        .در صورت وجود هر نوع مشکلی به وب سایت دفترداران مراجعه فرمایید
        """
        tk.Label(root, justify=tk.RIGHT, text=explanation).pack(side="left", ipadx=10)

    def __Binder(self):
        self.__btnSarDaftar.bind('<ButtonRelease>', lambda event: self.__ChangeUsb(event, "btnSarDaftar"))
        self.__btnArbabRojoo.bind('<ButtonRelease>', lambda event: self.__ChangeUsb(event, "btnArbabRojoo"))

        return self

    def StartGui(self):
        self.__root.mainloop()
