#!/bin/bash

cc check-version.cpp -I libcamera/include -lcamera -lstdc++ -o check-version

./check-version
