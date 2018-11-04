#!/usr/bin/env python3

import cmakehelpers
import unittest
import os


class CacheFileNameTest(unittest.TestCase):
    """
    Test the cache name file getter

    Should throw FileNotFoundError when the dire
    """

    def test_not_found(self):
        with self.assertRaises(FileNotFoundError):
            cmakehelpers.get_cache_name("tests/GetCacheName/Incorrect")

    def test_wrong_file(self):
        with self.assertRaises(cmakehelpers.IncorrectFileError):
            cmakehelpers.get_cache_name("tests/GetCacheName/Incorrect/Wrong.txt")

    def test_found(self):
        dirname = os.path.join(*["tests", "GetCacheName", "Found"])

        correct_fname = os.path.abspath(os.path.join(dirname, "CMakeCache.txt"))
        fname = cmakehelpers.get_cache_name(dirname)
        self.assertEqual(correct_fname, fname)

        fname = cmakehelpers.get_cache_name(correct_fname)
        self.assertEqual(correct_fname, fname)


class ChangeBaseDir(unittest.TestCase):
    """
    Test the base build directory changer

    This is a non-permanent change and isn't written back.
    """

    def test_simple(self):
        """
        This is a very simple cmake configuration
        """

        # Name of the directory holding the CMakeCache file
        test_dirname = os.path.join("tests", "ChangeBase", "simple")
        test_fname = cmakehelpers.get_cache_name(test_dirname)

        # Name of the directory used to create the CMakeCache file
        cache_build_dirname = "/tmp/tests/build"
        cache_new_dirname = "/tmp/build"

        with open(test_fname, 'r') as input_file:
            lines = [line.rstrip() for line in input_file]

            new_lines = cmakehelpers.change_base_dir(cache_build_dirname,
                                                     cache_new_dirname,
                                                     lines)
            new_lines = list(new_lines)
            match_lines = cmakehelpers.change_base_dir(cache_new_dirname,
                                                       cache_build_dirname,
                                                       new_lines)
            match_lines = list(match_lines)
            self.assertNotEqual(lines, new_lines)
            self.assertEqual(lines, match_lines)

    def test_llvm(self):
        """
        This is a pretty complicated cmake configuration from LLVM

        This specific cmake file was giving some issues before.
        """
        # Where the CMakeCache.txt is kept for this test
        test_dirname = os.path.join("tests", "ChangeBase", "llvm")
        test_fname = cmakehelpers.get_cache_name(test_dirname)

        # Name of the directory used to "create" the CMakeCache file
        cache_build_dirname = "/tmp/llvm-build"
        cache_new_dirname = "/usr/src/llvm-build"

        # Test operates by moving it to the new directory and back again
        with open(test_fname, 'r') as input_file:
            lines = [line.rstrip() for line in input_file]
            new_lines = cmakehelpers.change_base_dir(cache_build_dirname,
                                                     cache_new_dirname,
                                                     lines)
            new_lines = list(new_lines)
            match_lines = cmakehelpers.change_base_dir(cache_new_dirname,
                                                       cache_build_dirname,
                                                       new_lines)
            match_lines = list(match_lines)
            self.assertEqual(lines, match_lines)
            self.assertNotEqual(lines, new_lines)


if __name__ == "__main__":
    unittest.main()
