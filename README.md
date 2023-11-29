# Pylibcamera
This package is for the libcamera python bindings only. It requires you to already have installed a version of libcamera onto your system.

## Caveats
***For most users this package is not the best approach to use libcamera in python - there are simpler ways***

**If you are able to use the system python**, then running `sudo apt install -y python3-libcamera` will install the libcamera python bindings in the simplest way.

**If you do require a virtual environment** (for example, in order to use a python package not available through apt) then the simplest way is to install the apt package and then create a virtual environment using system-site-packages.
```
sudo apt install -y python3-libcamera
python3 -m venv --system-site-packages my-env
```
This will allow you to use pip to install other packages in the virtual environment, while using the system versions of packages such as libcamera and PyQt5, which is a much simpler approach than pip installing these packages.

**If you must use this package** then be aware that there may be other troubleshooting required to get your virtual environment working correctly. For example, packages such as PyQt5 and OpenCV can require additional steps in order to pip install them, so it is much easier to apt install them and use a virtual environment with system-site-packages. If you have no other option but to use an isolated virtual environment (for example, if you require a different version of python to the system installed version), then this package will help with installing the libcamera python bindings, but be warned that other packages related to the camera will not be as easy to install.

## Installation Instructions
These instructions are designed for use in a python virtual environment. If you are using the system python then it is much simpler to install the system apt package for the libcamera python bindings (eg `sudo apt install -y python3-libcamera`), as these will match the version of libcamera correctly.

The default installation instructions (which work on Raspberry Pi OS) are:
```
sudo apt install -y libcamera-dev
pip install rpi-libcamera
```
If you have an older release of libcamera on your system then you may need to use `rpi-libcamera==version` to install the correct release.

To update your installation (which may be required when you update your version of libcamera) you can run `pip install --upgrade rpi-libcamera` to update to the latest version.

### If you get a version error
If you get the error `This package works with libcamera version ..., but you have version ... installed`, then this means the version strings are not matching. If you have built your own version of libcamera, then just pass `-C setup-args="-Dversion=unknown"` to skip this check and follow the instructions in the next section. If you have a system installed version of libcamera then you will need to check this table for the correct pip package version to install, based on the version of libcamera you have installed. You can see your currently installed version of libcamera by running `rpicam-hello --version`. These are the common versions found on Raspberry Pis.

| System and Date | libcamera Reported Version | Pip Package Version |
| --------------- | -------------------------- | ------------------- |
| Raspberry Pi Bookworm 22/11/2023 | v0.1.0+118-563cd78e | 0.1a2 |

### If that doesn't work...

If you have built your own version of libcamera, or your system has a version which is not compatible with a release version, then you may need to pass the repository and revision to meson. The arguments to do this are `-C setup-args="-Drepository=https://my.repository.git"` for the repository and `-C setup-args="-Drevision=branch"` for the revision. These are passed directly into `git clone` and `git checkout` respectively, so and strings that work with those will work here. The `-C, --config-settings` argument require an up to date version of `pip>=23.1` so you may first need to run `pip install --upgrade pip`

For example, the if you have built the master version of libcamera on your system, then you would run:
```
pip install rpi-libcamera -C setup-args="-Drevision=master"
```

If you have built the main version from the Raspberry Pi repository then you would use:
```
pip install rpi-libcamera -C setup-args="-Drepository=https://github.com/raspberrypi/libcamera.git" -C setup-args="-Drevision=main"
```

## How it works
This package works by building just the libcamera python bindings against your existing version of libcamera. It does this by cloning the libcamera repository and checking out the specified revision. A patch (pypatch.patch) is then applied to modify the src/py/libcamera/meson.build file to prevent building of the existing python bindings and allow for the building of custom ones using the meson-python build system. Finally, the build includes the subdirectory libcamera/src/py to only include the files required for the python bindings, rather than building the whole of libcamera.
