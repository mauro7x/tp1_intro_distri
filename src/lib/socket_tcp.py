from socket import (socket, AF_INET, SOCK_STREAM, SHUT_RDWR,
                    SOL_SOCKET, SO_REUSEADDR)
from lib.logger import logger
from lib.stats import stats


class Socket:

    def __init__(self, skt: socket = None) -> None:
        """
        Inicializacion de la clase socket.

        Parametros:
        skt(socket): una clase de socket inicializado con valor NULL

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
        Conexion con la direccion y el puerto.

        Parametros:
        host(str): La direccion de host.
        port(int): EL numero de puerto.

        Returns:
        None.
        """
        logger.debug(f"[Socket] Connecting to {host}:{port}...")
        self.skt.connect((host, port))
        logger.debug(f"[Socket] Connected to {host}:{port}.")

    def bind(self, host: str, port: int) -> None:
        """
        Asignacion de un socket local con address a un socket que 
        esta identificado por file descriptor que no tiene un direccion
        local aun.

        Parametros:
        host(str): La direccion de host.
        port(int): EL numero de puerto.

        Returns:
        None.
        """
        logger.debug(f"[Socket] Binding to {host}:{port}...")
        self.skt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.skt.bind((host, port))
        logger.debug(f"[Socket] Bound to {host}:{port}.")

    def listen(self, queue: int = 10) -> None:
        """
        Establece a escuchar los requests de las conexiones de clientes

        Parametros:
        queue(int): Cantidad de conexiones a esuchar

        Returns:
        None.
        """
        self.skt.listen(queue)

    def accept(self):
        """
        Creacion de un nuevo socket descriptor con las mismas 
        propiedades y devolverlo a lo que llama.

        Parametros:
        None

        Returns:
        peer(socket): Un socket con el mismo protocolo y el tipo de familia.
        """
        logger.debug("[Socket] Accepting client...")
        peer, addr = self.skt.accept()
        logger.debug(f"[Socket] Client connected from {addr[0]}:{addr[1]}.")
        return Socket(peer)

    def close(self) -> None:
        """
        Se cierra el socket

        Parametros:
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
        Se envia los datos desde el socket corresponde

        Parametros:
        data(bytearray): Los datos en formato binario.

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
        Se recibe los datos a partir del socket

        Parametros:
        size(int): La cantidad de bytes de los datos va a recibir.

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
        Se destruye la clase

        Parametros:
        None.

        Returns:
        None.
        """
        self.close()
