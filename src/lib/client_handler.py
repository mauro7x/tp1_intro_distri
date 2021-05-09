from threading import Thread
from itertools import count as it_count
from lib.socket_tcp import Socket
from lib.logger import logger
import lib.protocol as prt


def _handle_upload_file(skt: Socket) -> None:
    filename = prt.recv_filename(skt)

    with open(filename, 'wb') as f:
        for file_chunk in prt.recv_file(skt):
            f.write(file_chunk)


def _handle_download_file(skt: Socket) -> None:
    pass


def _handle_list_files(skt: Socket) -> None:
    pass


def _handle_unknown_cmd(skt: Socket) -> None:
    pass


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

        opcode = self.skt.recv(prt.OPCODE_SIZE)
        opcode = prt.decode_opcode(opcode)

        if opcode == prt.UPLOAD_FILE_OP:
            _handle_upload_file(self.skt)

        elif opcode == prt.DOWNLOAD_FILE_OP:
            _handle_download_file(self.skt)

        elif opcode == prt.LIST_FILES_OP:
            _handle_list_files(self.skt)

        else:
            _handle_unknown_cmd(self.skt)

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
