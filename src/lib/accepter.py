from threading import Thread
from lib.socket_tcp import Socket
from collections import deque
from lib.logger import logger


class ClientHandler:

    def __init__(self, skt: Socket):
        self.th = Thread(None, self._run, self)
        self.skt = skt

    def _run(self):
        pass

    def join(self, force=False):
        pass

    def is_done(self):
        return False


class Accepter:

    def __init__(self, skt: Socket):
        self.th = Thread(None, self._run)
        self.skt = skt
        self.accepting = True
        self.th.start()
        self.clients = deque()

    def _run(self):
        while self.accepting:
            logger.debug("Accepter: Waiting for Client.")
            try:
                peer = self.skt.accept()
            except OSError:
                break
            self.clients.append(ClientHandler(peer))
            self._join_connections()
        self._join_connections(True)

    def _join_connections(self, force=False):
        for _ in range(len(self.clients)):
            handler = self.clients.popleft()
            if force or handler.is_done():
                handler.join(force)
                continue
            self.clients.append(handler)

    def stop(self):
        self.accepting = False
        self.skt.close()
