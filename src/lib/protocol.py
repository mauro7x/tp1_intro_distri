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
    """
    Encode the integer type value to binary type.

    Parameters:
    i(int): An integer number.

    Returns:
    bytes(bytearray): A binary value.
    """

    return i.to_bytes(INT_SIZE, INT_ENCODING)


def decode_int(bytes: bytearray) -> int:
    """
    Decode the binary value to an integer value.


    Parameters:
    bytes(bytearray): Binary value.

    Returns:
    i(int): An integer number.
    """
    return int.from_bytes(bytes, INT_ENCODING)

# -----------------------------------------------------------------------------
# wrappers


def send_status(skt: Socket, status: int) -> None:
    """
    send the opcode of status in binary format.

    Parameters:
    skt(socket): Socket.
    status(int): Opcode of status.

    Returns:
    None
    """
    skt.send(status.to_bytes(STATUS_SIZE, INT_ENCODING))


def recv_status(skt: Socket) -> int:
    """
    Receive the status opcode and return it with integer value.

    Parameters:
    skt(socket): Socket.

    Returns:
    opcode(int): Opcode of status.
    """
    return int.from_bytes(skt.recv(STATUS_SIZE), INT_ENCODING)


def send_opcode(skt: Socket, opcode: int) -> None:
    """
    Send the command opcode in binary format.

    Parameters:
    skt(socket): Socket.
    status(int): Command opcode

    Returns:
    None
    """
    skt.send(opcode.to_bytes(OPCODE_SIZE, INT_ENCODING))


def recv_opcode(skt: Socket) -> int:
    """
    Receives the command opcode and return it with integer value.

    Parameters:
    skt(socket): Socket.

    Returns:
    opcode(int): Command opcode.
    """
    return int.from_bytes(skt.recv(OPCODE_SIZE), INT_ENCODING)


def send_filename(skt: Socket, filename: str) -> None:
    """
    Send the filename with binary formate

    Parameters:
    skt(socket): Socket.
    filename(str): the name of file.

    Returns:
    None
    """
    bytes = filename.encode()
    skt.send(encode_int(len(bytes)))
    skt.send(bytes)


def recv_filename(skt: Socket) -> str:
    """
    Receives the filename and return it with string type.

    Parameters:
    skt(socket): Socket.

    Returns:
    filename(str): The name of file.
    """
    filename_size = decode_int(skt.recv(INT_SIZE))
    filename = skt.recv(filename_size).decode()
    return filename


def send_file(skt: Socket, f):
    """
    Send the file with binay format

    Parameters:
    skt(socket): Socket.
    f(FILE): The file.

    Returns:
    None
    """
    f.seek(0, SEEK_END)
    filesize = f.tell()
    f.seek(0)

    skt.send(encode_int(filesize))

    chunk = f.read(CHUNK_SIZE)
    while chunk:
        skt.send(chunk)
        chunk = f.read(CHUNK_SIZE)

    if (e := recv_status(skt)) != NO_ERR:
        raise RuntimeError(get_error_msg(e))


def recv_file(skt: Socket):
    """
    Receive the file and write it into a new file.

    Parameters:
    skt(socket): Socket.

    Returns:
    None
    """
    file_size = decode_int(skt.recv(INT_SIZE))
    if file_size < 0:
        pass

    recd = 0
    while recd < file_size:
        file_chunk = skt.recv(min(file_size - recd, CHUNK_SIZE))
        recd += len(file_chunk)
        yield file_chunk

    send_status(skt, NO_ERR)


def send_list(skt: Socket, list: list) -> None:
    """
    Send the list of information about the file with binary format.

    Parameters:
    skt(socket):Socket.
    list(list): List of information about the file.

    Returns:
    None
    """
    bytes = ('\n'.join(map(str, list))).encode()

    skt.send(encode_int(len(bytes)))
    chunks = [bytes[i:i+CHUNK_SIZE] for i in range(0, len(bytes), CHUNK_SIZE)]

    for chunk in chunks:
        skt.send(chunk)


def recv_list(skt: Socket) -> list:
    """
    Receives the list of information about file and return the list

    Parameters:
    skt(socket): Socket.

    Returns:
    list(list): List of information about the file.
    """
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
    """
    Receives the error code and return the related message.

    Parameters:
    err_code(int): The code of error.

    Returns:
    mensaje(str): The message of error.
    """
    if err_code == UNKNOWN_OP_ERR:
        return "Opcode desconocido por el servidor."
    elif err_code == FILE_NOT_FOUND_ERR:
        return "El archivo no existe en el servidor."

    return ""


# -----------------------------------------------------------------------------
