# datemangler

This module modifies the last four bits of an NTFS timestamp to hide information. 
Data entered is encrypted with AES.

Note: The cryptography settings used in this demo aren't production-ready. They were
mostly chosen to still fit the data into the timestamp bits. Do not rely on this for
anything.

## Installation

Get the latest version with `pip install datemangler`.

### Notes about dependencies

This program requires the `xattr` package to function which will only install if the development files for
`libffi` are installed. Use `sudo apt-get install libffi-dev` on Debian/Ubuntu before installing `xattr` or
this package.

The datemangler module has been tested with Python 3.11.

## Usage

The module comes with a script entrypoint which you can see in use in [test.sh](test.sh).
A Dockerfile has been included in this repository to enable testing on other platforms as well.
Note that the container needs to be run with `--privileged` since it needs to `mount` a dummy NTFS volume.

By default, it will run the tests of this project:
```shell
$ docker run --privileged --rm -it foo 
Initializing device with zeroes: 100% - Done.
Creating NTFS volume structures.
mkntfs completed successfully. Have a nice day.
..
----------------------------------------------------------------------
Ran 2 tests in 0.798s

OK
```

If you run it with `--entrypoint ./test.sh`, you will get an interactive shell to play around with:

```shell
$ docker run --privileged --entrypoint ./test.sh --rm -it foo
Initializing device with zeroes: 100% - Done.
Creating NTFS volume structures.
mkntfs completed successfully. Have a nice day.

root@dedb7779c2e8:/app/test# datemangler
usage: datemangler [-h] [-R] [-i INPUT] [-l PAYLOAD_LENGTH] {read,write} path

root@dedb7779c2e8:/app/test# datemangler -i "Hello my friend!" write .
Payload length was 16

root@dedb7779c2e8:/app/test# datemangler -l 16 read .
Hello my friend!

root@6b72ecc409c7:/app/test/test# datemangler -i foo write 0
root@6b72ecc409c7:/app/test/test# datemangler read 0
foo
```