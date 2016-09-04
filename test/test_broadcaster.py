import helper
import unittest
from time import time

from omxsync import Broadcaster

class TestBroadcaster(unittest.TestCase):
    def test_stopped_no_problem(self):
        # create master and slave video players
        player = helper.DummyPlayer('/video/file.mp4')
        # create broadcaster and receiver instances
        broadcaster = Broadcaster(player)
        broadcaster.setup()

        self.assertIsNone(player.position())
        self.assertIsNone(player.get_filename())

        try:
            broadcaster.update()
        except TypeError as err:
            self.fail("broadcaster should be able to deal with Stopped-status players: " + str(err))

# run just the tests in this file
if __name__ == '__main__':
    unittest.main()
