import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from openfoamplatoons.settings import APP_TITLE, STL_DIR
from openfoamplatoons.assets import availableStl, referenceLength, referenceArea
from openfoamplatoons.gui.main_window import MainWindow


def dieNoStl():
    """Inform user that no STL is available and app will not start"""
    msgBox = QMessageBox()
    msgBox.setWindowTitle(APP_TITLE)
    msgBox.setText(f'No STL was found in directory {STL_DIR}.\n'
                   'Application will not start.')
    sys.exit(msgBox.exec_())


def dieNoMeasurements(stl):
    """Inform user that they did not specify the reference measurements of a given STL"""
    msgBox = QMessageBox()
    msgBox.setWindowTitle(APP_TITLE)
    msgBox.setText(f'{stl} has incomplete reference measurements.\n'
                   'Application will not start.')
    sys.exit(msgBox.exec_())


def main():
    """App launcher"""
    print('Launching app')

    app = QApplication([])
    if not availableStl():
        dieNoStl()
    for stl in availableStl():
        if not referenceLength(stl) or not referenceArea(stl):
            dieNoMeasurements(stl)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
