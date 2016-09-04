#!/usr/bin/env python2
try:
    from omxplayer import OMXPlayer
except ImportError:
    print("\n!! Could not import OMXPlayer, see https://github.com/willprice/python-omxplayer-wrapper for install instructions !!\n")

from omxsync.broadcaster import Broadcaster
import sys

if len(sys.argv) < 2:
    print('No video specified\nUsage: python test_master.py path/to/video.mp4\n')
    sys.exit(1)

try:
    print("Load player")
    player = OMXPlayer(sys.argv[1])

    print("Load broadcaster")
    broadcaster = Broadcaster(player, {'verbose': True})
    broadcaster.setup()

    print("Start playing")
    player.play()

    while player.playback_status() != "Stopped":
        broadcaster.update()

    print("Stop player")
    player.stop()

    print("Exit")
except Exception as err:
    print("An error occured:")
    print(err)
