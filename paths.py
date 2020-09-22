import os
import sys

base_dir = sys.argv[1]  # Root of the FTP filesystem


def assemble_ftp_path(*paths):
    """Returns the combined base directory and path components"""
    return os.path.join(base_dir, *paths)
