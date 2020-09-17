from os import listdir, path, getcwd
from shutil import copytree, copy
from string import Template
import sys

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QAction, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from openfoamplatoons.settings import APP_TITLE, APP_WIDTH, APP_HEIGHT, STL_DIR, FOAM_DIR, TEMPLATES_DIR
from openfoamplatoons.assets import icon, referenceLength, referenceArea

from openfoamplatoons.models.vehicles import Vehicles as VehiclesModel, Headers as VHeaders
from openfoamplatoons.models.regions import Regions as RegionsModel, Headers as RHeaders

from openfoamplatoons.gui.length import Length
from openfoamplatoons.gui.turbulence import Turbulence
from openfoamplatoons.gui.wind_tunnel import WindTunnel
from openfoamplatoons.gui.vehicles import Vehicles
from openfoamplatoons.gui.regions import Regions

from openfoamplatoons.stl.stl import translate, solids


def goodbye():
    msgBox = QMessageBox()
    msgBox.setWindowTitle(APP_TITLE)
    msgBox.setText(f'OpenFOAM case has been constructed. Application will close.')
    sys.exit(msgBox.exec_())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(APP_WIDTH, APP_HEIGHT)

        self.initFileMenu()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.length = Length(self)
        self.stack.addWidget(self.length)

        self.turbulence = Turbulence(self)
        self.stack.addWidget(self.turbulence)

        self.windTunnel = WindTunnel(self)
        self.stack.addWidget(self.windTunnel)

        self.vehiclesModel = VehiclesModel(self)

        self.vehicles = Vehicles(self.vehiclesModel, self)
        self.stack.addWidget(self.vehicles)

        self.regionsModel = RegionsModel(self)

        self.regions = Regions(self.regionsModel, self)
        self.stack.addWidget(self.regions)

        self.initViewMenu()

    def initFileMenu(self):
        fileMenu = self.menuBar().addMenu('&File')

        save = QAction('Save', self)
        save.setIcon(QIcon(icon('disk.png')))
        save.triggered.connect(self.onSaveClick)
        save.triggered.connect(goodbye)
        fileMenu.addAction(save)

    def initViewMenu(self):
        viewMenu = self.menuBar().addMenu('&View')

        vLength = QAction('Length', self)
        vLength.triggered.connect(lambda: self.stack.setCurrentWidget(self.length))
        viewMenu.addAction(vLength)

        vTurbulence = QAction('Turbulence', self)
        vTurbulence.triggered.connect(lambda: self.stack.setCurrentWidget(self.turbulence))
        viewMenu.addAction(vTurbulence)

        vWindTunnel = QAction('Wind tunnel', self)
        vWindTunnel.triggered.connect(lambda: self.stack.setCurrentWidget(self.windTunnel))
        viewMenu.addAction(vWindTunnel)

        vVehicles = viewMenu.addMenu('Vehicles')
        vVehicles.triggered.connect(lambda: self.stack.setCurrentWidget(self.vehicles))

        vDistanceStl = QAction('Distance and STL', self)
        vDistanceStl.triggered.connect(lambda: self.vehicles.showHeaders(
            VHeaders.DISTANCE,
            VHeaders.STL
        ))
        vVehicles.addAction(vDistanceStl)

        vRefinement = QAction('Refinement', self)
        vRefinement.triggered.connect(lambda: self.vehicles.showHeaders(
            VHeaders.FEATURE_REFINEMENT,
            VHeaders.SURFACE_REFINEMENT_MIN,
            VHeaders.SURFACE_REFINEMENT_MAX
        ))
        vVehicles.addAction(vRefinement)

        vLayers = QAction('Layers', self)
        vLayers.triggered.connect(lambda: self.vehicles.showHeaders(
            VHeaders.N_SURFACE_LAYERS,
            VHeaders.FIRST_LAYER_THICKNESS,
            VHeaders.EXPANSION_RATIO
        ))
        vVehicles.addAction(vLayers)

        vRegions = QAction('Region refinement', self)
        vRegions.triggered.connect(lambda: self.stack.setCurrentWidget(self.regions))
        viewMenu.addAction(vRegions)

    def onSaveClick(self):
        print('Save')

        # Init case
        for item in listdir(FOAM_DIR):
            if path.isdir(path.join(FOAM_DIR, item)):
                copytree(path.join(FOAM_DIR, item), path.join(getcwd(), item))
            else:
                copy(path.join(FOAM_DIR, item), getcwd())

        with open(path.join('0', 'include', 'initialConditions'), 'r') as f:
            temp = Template(f.read()).safe_substitute(flowVelocityX=self.turbulence.speed.value(),
                                                      turbulentKE=self.turbulence.k.value(),
                                                      turbulentOmega=self.turbulence.w.value())
        with open(path.join('0', 'include', 'initialConditions'), 'w') as f:
            f.write(temp)

        with open(path.join('system', 'decomposeParDict'), 'r') as f:
            temp = Template(f.read()).safe_substitute(numberOfSubdomains=self.length.cores.value())
        with open(path.join('system', 'decomposeParDict'), 'w') as f:
            f.write(temp)

        with open(path.join('system', 'controlDict'), 'r') as f:
            temp = Template(f.read()).safe_substitute(endTime=self.length.timeSteps.value())
        with open(path.join('system', 'controlDict'), 'w') as f:
            f.write(temp)

        with open(path.join('system', 'blockMeshDict'), 'r') as f:
            temp = Template(f.read()).safe_substitute(xMin=self.windTunnel.xMin.value(),
                                                      yMin=self.windTunnel.yMin.value(),
                                                      zMin=self.windTunnel.zMin.value(),
                                                      xMax=self.windTunnel.xMax.value(),
                                                      yMax=self.windTunnel.yMax.value(),
                                                      zMax=self.windTunnel.zMax.value())
        with open(path.join('system', 'blockMeshDict'), 'w') as f:
            f.write(temp)

        with open(path.join('system', 'snappyHexMeshDict'), 'r') as f:
            temp = Template(f.read()).safe_substitute(x=self.windTunnel.xMax.value() - 0.001,
                                                      y=self.windTunnel.yMax.value() - 0.001,
                                                      z=self.windTunnel.zMax.value() - 0.001)
        with open(path.join('system', 'snappyHexMeshDict'), 'w') as f:
            f.write(temp)

        with open(path.join('system', 'include', 'layers'), 'a') as dst:
            with open(path.join(TEMPLATES_DIR, 'system', 'snappyHexMesh', 'layers'), 'r') as src:
                temp = Template(src.read()).safe_substitute(name='lowerWall',
                                                            nSurfaceLayers=self.windTunnel.nSurfaceLayers.value(),
                                                            firstLayerThickness=self.windTunnel.firstLayerThickness.value(),
                                                            expansionRatio=self.windTunnel.expansionRatio.value())
                dst.write(temp)
                dst.write('\n')

        # Main loop of vehicles

        for i in range(self.vehiclesModel.rowCount()):
            vehicleName = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.NAME)), Qt.EditRole)
            stl = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.STL)), Qt.EditRole)
            stlSolids = solids(path.join(STL_DIR, stl))
            xMin = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.X_MIN)), Qt.EditRole)
            xMax = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.X_MAX)), Qt.EditRole)
            featureRefinement = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.FEATURE_REFINEMENT)), Qt.EditRole)
            surfaceRefinementMin = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.SURFACE_REFINEMENT_MIN)),
                Qt.EditRole)
            surfaceRefinementMax = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.SURFACE_REFINEMENT_MAX)),
                Qt.EditRole)
            nSurfaceLayers: dict = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.N_SURFACE_LAYERS)), Qt.EditRole)
            firstLayerThickness: dict = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.FIRST_LAYER_THICKNESS)), Qt.EditRole)
            expansionRatio: dict = self.vehiclesModel.data(
                self.vehiclesModel.index(i, self.vehiclesModel.attr.index(VHeaders.EXPANSION_RATIO)), Qt.EditRole)

            translate(path.join(STL_DIR, stl), path.join('constant', 'triSurface', f'{vehicleName}.stl'), xMin, 0, 0)

            with open(path.join('system', 'include', 'geometry'), 'a') as dst:
                with open(path.join(TEMPLATES_DIR, 'system', 'snappyHexMesh', 'geometry'), 'r') as src:
                    temp = Template(src.read()).safe_substitute(name=vehicleName,
                                                                file=f'{vehicleName}.stl')
                    dst.write(temp)
                    dst.write('\n')

            if featureRefinement > 0:
                with open(path.join('system', 'include', 'surfaces'), 'a') as dst:
                    dst.write(f'"{vehicleName}.stl"')
                    dst.write('\n')
                with open(path.join('system', 'include', 'features'), 'a') as dst:
                    with open(path.join(TEMPLATES_DIR, 'system', 'snappyHexMesh', 'features'), 'r') as src:
                        temp = Template(src.read()).safe_substitute(file=f'{vehicleName}.eMesh',
                                                                    level=featureRefinement)
                        dst.write(temp)
                        dst.write('\n')

            if surfaceRefinementMax > 0:
                with open(path.join('system', 'include', 'refinementSurfaces'), 'a') as dst:
                    with open(path.join(TEMPLATES_DIR, 'system', 'snappyHexMesh', 'refinementSurfaces'), 'r') as src:
                        temp = Template(src.read()).safe_substitute(name=vehicleName,
                                                                    min=surfaceRefinementMin,
                                                                    max=surfaceRefinementMax)
                        dst.write(temp)
                        dst.write('\n')

            nSurfaceLayers = {solid: value for solid, value in nSurfaceLayers.items() if value > 0}
            if len(nSurfaceLayers) > 0:
                with open(path.join('system', 'include', 'layers'), 'a') as dst:
                    for solid, value in nSurfaceLayers.items():
                        with open(path.join(TEMPLATES_DIR, 'system', 'snappyHexMesh', 'layers'), 'r') as src:
                            temp = Template(src.read()).safe_substitute(name=f'{vehicleName}_{solid}',
                                                                        nSurfaceLayers=value,
                                                                        firstLayerThickness=firstLayerThickness[solid],
                                                                        expansionRatio=expansionRatio[solid])
                            dst.write(temp)
                            dst.write('\n')

            with open(path.join('system', 'include', 'forceCoeffs'), 'a') as dst:
                with open(path.join(TEMPLATES_DIR, 'system', 'controlDict', 'forceCoeffs'), 'r') as src:
                    patches = ''
                    for solid in stlSolids:
                        patches += f'{vehicleName}_{solid} '
                    temp = Template(src.read()).safe_substitute(name=vehicleName,
                                                                patches=patches,
                                                                CofRX=(xMax - xMin) / 2,
                                                                magUInf=self.turbulence.speed.value(),
                                                                lRef=referenceLength(stl),
                                                                Aref=referenceArea(stl) / 2)
                    dst.write(temp)
                    dst.write('\n')

        # Main loop of regions

        for i in range(self.regionsModel.rowCount()):
            vehicleName = self.regionsModel.data(
                self.regionsModel.index(i, self.regionsModel.attr.index(RHeaders.NAME)), Qt.EditRole)
            xMin = self.regionsModel.data(
                self.regionsModel.index(i, self.regionsModel.attr.index(RHeaders.X_MIN)), Qt.EditRole)
            yMin = self.regionsModel.data(
                self.regionsModel.index(i, self.regionsModel.attr.index(RHeaders.Y_MIN)), Qt.EditRole)
            zMin = self.regionsModel.data(
                self.regionsModel.index(i, self.regionsModel.attr.index(RHeaders.Z_MIN)), Qt.EditRole)
            xMax = self.regionsModel.data(
                self.regionsModel.index(i, self.regionsModel.attr.index(RHeaders.X_MAX)), Qt.EditRole)
            yMax = self.regionsModel.data(
                self.regionsModel.index(i, self.regionsModel.attr.index(RHeaders.Y_MAX)), Qt.EditRole)
            zMax = self.regionsModel.data(
                self.regionsModel.index(i, self.regionsModel.attr.index(RHeaders.Z_MAX)), Qt.EditRole)
            refinement = self.regionsModel.data(
                self.regionsModel.index(i, self.regionsModel.attr.index(RHeaders.REFINEMENT)), Qt.EditRole)

            if refinement > 0:
                with open(path.join('system', 'include', 'geometry'), 'a') as dst:
                    with open(path.join(TEMPLATES_DIR, 'system', 'snappyHexMesh', 'refinementBox'), 'r') as src:
                        temp = Template(src.read()).safe_substitute(name=vehicleName,
                                                                    xMin=xMin, yMin=yMin, zMin=zMin,
                                                                    xMax=xMax, yMax=yMax, zMax=zMax)
                        dst.write(temp)
                        dst.write('\n')
                with open(path.join('system', 'include', 'refinementRegions'), 'a') as dst:
                    with open(path.join(TEMPLATES_DIR, 'system', 'snappyHexMesh', 'refinementRegions'), 'r') as src:
                        temp = Template(src.read()).safe_substitute(name=vehicleName,
                                                                    max=refinement)
                        dst.write(temp)
                        dst.write('\n')
