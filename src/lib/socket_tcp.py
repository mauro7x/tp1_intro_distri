from socket import (socket, AF_INET, SOCK_STREAM, SHUT_RDWR,
                    SOL_SOCKET, SO_REUSEADDR)
from lib.logger import logger


class Socket:

    def __init__(self, skt=None):
        if skt is None:
            self.skt = socket(AF_INET, SOCK_STREAM)
        else:
            self.skt = skt

    def connect(self, host, port):
        self.skt.connect((host, port))

    def bind(self, host, port):
        self.skt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.skt.bind((host, port))

    def listen(self, queue=10):
        self.skt.listen(queue)

    def accept(self):
        peer, addr = self.skt.accept()
        logger.debug(f"Socket: client connected from {addr}")
        return Socket(peer)

    def close(self):
        self.skt.shutdown(SHUT_RDWR)
        self.skt.close()

    def send_file(self, f):
        pass

    def recv_file(self, f):
        pass