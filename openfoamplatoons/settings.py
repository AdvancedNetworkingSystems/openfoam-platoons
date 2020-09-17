from pkg_resources import resource_filename
from os import environ, path
import sys

APP_TITLE = 'OpenFOAM case builder for platoons'
APP_WIDTH = 800
APP_HEIGHT = 800

STL_DIR = environ.get('STL_DIR')
if not STL_DIR:
    sys.exit("Please declare environment variable 'STL_DIR'")

REFERENCE_MEASURES_FILE = 'reference_measures.csv'
if not path.isfile(path.join(STL_DIR, REFERENCE_MEASURES_FILE)):
    sys.exit(f'Please define file {REFERENCE_MEASURES_FILE} inside directory {STL_DIR}')

ASSETS_DIR = resource_filename('openfoamplatoons', 'assets')

ICONS_DIR = path.join(ASSETS_DIR, 'icons')
IMAGES_DIR = path.join(ASSETS_DIR, 'images')
FOAM_DIR = path.join(ASSETS_DIR, 'foam')
TEMPLATES_DIR = path.join(ASSETS_DIR, 'templates')