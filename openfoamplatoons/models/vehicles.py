from os.path import join
from enum import Enum
from typing import Any

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex

from openfoamplatoons.settings import STL_DIR
from openfoamplatoons.assets import availableStl
from openfoamplatoons.stl.stl import coordinates, solids

from openfoamplatoons.models.common import validName


class Headers(Enum):
    NAME = 'Name'
    DISTANCE = 'Distance'
    STL = 'STL'
    FEATURE_REFINEMENT = 'Feature refinement'
    SURFACE_REFINEMENT_MIN = 'Surface refinement (min)'
    SURFACE_REFINEMENT_MAX = 'Surface refinement (max)'
    N_SURFACE_LAYERS = 'N. of surface layers'
    FIRST_LAYER_THICKNESS = 'First layer thickness'
    EXPANSION_RATIO = 'Expansion ratio'
    X_MIN = 'X min'
    Y_MIN = 'Y min'
    Z_MIN = 'Z min'
    X_MAX = 'X max'
    Y_MAX = 'Y max'
    Z_MAX = 'Z max'


class Vehicles(QAbstractTableModel):
    attr = [
        Headers.NAME,
        Headers.DISTANCE,
        Headers.STL,
        Headers.FEATURE_REFINEMENT,
        Headers.SURFACE_REFINEMENT_MIN,
        Headers.SURFACE_REFINEMENT_MAX,
        Headers.N_SURFACE_LAYERS,
        Headers.FIRST_LAYER_THICKNESS,
        Headers.EXPANSION_RATIO,
        Headers.X_MIN,
        Headers.Y_MIN,
        Headers.Z_MIN,
        Headers.X_MAX,
        Headers.Y_MAX,
        Headers.Z_MAX,
    ]

    def __init__(self, parent=None):
        super(Vehicles, self).__init__(parent)

        self.name = []
        self.distance = []
        self.stl = []
        self.featureRefinement = []
        self.surfaceRefinementMin = []
        self.surfaceRefinementMax = []
        self.nSurfaceLayers = []
        self.firstLayerThickness = []
        self.expansionRatio = []
        self.xMin = []
        self.yMin = []
        self.zMin = []
        self.xMax = []
        self.yMax = []
        self.zMax = []

        self.insertRows(0, 1, QModelIndex())

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return Vehicles.attr[section].value
            if orientation == Qt.Vertical:
                return section
        return QVariant()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.name)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(Vehicles.attr)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        col = index.column()
        if col == Vehicles.attr.index(Headers.X_MIN) or \
                col == Vehicles.attr.index(Headers.Y_MIN) or \
                col == Vehicles.attr.index(Headers.Z_MIN) or \
                col == Vehicles.attr.index(Headers.X_MAX) or \
                col == Vehicles.attr.index(Headers.Y_MAX) or \
                col == Vehicles.attr.index(Headers.Z_MAX):
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        row = index.row()
        col = index.column()
        if col == Vehicles.attr.index(Headers.NAME):
            return self._name(row, role)
        if col == Vehicles.attr.index(Headers.DISTANCE):
            return self._distance(row, role)
        if col == Vehicles.attr.index(Headers.STL):
            return self._stl(row, role)
        if col == Vehicles.attr.index(Headers.FEATURE_REFINEMENT):
            return self._featureRefinement(row, role)
        if col == Vehicles.attr.index(Headers.SURFACE_REFINEMENT_MIN):
            return self._surfaceRefinementMin(row, role)
        if col == Vehicles.attr.index(Headers.SURFACE_REFINEMENT_MAX):
            return self._surfaceRefinementMax(row, role)
        if col == Vehicles.attr.index(Headers.N_SURFACE_LAYERS):
            return self._nSurfaceLayers(row, role)
        if col == Vehicles.attr.index(Headers.FIRST_LAYER_THICKNESS):
            return self._firstLayerThickness(row, role)
        if col == Vehicles.attr.index(Headers.EXPANSION_RATIO):
            return self._expansionRatio(row, role)
        if col == Vehicles.attr.index(Headers.X_MIN):
            return self._xMin(row, role)
        if col == Vehicles.attr.index(Headers.Y_MIN):
            return self._yMin(row, role)
        if col == Vehicles.attr.index(Headers.Z_MIN):
            return self._zMin(row, role)
        if col == Vehicles.attr.index(Headers.X_MAX):
            return self._xMax(row, role)
        if col == Vehicles.attr.index(Headers.Y_MAX):
            return self._yMax(row, role)
        if col == Vehicles.attr.index(Headers.Z_MAX):
            return self._zMax(row, role)
        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        row = index.row()
        col = index.column()
        if role != Qt.EditRole:
            return False
        if col == Vehicles.attr.index(Headers.NAME):
            return self._setName(row, value)
        if col == Vehicles.attr.index(Headers.DISTANCE):
            return self._setDistance(row, value)
        if col == Vehicles.attr.index(Headers.STL):
            return self._setStl(row, value)
        if col == Vehicles.attr.index(Headers.FEATURE_REFINEMENT):
            return self._setFeatureRefinement(row, value)
        if col == Vehicles.attr.index(Headers.SURFACE_REFINEMENT_MIN):
            return self._setSurfaceRefinementMin(row, value)
        if col == Vehicles.attr.index(Headers.SURFACE_REFINEMENT_MAX):
            return self._setSurfaceRefinementMax(row, value)
        if col == Vehicles.attr.index(Headers.N_SURFACE_LAYERS):
            return self._setNSurfaceLayers(row, value[0], value[1])
        if col == Vehicles.attr.index(Headers.FIRST_LAYER_THICKNESS):
            return self._setFirstLayerThickness(row, value[0], value[1])
        if col == Vehicles.attr.index(Headers.EXPANSION_RATIO):
            return self._setExpansionRatio(row, value[0], value[1])
        if col == Vehicles.attr.index(Headers.X_MIN):
            return self._setXmin(row, value)
        if col == Vehicles.attr.index(Headers.Y_MIN):
            return self._setYmin(row, value)
        if col == Vehicles.attr.index(Headers.Z_MIN):
            return self._setZmin(row, value)
        if col == Vehicles.attr.index(Headers.X_MAX):
            return self._setXmax(row, value)
        if col == Vehicles.attr.index(Headers.Y_MAX):
            return self._setYmax(row, value)
        if col == Vehicles.attr.index(Headers.Z_MAX):
            return self._setZmax(row, value)

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(parent, row, row + count - 1)

        self.name.append(f'Vehicle{self.rowCount()}')
        self.distance.append(0.)
        self.stl.append(availableStl()[0])
        self.featureRefinement.append(8)
        self.surfaceRefinementMin.append(8)
        self.surfaceRefinementMax.append(8)

        nSurfaceLayers = {}
        firstLayerThickness = {}
        expansionRatio = {}
        for solid in solids(join(STL_DIR, availableStl()[0])):
            nSurfaceLayers[solid] = 4
            firstLayerThickness[solid] = 0.001044
            expansionRatio[solid] = 1.2
        self.nSurfaceLayers.append(nSurfaceLayers)
        self.firstLayerThickness.append(firstLayerThickness)
        self.expansionRatio.append(expansionRatio)

        xMin, yMin, zMin, xMax, yMax, zMax = coordinates(join(STL_DIR, availableStl()[0]))

        self.xMin.append(xMin)
        self.yMin.append(yMin)
        self.zMin.append(zMin)
        self.xMax.append(xMax)
        self.yMax.append(yMax)
        self.zMax.append(zMax)

        if row > 0:
            self._setXmin(row, self.xMin[row] + self.xMax[row - 1])
            self._setXmax(row, self.xMax[row] + self.xMax[row - 1])

        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        if self.rowCount() == 0 or row != self.rowCount() - 1:
            # Only allow removal of last row
            return False

        self.beginRemoveRows(parent, row, row + count - 1)

        del self.name[row]
        del self.distance[row]
        del self.stl[row]
        del self.featureRefinement[row]
        del self.surfaceRefinementMin[row]
        del self.surfaceRefinementMax[row]
        del self.nSurfaceLayers[row]
        del self.firstLayerThickness[row]
        del self.expansionRatio[row]
        del self.xMin[row]
        del self.yMin[row]
        del self.zMin[row]
        del self.xMax[row]
        del self.yMax[row]
        del self.zMax[row]

        self.endRemoveRows()
        return True

    def _name(self, row: int, role: int):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.name[row]
        return QVariant()

    def _setName(self, row: int, newName: str) -> bool:
        if not validName(newName) or newName in self.name:
            return False
        self.name[row] = newName
        return True

    def _distance(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.distance[row])
        if role == Qt.EditRole:
            return self.distance[row]
        return QVariant()

    def _setDistance(self, row: int, newDist: float) -> bool:
        if row == 0:
            # The first vehicle has no predecessors
            return False
        dL = newDist - self.distance[row]

        for i in range(row, self.rowCount()):
            self._setXmin(i, self.xMin[i] + dL)
            self._setXmax(i, self.xMax[i] + dL)

        self.distance[row] = newDist
        return True

    def _stl(self, row: int, role: int):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.stl[row]
        return QVariant()

    def _setStl(self, row: int, newStl: str) -> bool:
        # Update coordinates
        xMin, yMin, zMin, xMax, yMax, zMax = coordinates(join(STL_DIR, newStl))
        L = xMax - xMin
        oldL = self.xMax[row] - self.xMin[row]
        dL = L - oldL

        self._setXmax(row, self.xMax[row] + dL)
        for i in range(row + 1, self.rowCount()):
            self._setXmin(i, self.xMin[i] + dL)
            self._setXmax(i, self.xMax[i] + dL)

        self._setYmin(row, yMin)
        self._setZmin(row, zMin)
        self._setYmax(row, yMax)
        self._setZmax(row, zMax)

        self.stl[row] = newStl

        # Update layers
        stlSolids = solids(join(STL_DIR, newStl))
        self.nSurfaceLayers[row] = {solid: 4 for solid in stlSolids}
        self.firstLayerThickness[row] = {solid: 0.001044 for solid in stlSolids}
        self.expansionRatio[row] = {solid: 1.2 for solid in stlSolids}

        return True

    def _featureRefinement(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.featureRefinement[row])
        if role == Qt.EditRole:
            return self.featureRefinement[row]
        return QVariant()

    def _setFeatureRefinement(self, row: int, newValue: int) -> bool:
        self.featureRefinement[row] = newValue
        return True

    def _surfaceRefinementMin(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.surfaceRefinementMin[row])
        if role == Qt.EditRole:
            return self.surfaceRefinementMin[row]
        return QVariant()

    def _setSurfaceRefinementMin(self, row: int, newValue: int) -> bool:
        self.surfaceRefinementMin[row] = newValue
        return True

    def _surfaceRefinementMax(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.surfaceRefinementMax[row])
        if role == Qt.EditRole:
            return self.surfaceRefinementMax[row]
        return QVariant()

    def _setSurfaceRefinementMax(self, row: int, newValue: int) -> bool:
        if newValue < self.surfaceRefinementMin[row]:
            return False
        self.surfaceRefinementMax[row] = newValue
        return True

    def _nSurfaceLayers(self, row: int, role: int):
        if role == Qt.DisplayRole:
            string = ''
            for solid, value in self.nSurfaceLayers[row].items():
                string += f'{solid}: {value}, '
            return string[0:-2]
        if role == Qt.EditRole:
            return self.nSurfaceLayers[row]
        return QVariant()

    def _setNSurfaceLayers(self, row: int, solid: str, newValue: int) -> bool:
        if newValue == 0:
            del self.firstLayerThickness[row][solid]
            del self.expansionRatio[row][solid]
        else:
            if solid not in self.firstLayerThickness[row]:
                self.firstLayerThickness[row][solid] = 0.001044
            if solid not in self.expansionRatio[row]:
                self.expansionRatio[row][solid] = 1.2

        self.nSurfaceLayers[row][solid] = newValue
        return True

    def _firstLayerThickness(self, row: int, role: int):
        if role == Qt.DisplayRole:
            string = ''
            for solid, value in self.firstLayerThickness[row].items():
                string += f'{solid}: {value}, '
            return string[0:-2]
        if role == Qt.EditRole:
            return self.firstLayerThickness[row]
        return QVariant()

    def _setFirstLayerThickness(self, row: int, solid: str, newValue: float) -> bool:
        self.firstLayerThickness[row][solid] = newValue
        return True

    def _expansionRatio(self, row: int, role: int):
        if role == Qt.DisplayRole:
            string = ''
            for solid, value in self.expansionRatio[row].items():
                string += f'{solid}: {value}, '
            return string[0:-2]
        if role == Qt.EditRole:
            return self.expansionRatio[row]
        return QVariant()

    def _setExpansionRatio(self, row: int, solid: str, newValue: float) -> bool:
        self.expansionRatio[row][solid] = newValue
        return True

    def _xMin(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.xMin[row])
        if role == Qt.EditRole:
            return self.xMin[row]
        return QVariant()

    def _setXmin(self, row: int, newValue: float) -> bool:
        self.xMin[row] = newValue
        return True

    def _yMin(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.yMin[row])
        if role == Qt.EditRole:
            return self.yMin[row]
        return QVariant()

    def _setYmin(self, row: int, newValue: float) -> bool:
        self.yMin[row] = newValue
        return True

    def _zMin(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.zMin[row])
        if role == Qt.EditRole:
            return self.zMin[row]
        return QVariant()

    def _setZmin(self, row: int, newValue: float) -> bool:
        self.zMin[row] = newValue
        return True

    def _xMax(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.xMax[row])
        if role == Qt.EditRole:
            return self.xMax[row]
        return QVariant()

    def _setXmax(self, row: int, newValue: float) -> bool:
        self.xMax[row] = newValue
        return True

    def _yMax(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.yMax[row])
        if role == Qt.EditRole:
            return self.yMax[row]
        return QVariant()

    def _setYmax(self, row: int, newValue: float) -> bool:
        self.yMax[row] = newValue
        return True

    def _zMax(self, row: int, role: int):
        if role == Qt.DisplayRole:
            return str(self.zMax[row])
        if role == Qt.EditRole:
            return self.zMax[row]
        return QVariant()

    def _setZmax(self, row: int, newValue: float) -> bool:
        self.zMax[row] = newValue
        return True
