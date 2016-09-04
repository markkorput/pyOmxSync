import helper
import unittest
from time import time

from omxsync import Receiver, Broadcaster

class TestReceiver(unittest.TestCase):
    def setUp(self):
        # create master and slave video players
        self.mplayer = helper.DummyPlayer('/video/file.mp4')
        self.splayer = helper.DummyPlayer('/video/file.mp4')
        # create broadcaster and receiver instances
        self.broadcaster = Broadcaster(self.mplayer, {'host': '127.0.0.1'})
        self.broadcaster.setup()

    def tearDown(self):
        self.receiver.destroy()
        self.broadcaster.destroy()

    def test_stopped_no_problem(self):
        self.receiver = Receiver(self.splayer, {'host': '127.0.0.1'})
        self.receiver.setup()

        # start both players and move the master player ahead 40.3 seconds
        self.splayer.stop()
        self.mplayer.play()
        # splayer.play() # SHOULD BE STOPPED
        self.mplayer.set_position(40.3)

        # broadcast master's position
        self.broadcaster.update()

        # before
        self.assertEqual(self.splayer.playback_status(), 'Stopped')
        self.assertEqual(self.splayer.position(), None)

        # wait max. 1 seconds for broadcasted data to be received
        t = time()
        while time() - t < 1:
            # receive and apply broadcasted data
            try:
                self.receiver.update()
            except TypeError as err:
                self.fail("Receiver should be able to deal with stopped-status players: " + str(err))

            # if slave's player is paused, no need to wait longer
            if self.splayer.playback_status() == 'Paused':
                break

        self.assertEqual(self.splayer.playback_status(), 'Stopped')

    def test_network_delay_compensation(self):
        self.receiver = Receiver(self.splayer, {'network_delay': 3.5})
        self.receiver.setup()

        # start both players and move the master player ahead 40.3 seconds
        self.mplayer.play()
        self.splayer.play()
        self.splayer.set_position(0.0)
        self.mplayer.set_position(40.3)

        # broadcast master's position
        self.broadcaster.update()

        # before
        self.assertEqual(self.splayer.playback_status(), 'Playing')
        self.assertEqual(self.splayer.position(), 0.0)

        # wait max. 1 seconds for broadcasted data to be received
        t = time()
        while time() - t < 1:
            self.receiver.update()
            # if slave's player is paused, no need to wait longer
            if self.splayer.playback_status() == 'Paused':
                break

        # verify the slave's player is paused (until master catches up)
        self.assertEqual(self.splayer.playback_status(), 'Paused')
        # assert that the slave's playback position has been moved a bit ahead of master
        self.assertEqual(self.splayer.position(), self.mplayer.position() + self.receiver.jump_ahead + self.receiver.network_delay)


# run just the tests in this file
if __name__ == '__main__':
    unittest.main()
