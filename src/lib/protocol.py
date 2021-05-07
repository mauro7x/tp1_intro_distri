
CHUNK_SIZE = 1024
MAX_NAME = 255
INT_LENGHT = 8
INT_ENCODING = 'big'


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
