#!/usr/bin/python3

import _thread
import pynput  # get mouse position for interface initialization | *
from typing import List  # type hint iterables for older Python 3.x versions
from .interface_manager import interface
from .config_handler import get_config


def hotkey_listener():
    def on_activate(is_active_notifier: List[bool]):
        if not is_active_notifier[0]:
            print("Hotkey triggered.")
            is_active_notifier[0] = True
            mouse: pynput.mouse = pynput.mouse.Controller()
            _thread.start_new_thread(interface, (mouse.position, is_active_notifier))

    def on_kill():
        print("Application killed by hotkey.")
        raise SystemExit()

    is_active = [False]

    config = get_config()
    with pynput.keyboard.GlobalHotKeys({
        config['hotkey']: lambda: on_activate(is_active),
        config['application_kill_hotkey']: on_kill
    }) as listener:
        listener.join()
