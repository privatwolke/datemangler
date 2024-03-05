#!/bin/bash

truncate --size 20M volume
mkfs.ntfs -F volume
mkdir test
mount volume test/
cd test
for i in {0..100}; do touch $i; done

bash

cd ..
umount test