from lib.socket_tcp import Socket
from os import SEEK_END


MAX_NAME = 255
INT_ENCODING = 'big'

# sizes
OPCODE_SIZE = 1
INT_SIZE = 8
CHUNK_SIZE = 1024

# opcodes
UPLOAD_FILE_OP = 0
DOWNLOAD_FILE_OP = 1
LIST_FILES_OP = 2


def decode_int(bytes: bytearray) -> int:
    return int.from_bytes(bytes, INT_ENCODING)


def encode_int(i: int) -> bytearray:
    return i.to_bytes(INT_SIZE, INT_ENCODING)


def recv_opcode(skt: Socket) -> int:
    return int.from_bytes(skt.recv(OPCODE_SIZE), INT_ENCODING)


def send_opcode(skt: Socket, opcode: int) -> None:
    skt.send(opcode.to_bytes(OPCODE_SIZE, INT_ENCODING))


def recv_filename(skt: Socket) -> str:
    filename_size = decode_int(skt.recv(INT_SIZE))
    filename = skt.recv(filename_size).decode()
    return filename


def recv_file(skt: Socket):
    file_size = decode_int(skt.recv(INT_SIZE))
    if file_size < 0:
        pass

    recd = 0
    while recd < file_size:
        file_chunk = skt.recv(min(file_size - recd, CHUNK_SIZE))
        recd += len(file_chunk)
        yield file_chunk


def send_filename(skt: Socket, filename: str) -> None:
    bytes = filename.encode()
    skt.send(encode_int(len(bytes)))
    skt.send(bytes)


def send_file(skt: Socket, f):

    f.seek(0, SEEK_END)
    filesize = f.tell()
    f.seek(0)

    skt.send(encode_int(filesize))

    chunk = f.read(CHUNK_SIZE)
    while chunk:
        skt.send(chunk)
        chunk = f.read(CHUNK_SIZE)


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

    return list(map(eval, (''.join(chunks)).split('\n')))
