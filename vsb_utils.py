"""Generic utilities needed for other parts to work."""

import json
import vsb_consts as consts
import shutil
import os
import datetime
import time
import tarfile
import glob


def loadJsonFile(filename):
    """Load JSON file given."""
    data = None
    with open(filename) as data_file:
        data = json.load(data_file)
    print("Settings loaded from", filename, " :", data)
    return data


def tmpBackupDir(settings):
    """Give the tmp directory to build a backup tree."""
    path = os.path.join(settings['tmp_dir'], consts.dir_root)
    return path


def clearTmp(settings, sections):
    """Clear temporary files."""
    path = tmpBackupDir(settings)
    if os.path.exists(path):
        print("Removing tmp files: ", path)
        shutil.rmtree(path)
    # call(["rm", "-rf", path])


def genTimestamp():
    """Return a timestamp from now."""
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dat%H:%M:%S')


def compress(src, dst):
    """Compress src directory and content to src tar.gz."""
    directory = os.path.dirname(dst)
    if not os.path.exists(directory):
        os.makedirs(directory)
    tar = tarfile.open(dst, "w:gz")
    for file_name in glob.glob(os.path.join(src, "*")):
        print("  Adding %s..." % file_name)
        print(os.path.basename(file_name))
        tar.add(file_name, os.path.basename(file_name))
    tar.close()
    pass


def copy(src, dst):
    """Copy src to dst regardless it's a file or directory."""
    if os.path.isfile(src):
        shutil.copy2(src, dst)
    elif os.path.isdir(src):
        os.mkdir(dst)
        shutil.copymode(src, dst)
    pass
