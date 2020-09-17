"""
https://www.openfoam.com/documentation/guides/latest/doc/guide-turbulence-ras-k-omega-sst.html
https://www.simscale.com/docs/validation-cases/aerodynamics-flow-around-the-ahmed-body/
"""

from PyQt5.QtWidgets import QWidget, QComboBox, QDoubleSpinBox
from PyQt5.QtWidgets import QFormLayout


class Turbulence(QWidget):
    def __init__(self, parent=None):
        super(Turbulence, self).__init__(parent)

        form = QFormLayout()
        self.setLayout(form)

        self.combobox = QComboBox()
        self.combobox.addItems(['Custom', 'Ahmed body (Simscale)'])
        self.combobox.currentIndexChanged.connect(lambda index: self.loadPreset(index))
        form.addRow('Preset', self.combobox)

        self.speed = QDoubleSpinBox()
        self.speed.setRange(0.01, 140.)
        form.addRow('Flow speed (m/s)', self.speed)

        self.k = QDoubleSpinBox()
        self.k.setRange(0.01, 50000)
        form.addRow('Turbulence kinetic energy', self.k)

        self.w = QDoubleSpinBox()
        self.w.setRange(0.01, 50000)
        form.addRow('Turbulence specific dissipation rate', self.w)

        self.loadPreset(1)
        self.loadPreset(0)

    def loadPreset(self, index: int):
        if index == 0:
            self.speed.setEnabled(True)
            self.k.setEnabled(True)
            self.w.setEnabled(True)
        elif index == 1:
            self.speed.setValue(63.7)
            self.speed.setEnabled(False)
            self.k.setValue(21.9)
            self.k.setEnabled(False)
            self.w.setValue(29215)
            self.w.setEnabled(False)
