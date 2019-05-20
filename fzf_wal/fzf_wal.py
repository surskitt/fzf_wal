# -*- coding: utf-8 -*-

"""Main module."""

import os
import sys

import pywal
from iterfzf import iterfzf


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
    out = rf'[{attr};2;{r};{g};{b}m{s}'

    return out


def rgb_bg_string(s: str, rgb: [int, int, int]) -> str:
    """ Return shell colour sequence for background colours """
    return rgb_string(s, rgb, 48)


def escape_colour(s):
    return f'{s}[m'


def colour_band(colours: list) -> str:
    """ Return a string with coloured blocks for all given rgb lists """
    out = ' '.join(rgb_string('▄', rgb) for rgb in colours[:16])

    return out


def theme_dict_colours(d: dict) -> list:
    """ Extract colours from wal theme dict """
    return [d['colors'][k] for k in sorted(d['colors'])]


def name_from_path(path: str) -> str:
    """ extract shade (light/dark) and theme name from path """
    dirname, fn = os.path.split(path)
    _, shade = os.path.split(dirname)
    name, _ = os.path.splitext(fn)

    return f'{shade}/{name}'


def theme_name_iter(theme_dicts: dict):
    """ an iterable containing previews and names of themes  for fzf """
    for name, theme in theme_dicts.items():
        rgbs = [hex_to_rgb(i) for i in theme_dict_colours(theme)]
        fg, bg = theme['special']['foreground'], theme['special']['background']
        fg_rgb, bg_rgb = [hex_to_rgb(i) for i in [fg, bg]]

        band = colour_band(rgbs)
        fg_block = rgb_string("▄", fg_rgb)
        preview = escape_colour(rgb_bg_string(f' {band} {fg_block} ', bg_rgb))

        yield f'{preview} {name}'


def name_from_selection(s: str) -> str:
    """ extract theme name from fzf selection """
    return s.split()[-1].strip()


def theme_selector(theme_dicts: dict) -> str:
    """ Use fzf to select a theme """
    os.environ['FZF_DEFAULT_OPTS'] = '--ansi'
    selected = iterfzf(theme_name_iter(theme_dicts))
    if selected is None:
        return None

    return name_from_selection(selected)


def main():
    # load all pywal themes
    themes = (pywal.theme.list_themes() +
              pywal.theme.list_themes(dark=False) +
              pywal.theme.list_themes_user())
    # create a dictionary of paths
    theme_files = {name_from_path(i): i.path for i in themes}
    # create a dictionary of theme dictionaries
    theme_dicts = {k: pywal.colors.file(v) for k, v in theme_files.items()}

    # select a theme using fzf
    selected = theme_selector(theme_dicts)
    # if no theme was selected, exit with return status 1
    if selected is None:
        sys.exit(1)

    # if theme was selected, load from dict
    theme = theme_dicts[selected]

    # apply theme
    pywal.sequences.send(theme)
    pywal.export.every(theme)
    pywal.reload.env()
