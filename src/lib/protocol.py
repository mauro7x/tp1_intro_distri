from os import SEEK_END
from lib.socket_tcp import Socket

# -----------------------------------------------------------------------------
# constants

# config
INT_ENCODING = 'big'

# sizes
OPCODE_SIZE = 1
STATUS_SIZE = 1
INT_SIZE = 8
CHUNK_SIZE = 1024

# opcodes
UPLOAD_FILE_OP = 0
DOWNLOAD_FILE_OP = 1
LIST_FILES_OP = 2

# status codes
NO_ERR = 0
UNKNOWN_OP_ERR = 1
FILE_NOT_FOUND_ERR = 2

# -----------------------------------------------------------------------------
# encoders/decoders


def encode_int(i: int) -> bytearray:
    return i.to_bytes(INT_SIZE, INT_ENCODING)


def decode_int(bytes: bytearray) -> int:
    return int.from_bytes(bytes, INT_ENCODING)

# -----------------------------------------------------------------------------
# wrappers


def send_status(skt: Socket, status: int) -> None:
    skt.send(status.to_bytes(STATUS_SIZE, INT_ENCODING))


def recv_status(skt: Socket) -> int:
    return int.from_bytes(skt.recv(STATUS_SIZE), INT_ENCODING)


def send_opcode(skt: Socket, opcode: int) -> None:
    skt.send(opcode.to_bytes(OPCODE_SIZE, INT_ENCODING))


def recv_opcode(skt: Socket) -> int:
    return int.from_bytes(skt.recv(OPCODE_SIZE), INT_ENCODING)


def send_filename(skt: Socket, filename: str) -> None:
    bytes = filename.encode()
    skt.send(encode_int(len(bytes)))
    skt.send(bytes)


def recv_filename(skt: Socket) -> str:
    filename_size = decode_int(skt.recv(INT_SIZE))
    filename = skt.recv(filename_size).decode()
    return filename


def send_file(skt: Socket, f):

    f.seek(0, SEEK_END)
    filesize = f.tell()
    f.seek(0)

    skt.send(encode_int(filesize))

    chunk = f.read(CHUNK_SIZE)
    while chunk:
        skt.send(chunk)
        chunk = f.read(CHUNK_SIZE)


def recv_file(skt: Socket):
    file_size = decode_int(skt.recv(INT_SIZE))
    if file_size < 0:
        pass

    recd = 0
    while recd < file_size:
        file_chunk = skt.recv(min(file_size - recd, CHUNK_SIZE))
        recd += len(file_chunk)
        yield file_chunk


def send_list(skt: Socket, list: list) -> None:
    bytes = ('\n'.join(map(str, list))).encode()

    skt.send(encode_int(len(bytes)))
    chunks = [bytes[i:i+CHUNK_SIZE] for i in range(0, len(bytes), CHUNK_SIZE)]

    for chunk in chunks:
        skt.send(chunk)


def recv_list(skt: Socket) -> list:
    total_len = decode_int(skt.recv(INT_SIZE))

    chunks = []
    recd = 0
    while recd < total_len:
        chunk = skt.recv(min(total_len - recd, CHUNK_SIZE))
        recd += len(chunk)
        chunks.append(chunk.decode())

    if chunks:
        return list(map(eval, (''.join(chunks)).split('\n')))
    return []

# -----------------------------------------------------------------------------
# error msgs


def get_error_msg(err_code: int) -> str:
    if err_code == UNKNOWN_OP_ERR:
        return "Opcode desconocido por el servidor."
    elif err_code == FILE_NOT_FOUND_ERR:
        return "El archivo no existe en el servidor."

    return ""


# -----------------------------------------------------------------------------
