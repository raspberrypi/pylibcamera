#!/bin/bash

rm -rf libcamera

git clone $1 libcamera
pushd libcamera

git checkout $2
git apply ../$3.patch

popd
