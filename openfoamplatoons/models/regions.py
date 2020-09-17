from enum import Enum
from typing import Any

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex

from openfoamplatoons.models.common import validName


class Headers(Enum):
    NAME = 'Name'
    X_MIN = 'X min'
    Y_MIN = 'Y min'
    Z_MIN = 'Z min'
    X_MAX = 'X max'
    Y_MAX = 'Y max'
    Z_MAX = 'Z max'
    REFINEMENT = 'Refinement'


class Regions(QAbstractTableModel):
    attr = [
        Headers.NAME,
        Headers.X_MIN,
        Headers.Y_MIN,
        Headers.Z_MIN,
        Headers.X_MAX,
        Headers.Y_MAX,
        Headers.Z_MAX,
        Headers.REFINEMENT
    ]

    def __init__(self, parent=None):
        super(Regions, self).__init__(parent)

        self.name = []
        self.xMin = []
        self.yMin = []
        self.zMin = []
        self.xMax = []
        self.yMax = []
        self.zMax = []
        self.refinement = []

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return Regions.attr[section].value
            if orientation == Qt.Vertical:
                return section
        return QVariant()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.name)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(Regions.attr)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if col == Regions.attr.index(Headers.NAME):
                return self.name[row]
            if col == Regions.attr.index(Headers.X_MIN):
                return self.xMin[row]
            if col == Regions.attr.index(Headers.Y_MIN):
                return self.yMin[row]
            if col == Regions.attr.index(Headers.Z_MIN):
                return self.zMin[row]
            if col == Regions.attr.index(Headers.X_MAX):
                return self.xMax[row]
            if col == Regions.attr.index(Headers.Y_MAX):
                return self.yMax[row]
            if col == Regions.attr.index(Headers.Z_MAX):
                return self.zMax[row]
            if col == Regions.attr.index(Headers.REFINEMENT):
                return self.refinement[row]
        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if col == Regions.attr.index(Headers.NAME):
                return self._setName(row, value)
            if col == Regions.attr.index(Headers.X_MIN):
                return self._setXmin(row, value)
            if col == Regions.attr.index(Headers.Y_MIN):
                return self._setYmin(row, value)
            if col == Regions.attr.index(Headers.Z_MIN):
                return self._setZmin(row, value)
            if col == Regions.attr.index(Headers.X_MAX):
                return self._setXmax(row, value)
            if col == Regions.attr.index(Headers.Y_MAX):
                return self._setYmax(row, value)
            if col == Regions.attr.index(Headers.Z_MAX):
                return self._setZmax(row, value)
            if col == Regions.attr.index(Headers.REFINEMENT):
                return self._setRefinement(row, value)
        return False

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(parent, row, row + count - 1)

        self.name.append(f'Region{self.rowCount()}')

        self.xMin.append(0.)
        self.yMin.append(0.)
        self.zMin.append(0.)
        self.xMax.append(1.)
        self.yMax.append(1.)
        self.zMax.append(1.)
        self.refinement.append(4)

        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(parent, row, row + count - 1)

        del self.name[row]
        del self.xMin[row]
        del self.yMin[row]
        del self.zMin[row]
        del self.xMax[row]
        del self.yMax[row]
        del self.zMax[row]
        del self.refinement[row]

        self.endRemoveRows()
        return True

    def _setName(self, row: int, newName: str) -> bool:
        if not validName(newName) or newName in self.name:
            return False
        self.name[row] = newName
        return True

    def _setXmin(self, row: int, newValue: float) -> bool:
        if newValue >= self.xMax[row]:
            return False
        self.xMin[row] = newValue
        return True

    def _setYmin(self, row: int, newValue: float) -> bool:
        if newValue >= self.yMax[row]:
            return False
        self.yMin[row] = newValue
        return True

    def _setZmin(self, row: int, newValue: float) -> bool:
        if newValue >= self.yMax[row]:
            return False
        self.zMin[row] = newValue
        return True

    def _setXmax(self, row: int, newValue: float) -> bool:
        if newValue <= self.xMin[row]:
            return False
        self.xMax[row] = newValue
        return True

    def _setYmax(self, row: int, newValue: float) -> bool:
        if newValue <= self.yMin[row]:
            return False
        self.yMax[row] = newValue
        return True

    def _setZmax(self, row: int, newValue: float) -> bool:
        if newValue <= self.zMin[row]:
            return False
        self.zMax[row] = newValue
        return True

    def _setRefinement(self, row: int, newValue: int) -> bool:
        self.refinement[row] = newValue
        return True
