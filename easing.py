#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/3/14
import numpy as np


# https://github.com/gdsmith/jquery.easing/blob/master/jquery.easing.js
def ease_in_quad(x):
    return x * x


def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)


def ease_out_quart(x):
    return 1 - pow(1 - x, 4)


def get_tracks(distance, seconds, ease_func):
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        ease = globals()[ease_func]
        offset = round(ease(t/seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    return offsets, tracks
