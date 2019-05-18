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


def colour_band(colours: list):
    """ Return a string with coloured blocks for all given rgb lists """
    out = ' '.join(rgb_string('▄', rgb) for rgb in colours)

    return out


def theme_dict_colours(d: dict):
    """ Extract colours from wal theme dict """
    return [d['colors'][k] for k in sorted(d['colors'])]


def name_from_path(path: str):
    dirname, fn = os.path.split(path)
    _, shade = os.path.split(dirname)
    name, _ = os.path.splitext(fn)

    return f'{shade}/{name}'


def main():
    theme_files = [i.path for i in pywal.theme.list_themes()]
    theme_dicts = {i: pywal.colors.file(i) for i in theme_files}


if __name__ == '__main__':
    main()
