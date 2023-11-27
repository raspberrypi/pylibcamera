# Pylibcamera
This package is for the libcamera python bindings only. It requires you to already have installed a version of libcamera onto your system.

## Installation Instructions
These instructions are designed for use in a python virtual environment. If you are using the system python then it is much simpler to install the system apt package for the libcamera python bindings (eg `sudo apt install python3-libcamera`), as these will match the version of libcamera correctly.

The default installation instructions (which work on Raspberry Pi OS) are:
```
sudo apt install -y libcamera-dev
pip install libcamera
```
If you have an older release of libcamera on your system then you may need to use `libcamera==version` to install the correct release.

### If you get a version error
If you get the error `This package works with libcamera version ..., but you have version ... installed`, then this means the version strings are not matching. If you have built your own version of libcamera, then just pass `-C setup-args="-Dversion=unknown"` to skip this check and follow the instructions in the next section. If you have a system installed version of libcamera then you will need to check this table for the correct pip package version to install, based on the version of libcamera you have installed. These are the common versions found on Raspberry Pis.

| system and date | libcamera reported version | pip package version |
| --------------- | -------------------------- | ------------------- |
| Raspberry Pi Bookworm 22/11/2023 | v0.1.0+118-563cd78e | 0.1a2 |

### If that doesn't work...

If you have built your own version of libcamera, or your system has a version which is not compatible with a release version, then you may need to pass the repository and revision to meson. The arguments to do this are `-C setup-args="-Drepository=https://my.repository.git"` for the repository and `-C setup-args="-Drevision=branch"` for the revision. These are passed directly into `git clone` and `git checkout` respectively, so and strings that work with those will work here. The `-C, --config-settings` argument require an up to date version of `pip>=23.1` so you may first need to run `pip install --upgrade pip`

For example, the if you have built the master version of libcamera on your system, then you would run:
```
pip install libcamera -C setup-args="-Drevision=master"
```

If you have built the main version from the Raspberry Pi repository then you would use:
```
pip install libcamera -C setup-args="-Drepository=https://github.com/raspberrypi/libcamera.git" -C setup-args="-Drevision=main"
```

## How it works
This package works by building just the libcamera python bindings against your existing version of libcamera. It does this by cloning the libcamera repository and checking out the specified revision. A patch (pypatch.patch) is then applied to modify the src/py/libcamera/meson.build file to prevent building of the existing python bindings and allow for the building of custom ones using the meson-python build system. Finally, the build includes the subdirectory libcamera/src/py to only include the files required for the python bindings, rather than building the whole of libcamera.
