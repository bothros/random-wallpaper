Random wallpaper scripts to support two monitors, using feh.

Should support separate directories for the two monitors, querying the current image for each monitor, and marking an image to be removed from the rotation.

Screens are referred to by indexes 0 and 1.

A config is stored in .random\_wallpaper/config . A sample config file is included here.

The following utilities are available, and can be bound to whatever keys, or run in whatever startup scripts:

rw\_flush.py - displays the wallpapers in .random\_wallpaper/current, can be put in a startup script to reload what was showing when the machine was shutdown.
rw\_randomize.py SCREEN? - randomizes and displays one or both wallpapers (both is the default), can be put in a startup script or a cron job.
rw\_blacklist.py SCREEN - blacklists the wallpaper currently in screen 0 or screen 1, and randomizes and displays a new one.

If method is 'location', wallpapers are blacklisted by adding '.black' to their filenames. They can be cleared out with 'rm \*.black'. If you want to unblacklist them, you can do it with '[mmv](http://linux.maruhn.com/sec/mmv.html) "\*.black" "#1"'.

If method is 'tags', files with the tmsu tag 'wallpaper', that do not have the tag 'blacklisted', and also match the query listed in the config file for a certain screen, will be selected from. Blacklisting a wallpaper will give it the tag 'blacklisted'.

Requirements:
python3
PyYAML
feh
tmsu (optional)
