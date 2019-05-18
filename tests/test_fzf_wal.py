#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fzf_wal` package."""

import pytest

import os


from fzf_wal import fzf_wal


def open_relative(fn: str) -> str:
    dir_name = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_name, fn)) as f:
        return f.read()


hex_to_rgb_params = [
    ('#aabbcc', [170, 187, 204]),
    ('#ddeeff', [221, 238, 255]),
    ('112233',  [17,  34,  51])
]


@pytest.mark.parametrize('hexstring,expected', hex_to_rgb_params)
def test_hex_to_rgb(hexstring, expected):
    rgb = fzf_wal.hex_to_rgb(hexstring)

    assert expected == rgb


def test_hex_to_rgb_too_short():
    with pytest.raises(ValueError) as excinfo:
        fzf_wal.hex_to_rgb('aabb')
    assert str(excinfo.value) == 'RGB hex value must be at least 6 chars'


def test_rgb_string():
    expected = r'[38;2;12;34;56mtest[m'
    out = fzf_wal.rgb_string('test', [12, 34, 56])

    assert expected == out


def test_rgb_bg_string():
    expected = r'[48;2;12;34;56mtest[m'
    out = fzf_wal.rgb_bg_string('test', [12, 34, 56])

    assert expected == out


def test_color_band():
    expected = open_relative('color_band.txt')
    colours = [[0, 0, 0]]*16
    band = fzf_wal.colour_band(colours)

    assert expected == band


def test_theme_dict_colours():
    expected = ['a', 'b', 'c']
    in_dict = {'colors': {'color0': 'a', 'color2': 'c', 'color1': 'b'}}

    colours = fzf_wal.theme_dict_colours(in_dict)

    assert colours == expected
