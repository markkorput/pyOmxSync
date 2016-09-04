import helper
import unittest
from time import time

from omxsync import Receiver, Broadcaster

class TestReceiver(unittest.TestCase):
    def test_stopped_no_problem(self):
        # create master and slave video players
        mplayer = helper.DummyPlayer('/video/file.mp4')
        splayer = helper.DummyPlayer('/video/file.mp4')
        # create broadcaster and receiver instances
        broadcaster = Broadcaster(mplayer, {'host': '127.0.0.1'})
        broadcaster.setup()
        receiver = Receiver(splayer, {'host': '127.0.0.1'})
        receiver.setup()

        # start both players and move the master player ahead 40.3 seconds
        mplayer.play()
        # splayer.play() # SHOULD BE STOPPED
        mplayer.set_position(40.3)

        # broadcast master's position
        broadcaster.update()

        # before
        self.assertEqual(splayer.playback_status(), 'Stopped')
        self.assertEqual(splayer.position(), None)

        # wait max. 1 seconds for broadcasted data to be received
        t = time()
        while time() - t < 1:
            # receive and apply broadcasted data
            try:
                receiver.update()
            except TypeError as err:
                self.fail("Receiver should be able to deal with stopped-status players: " + str(err))

            # if slave's player is paused, no need to wait longer
            if splayer.playback_status() == 'Paused':
                break

        self.assertEqual(splayer.playback_status(), 'Stopped')


# run just the tests in this file
if __name__ == '__main__':
    unittest.main()
