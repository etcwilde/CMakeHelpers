from cmakehelpers.errors import IncorrectFileError
from cmakehelpers.CMake import change_base_dir, get_cache_name

import os
import shutil


# Helper functions

def create_destination(dirname, overwrite=False):
    """
    Create a destination directory, optionally overwriting the original

    :dirname: The directory to create
    :overwrite: Overwrite if the directory/file already exists
    """
    # Delete the original if we're allowed to
    if os.path.exists(dirname):
        if overwrite:
            shutil.rmtree(dirname)
        else:
            raise FileExistsError(dirname)
    os.mkdir(dirname)
