import helper
import unittest
from time import time

import omxsync

class TestSync(unittest.TestCase):
    def test_sync(self):
        # create master and slave video players
        mplayer = helper.DummyPlayer('/video/file.mp4')
        splayer = helper.DummyPlayer('/video/file.mp4')
        # create broadcaster and receiver instances
        broadcaster = omxsync.Broadcaster(mplayer, {'host': '127.0.0.1'})
        broadcaster.setup()
        receiver = omxsync.Receiver(splayer, {'host': '127.0.0.1'})
        receiver.setup()

        # start both players and move the master player ahead 40.3 seconds
        mplayer.play()
        splayer.play()
        mplayer.set_position(40.3)

        # broadcast master's position
        broadcaster.update()

        # before
        self.assertEqual(splayer.playback_status(), 'Playing')
        self.assertEqual(splayer.position(), 0.0)

        # wait max. 1 seconds for broadcasted data to be received
        t = time()
        while time() - t < 1:
            # receive and apply broadcasted data
            receiver.update()
            # if slave's player is paused, no need to wait longer
            if splayer.playback_status() == 'Paused':
                break

        # verify the slave's player is paused (until master catches up)
        self.assertEqual(splayer.playback_status(), 'Paused')
        # assert that the slave's playback position has been moved a bit ahead of master
        self.assertEqual(splayer.position(), mplayer.position() + receiver.jump_ahead)

# run just the tests in this file
if __name__ == '__main__':
    unittest.main()
