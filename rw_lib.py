#! /usr/bin/env python3

import os
import subprocess
import itertools

RANDOM_WALLPAPER_DIR = 'RANDOM_WALLPAPER_DIR'
HOME = os.environ.get('HOME', '')
DEFAULT_RANDOM_WALLPAPER_DIR = os.path.join(HOME, '.random_wallpaper')
CURRENT_WALLPAPERS_FILE = 'current'

def get_rw_dir():
    return os.environ.get(RANDOM_WALLPAPER_DIR, DEFAULT_RANDOM_WALLPAPER_DIR)

def get_current_wallpapers():
    filename = os.path.join(get_rw_dir(), CURRENT_WALLPAPERS_FILE)
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

def flush():
    x = ['feh'] + list(itertools.chain.from_iterable([['--bg-scale', wp] for wp in get_current_wallpapers()]))
    subprocess.call(x)
    print(x)
