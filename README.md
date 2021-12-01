# AutoTextDrawer
This application automatically draws text on canvases by sending mouse events.

When used with the default config using the hotkey <kbd>ctrl</kbd>+<kbd>alt</kbd>+<kbd>=</kbd> will open the draw initiation panel.

![image of the draw initiation panel](https://i.imgur.com/6SXmeTv.png)

After setting up the available configurations the draw can be initiated by pressing the downmost button. This will result in an image similar to this, which is drawn in around 3 seconds (processing of the input by the drawing program may take longer):

![image of a example text on paint](https://i.imgur.com/MKBkep3.png)

The application ships with several open-source licensed fonts 
and uses [a ttk theme](https://github.com/rdbende/Azure-ttk-theme) made by [rdbende](https://github.com/rdbende) 
(The [Sun Valley theme](https://github.com/rdbende/Sun-Valley-ttk-theme) is also available and can be selected in the config.).

Additional fonts can be added by placing a .ttf in the [/fonts](/fonts) directory and specifying the relative
path in [config.json](config.json). Other types of configuration such as, the hotkey or interface texts can also be made using
this config file.

In case of an emergency the application can be forced killed with <kbd>ctrl</kbd>+<kbd>alt</kbd>+<kbd>=</kbd>+<kbd>-</kbd>.

# How to Install
**Windows via executable**
1. Download a release from the [releases section](https://github.com/IsAvaible/AutoTextDrawer/releases).
2. Unzip the folder.
3. Run the application by using the `AutoTextDrawer.exe`.

**Linux / Windows via local Python install**
1. Download the Source Code from the [releases section](https://github.com/IsAvaible/AutoTextDrawer/releases) and unzip it.
2. The application needs Python 3.9 or higher to be installed on the host system. To install Python, visit
   [Python's official website](https://www.python.org/downloads/) and download the latest version. Make sure to check the Path
   option during the installation progress.
3. Open a terminal session in the downloaded project folder (<kbd>shift</kbd> + <kbd>right-click</kbd> Open Powershell window here) and run
`pip -r install requirments.txt`.
4. After finishing these initial steps the application can be run using the **AutoTextDrawer.py/pyw** file.
5. Optional: If you want to autostart the application, open the startup directory with <kbd>Win</kbd> + <kbd>r</kbd>
and put a shortcut to either of the files into the appearing directory.

# Troubleshooting
If you are using a high dpi setting on your monitor, you may experience the problem, that the draw initiation panel is
cropped after opening it for the second time. With the current way the User Interface is being built there is no way to 
fix this via the application source code. Instead, you need to force the High DPI scaling override in the pythonw.exe 
compatibility setting, as explained in this [Stackoverflow Answer](https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp).

If you encounter any other bugs or above issue isn't fixed by the provided solution, you can report the issue in the 
[Issues section](/../../issues).
