# Contains everything related to manipulating CMake Cache and
# CMake-specificities.

import os
from cmakehelpers.errors import IncorrectFileError


def get_cache_name(fname):
    """
    Gets the name of the cache if it exists, otherwise will throw an
    error

    :fname: Could be the build directory, or the name of a file
    :returns: The absolute path to the CMakeCache
    """
    if os.path.isdir(fname):
        fname = os.path.abspath(fname + '/CMakeCache.txt')
        if not os.path.exists(fname):
            raise FileNotFoundError(fname)
    if os.path.basename(fname) != 'CMakeCache.txt':
        raise IncorrectFileError(fname, 'CMakeCache.txt')
    return fname


def change_base_dir(olddirname, newdirname, lines):
    """
    Replace the old directory with the new directory

    :olddirname: Original build directory name
    :newdirname: New build directory name
    :lines: The input lines
    :returns: The fixed lines
    """
    for line in lines:
        if olddirname in line:
            line = line.replace(olddirname, newdirname)
        yield line
