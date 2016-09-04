#!/usr/bin/env python

# Add project path to system's python path,
# so we can find and import the pymocap package
import os, sys
from time import time

thisdir = os.path.dirname(__file__)
packagedir = os.path.abspath(os.path.join(thisdir, '..'))

if packagedir not in sys.path:
  sys.path.insert(0, packagedir)

if __name__ == '__main__':
    import subprocess
    os.chdir(thisdir)
    subprocess.call(['python', '-m', 'unittest', 'discover'])

class DummyPlayer:
    def __init__(self, path):
        # config
        self.path = path
        # attributes
        self.start_time = None
        self.start_pos = None
        self.status = 'Stopped'

    def set_position(self, pos):
        self.start_time = time()
        self.start_pos = pos

    def position(self):
        if self.status == 'Stopped':
            return None

        if not self.start_pos or not self.start_time:
            return 0.0

        if self.status == 'Playing':
            self.start_pos + time() - self.start_time

        return self.start_pos

    def get_filename(self):
        if self.status == 'Stopped':
            return None
        return self.path

    def play(self):
        self.status = 'Playing'
        self.set_position(self.position())

    def pause(self):
        self.status = 'Paused'

    def stop(self):
        self.status = 'Stopped'

    def playback_status(self):
        return self.status
