#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import os
import sys
import xattr

try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO

from Crypto.Cipher import AES


class DateMangler:

	def listdir_recursive(self, path, depth = -1):
		files = []

		if depth == 0: return files

		try:
			for entry in os.listdir(path):
				current = os.path.join(path, entry)

				if os.path.isfile(current):
					files.append(current)

				elif os.path.isdir(current):
					files += listdir_recursive(current, depth = depth - 1)

		except OSError:
			# ignore directories for which we don't have permission
			pass

		return files


	def available_space(self, path, depth = -1):
		return 4 * len(listdir_recursive(path, depth = depth))


	def padding(self, secret, blocksize = 32, padding = '!'):
		if not len(secret) in (16, 24, 32):
			return secret + (blocksize - len(secret)) * padding
		return secret


	def encrypt(self, plaintext, secret):
		enc = AES.new(self.padding(secret), AES.MODE_CFB, IV = self.padding(secret, blocksize = 16))
		return enc.encrypt(plaintext)


	def decrypt(self, ciphertext, secret):
		enc = AES.new(self.padding(secret), AES.MODE_CFB, IV = self.padding(secret, blocksize = 16))
		return enc.decrypt(ciphertext)


	def write(self, file, bytes, password):
		attributes = xattr.xattr(file)
		try:
			crtime = attributes.get("system.ntfs_crtime")
			attributes.set("system.ntfs_crtime", crtime[:4] + self.encrypt(bytes[:4], password))
		except IOError:
			print("Cannot access NTFS attributes. Are you on an NTFS volume?", file = sys.stderr)


	def read(self, file, password):
		attributes = xattr.xattr(file)
		try:
			crtime = attributes.get("system.ntfs_crtime")
			return self.decrypt(crtime[-4:], password)
		except IOError:
			print("Cannot access NTFS attributes. Are you on an NTFS volume?", file = sys.stderr)


	def read_directory(self, path, password):
		return "".join([self.read(x, password) for x in filter(lambda x: os.path.isfile(os.path.join(path, x)), os.listdir(path))])


	def write_directory(self, path, bytes, password):
		buffer = StringIO(bytes)
		for file in filter(lambda x: os.path.isfile(os.path.join(path, x)), os.listdir(path)):
			b = buffer.read(4)
			if len(b) == 0:
				break

			self.write(file, self.padding(b, blocksize = 4, padding = " "), password)
