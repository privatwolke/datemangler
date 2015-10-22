#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os
import argparse
import getpass

try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO

from datemangler import DateMangler

def main():
	parser = argparse.ArgumentParser(description = "Hide and retrieve data in NTFS timestamps. If no input is given, the program reads from standard input.")
	parser.add_argument("mode", choices = ["read", "write"], help = "read or write data to a file or directory of files")
	parser.add_argument("path", help = "single file or directory of files")
	parser.add_argument("-R", dest = "recursive", action = "store_true", help = "handle directories recursively")
	parser.add_argument("-i", dest = "input", help = "input to be hidden")
	args = vars(parser.parse_args())

	dm = DateMangler()

	if (args["mode"] == "read"):

		if (os.path.isfile(args["path"])):
			print(dm.read(args["path"], getpass.getpass()))

		elif (os.path.isdir(args["path"])):
			print(dm.read_directory(args["path"], getpass.getpass()))

	else:

		if (os.path.isfile(args["path"])):
			dm.write(args["path"], args["input"], getpass.getpass())

		else:
			dm.write_directory(args["path"], args["input"], getpass.getpass())


if __name__ == "__main__":
	main()
