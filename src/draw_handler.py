#!/usr/bin/python3

import pynput
from PIL import ImageFont  # type hint font
from typing import Union  # type hint with multiple possible types
from ctypes import windll  # fix dpi inconsistency between controller and listener
from .font_handler import get_letter


def array_to_input_motion(array: list[list[int]], initial_position: tuple[int, int], accurate_clicks: bool = False):
    mouse: pynput.mouse = pynput.mouse.Controller()
    mouse.position = initial_position

    fix_dpi_inconsistency()

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
        letter_position_tuple = (letter_position[0], letter_position[1])
        letter_width = draw_letter(font, letter, letter_position_tuple, accurate_clicks)
        letter_position[0] += letter_width + spacing * (letter != ' ')


def fix_dpi_inconsistency():
    windll.shcore.SetProcessDpiAwareness(2)
