# CMakeHelpers 0.1

There are many times that I want to either move a configured cmake
project, or clone one. CMake expands the relative paths to be in
relation to the build directory, so simple `mv` will cause the
CMakeCache to need re-building, losing the desired configuration.

My goal in the project is to build a small suite of helper tools that
can assist with copying, moving, and doing simple operations with cmake
build directories.

# Usage

After moving or copying, run `cmake .` in the new build directory to
have CMake fix the rest of the build system (either the makefile or the
ninja.rules).

## cmake-mv

CMake move moves the build directory of a cmake project and fixes the
paths to point to the new build directory location.

```sh
usage: cmake-mv [-h] SOURCE DESTINATION
```

## cmake-cp

CMake copy makes a copy of the build directory pointed at by SOURCE into
a new build directory, DESTINATION, fixing the build directory location
in the CMakeCache file to point to the new build directory.

```sh
usage: cmake-cp [-h] SOURCE DESTINATION
```


# Installation

This is written with the same design as the BusyBox project. All of the
parts are in one program, then that program uses the name of the calling
script to determine what it should actually do.

Right now the program knows how to operate under two names
- cmake-cp
- cmake-mv

The actual program is under the name "cmake-helpers".
If you just try to run cmake-helpers directly, it will give an error
message saying that it doesn't know how to run under that name.

To install the program, move the `cmake-helpers` to some directory (I
usually keep this in `/usr/local/src`), then create symbolic links from
a directory that is in your path. (I usually keep it in
`/usr/local/bin`).

Assuming you've cloned the CMakeHelpers repository into
`/usr/local/src`, this is how you can "install" the helpers.

```sh
cd /usr/local/bin
ln -s /usr/local/src/CMakeHelpers/cmake-helpers cmake-cp
ln -s /usr/local/src/CMakeHelpers/cmake-helpers cmake-mv
```


# Requirements

This program is written for python 3.x.
I've written it with python 3.7.1, but I don't think I used any features
that require python 3.6 or above.

# Author(s)

- Evan Wilde <etceterawilde@gmail.com>

# License

These tools are under the BSD-3 license, which are consistent with
CMake. If you can use CMake, you probably can use these tools.
