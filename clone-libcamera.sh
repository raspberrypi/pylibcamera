#!/bin/bash

rm -rf libcamera

git clone git@github.com:raspberrypi/libcamera.git libcamera
pushd libcamera

git checkout release-v0.0.5+83-bde9b04f
git apply ../pypatch.patch

popd
