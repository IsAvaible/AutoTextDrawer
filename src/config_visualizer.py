#!/usr/bin/python3

import tkinter as tk  # user interface
import darkdetect  # detect os dark-mode | *
import _thread  # create sub-threads
from tkinter import ttk  # use themes with tkinter
from .config_handler import get_config


def show():
    config = get_config()
    theme_location = (i_config := config['interface_config'])['interface_theme_paths'][i_config['interface_theme']]

    root = tk.Tk()
    root.title('')
    root.tk.call("source", theme_location)

    theme_brightness = i_config["interface_theme_brightness"]
    if theme_brightness == 'system':
        theme_brightness = ('light', 'dark')[darkdetect.isDark()]
    root.tk.call("set_theme", theme_brightness)


    root.attributes('-topmost', True)
    # root_width, root_height = 300, 285

    def __recursive_root_build(dictionary: dict, win: tk.Tk) -> dict:
        entry_dict = {}
        ttk.Label(text="Add config option", font='Segeo 12 normal').pack()
        entry = ttk.Entry(justify='center', width=30)
        entry.insert(0, "name : value")
        entry.pack()
        entry_dict['ADD'] = entry

        for key, value in dictionary.items():
            if isinstance(value, dict):
                ttk.Label(text=key, font='Segeo 15 bold').pack()
                sub_entry_dictionary = __recursive_root_build(value, win)
                for sub_key, sub_entry in sub_entry_dictionary.items():
                    entry_dict[f"{key}`|`{sub_key}"] = sub_entry

            else:
                if not key.startswith('__'):
                    ttk.Label(text=key).pack()
                    value = str(value)
                    entry = ttk.Entry(justify='center', width=round(len(value)*1.3))
                    entry.insert(0, value)
                    entry.pack()
                    entry_dict[key] = entry
                else:
                    ttk.Label(text=f"~ {value}", font='Segeo 10 italic').pack()

        return entry_dict

    ttk.Label(text="Config", font='Segeo 25 ').pack()
    __recursive_root_build(config, root)
    ttk.Button(text="Confirm")

    root.mainloop()