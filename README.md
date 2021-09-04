# AutoTextDrawer
This application automatically draws text on canvases by sending mouse events. 

Additional fonts can be added by placing a .ttf in the /fonts directory and specifying the relative
path in res/config.json. Other types of configuration such as, the hotkey can also be done by using
this config file.

When used with the default config using the hotkey \<ctrl\>+\<alt\>+[=] will open the draw initiation panel.

![image of the draw initiation panel](https://i.imgur.com/R8oOHXl.png)

After setting up the avaible configurations the draw can be initiated by pressing the downmost button. This will result in an image similar to this, which is drawn in around 2 seconds (processing of the input by the drawing program may take longer):

![image of a example text on paint](https://i.imgur.com/PoncNhM.png)
