from PyQt5.QtWidgets import QWidget, QStyledItemDelegate, QStyleOptionViewItem, QFormLayout, QDialog, \
    QLabel, QLayoutItem
from PyQt5.QtWidgets import QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator

from openfoamplatoons.assets import availableStl
from openfoamplatoons.models.common import nameRegex


class NameDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(NameDelegate, self).__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        lineEdit = QLineEdit(parent)
        regexp = QRegExp(nameRegex)
        validator = QRegExpValidator(regexp, parent)
        lineEdit.setValidator(validator)
        lineEdit.setFrame(False)
        return lineEdit

    def setEditorData(self, editor: QLineEdit, index: QtCore.QModelIndex) -> None:
        editor.setText(index.data(Qt.EditRole))

    def setModelData(self, editor: QLineEdit, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        model.setData(index, editor.text(), Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        editor.setGeometry(option.rect)


class RealDelegate(QStyledItemDelegate):
    def __init__(self, decimals: int, minVal: float = None, maxVal: float = None, parent=None):
        super(RealDelegate, self).__init__(parent)
        self.decimals = decimals
        self.minVal = minVal
        self.maxVal = maxVal

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        spinbox = QDoubleSpinBox(parent)
        spinbox.setDecimals(self.decimals)
        if self.minVal:
            spinbox.setMinimum(self.minVal)
        if self.maxVal:
            spinbox.setMaximum(self.maxVal)
        spinbox.setFrame(False)
        return spinbox

    def setEditorData(self, editor: QDoubleSpinBox, index: QtCore.QModelIndex) -> None:
        editor.setValue(index.data(Qt.EditRole))

    def setModelData(self, editor: QDoubleSpinBox, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        model.setData(index, editor.value(), Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        editor.setGeometry(option.rect)


class IntegerDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(IntegerDelegate, self).__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        spinbox = QSpinBox(parent)
        spinbox.setFrame(False)
        return spinbox

    def setEditorData(self, editor: QSpinBox, index: QtCore.QModelIndex) -> None:
        editor.setValue(index.data(Qt.EditRole))

    def setModelData(self, editor: QSpinBox, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        model.setData(index, editor.value(), Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        editor.setGeometry(option.rect)


class StlDelegate(QStyledItemDelegate):
    items = availableStl()

    def __init__(self, parent=None):
        super(StlDelegate, self).__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        combobox = QComboBox(parent)
        combobox.setFrame(False)
        return combobox

    def setEditorData(self, editor: QComboBox, index: QtCore.QModelIndex) -> None:
        stl = index.data(Qt.EditRole)
        editor.addItems(StlDelegate.items)
        stlIndex = editor.findText(stl)
        if stlIndex > -1:
            editor.setCurrentIndex(stlIndex)

    def setModelData(self, editor: QComboBox, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        model.setData(index, editor.currentText(), Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        editor.setGeometry(option.rect)


class AbstractDialogFormDelegate(QStyledItemDelegate):
    class Editor(QDialog):
        def __init__(self, parent):
            super(AbstractDialogFormDelegate.Editor, self).__init__(parent)
            self.form = QFormLayout()
            self.setLayout(self.form)

        def reset(self):
            while self.form.rowCount() > 0:
                self.form.takeRow(0)

    def __init__(self, parent=None):
        super(AbstractDialogFormDelegate, self).__init__(parent)

    def setModelData(self, wrapper: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        editor: AbstractDialogFormDelegate.Editor = wrapper.editor
        for i in range(editor.form.rowCount()):
            item: QLayoutItem = editor.form.itemAt(i, QFormLayout.FieldRole)
            if not item:
                continue
            spinbox = item.widget()
            label: QLabel = editor.form.labelForField(spinbox)
            label.setWordWrap(True)
            model.setData(index, (label.text(), spinbox.value()), Qt.EditRole)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        wrapper = QWidget(parent)
        wrapper.editor = AbstractDialogFormDelegate.Editor(wrapper)
        return wrapper

    def updateEditorGeometry(self, wrapper: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        editor: AbstractDialogFormDelegate.Editor = wrapper.editor
        editor.setMinimumWidth(400)
        editor.show()


class DialogFormRealDelegate(AbstractDialogFormDelegate):
    def __init__(self, decimals: int, minVal: float = None, maxVal: float = None, parent=None):
        super(DialogFormRealDelegate, self).__init__(parent)
        self.decimals = decimals
        self.minVal = minVal
        self.maxVal = maxVal

    def setEditorData(self, wrapper: QWidget, index: QtCore.QModelIndex) -> None:
        editor: AbstractDialogFormDelegate.Editor = wrapper.editor
        editor.reset()

        data: dict = index.data(Qt.EditRole)
        for solid, value in data.items():
            spinbox = QDoubleSpinBox(editor)
            spinbox.setDecimals(self.decimals)
            if self.minVal:
                spinbox.setMinimum(self.minVal)
            if self.maxVal:
                spinbox.setMaximum(self.maxVal)
            spinbox.setValue(value)
            editor.form.addRow(solid, spinbox)


class DialogFormIntegerDelegate(AbstractDialogFormDelegate):
    def setEditorData(self, wrapper: QWidget, index: QtCore.QModelIndex) -> None:
        editor: AbstractDialogFormDelegate.Editor = wrapper.editor
        editor.reset()

        data: dict = index.data(Qt.EditRole)
        for solid, value in data.items():
            spinbox = QSpinBox(editor)
            spinbox.setValue(value)
            editor.form.addRow(solid, spinbox)
