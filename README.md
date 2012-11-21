date-mangler
============

This script modifies the last four bits of an NTFS timestamp to hide information.
Data entered is encrypted with AES.


Usage example
-------------

	# create test files
	$ for i in {0..100}; do touch $i; done

	# write to a single file
	$ date-manger -i "helo" write 0

	# read again
	$ date-mangler read 0

	# write more text to a directory of files
	$ date-mangler -i "hello world, how are you?" write .

	# read again
	$ date-mangler read .


Notes
-----

This script has been tested on Ubuntu 12.10 with kernel 3.5.0-18-generic x64 with ntfs-3g
2012.1.15AR.5 external FUSE 29. Note that the script must be run on files in an NTFS volume!