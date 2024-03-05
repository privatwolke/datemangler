import platform
import secrets
import subprocess
import unittest
from base64 import urlsafe_b64encode
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import datemangler


class TestDateMangler(unittest.TestCase):
    test_volume = Path('test_volume')
    test_mount = Path('test_mount')

    @classmethod
    def setUpClass(cls):
        if platform.system() != 'Linux':
            raise RuntimeError('This test requires Linux.')

        cls.test_volume.unlink(missing_ok=True)
        test_volume_path = str(cls.test_volume.absolute())
        subprocess.run(['rm', '-rf', test_volume_path], check=True)
        subprocess.run(['truncate', '--size', '20M', test_volume_path], check=True)
        subprocess.run(['mkfs.ntfs', '-F', test_volume_path], check=True)

        cls.test_mount.mkdir(exist_ok=True)
        subprocess.run(['mount', test_volume_path, str(cls.test_mount.absolute())], check=True)

    @classmethod
    def tearDownClass(cls):
        subprocess.run(['umount', str(cls.test_mount.absolute())], check=True)

    def setUp(self):
        password = secrets.token_hex(16)

        for f in self.test_mount.glob('*'):
            f.unlink()

        for i in range(100):
            (self.test_mount / str(i)).touch(exist_ok=False)

        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )

        key = kdf.derive(password.encode('utf-8'))
        self.cipher = Cipher(algorithms.AES(key), modes.CTR(salt))

    def test_single_file(self):
        datemangler.write(self.test_mount / '0', 'foo', self.cipher)
        self.assertEqual(
            datemangler.read(self.test_mount / '0', self.cipher),
            'foo',
        )

    def test_multiple_files(self):
        datemangler.write_directory(self.test_mount, 'foo'*10, self.cipher)
        self.assertEqual(
            datemangler.read_directory(self.test_mount, self.cipher, len('foo'*10)),
            'foo'*10,
        )
