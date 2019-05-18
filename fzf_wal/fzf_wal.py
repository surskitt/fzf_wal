# -*- coding: utf-8 -*-

"""Main module."""

import os
import pywal


def hex_to_rgb(hexstring: str) -> [int, int, int]:
    """ Convert base 16 hex (ffffff) string to rgb decimals [255,255,255] """
    if len(hexstring) < 6:
        raise ValueError('RGB hex value must be at least 6 chars')

    hexchars = hexstring[-6:]
    colours = [hexchars[i:i+2] for i in range(0, 6, 2)]
    rgb = [int(i, 16) for i in colours]

    return rgb


def rgb_string(s: str, rgb: [int, int, int], attr: str = 38) -> str:
    """ Take a rgb decimal list and string, return a shell colour sequence """
    r, g, b = rgb
    out = rf'[{attr};2;{r};{g};{b}m{s}[m'

    return out


def rgb_bg_string(s: str, rgb: [int, int, int]) -> str:
    """ Return shell colour sequence for background colours """
    return rgb_string(s, rgb, 48)


def colour_band(colours: list) -> str:
    """ Return a string with coloured blocks for all given rgb lists """
    out = ' '.join(rgb_string('▄', rgb) for rgb in colours[:16])

    return out


def theme_dict_colours(d: dict) -> list:
    """ Extract colours from wal theme dict """
    return [d['colors'][k] for k in sorted(d['colors'])]


def name_from_path(path: str) -> str:
    dirname, fn = os.path.split(path)
    _, shade = os.path.split(dirname)
    name, _ = os.path.splitext(fn)

    return f'{shade}/{name}'


def theme_name_iter(theme_dicts: dict):
    for name, theme in theme_dicts.items():
        rgbs = [hex_to_rgb(i) for i in theme_dict_colours(theme)]
        fg, bg = theme['special']['foreground'], theme['special']['background']
        fg_rgb, bg_rgb = [hex_to_rgb(i) for i in [fg, bg]]

        band = colour_band(rgbs)
        fg_block = rgb_string("▄", fg_rgb)
        preview = f'{band} {fg_block}'
        #  preview = rgb_bg_string(f'{band} {fg_block}', bg_rgb)

        yield f'{preview} {name}'


def main():
    themes = pywal.theme.list_themes() + pywal.theme.list_themes_user()
    theme_files = {name_from_path(i): i.path for i in themes}
    theme_dicts = {k: pywal.colors.file(v) for k, v in theme_files.items()}

    for i in theme_name_iter(theme_dicts):
        print(i)


if __name__ == '__main__':
    main()
