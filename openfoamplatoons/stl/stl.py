from os import system

"""
solid name
facet normal Ni Nj Nk
    outer loop
        vertex V1x V1y V1z
        vertex V2x V2y V2z
        vertex V3x V3y V3z
    endloop
endfacet
endsolid name
"""


def coordinates(stlFile: str):
    xMin = yMin = zMin = None
    xMax = yMax = zMax = None

    with open(stlFile) as f:
        lines = iter(f.readlines())
        while True:
            try:
                line = next(lines)
                if 'solid' in line or 'endsolid' in line:
                    continue
                if 'facet normal' in line or 'endfacet' in line:
                    continue
                if 'outer loop' in line or 'endloop' in line:
                    continue
                (V1, V2, V3) = line.split()[1:]
                V1 = float(V1)
                V2 = float(V2)
                V3 = float(V3)
                if not xMin or V1 < xMin:
                    xMin = V1
                if not yMin or V2 < yMin:
                    yMin = V2
                if not zMin or V3 < zMin:
                    zMin = V3
                if not xMax or V1 > xMax:
                    xMax = V1
                if not yMax or V2 > yMax:
                    yMax = V2
                if not zMax or V3 > zMax:
                    zMax = V3
            except StopIteration:
                break
    return xMin, yMin, zMin, xMax, yMax, zMax


def solids(stlFile: str):
    # STL files exported by Paraview have such lines:
    # solid Visualization Toolkit generated SLA File
    solidList = set()
    with open(stlFile) as f:
        lines = iter(f.readlines())
        while True:
            try:
                line = next(lines)
                if 'endsolid' in line:
                    continue
                if 'solid' in line:
                    solidList.add(' '.join(line.split()[1:]))
            except StopIteration:
                break
    return solidList


def translate(stlFile: str, outputFile: str, x: float, y: float, z: float):
    system(f'surfaceTransformPoints -translate "({x} {y} {z})" {stlFile} {outputFile}')
