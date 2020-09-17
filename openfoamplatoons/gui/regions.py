from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QTableView, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from openfoamplatoons.assets import icon
from openfoamplatoons.models.delegates import NameDelegate as Name
from openfoamplatoons.models.delegates import IntegerDelegate as Integer
from openfoamplatoons.models.regions import Headers
from openfoamplatoons.models.regions import Regions as RegionsModel


class Regions(QWidget):
    def __init__(self, model: RegionsModel, parent=None):
        super(Regions, self).__init__(parent)

        self.model = model

        vbox = QVBoxLayout(self)
        self.setLayout(vbox)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        vbox.addLayout(hbox)

        self.add = QPushButton()
        self.add.setIcon(QIcon(icon('plus.png')))
        self.add.setToolTip('Add region')
        self.add.clicked.connect(self.addRegion)
        hbox.addWidget(self.add)

        self.remove = QPushButton()
        self.remove.setIcon(QIcon(icon('minus.png')))
        self.remove.setToolTip('Remove selected region')
        self.remove.setEnabled(False)
        self.remove.clicked.connect(self.removeRegion)
        hbox.addWidget(self.remove)

        self.view = QTableView()
        self.view.setModel(model)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        vbox.addWidget(self.view)

        self.view.setItemDelegateForColumn(RegionsModel.attr.index(Headers.NAME), Name(self.view))
        self.view.setItemDelegateForColumn(RegionsModel.attr.index(Headers.REFINEMENT), Integer(self.view))

    def addRegion(self):
        self.model.insertRow(self.model.rowCount())
        self.view.selectRow(self.model.rowCount() - 1)
        self.remove.setEnabled(True)

    def removeRegion(self):
        row = self.view.currentIndex().row()
        self.model.removeRow(row)
        if self.model.rowCount() == 0:
            self.remove.setEnabled(False)
