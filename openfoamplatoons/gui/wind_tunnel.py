from builtins import set

from PyQt5.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from openfoamplatoons.assets import image

# We borrow some header names from here
from openfoamplatoons.models.vehicles import Headers


class WindTunnel(QWidget):
    def __init__(self, parent=None):
        super(WindTunnel, self).__init__(parent)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        leftCol = QFormLayout()
        leftCol.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        hbox.addLayout(leftCol)

        rightCol = QFormLayout()
        rightCol.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        hbox.addLayout(rightCol)

        self.xMin = QSpinBox()
        self.xMin.setRange(-50, 0)
        self.xMin.setValue(-3)
        leftCol.addRow('X min', self.xMin)

        self.yMin = QSpinBox()
        self.yMin.setEnabled(False)
        self.yMin.setRange(-50, 0)
        leftCol.addRow('Y min', self.yMin)

        self.zMin = QSpinBox()
        self.zMin.setRange(-50, 0)
        self.zMin.setEnabled(False)
        leftCol.addRow('Z min', self.zMin)

        self.xMax = QSpinBox()
        self.xMax.setRange(1, 250)
        self.xMax.setValue(9)
        rightCol.addRow('X max', self.xMax)

        self.yMax = QSpinBox()
        self.yMax.setRange(1, 100)
        self.yMax.setValue(3)
        rightCol.addRow('Y max', self.yMax)

        self.zMax = QSpinBox()
        self.zMax.setRange(1, 100)
        self.zMax.setValue(5)
        rightCol.addRow('Z max', self.zMax)

        layers = QFormLayout()
        layers.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        vbox.addLayout(layers)

        self.nSurfaceLayers = QSpinBox()
        self.nSurfaceLayers.setValue(2)
        layers.addRow(Headers.N_SURFACE_LAYERS.value, self.nSurfaceLayers)

        self.firstLayerThickness = QDoubleSpinBox()
        self.firstLayerThickness.setDecimals(6)
        self.firstLayerThickness.setValue(0.0033)
        layers.addRow(Headers.FIRST_LAYER_THICKNESS.value, self.firstLayerThickness)

        self.expansionRatio = QDoubleSpinBox()
        self.expansionRatio.setDecimals(2)
        self.expansionRatio.setValue(1.2)
        layers.addRow(Headers.EXPANSION_RATIO.value, self.expansionRatio)

        imgLabel = QLabel()
        imgLabel.setAlignment(Qt.AlignCenter)
        imgLabel.setPixmap(QPixmap(image('wind_tunnel.png')))
        # scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        vbox.addStretch()
        vbox.addWidget(imgLabel)
        vbox.addStretch()
