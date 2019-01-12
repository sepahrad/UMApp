# define name of installer
OutFile "UsbManagerInstaller-Win7-64bit.exe"
 
# define installation directory
InstallDir "$PROGRAMFILES\UsbManager"
 
# For removing Start Menu shortcut in Windows 7
RequestExecutionLevel user
 
# start default section
Section
 
    # set the installation directory as the destination for the following actions
    SetOutPath $INSTDIR
 
    WriteUninstaller "$INSTDIR\usbmanageruninstall.exe"

    # Copy Files
    File /nonfatal /a /r "main\"

    CreateShortCut "$SMPROGRAMS\UsbManagerUninstaller.lnk" "$INSTDIR\usbmanageruninstall.exe"
    CreateShortCut "$SMPROGRAMS\UsbManager.lnk" "$INSTDIR\usbmanager.exe"
    CreateShortcut "$DESKTOP\UsbManager.lnk" "$INSTDIR\usbmanager.exe"

SectionEnd
 
# uninstaller section start
Section "uninstall"
 
    Delete "$INSTDIR\usbmanageruninstall.exe"
    Delete "$SMPROGRAMS\UsbManager.lnk"
    Delete "$DESKTOP\UsbManager.lnk"

    Delete "$INSTDIR\*"

# uninstaller section end
SectionEnd