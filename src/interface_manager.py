#!/usr/bin/python3

import tkinter as tk  # user interface
import darkdetect  # detect os dark-mode | *
import _thread  # create sub-threads
from time import time, sleep  # measure draw time, show alert message on missing input text
from tkinter import ttk  # use themes with tkinter
from .config_handler import get_config
from .font_handler import show_all_fonts, read_font
from .draw_handler import draw_text


def interface(initial_position: tuple[int, int], destroy_notifier: list[bool] = None):
    # Initiate root window
    root = tk.Tk()
    root.title('')

    # Get config
    config = get_config()
    interface_config = config['interface_config']

    # Import theme
    theme_name = interface_config['interface_theme']
    root.tk.call("source", interface_config['interface_theme_paths'][theme_name])

    # Set the theme brightness
    theme = interface_config["interface_theme_brightness"]
    if theme == 'system':
        theme = ('light', 'dark')[darkdetect.isDark()]

    root.tk.call("set_theme", theme)

    # Set window size, disable resizable-ity and set the window to be always on top
    root_width, root_height = 300, 285
    root.resizable(0, 0)
    root.attributes('-topmost', True)

    # Remove title-bar and make background transparent
    # root.overrideredirect(1)
    # root.wm_attributes('-transparentcolor', 'pink')

    interface_texts = interface_config['texts']
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
    font_size_range = interface_config['font_size_range']

    font_size_slider = ttk.LabeledScale(root, from_=font_size_range['min'], to=font_size_range['max'],
                                        variable=font_size)
    font_size_slider.scale.set(font_size_range['default'])
    font_size_slider.pack()

    get_padding(10).pack()

    show_fonts_button = ttk.Button(text=interface_texts['show_fonts_button'],
                                   command=lambda: _thread.start_new_thread(show_all_fonts, ()))
    accurate_draw_toggle = tk.IntVar()
    if interface_config['accurate_draw_is_default']:
        accurate_draw_toggle.set(1)
    accurate_draw_button = ttk.Checkbutton(text=interface_texts['accurate_draw_button'], variable=accurate_draw_toggle)

    letter_spacing = tk.IntVar()
    letter_spacing_range = interface_config['letter_spacing_range']
    letter_spacing_slider = ttk.LabeledScale(root, from_=letter_spacing_range['min'], to=letter_spacing_range['max'],
                                             variable=letter_spacing)
    letter_spacing_slider.scale.set(letter_spacing_range['default'])
    letter_spacing_text = ttk.Label(text=interface_texts['letter_spacing_info'])

    more_paddings = [get_padding(10), get_padding(5)]

    def toggle_more_options():
        if more_options.get() == 1:
            more_options_button.state(['alternate'])
            more_options_text.set(interface_texts['less_options_button'])
            pre_start_button_padding.pack_forget()
            start_button.pack_forget()

            root.geometry(f'{root_width}x{root_height + 140}+{root.winfo_x()}+{root.winfo_y()}')
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

            root.geometry(f'{root_width}x{root_height}+{root.winfo_x()}+{root.winfo_y()}')
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

    start_button_text = tk.StringVar()
    start_button_text.set(interface_texts['start_button'])
    start_button = ttk.Button(
        root, textvariable=start_button_text, command=lambda: on_start_button_press(
            input_field.get(), dropdown_value.get(), font_size.get(), accurate_draw_toggle.get() == 1,
            letter_spacing.get(), root, start_button_text, destroy_notifier)
    )

    start_button.pack()

    # Set position
    root.geometry(f'{root_width}x{root_height}+{initial_position[0]}+{initial_position[1]}')

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
                          root: tk.Tk, start_button_text_var: tk.StringVar, destroy_notifier: list[bool] = None):
    if not input_text.strip():
        print('Input text not provided.')
        error_text = get_config()['interface_config']['texts']['start_button_no_input']
        _thread.start_new_thread(on_start_button_error, (start_button_text_var, error_text))
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


def on_start_button_error(start_button_text_var: tk.StringVar, error_text: str):
    default_text = get_config()['interface_config']['texts']['start_button']
    start_button_text_var.set(error_text)
    sleep(1)
    start_button_text_var.set(default_text)
