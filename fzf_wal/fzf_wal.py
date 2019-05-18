# -*- coding: utf-8 -*-

"""Main module."""

import pywal


def hex_to_rgb(hexstring: str) -> [int, int, int]:
    if len(hexstring) < 6:
        raise ValueError('RGB hex value must be at least 6 chars')

    hexchars = hexstring[-6:]
    colours = [hexchars[i:i+2] for i in range(0, 6, 2)]
    rgb = [int(i, 16) for i in colours]

    return rgb


def rgb_string(s: str, rgb: [int, int, int], attr: str = 38):
    r, g, b = rgb
    out = rf'\e[{attr};2;{r};{g};{b}testm'

    return out


def rgb_bg_string(s: str, rgb: [int, int, int]):
    return rgb_string(s, rgb, 48)


def main():
    theme_files = [i.path for i in pywal.theme.list_themes()]


if __name__ == '__main__':
    main()
