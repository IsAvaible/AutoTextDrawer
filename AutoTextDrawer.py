#!/usr/bin/python3

"""
This is the source code of AutoTextDrawer a application, which automatically draws text on canvases by sending
mouse events.
Additional fonts can be added by placing a .ttf in the /fonts directory and specifying the relative
path in res/config.json. Other types of configuration such as, the hotkey, can also be done by using
the config.json file.
"""
__author__ = 'Simon Felix Conrad'
__copyright__ = 'Copyright © 2021, Simon Felix Conrad'
__license__ = 'BSD 3.0'
__version__ = '1.0.0'
__github__ = 'https://github.com/IsAvaible'

import pynput  # keyboard and mouse controller / listeners
import tkinter as tk  # user interface
import darkdetect  # detect os dark-mode
import json  # read and parse json files
import _thread  # create sub-threads
from tkinter import ttk  # use themes with tkinter
from PIL import Image, ImageDraw, ImageFont  # read fonts and convert them to pixel information
from os import path  # get absolute paths
from numpy import asarray  # transform image to pixel array
from typing import Union  # type hint with multiple possible types
from ctypes import windll  # fix dpi inconsistency between controller and listener
from time import time  # measure draw time
from time import sleep  # Animate interface size change


def main():
    fix_dpi_inconsistency()
    # font = read_font('fonts\\Roboto\\Roboto-Black.ttf', 80)
    # font = read_font('fonts\\Tangerine\\Tangerine-Regular.ttf', 100)
    # Speed comparison clicks vs hold and swipe
    # draw_letter(font, u'<', (300, 300), accurate_clicks=True)
    # draw_letter(font, u'>', (400, 300), accurate_clicks=False)
    # draw_text(font, u'Hi, person who is interested in the source code :)', (200, 300), letter_spacing=5)
    # interface((500, 500))
    # show_all_fonts()
    hotkey_listener()


def read_font(relative_path: str, size: int = 100):
    absolute_path = path.join(path.dirname(path.realpath(__file__)), relative_path)
    font = ImageFont.truetype(absolute_path, size=size, encoding='unic')
    return font


def get_letter(font: ImageFont.FreeTypeFont, unicode_letter: str) -> list[list[int]]:
    assert len(unicode_letter) == 1
    text_width, text_height = font.getsize(unicode_letter)
    # Initialize Canvas
    canvas = Image.new('RGB', (text_width, text_height), 'white')
    # Draw letter on canvas
    ImageDraw.Draw(canvas).text((0, 0), unicode_letter, fill='black', font=font)
    # Get canvas data as pixel array
    rounding_factor = 0.5
    image_data = [[sum([1 if color_value > rounding_factor else 0 for color_value in pixel]) // 3 for pixel in row] for
                  row in (255 - asarray(canvas)) / 255.0]
    # Return the array
    return image_data


def show_font(font: ImageFont.FreeTypeFont, unicode_text: str = None):
    # get the config
    config = get_config()['show_font(s)_config']
    if unicode_text is None:
        unicode_text = config['default_show_font(s)_text']
    fg, bg = config['colors']['foreground'], config['colors']['background']

    # get the line size
    text_width, text_height = font.getsize(unicode_text)

    # create a blank canvas with extra space between lines
    canvas = Image.new('RGB', (text_width + 10, text_height + 10), bg)

    # draw the text onto the text canvas
    draw = ImageDraw.Draw(canvas)
    draw.text((5, 5), unicode_text, fg, font)

    # show the canvas in local image viewer
    canvas.show()


def show_all_fonts():
    # get config
    config = get_config()
    show_fonts_config = config['show_font(s)_config']
    text = show_fonts_config['default_show_font(s)_text']
    font_size = show_fonts_config['default_font_size']
    fg, bg = show_fonts_config['colors']['foreground'], show_fonts_config['colors']['background']
    # get fonts
    font_names = [key for key in config['fonts'].keys() if not key.startswith('__') and not key.startswith('Default')]
    fonts = [read_font(font_path, font_size) for font_path in map(config['fonts'].get, font_names)]
    texts = [f"{font_names[f_index]}: {text}" for f_index in range(len(fonts))]
    # get the line size
    font_sizes = [font.getsize(text) for font in fonts]
    img_width, img_height = max(size[0] for size in font_sizes), sum(size[1] for size in font_sizes) + 5 * len(fonts)
    # create a blank canvas with extra space between lines
    canvas = Image.new('RGB', (img_width + 10, img_height + 5), bg)
    draw = ImageDraw.Draw(canvas)
    # draw the fonts onto the canvas
    for f_index in range(len(fonts)):
        draw.text((5, 5 + sum(size[1] for size in font_sizes[:f_index])), texts[f_index], fg, fonts[f_index])
    # show the canvas in local image viewer
    canvas.show()


def array_to_input_motion(array: list[list[int]], initial_position: tuple[int, int], accurate_clicks: bool = False):
    mouse: pynput.mouse = pynput.mouse.Controller()
    mouse.position = initial_position

    for y in range(len(array)):
        # Stores amount of consecutive pixels in a row, allowing single swipe motions to draw them
        consecutive_pixels = 0
        for x in range(len(array[y])):
            new_position = (initial_position[0] + x, initial_position[1] + y)
            if array[y][x] == 1:  # Pixel is active
                if not accurate_clicks:
                    if consecutive_pixels == 0:
                        mouse.position = new_position
                    consecutive_pixels += 1
                else:  # Clicks each pixel instead of using swipes
                    mouse.position = new_position
                    mouse.click(pynput.mouse.Button.left)
            elif not accurate_clicks:  # Pixel is inactive
                if consecutive_pixels > 0:  # Draws pending pixels
                    mouse.press(pynput.mouse.Button.left)
                    mouse.position = new_position
                    mouse.release(pynput.mouse.Button.left)
                consecutive_pixels = 0


def draw_letter(font: ImageFont.FreeTypeFont, letter: str, initial_position: tuple[int, int],
                accurate_clicks: bool = False) -> int:
    if letter != ' ':
        letter_as_pixel_array = get_letter(font, letter)
        array_to_input_motion(letter_as_pixel_array, initial_position, accurate_clicks)
    else:
        letter_as_pixel_array = get_letter(font, u'A')

    return len(letter_as_pixel_array[0])


def draw_text(font: ImageFont.FreeTypeFont, text: str, initial_position: tuple[int, int], accurate_clicks: bool = False,
              letter_spacing: Union[int, float] = 5):
    letter_position: list[int, int] = [*initial_position]
    spacing = len(get_letter(font, u'-')) // letter_spacing
    for letter in text:
        letter_width = draw_letter(font, letter, tuple(letter_position), accurate_clicks)
        letter_position[0] += letter_width + spacing * (letter != ' ')


def interface(initial_position: tuple[int, int], destroy_notifier: list[bool] = None):
    root = tk.Tk()
    root.title('')

    # Import theme
    root.tk.call("source", "res/Azure-ttk-theme/azure.tcl")
    # Set the initial theme
    config = get_config()
    theme = config["interface-theme-brightness"]
    if theme == 'system':
        theme = ('light', 'dark')[darkdetect.isDark()]

    assert theme in ('light', 'dark')
    root.tk.call("set_theme", theme)

    # Remove title-bar and make background transparent
    root.resizable(0, 0)
    root.attributes('-topmost', True)

    # root.overrideredirect(1)
    # root.wm_attributes('-transparentcolor', 'pink')
    rwidth, rheight = 300, 285

    interface_texts = config['interface_config']['texts']
    # Remember, you have to use ttk widgets
    title_label = ttk.Label(text=interface_texts['title'], font=' 15 ', justify=tk.CENTER)
    title_label.pack()

    def get_padding(padding: int = 10):
        return ttk.Frame(height=padding)

    info_label_1 = ttk.Label(text=interface_texts['info_1'])
    info_label_1.pack()

    get_padding().pack()

    input_field = ttk.Entry(justify='center')
    input_field.pack()

    get_padding().pack()

    info_label_2 = ttk.Label(text=interface_texts['info_2'])
    info_label_2.pack()
    get_padding(5).pack()

    dropdown_labels = [*filter(lambda name: not name.startswith('__'), config['fonts'].keys())]

    dropdown_value = tk.StringVar()

    dropdown_menu = ttk.OptionMenu(root, dropdown_value, *dropdown_labels)
    dropdown_menu.pack()

    font_size = tk.IntVar()
    font_size_range = config['interface_config']['font_size_range']

    font_size_slider = ttk.LabeledScale(root, from_=font_size_range['min'], to=font_size_range['max'], variable=font_size)
    font_size_slider.scale.set(font_size_range['default'])
    font_size_slider.pack()

    get_padding(10).pack()

    show_fonts_button = ttk.Button(text=interface_texts['show_fonts_button'],
                                   command=lambda: _thread.start_new_thread(show_all_fonts, ()))
    accurate_draw_toggle = tk.IntVar()
    if config['interface_config']['accurate_draw_is_default']:
        accurate_draw_toggle.set(1)
    accurate_draw_button = ttk.Checkbutton(text=interface_texts['accurate_draw_button'], variable=accurate_draw_toggle)

    letter_spacing = tk.IntVar()
    letter_spacing_range = config['interface_config']['letter_spacing_range']
    letter_spacing_slider = ttk.LabeledScale(root, from_=letter_spacing_range['min'], to=letter_spacing_range['max'], variable=letter_spacing)
    letter_spacing_slider.scale.set(letter_spacing_range['default'])
    letter_spacing_text = ttk.Label(text=interface_texts['letter_spacing_info'])

    more_paddings = [get_padding(10), get_padding(5)]

    def toggle_more_options():
        if more_options.get() == 1:
            more_options_button.state(['alternate'])
            more_options_text.set(interface_texts['less_options_button'])
            pre_start_button_padding.pack_forget()
            start_button.pack_forget()

            root.geometry(f'{rwidth}x{rheight + 140}+{root.winfo_x()}+{root.winfo_y()}')
            more_paddings[0].pack()
            show_fonts_button.pack()
            more_paddings[1].pack()
            accurate_draw_button.pack()
            letter_spacing_slider.pack()
            letter_spacing_text.pack()
            pre_start_button_padding.pack()
            start_button.pack()
        else:
            more_options_text.set(interface_texts['more_options_button'])
            show_fonts_button.pack_forget()
            accurate_draw_button.pack_forget()
            letter_spacing_text.pack_forget()
            letter_spacing_slider.pack_forget()
            pre_start_button_padding.pack_forget()
            start_button.pack_forget()
            for padding in more_paddings:
                padding.pack_forget()

            root.geometry(f'{rwidth}x{rheight}+{root.winfo_x()}+{root.winfo_y()}')
            pre_start_button_padding.pack()
            start_button.pack()

    more_options = tk.IntVar()
    more_options_text = tk.StringVar()
    more_options_text.set(interface_texts['more_options_button'])
    more_options_button = ttk.Checkbutton(
        textvar=more_options_text, command=toggle_more_options, variable=more_options,
    )
    more_options_button.pack()

    pre_start_button_padding = get_padding(10)
    pre_start_button_padding.pack()

    start_button = ttk.Button(
        root, text=interface_texts['start_button'], command=lambda:
        on_start_button_press(input_field.get(), dropdown_value.get(), font_size.get(), accurate_draw_toggle.get() == 1,
                              letter_spacing.get(), root, destroy_notifier)
    )

    start_button.pack()

    # Set position
    root.geometry(f'{rwidth}x{rheight}+{initial_position[0]}+{initial_position[1]}')

    # Set on_close
    def on_close():
        if destroy_notifier is not None:
            destroy_notifier[0] = False
        print("Window destroyed by user action.")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Mainloop
    root.mainloop()


def on_start_button_press(input_text: str, selected_font: str, font_size: int, accurate_draw: bool, letter_spacing: int,
                          root: tk.Tk, destroy_notifier: list[bool] = None):
    if not input_text.strip():
        print('Input text not provided.')
        return
    else:
        print(f'Received input: {input_text=}, {selected_font=}, {font_size=}, {accurate_draw=}, {letter_spacing=}')

        window_position = (root.winfo_x(), root.winfo_y())
        root.destroy()

        font_path = get_config()['fonts'][selected_font].replace('\\', '\\')
        font = read_font(font_path, font_size)

        start_time = time()
        draw_text(font, input_text, window_position, accurate_draw, letter_spacing)
        print(f'Drawing finished in {time() - start_time: .2f} seconds.')

        if destroy_notifier is not None:
            destroy_notifier[0] = False


def hotkey_listener():
    def on_activate(is_active_notifier):
        if not is_active_notifier[0]:
            print('Hotkey triggered.')
            is_active_notifier[0] = True
            mouse: pynput.mouse = pynput.mouse.Controller()
            _thread.start_new_thread(interface, (mouse.position, is_active_notifier))

    def for_canonical(f):
        return lambda k: f(listener.canonical(k))

    hotkey = pynput.keyboard.HotKey(pynput.keyboard.HotKey.parse(get_config()['hotkey']),
                                    lambda: on_activate(is_active))
    is_active = [False]

    with pynput.keyboard.Listener(on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release)) \
            as listener:
        listener.join()


def get_config() -> dict:
    with open("res\\config.json", 'r') as config:
        config = json.loads(config.read())

        return config


def fix_dpi_inconsistency():
    windll.shcore.SetProcessDpiAwareness(2)


if __name__ == '__main__':
    main()
