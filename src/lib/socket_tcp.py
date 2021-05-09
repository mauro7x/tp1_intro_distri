from socket import (socket, AF_INET, SOCK_STREAM, SHUT_RDWR,
                    SOL_SOCKET, SO_REUSEADDR)
from lib.logger import logger


class Socket:

    def __init__(self, skt: socket = None) -> None:
        if skt is None:
            self.skt = socket(AF_INET, SOCK_STREAM)
        else:
            self.skt = skt

    def connect(self, host: str, port: int) -> None:
        self.skt.connect((host, port))

    def bind(self, host: str, port: int) -> None:
        self.skt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.skt.bind((host, port))

    def listen(self, queue: int = 10) -> None:
        self.skt.listen(queue)

    def accept(self):
        peer, addr = self.skt.accept()
        logger.info(f"[Socket] Client connected from {addr[0]}:{addr[1]}.")
        return Socket(peer)

    def close(self) -> None:
        try:
            self.skt.shutdown(SHUT_RDWR)
            self.skt.close()
        except OSError:
            return

    def send(self, data: bytearray) -> None:
        total_bytes = len(data)
        bytes_sent = 0
        while bytes_sent < total_bytes:
            last_sent = self.skt.send(data[bytes_sent:])
            if last_sent == 0:
                raise RuntimeError("Socket closed by the peer.")

            bytes_sent += last_sent

    def recv(self, size: int) -> bytearray:
        data = []
        bytes_recd = 0
        while bytes_recd < size:
            segment = self.skt.recv(size - bytes_recd)
            if segment == b'':
                raise RuntimeError("Socket closed by the peer.")
            data.append(segment)
            bytes_recd += len(segment)

        return b''.join(data)
