import socket
from time import time

DEFAULT_PORT = 1666
DEFAULT_HOST = '255.255.255.255'
DEFAULT_INTERVAL = 1.0 # seconds

class Broadcaster:
    def __init__(self, omxplayer, options = {}):
        # config
        self.player = omxplayer
        self.options = options
        self.verbose = options['verbose'] if 'verbose' in options else False
        self.interval = options['interval'] if 'interval' in options else DEFAULT_INTERVAL
        # attributes
        self.socket = None
        self.next_broadcast_time = 0

    def __del__(self):
        self.destroy()

    def setup(self):
        host = self.options['host'] if 'host' in self.options else DEFAULT_HOST
        port = self.options['port'] if 'port' in self.options else DEFAULT_PORT

        # create socket connections
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        # enable broadcasting
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            self.socket.connect((host, port))
        except:
            print("PositionBroadcaster: network is unreachable")

    def destroy(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def update(self):
        t = time()

        # time for next broadcast?
        if t >= self.next_broadcast_time:
            # broadcast
            self._broadcast_position()
            # "schedule" next broadcast
            self.next_broadcast_time = t + self.interval

    def _broadcast_position(self):
        p = self.player.position()

        try:
            self.socket.send(("%s%%%s" % (str(p),  self.player.get_filename())).encode('utf-8'))
        except socket.error as err:
            print("PositionBroadcaster: socket.send failed:")
            print(err)

        if self.verbose:
            print 'broadcast position: ' + str(p) + ', with filename: ' + self.player.get_filename()
