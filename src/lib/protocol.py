from lib.socket_tcp import Socket

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


def recv_filename(skt: Socket) -> str:
    filename_size = decode_int(skt.recv(INT_SIZE))
    filename = skt.recv(filename_size).decode()
    return filename


def recv_file(skt: Socket):
    file_size = decode_int(skt.recv(INT_SIZE))

    recd = 0
    while recd < file_size:
        file_chunk = skt.recv(min(file_size - recd, CHUNK_SIZE))
        recd += len(file_chunk)
        yield file_chunk.decode()


def decode_int(bytes: bytearray) -> int:
    return int.from_bytes(bytes, INT_ENCODING)


# old -------------------------------------------------------------------------

def send_notification(name, dst):
    if len(dst) > MAX_NAME:
        raise ValueError(f"Destination file name is to large {len(dst)}")

    with open(name, "rb") as f:
        f.seek(-1)
        size = f.tell()
        f.seek(0)

    return size.to_bytes(INT_LENGHT, INT_ENCODING) + dst.encode()


def send_file(name):
    with open(name, "rb") as f:
        while not f.feof():
            yield f.read(CHUNK_SIZE)


def recv_notification(buffer):
    size = int.from_bytes(buffer[:INT_LENGHT], INT_ENCODING)
    src = buffer[INT_LENGHT:].decode()

    return size, src


def recv_file(src, buffer):
    total_size = 0

    with open(src, "wb") as f:
        for b in buffer:
            f.write(b)
            total_size += len(b)

    return total_size
