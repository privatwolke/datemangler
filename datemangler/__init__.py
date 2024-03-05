import math
from io import StringIO
from pathlib import Path

import xattr
from cryptography.hazmat.primitives.ciphers import Cipher


def _padding(data: bytes, blocksize: int = 16) -> bytes:
    # We pad with NULLs to avoid overflowing any numerical limits in the last chunk.
    # This is probably very insecure. Don't do this in production.
    if len(data) != 16:
        return data + (blocksize - len(data)) * b'\x00'
    return data


def write(file: Path, value: str, cipher: Cipher):
    """
    Encrypts the value using the given cipher and hides the result in the
    creation timestamp of the file.

    :param file: path to file to mangle creation timestamp
    :param value: string to write (max. 4 characters)
    :param cipher: initialized cipher to perform encryption
    :return:
    """
    if len(value) > 4:
        raise RuntimeError('value too long')

    value = _padding(value.encode('utf'))
    enc = cipher.encryptor()
    chunk = enc.update(value) + enc.finalize()

    try:
        attributes = xattr.xattr(file)
        crtime = attributes.get('system.ntfs_crtime')
        attributes.set('system.ntfs_crtime', crtime[:4] + chunk)
    except IOError as exc:
        raise RuntimeError('Cannot write NTFS attributes. Are you on an NTFS volume?') from exc


def read(file: Path, cipher: Cipher) -> str:
    """
    Reads and decrypts data from the creation timestamp of the given file.

    :param file: path to file to read timestamp from
    :param cipher: initialized cipher to perform decryption
    :return: decrypted value
    """
    try:
        attributes = xattr.xattr(file)
        crtime = attributes.get('system.ntfs_crtime')
        dec = cipher.decryptor()
        plain = dec.update(crtime[-4:]) + dec.finalize()
    except IOError as exc:
        raise RuntimeError('Cannot read NTFS attributes. Are you on an NTFS volume?') from exc

    return plain.rstrip(b'\x00').decode('utf-8')


def read_directory(path: Path, cipher: Cipher, payload_size: int) -> str:
    """
    Reads and decrypts data from the creation timestamps of a list of files.
    :param path: directory to list files from
    :param cipher: initialized cipher to perform decryption
    :param payload_size: expected (decrypted) payload length
    :return: decrypted value
    """
    buffer = StringIO()
    for file in sorted(filter(lambda x: x.is_file(), path.glob('*')))[:math.ceil(payload_size / 4)]:
        buffer.write(read(file, cipher))

    return buffer.getvalue()


def write_directory(path: Path, value: str, cipher: Cipher):
    """
    Writes encrypted value by mangling the creation timestamps of as many files
    as needed in the given path.

    :param path: path to mangle timestamps in
    :param value: plaintext to write
    :param cipher: initialized cipher to perform encryption
    """
    buffer = StringIO(value)
    for file in sorted(filter(lambda x: x.is_file(), path.glob('*'))):
        b = buffer.read(4)
        if len(b) == 0:
            break

        write(file, b, cipher)
