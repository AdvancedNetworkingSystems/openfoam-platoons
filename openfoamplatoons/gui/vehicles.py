from PyQt5.QtWidgets import QWidget, QPushButton, QTableView, QHeaderView, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from openfoamplatoons.settings import APP_WIDTH, APP_HEIGHT
from openfoamplatoons.assets import icon
from openfoamplatoons.models.delegates import IntegerDelegate as Integer, RealDelegate as Real
from openfoamplatoons.models.delegates import NameDelegate as Name, StlDelegate as Stl, \
    DialogFormRealDelegate as DReal, DialogFormIntegerDelegate as DInteger
from openfoamplatoons.models.vehicles import Headers
from openfoamplatoons.models.vehicles import Vehicles as VehiclesModel


class Coordinates(QDialog):
    def __init__(self, model: VehiclesModel, parent=None):
        super(Coordinates, self).__init__(parent)

        self.setFixedSize(APP_WIDTH, APP_HEIGHT)
        self.setWindowTitle('Vehicles\' coordinates')

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        view = QTableView()
        view.setModel(model)
        view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        view.setSelectionMode(QTableView.NoSelection)
        vbox.addWidget(view)

        for i in range(0, model.columnCount()):
            view.setColumnHidden(i, True)
        view.setColumnHidden(VehiclesModel.attr.index(Headers.NAME), False)
        view.setColumnHidden(VehiclesModel.attr.index(Headers.X_MIN), False)
        view.setColumnHidden(VehiclesModel.attr.index(Headers.Y_MIN), False)
        view.setColumnHidden(VehiclesModel.attr.index(Headers.Z_MIN), False)
        view.setColumnHidden(VehiclesModel.attr.index(Headers.X_MAX), False)
        view.setColumnHidden(VehiclesModel.attr.index(Headers.Y_MAX), False)
        view.setColumnHidden(VehiclesModel.attr.index(Headers.Z_MAX), False)


class Vehicles(QWidget):
    def __init__(self, model: VehiclesModel, parent=None):
        super(Vehicles, self).__init__(parent)

        self.model = model

        vbox = QVBoxLayout(self)
        self.setLayout(vbox)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        vbox.addLayout(hbox)

        self.add = QPushButton()
        self.add.setIcon(QIcon(icon('car--plus.png')))
        self.add.setToolTip('Add vehicle')
        self.add.clicked.connect(self.addVehicle)
        hbox.addWidget(self.add)

        self.remove = QPushButton()
        self.remove.setIcon(QIcon(icon('car--minus.png')))
        self.remove.setToolTip('Remove last vehicle')
        self.remove.setEnabled(False)
        self.remove.clicked.connect(self.removeVehicle)
        hbox.addWidget(self.remove)

        self.show_ = QPushButton()
        self.show_.setIcon(QIcon(icon('eye.png')))
        self.show_.setToolTip('Show vehicles\' coordinates')
        self.show_.clicked.connect(self.showCoordinates)
        hbox.addWidget(self.show_)

        self.view = QTableView()
        self.view.setModel(model)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        vbox.addWidget(self.view)

        self.view.setItemDelegateForColumn(VehiclesModel.attr.index(Headers.NAME), Name(self.view))
        self.view.setItemDelegateForColumn(VehiclesModel.attr.index(Headers.DISTANCE), Real(3, None, None, self.view))
        self.view.setItemDelegateForColumn(VehiclesModel.attr.index(Headers.STL), Stl(self.view))
        self.view.setItemDelegateForColumn(VehiclesModel.attr.index(Headers.FEATURE_REFINEMENT), Integer(self.view))
        self.view.setItemDelegateForColumn(VehiclesModel.attr.index(Headers.SURFACE_REFINEMENT_MIN), Integer(self.view))
        self.view.setItemDelegateForColumn(VehiclesModel.attr.index(Headers.SURFACE_REFINEMENT_MAX), Integer(self.view))
        self.view.setItemDelegateForColumn(VehiclesModel.attr.index(Headers.N_SURFACE_LAYERS), DInteger(self.view))
        self.view.setItemDelegateForColumn(VehiclesModel.attr.index(Headers.FIRST_LAYER_THICKNESS),
                                           DReal(6, pow(10, -6), None, self.view))
        self.view.setItemDelegateForColumn(VehiclesModel.attr.index(Headers.EXPANSION_RATIO),
                                           DReal(2, pow(10, -2), None, self.view))
        self.view.setColumnHidden(VehiclesModel.attr.index(Headers.X_MIN), True)
        self.view.setColumnHidden(VehiclesModel.attr.index(Headers.Y_MIN), True)
        self.view.setColumnHidden(VehiclesModel.attr.index(Headers.Z_MIN), True)
        self.view.setColumnHidden(VehiclesModel.attr.index(Headers.X_MAX), True)
        self.view.setColumnHidden(VehiclesModel.attr.index(Headers.Y_MAX), True)
        self.view.setColumnHidden(VehiclesModel.attr.index(Headers.Z_MAX), True)

        self.coordinates = Coordinates(model, self)
        self.coordinates.closeEvent = lambda args=...: self.show_.setEnabled(True)
        self.coordinates.hideEvent = lambda args=...: self.show_.setEnabled(True)

    def addVehicle(self):
        self.model.insertRow(self.model.rowCount())
        self.remove.setEnabled(True)

    def removeVehicle(self):
        if self.model.rowCount() == 1:
            return
        self.model.removeRow(self.model.rowCount() - 1)
        if self.model.rowCount() == 1:
            self.remove.setEnabled(False)

    def showCoordinates(self):
        self.show_.setEnabled(False)
        self.coordinates.show()

    def showHeaders(self, *args: Headers):
        for i in range(self.model.columnCount()):
            self.view.setColumnHidden(i, True)
        self.view.setColumnHidden(VehiclesModel.attr.index(Headers.NAME), False)

        for header in args:
            self.view.setColumnHidden(VehiclesModel.attr.index(header), False)
