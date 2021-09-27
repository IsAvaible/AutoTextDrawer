#!/usr/bin/python3

import _thread
import pynput  # get mouse position for interface initialization | *
from typing import List  # type hint iterables for older Python 3.x versions
from tempfile import TemporaryFile
from .interface_manager import interface
from .config_handler import get_config


def hotkey_listener():
    def on_activate(is_active_notifier: List[bool], temp_config_override_handle: TemporaryFile):
        if not is_active_notifier[0]:
            print("Hotkey triggered.")
            is_active_notifier[0] = True
            mouse: pynput.mouse = pynput.mouse.Controller()
            _thread.start_new_thread(interface, (mouse.position, is_active_notifier, temp_config_override_handle))

    def on_kill(temp_file: TemporaryFile):
        if temp_file is not None:
            temp_file.close()
        print("Application killed by hotkey.")
        raise SystemExit()

    is_active = [False]

    config = get_config()
    temp_config_override_handle = None
    if config['interface_config']['keep_draw_config_between_sessions']:
        temp_config_override_handle = TemporaryFile()
    with pynput.keyboard.GlobalHotKeys({
        config['hotkey']: lambda: on_activate(is_active, temp_config_override_handle),
        config['application_kill_hotkey']: lambda: on_kill(temp_config_override_handle)
    }) as listener:
        listener.join()
