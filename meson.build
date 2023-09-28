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

message('Cloning from: @0@, revision @1@'.format(get_option('repository'), get_option('revision')))

r = run_command('clone-libcamera.sh', get_option('repository'), get_option('revision'), get_option('patch'), check : true)

libcamera_includes = include_directories('libcamera/include')
libcamera_private = dependency('libcamera', required : true)

py = import('python').find_installation()

subdir('libcamera/src/py')

message('Using python version @0@ from @1@'.format(py.version(), py.path()))

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
