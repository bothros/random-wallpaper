#!/usr/bin/env python3

import os
import sys
import subprocess
import itertools
import random
import yaml


NUM_SCREENS = 2

RANDOM_WALLPAPER_DIR = 'RANDOM_WALLPAPER_DIR'
HOME = os.environ.get('HOME', '')
DEFAULT_RANDOM_WALLPAPER_DIR = os.path.join(HOME, '.random_wallpaper')
CURRENT_FILE = 'current'
CONFIG_FILE = 'config'

BLACKLIST_EXTENSION = '{}.black'
GLOB_EXTENSION = '*.jpg'

BLACKLIST_TAG = 'blacklisted'
WALLPAPER_TAG = 'wallpaper'


def get_rw_dir():
    # Get the directory for data and location config
    return os.environ.get(RANDOM_WALLPAPER_DIR, DEFAULT_RANDOM_WALLPAPER_DIR)

def get_config():
    # Get the contents of the config file
    filename = os.path.join(get_rw_dir(), CONFIG_FILE)
    with open(filename, 'r') as f:
        return yaml.load(f)

config = get_config()
if config.get('method') == 'location':
    import glob

def get_current_wallpapers():
    # Get current wallpapers, as shown in DIR/current
    filename = os.path.join(get_rw_dir(), CURRENT_FILE)
    try:
        with open(filename, 'r') as f:
            wps = yaml.load(f)
            if len(wps) < NUM_SCREENS:
                wps = wps + list(itertools.repeat(None, NUM_SCREENS-len(wps)))
            return wps
    except:
        return list(itertools.repeat(None, NUM_SCREENS))
    #return [line.strip() for line in fileinput.input(filename)]

def get_current_wallpaper(screen):
    # Get current wallper for a screen, from DIR/current
    filename = os.path.join(get_rw_dir(), CURRENT_FILE)
    with open(filename, 'r') as f:
        return yaml.load(f)[screen-1]
    #for line in fileinput.input(filename):
        #if fileinput.lineno() == screen:
            #wp = line.strip()
    #return wp

def set_current_wallpaper(screen, wallpaper):
    # Set current wallpaper at a screen, in DIR/current
    filename = os.path.join(get_rw_dir(), CURRENT_FILE)
    wp = get_current_wallpapers()
    wp[screen-1] = wallpaper
    with open(filename, 'w') as f:
        f.write(yaml.dump(wp))
    #for line in fileinput.input(filename, inplace=True):
        #if fileinput.lineno() == screen:
            #print(wallpaper)
        #else:
            #print(line.strip())

def get_wallpapers(screen):
    # Gets all wallpapers to select from for a screen
    if config.get('method') == 'location':
        loc = config['screens'][screen]['location']
        return glob.glob(os.path.join(loc, GLOB_EXTENSION))
    elif config.get('method') == 'tags':
        query = '({} and not {}) and ({})'.format(
            WALLPAPER_TAG,
            BLACKLIST_TAG,
            config['screens'][screen]['query'],
        )
        return tmsu_files(query)
    else:
        raise(Exception("Invalid 'method' option in config."))

def tmsu_files(query):
    return [file.strip() for file in subprocess.check_output(['tmsu', 'files', query]).decode(sys.stdout.encoding).split('\n')]

def tmsu_tag(filename, tags):
    subprocess.check_call(['tmsu', 'tag', filename] + tags)

def randomize_wallpaper(screen):
    # Randomize the current wallpaper at a screen
    selection = random.choice(get_wallpapers(screen))
    set_current_wallpaper(screen, selection)

def blacklist_wallpaper(wallpaper):
    # Blacklist a wallpaper, by adding BLACKLIST_EXTENSION to it, so glob won't find it.
    if config.get('method') == 'location':
        os.rename(wallpaper, BLACKLIST_EXTENSION.format(wallpaper))
    elif config.get('method') == 'tags':
        tmsu_tag(wallpaper, [BLACKLIST_TAG])
    else:
        raise(Exception("Invalid 'method' option in config."))

def flush():
    # Use feh to set the actual background to the wallpapers in DIR/current
    x = ['feh'] + list(itertools.chain.from_iterable([['--bg-scale', wp] for wp in get_current_wallpapers()]))
    subprocess.call(x)
