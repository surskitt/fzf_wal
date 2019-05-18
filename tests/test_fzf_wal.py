#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fzf_wal` package."""

import pytest


from fzf_wal import fzf_wal


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
    expected = r'\e[38;2;12;34;56testm'
    out = fzf_wal.rgb_string('test', [12, 34, 56])

    assert expected == out


def test_rgb_bg_string():
    expected = r'\e[48;2;12;34;56testm'
    out = fzf_wal.rgb_bg_string('test', [12, 34, 56])

    assert expected == out
