#!/usr/bin/env python2
try:
    from omxplayer import OMXPlayer
except ImportError:
    print("\n!! Could not import OMXPlayer, see https://github.com/willprice/python-omxplayer-wrapper for install instructions !!\n")

from pyOmxSync.receiver import Receiver
import sys

if len(sys.argv) < 2:
    print('No video specified\nUsage: python test_slave.py path/to/video.mp4\n')
    sys.exit(1)

try:
    print("Load player")
    player = OMXPlayer(sys.argv[1])

    print("Load Receiver")
    receiver = Receiver(player, {'verbose': True})
    receiver.setup()

    print("Start playing")
    player.play()

    while player.playback_status() != "Stopped":
        receiver.update()

    print("Stop player")
    player.stop()

    print("Exit")
except Exception as err:
    print("An error occured:")
    print(err)
