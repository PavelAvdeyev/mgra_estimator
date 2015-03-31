"""
    Some basic functions which needed to script
"""

import os


def get_immediate_subdirectories(a_dir):
    """
    This function get subdirectories
    """
    return ((os.path.join(a_dir, name), name) for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name)))


def get_immediate_files(a_dir):
    """
    This function get files
    """
    return ((os.path.join(a_dir, name), name) for name in os.listdir(a_dir) if
            os.path.isfile(os.path.join(a_dir, name)))


def which(program):
    """
    Mimics UNIX "which" command
    """

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None