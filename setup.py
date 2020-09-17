from os.path import join
from setuptools import setup, find_packages

setup(
    name='openfoamplatoons',
    version='1.0',
    author='Andrea Stedile',
    author_email='andrea.stedile@studenti.unitn.it',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ofp = openfoamplatoons.__main__:main'
        ]
    },
    package_data={
        '': [
            join('assets', 'icons', '*'),
            join('assets', 'images', '*'),
            # OpenFOAM files
            join('assets', 'foam', '*'),
            join('assets', 'foam', '0', '*'),
            join('assets', 'foam', '0', 'include', '*'),
            join('assets', 'foam', 'constant', '*'),
            join('assets', 'foam', 'constant', 'triSurface', '*'),
            join('assets', 'foam', 'system', '*'),
            join('assets', 'foam', 'system', 'include', '*'),
            # OpenFOAM template files
            join('assets', 'templates', 'system', 'snappyHexMesh', '*'),
            join('assets', 'templates', 'system', 'controlDict', '*')
        ]
    },
    install_requires=['setuptools', 'PyQt5', 'psutil']
)
