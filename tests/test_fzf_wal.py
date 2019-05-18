#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fzf_wal` package."""

import pytest
from unittest.mock import patch

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
    colours = [[0, 0, 0]]*18
    band = fzf_wal.colour_band(colours)

    assert expected == band


def test_theme_dict_colours():
    expected = ['a', 'b', 'c']
    in_dict = {'colors': {'color0': 'a', 'color2': 'c', 'color1': 'b'}}

    colours = fzf_wal.theme_dict_colours(in_dict)

    assert colours == expected


def test_name_from_path():
    path = '/a/b/c/dark/theme'
    expected = 'dark/theme'

    name = fzf_wal.name_from_path(path)

    assert name == expected


@patch('fzf_wal.fzf_wal.rgb_string')
def test_theme_name_iter(mock_rgb_string):
    # mock rgb_string as pass-through (returns args)
    def mock_rgb_string_f(s, rgb, attr=38):
        r, g, b = rgb
        return s

    mock_rgb_string.side_effect = mock_rgb_string_f

    in_dict = {
        't1': {
            'colors': {'color0': 'aaaaaa'},
            'special': {'foreground': 'bbbbbb', 'background': 'cccccc'}
        },
        't2': {
            'colors': {'color0': 'dddddd'},
            'special': {'foreground': 'eeeeee', 'background': 'ffffff'}
        }
    }
    expected = [
        '▄ ▄ t1',
        '▄ ▄ t2'
    ]

    assert list(fzf_wal.theme_name_iter(in_dict)) == expected
