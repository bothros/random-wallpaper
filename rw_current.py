#!/usr/bin/env python3

import sys
import random_wallpaper

if len(sys.argv) < 2:
    for wp in random_wallpaper.get_current_wallpapers():
        print(wp)
else:
    screen = int(sys.argv[1])
    print(random_wallpaper.get_current_wallpaper(screen))

