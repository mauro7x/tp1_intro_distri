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
    Se transforma el numero entero al valor binario.

    Parametros:
    i(int): Un numero entero

    Returns:
    bytes(bytearray): El valor binario.
    """

    return i.to_bytes(INT_SIZE, INT_ENCODING)


def decode_int(bytes: bytearray) -> int:
    """
    Se transforma el numero binario a un valor entero

    Parametros:
    bytes(bytearray): Un numero binario

    Returns:
    i(int): El valor entero.
    """
    return int.from_bytes(bytes, INT_ENCODING)

# -----------------------------------------------------------------------------
# wrappers


def send_status(skt: Socket, status: int) -> None:
    """
    Se envia el estado en forma binaria.

    Parametros:
    skt(socket): un socket.
    status(int): El opcode del estado

    Returns:
    None
    """
    skt.send(status.to_bytes(STATUS_SIZE, INT_ENCODING))


def recv_status(skt: Socket) -> int:
    """
    Se recibe el opcode del estado y devolver en forma entero

    Parametros:
    skt(socket): un socket.

    Returns:
    opcode(int): El opcode del estado.
    """
    return int.from_bytes(skt.recv(STATUS_SIZE), INT_ENCODING)


def send_opcode(skt: Socket, opcode: int) -> None:
    """
    Se envia el estado del comando en forma binaria

    Parametros:
    skt(socket): un socket.
    status(int): El opcode del comando.

    Returns:
    None
    """
    skt.send(opcode.to_bytes(OPCODE_SIZE, INT_ENCODING))


def recv_opcode(skt: Socket) -> int:
    """
    Se recibe el opcode del comando y devolver en forma entero

    Parametros:
    skt(socket): un socket.

    Returns:
    opcode(int): El opcode del comando.
    """
    return int.from_bytes(skt.recv(OPCODE_SIZE), INT_ENCODING)


def send_filename(skt: Socket, filename: str) -> None:
    """
    Se envia el nombre del archivo en forma binaria

    Parametros:
    skt(socket): un socket.
    filename(str): El nombre del archivo

    Returns:
    None
    """
    bytes = filename.encode()
    skt.send(encode_int(len(bytes)))
    skt.send(bytes)


def recv_filename(skt: Socket) -> str:
    """
    Se recibe el nombre del archivo y devolver en forma cadena

    Parametros:
    skt(socket): un socket.

    Returns:
    filename(str): El nombre del archivo.
    """
    filename_size = decode_int(skt.recv(INT_SIZE))
    filename = skt.recv(filename_size).decode()
    return filename


def send_file(skt: Socket, f):
    """
    Se envia el archivo en forma binaria

    Parametros:
    skt(socket): un socket.
    f(FILE): El archivo que desea enviar

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


def recv_file(skt: Socket):
    """
    Se recibe el archivo y escribirlo en un archivo nuevo

    Parametros:
    skt(socket): un socket.

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


def send_list(skt: Socket, list: list) -> None:
    """
    Se envia la lista de informaciones en forma binaria

    Parametros:
    skt(socket): un socket.
    list(list): Una lista de informaciones

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
    Se recibe la lista desde socket y devolverla

    Parametros:
    skt(socket): un socket.

    Returns:
    list(list): Una lista de informaciones.
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
    Se recibe el error code y devolver el mensaje corresponde

    Parametros:
    err_code(int): El codigo del error.

    Returns:
    mensaje(str): El mensaje del error.
    """
    if err_code == UNKNOWN_OP_ERR:
        return "Opcode desconocido por el servidor."
    elif err_code == FILE_NOT_FOUND_ERR:
        return "El archivo no existe en el servidor."

    return ""


# -----------------------------------------------------------------------------
