from socket import (socket, AF_INET, SOCK_STREAM, SHUT_RDWR,
                    SOL_SOCKET, SO_REUSEADDR)
from lib.logger import logger
from lib.stats import stats


class Socket:

    def __init__(self, skt: socket = None) -> None:
        """
        Inicialization of socket class.

        Parameters:
        skt(socket): a socket class with inicial value NULL.

        Returns:
        None.
        """

        logger.debug("[Socket] Creating socket...")
        if skt is None:
            self.skt = socket(AF_INET, SOCK_STREAM)
        else:
            self.skt = skt
        logger.debug("[Socket] Socket created.")

    def connect(self, host: str, port: int) -> None:
        """
        Build a connection with a especific host address and a port number.

        Parameters:
        host(str): Host address.
        port(int): Number of port.

        Returns:
        None.
        """
        logger.debug(f"[Socket] Connecting to {host}:{port}...")
        self.skt.connect((host, port))
        logger.debug(f"[Socket] Connected to {host}:{port}.")

    def bind(self, host: str, port: int) -> None:
        """
        assign a local socket address address to a socket identified 
        by descriptor socket that has no local socket address assigned. 

        Parameters:
        host(str): Host address.
        port(int): Number of port.

        Returns:
        None.
        """
        logger.debug(f"[Socket] Binding to {host}:{port}...")
        self.skt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.skt.bind((host, port))
        logger.debug(f"[Socket] Bound to {host}:{port}.")

    def listen(self, queue: int = 10) -> None:
        """
        mark a connection-mode socket, specified by the socket argument, as accepting connections.

        P:
        queue(int): Amount of connection to listen.

        Returns:
        None.
        """
        self.skt.listen(queue)

    def accept(self):
        """
        extracts the first  connection request on the queue of pending connections for the
        listening socket, sockfd, creates a new connected socket, and  returns a new file 
        descriptor referring to that socket.

        Parameters:
        None

        Returns:
        peer(socket): Un socket with the same  protocol and familiy type
        """
        logger.debug("[Socket] Accepting client...")
        peer, addr = self.skt.accept()
        logger.debug(f"[Socket] Client connected from {addr[0]}:{addr[1]}.")
        return Socket(peer)

    def close(self) -> None:
        """
        Close the socket

        Parameters:
        None.

        Returns:
        None.
        """
        try:
            logger.debug("[Socket] Closing socket...")
            self.skt.shutdown(SHUT_RDWR)
            self.skt.close()
            logger.debug("[Socket] Socket closed.")
        except OSError:
            return

    def send(self, data: bytearray) -> None:
        """
        Initiate transmission of a message from the specified socket to its peer. 

        Parameters:
        data(bytearray): Data in binary format.

        Returns:
        None.
        """
        total_bytes = len(data)
        bytes_sent = 0
        while bytes_sent < total_bytes:
            last_sent = self.skt.send(data[bytes_sent:])
            stats['bytes']['sent'] += last_sent
            if last_sent == 0:
                raise RuntimeError("Socket closed by the peer.")

            bytes_sent += last_sent

    def recv(self, size: int) -> bytearray:
        """
        Receives data on a socket with descriptor socket and stores it in a buffer.

        Parameters:
        size(int): The size of buffer that need to be stored.

        Returns:
        None.
        """
        data = []
        bytes_recd = 0
        while bytes_recd < size:
            segment = self.skt.recv(size - bytes_recd)
            stats['bytes']['recd'] += len(segment)
            if segment == b'':
                raise RuntimeError("Socket closed by the peer.")
            data.append(segment)
            bytes_recd += len(segment)

        return b''.join(data)

    def __del__(self):
        """
        Destory the class

        Parameters:
        None.

        Returns:
        None.
        """
        self.close()
