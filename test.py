#!/usr/bin/env python3

import cmakehelpers
import unittest
import os
import shutil


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


class CreateDestination(unittest.TestCase):
    """
    Test the behaviour of the create_destination function
    """

    dirname = os.path.join(os.path.abspath("tests"), "CreateDestination")

    def cleanup(self):
        """
        Setup a directory structure

        Should make a directory in tests called "CreateDestination"
        """
        if os.path.exists(self.dirname):
            shutil.rmtree(self.dirname)
        os.mkdir(self.dirname)

    def test_exists(self):
        """
        Test the behaviour of create_destination when the test directory
        exists
        """
        self.cleanup()

        # Add something to the directory
        with open(os.path.join(self.dirname, "tmpfile.txt"), "w") as tmp_file:
            tmp_file.write("Hello to whom it may concern, this is a temp file\n")

        # Default (without overwrite) should throw an error and not delete the file
        with self.assertRaises(FileExistsError):
            cmakehelpers.create_destination(self.dirname, False)
        self.assertTrue(os.path.exists(os.path.join(self.dirname, "tmpfile.txt")))

        # Not overwriting should throw an error and not delete the file
        with self.assertRaises(FileExistsError):
            cmakehelpers.create_destination(self.dirname, False)
        self.assertTrue(os.path.exists(os.path.join(self.dirname, "tmpfile.txt")))

        # With overwriting enabled should delete remove anything that
        # was already there
        cmakehelpers.create_destination(self.dirname, True)
        self.assertFalse(os.path.exists(os.path.join(self.dirname, "tmpfile.txt")))

    def test_not_exits(self):
        """
        Test the behaviour of create_destination when the destination
        doesn't already exist.
        """
        self.cleanup()

        # Default case
        self.assertFalse(os.path.exists(os.path.join(self.dirname, "test1")))
        cmakehelpers.create_destination(os.path.join(self.dirname, "test1"))
        self.assertTrue(os.path.exists(os.path.join(self.dirname, "test1")))

        # Not overwrite case
        self.assertFalse(os.path.exists(os.path.join(self.dirname, "test2")))
        cmakehelpers.create_destination(os.path.join(self.dirname, "test2"), False)
        self.assertTrue(os.path.exists(os.path.join(self.dirname, "test2")))

        # Overwrite case
        self.assertFalse(os.path.exists(os.path.join(self.dirname, "test3")))
        cmakehelpers.create_destination(os.path.join(self.dirname, "test3"), True)
        self.assertTrue(os.path.exists(os.path.join(self.dirname, "test3")))


if __name__ == "__main__":
    unittest.main()
