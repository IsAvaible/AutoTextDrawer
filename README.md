# AutoTextDrawer
This application automatically draws text on canvases by sending mouse events.

When used with the default config using the hotkey \<ctrl\>+\<alt\>+[=] will open the draw initiation panel.

![image of the draw initiation panel](https://i.imgur.com/6SXmeTv.png)

After setting up the available configurations the draw can be initiated by pressing the downmost button. This will result in an image similar to this, which is drawn in around 3 seconds (processing of the input by the drawing program may take longer):

![image of a example text on paint](https://i.imgur.com/MKBkep3.png)

The application ships with several open-source licensed fonts 
and uses [a ttk theme](https://github.com/rdbende/Azure-ttk-theme) made by [rdbende](https://github.com/rdbende) 
(The [Sun Valley theme](https://github.com/rdbende/Sun-Valley-ttk-theme) is also available and can be selected in the config.).

Additional fonts can be added by placing a .ttf in the [/fonts](/fonts) directory and specifying the relative
path in [res/config.json](res/config.json). Other types of configuration such as, the hotkey or interface texts can also be made using
this config file.


