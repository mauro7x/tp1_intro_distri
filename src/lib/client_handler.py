from threading import Thread
from itertools import count as it_count
from lib.socket_tcp import Socket
from lib.logger import logger


class ClientHandler:

    id_it = it_count()

    def __init__(self, skt: Socket):
        self.id = next(ClientHandler.id_it)
        self.th = Thread(None, self._run, self)
        self.skt = skt
        self.running = True
        self.th.start()

    def _run(self):
        logger.debug(f"[ClientHandler:{self.id}] Started.")

        # do some stuff
        self.skt.close()  # mock

        logger.debug(f"[ClientHandler:{self.id}] Finished.")
        self.running = False

    def join(self, force=False):
        if force:
            self.skt.close()
            self.running = False
            # finish connection

        self.th.join()

    def is_done(self):
        return not self.running
