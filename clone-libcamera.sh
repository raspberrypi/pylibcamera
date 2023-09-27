#!/bin/bash

rm -rf libcamera

# mkdir libcamera
git clone --depth 1 git@github.com:raspberrypi/libcamera.git libcamera
pushd libcamera

# git init
# git remote add -f origin git@github.com:raspberrypi/libcamera-pi5.git
# git config core.sparsecheckout true
# cp ../sparse-checkout .git/info
# git checkout origin/main
git apply ../pypatch.patch

popd
