#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fzf_wal` package."""

import pytest
import unittest.mock

import os


from fzf_wal import fzf_wal


def open_relative(fn: str) -> str:
    dir_name = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_name, fn)) as f:
        return f.read()


@pytest.fixture
def theme_dict():
    return {
        't1': {
            'colors': {'color0': '000000'},
            'special': {'foreground': '000000', 'background': 'ffffff'}
        },
        't2': {
            'colors': {'color0': '000000'},
            'special': {'foreground': '000000', 'background': 'ffffff'}
        }
    }


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
    expected = r'[38;2;12;34;56mtest'
    out = fzf_wal.rgb_string('test', [12, 34, 56])

    assert expected == out


def test_rgb_bg_string():
    expected = r'[48;2;12;34;56mtest'
    out = fzf_wal.rgb_bg_string('test', [12, 34, 56])

    assert expected == out


def test_escape_colour():
    expected = 'hello[m'
    escaped = fzf_wal.escape_colour('hello')

    assert escaped == expected


def test_color_band():
    expected = open_relative('colour_band.txt')
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


def test_theme_name_iter(theme_dict):
    expected = open_relative('theme_name.txt')

    assert '\n'.join((fzf_wal.theme_name_iter(theme_dict))) == expected


def test_name_from_selection():
    expected = 'test'
    name = fzf_wal.name_from_selection(' a b c d test ')

    assert name == expected


@unittest.mock.patch('fzf_wal.fzf_wal.iterfzf')
def test_theme_selector(mock_fzf, theme_dict):
    mock_fzf.side_effect = lambda x: list(x)[0]

    assert fzf_wal.theme_selector(theme_dict) == 't1'


@unittest.mock.patch('fzf_wal.fzf_wal.iterfzf')
def test_theme_selector_cancelled(mock_fzf, theme_dict):
    mock_fzf.return_value = None

    assert fzf_wal.theme_selector(theme_dict) is None


@unittest.mock.patch('fzf_wal.fzf_wal.pywal')
@unittest.mock.patch('fzf_wal.fzf_wal.iterfzf')
def test_fzf_cancelled_sysexit(mock_fzf, mock_pywal):
    mock_fzf.return_value = None

    with pytest.raises(SystemExit) as e:
        fzf_wal.main()
    assert e.type == SystemExit
    assert e.value.code == 1
