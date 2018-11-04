import os

# Exceptions

class IncorrectFileError(Exception):
    def __init__(self, fname, expected_name):
        self.name = os.path.basename(expected_name)
        self.input_name = os.path.basename(fname)
