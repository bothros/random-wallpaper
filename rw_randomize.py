#!/usr/bin/env python3

import sys
import random_wallpaper

if len(sys.argv) < 2:
    random_wallpaper.randomize_wallpaper(1)
    random_wallpaper.randomize_wallpaper(2)
else:
    screen = int(sys.argv[1])
    random_wallpaper.randomize_wallpaper(screen)
random_wallpaper.flush()
