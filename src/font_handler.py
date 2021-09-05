#!/usr/bin/python3

from PIL import Image, ImageDraw, ImageFont  # read fonts and convert them to pixel information | * (Pillow)
from os import path  # get absolute paths
from numpy import asarray  # transform image to pixel array | *
from .config_handler import get_config


def read_font(relative_path: str, size: int = 100):
    # absolute_path = path.join(path.dirname(path.realpath(__file__)), relative_path)
    font = ImageFont.truetype(relative_path, size=size, encoding='unic')
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
