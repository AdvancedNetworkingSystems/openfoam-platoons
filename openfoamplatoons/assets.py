from os import path
import sys
from csv import DictReader

from PyQt5.QtCore import QDir

from openfoamplatoons.settings import ICONS_DIR, IMAGES_DIR, STL_DIR, REFERENCE_MEASURES_FILE


def icon(fileName):
    return path.join(ICONS_DIR, fileName)


def image(fileName):
    return path.join(IMAGES_DIR, fileName)


def availableStl():
    qDir = QDir(STL_DIR, '*.stl')
    return qDir.entryList(QDir.Files)


def referenceLength(fileName) -> float:
    with open(path.join(STL_DIR, REFERENCE_MEASURES_FILE), 'r') as f:
        myDict = DictReader(f)
        for row in myDict:
            if row['stl'] == fileName:
                return float(row['referenceLength'])


def referenceArea(fileName) -> float:
    with open(path.join(STL_DIR, REFERENCE_MEASURES_FILE), 'r') as f:
        myDict = DictReader(f)
        for row in myDict:
            if row['stl'] == fileName:
                return float(row['referenceArea'])
