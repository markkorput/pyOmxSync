# pyOmxSync
python module to sync playback of several omxplayer instances


## Summary

A small python module that syncs omxplayers over the network using sockets and a master/slave configuration. The syncing logic was initialy inspired by the [omxplayer-sync](https://github.com/turingmachine/omxplayer-sync) implementation, but designed to be easily implementable in your python project (and not as a stand-alone runnable script). It uses [python-omxplayer-wrapper](https://github.com/willprice/python-omxplayer-wrapper) to interface with the OMXPlayer process.


## Install

First make sure willprice's [python-omxplayer-wrapper](https://github.com/willprice/python-omxplayer-wrapper) is installed. Go to [https://github.com/willprice/python-omxplayer-wrapper](https://github.com/willprice/python-omxplayer-wrapper) for instructions.

There is no pip-installable package yet, so just copy this repo's pyOmxSync folder into your own project for now.


On the slave you _might_ need to change your raspi's configuration to allow incoming broadcast messages:
```shell
echo 0 | sudo tee /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts
```

## Usage - master

```python

from omxplayer import OMXPlayer
from pyOmxSync.broadcaster import Broadcaster

player = OMXPlayer('path/to/video.mp4')
broadcaster = Broadcaster(player, {'verbose': True})
broadcaster.setup()
player.play()

while player.playback_status() != "Stopped":
	broadcaster.update()
```

## Usage - slave

```python

from omxplayer import OMXPlayer
from receiver import Receiver

player = OMXPlayer('path/to/video.mp4')
receiver = Receiver(player, {'verbose': True})
receiver.setup()
player.play()

while player.playback_status() != "Stopped":
	receiver.update()
```