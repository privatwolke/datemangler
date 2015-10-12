datemangler
===========

This script modifies the last four bits of an NTFS timestamp to hide information.
Data entered is encrypted with AES.


Installation
------------

Get the latest version with `pip install datemangler`.


Notes about Dependencies
------------------------

This program requires the `xattr` package to function which will only install
if the development files for `libffi` are installed. Use `sudo apt-get install
libffi-dev` on Debian/Ubuntu before installing `xattr` or this package.

The datemangler package is a universal package that is compatible with both
python 2 and 3.


Usage example
-------------

	# create test file system in a file
	$ truncate --size 20M volume
	$ mkfs.ntfs -F volume
	$ mount volume test/

	# create test files
	$ for i in {0..100}; do touch $i; done

	# write to a single file
	$ datemangler -i "helo" write 0

	# read again
	$ datemangler read 0

	# write more text to a directory of files
	$ datemangler -i "hello world, how are you?" write .

	# read again
	$ datemangler read .


Notes
-----

This script has been tested successfully on the following platforms:

* Ubuntu 12.10 with kernel 3.5.0-18-generic x64 with ntfs-3g 2012.1.15AR.5 external FUSE 29
* Debian testing with kernel 4.2.0-1-amd64 with ntfs-3g 2015.3.14AR.1 integrated FUSE 28

Note that the script must be run on files in an NTFS volume!
