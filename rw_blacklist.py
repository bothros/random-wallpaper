#!/usr/bin/env python3

import sys
import random_wallpaper

if len(sys.argv) < 2:
    print('Takes one argument, the screen to blacklist, 0 or 1')
else:
    screen = int(sys.argv[1])

    black_wp = random_wallpaper.get_current_wallpapers()[screen]
    random_wallpaper.blacklist_wallpaper(black_wp)
    random_wallpaper.randomize_wallpaper(screen)
    random_wallpaper.flush()
