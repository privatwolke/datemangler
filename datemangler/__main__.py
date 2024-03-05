#!/usr/bin/env python

import argparse
import getpass
from base64 import urlsafe_b64encode
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import datemangler


def main():
    parser = argparse.ArgumentParser(description='Hide and retrieve data in NTFS timestamps. If no input is given, the program reads from standard input.')
    parser.add_argument('mode', choices=['read', 'write'], help='read or write data to a file or directory of files')
    parser.add_argument('path', help='single file or directory of files')
    parser.add_argument('-R', dest='recursive', action='store_true', help='handle directories recursively')
    parser.add_argument('-i', dest='input', help='input to be hidden')
    parser.add_argument('-l', dest='payload_length', help='length of the payload to be read')
    args = vars(parser.parse_args())

    salt = getpass.getpass(prompt='Salt: ')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=bytes.fromhex(salt),
        iterations=480000,
    )

    password = getpass.getpass(prompt='Password: ')
    cipher = Cipher(algorithms.AES(kdf.derive(password.encode('utf-8'))), modes.CTR(bytes.fromhex(salt)))

    path = Path(args['path'])

    if args['mode'] == 'read':

        if path.is_file():
            print(datemangler.read(path, cipher))

        elif path.is_dir():
            print(datemangler.read_directory(path, cipher, int(args['payload_length'])))

    else:
        if path.is_file():
            datemangler.write(path, args['input'], cipher)

        elif path.is_dir():
            datemangler.write_directory(path, args['input'], cipher)
            print(f'Payload length was {len(args["input"])}')


if __name__ == '__main__':
    main()
