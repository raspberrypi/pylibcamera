# SPDX-License-Identifier: CC0-1.0

project('pylibcamera', 'c', 'cpp',
    meson_version : '>= 0.64',
    version : '0.1.0',
    default_options : [
        'werror=true',
        'warning_level=2',
        'cpp_std=c++17',
    ],
    license : 'LGPL 2.1+')

if not get_option('pycamera').enabled()
    error('pycamera must be enabled')
endif

message('Cloning from: @0@, revision @1@'.format(get_option('repository'), get_option('revision')))

run_command('clone-libcamera.sh', get_option('repository'), get_option('revision'), get_option('patch'), check : true)

r = run_command('check-version.sh', capture : true, check : false)
if r.returncode() == 0 and get_option('version') != 'unknown'
    version = r.stdout()
    message('libcamera version is @0@'.format(version))
    if version.strip() != get_option('version').strip()
        error('This package works with libcamera version @0@, but you have version @1@ installed. Please check the readme for help with this error'.format(get_option('version'), version))
    endif
else
    message('Version Check Not Done')
endif

libcamera_includes = include_directories('libcamera/include')
libcamera_private = dependency(
    'libcamera', required : true,
    not_found_message : 'Requires libcamera-dev package to be installed - apt install libcamera-dev'
)

py = import('python').find_installation()

subdir('libcamera/src/py')

message('Using python version @0@ from @1@'.format(py.version(), py.full_path()))

py.install_sources(
    'libcamera/src/py/libcamera/__init__.py',
    subdir : 'libcamera',
    pure : false,
)

py.extension_module(
    '_libcamera',
    pycamera_sources,
    install : true,
    subdir : 'libcamera',
    dependencies : pycamera_deps,
    include_directories : libcamera_includes,
    cpp_args : pycamera_args,
)
