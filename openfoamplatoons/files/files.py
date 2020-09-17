from os import getcwd, listdir, path
from shutil import copytree, copy

from openfoamplatoons.settings import FOAM_DIR


def initCase():
    for item in listdir(FOAM_DIR):
        if path.isdir(path.join(FOAM_DIR, item)):
            copytree(path.join(FOAM_DIR, item), path.join(getcwd(), item))
        else:
            copy(path.join(FOAM_DIR, item), getcwd())
