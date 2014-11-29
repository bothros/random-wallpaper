#! /usr/bin/env python3

import os
import subprocess
import itertools
import glob
import random
import fileinput

RANDOM_WALLPAPER_DIR = 'RANDOM_WALLPAPER_DIR'
HOME = os.environ.get('HOME', '')
DEFAULT_RANDOM_WALLPAPER_DIR = os.path.join(HOME, '.random_wallpaper')
CURRENT_FILE = 'current'
LOCATIONS_FILE = 'location'

BLACKLIST_EXTENSION = '{}.black'
GLOB_EXTENSION = '*.jpg'


def get_rw_dir():
    return os.environ.get(RANDOM_WALLPAPER_DIR, DEFAULT_RANDOM_WALLPAPER_DIR)

def get_current_wallpapers():
    filename = os.path.join(get_rw_dir(), CURRENT_FILE)
    return [line.strip() for line in fileinput.input(filename)]

def set_current_wallpaper(screen, wallpaper):
    filename = os.path.join(get_rw_dir(), CURRENT_FILE)
    for line in fileinput.input(filename, inplace=True):
        if fileinput.lineno() == screen+1:
            print(wallpaper)
        else:
            print(line.strip())

def get_wallpaper_location(screen):
    filename = os.path.join(get_rw_dir(), LOCATIONS_FILE)
    return [line.strip() for line in fileinput.input(filename)][screen]

def randomize_wallpaper(screen):
    loc = get_wallpaper_location(screen)
    wps = glob.glob(os.path.join(loc, GLOB_EXTENSION))
    selection = random.choice(wps)
    set_current_wallpaper(screen, selection)

def flush():
    x = ['feh'] + list(itertools.chain.from_iterable([['--bg-scale', wp] for wp in get_current_wallpapers()]))
    subprocess.call(x)
