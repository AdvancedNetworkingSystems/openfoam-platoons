from psutil import cpu_count

from PyQt5.QtWidgets import QWidget, QGroupBox, QLabel, QSpinBox, QVBoxLayout, QFormLayout


class CpuInfo(QGroupBox):
    def __init__(self, parent=None):
        super(CpuInfo, self).__init__('Detected CPU', parent)

        form = QFormLayout()
        self.setLayout(form)

        form.addRow(QLabel(f'Physical cores: {cpu_count(logical=False)}'))
        form.addRow(QLabel(f'Logical cores: {cpu_count()}'))


class Length(QWidget):
    def __init__(self, parent=None):
        super(Length, self).__init__(parent)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        form = QFormLayout()
        vbox.addLayout(form)

        self.timeSteps = QSpinBox()
        self.timeSteps.setRange(1, 10000)
        self.timeSteps.setValue(1000)
        self.timeSteps.setSingleStep(100)
        form.addRow('Time steps', self.timeSteps)

        self.cores = QSpinBox()
        self.cores.setRange(1, 200)
        self.cores.setValue(cpu_count(logical=False))
        form.addRow('CPU cores', self.cores)

        vbox.addStretch()
        vbox.addWidget(CpuInfo(self))
