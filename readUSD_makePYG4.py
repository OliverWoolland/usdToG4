# ------------------------------------------------------------------------------
# Libraries

## Pixar
from pxr import Usd, Vt

## General
import math, os
import matplotlib.pyplot as plt
import numpy as np

## Geant4
import pyg4ometry as pyg4

## Local
import usdHelpers as uh
import pyg4Helpers as pgh

# ------------------------------------------------------------------------------
# Support functions

# ------------------------------------------------------------------------------
# Set up USD env

#stage = Usd.Stage.Open('../USDExamples/Kitchen_set/assets/Ball/Ball.usd')
#stage = Usd.Stage.Open('../USDExamples/Kitchen_set/assets/GarlicRope/GarlicRope.usd')
#stage = Usd.Stage.Open('../USDExamples/Kitchen_set/Kitchen_set.usd')

#stage = Usd.Stage.Open('../USDExamples/omniverse/example_meshAndShape.usd')
stage = Usd.Stage.Open('../USDExamples/omniverse/example_mesh.usd')
#stage = Usd.Stage.Open('../USDExamples/omniverse/example_shape.usd')
#stage = Usd.Stage.Open('../USDExamples/omniverse/example_cubes.usd')
#stage = Usd.Stage.Open('../USDExamples/omniverse/example_spheres.usd')
stage = Usd.Stage.Open('../USDExamples/omniverse/cppscript.usd')

#stage = Usd.Stage.Open('../USDExamples/PointInstancedMedCity.usd')
#stage = Usd.Stage.Open('../USDExamples/UsdSkelExamples/HumanFemale/HumanFemale.usd')

#stage = Usd.Stage.Open('../USDExamples/Reactor/octomak4.usd')

# ------------------------------------------------------------------------------
# Set up G4 env

# registry to store gdml data
registry = pyg4.geant4.Registry()

# world solid and logical
worldSolid  = pyg4.geant4.solid.Box( "worldSolid", # name
                                     100000,         # x size
                                     100000,         # y size
                                     100000,         # z size
                                     registry )     # registry
worldLogical = pyg4.geant4.LogicalVolume( worldSolid,     # solid volume
                                          "G4_Galactic",  # material
                                          "worldLogical", # name
                                          registry )      # registry
registry.setWorld(worldLogical.name)

# ------------------------------------------------------------------------------
# Begin traversing USD

primID = -1
for x in stage.Traverse():
    primID = primID + 1

    primType = x.GetTypeName()
    print("PRIM: " + str(primType))

    tess = None
    if (primType == "Cube"):
        tess = pgh.addCube(x, registry, worldLogical, primID)
    elif (primType == "Cone"):
        tess = pgh.addCone(x, registry, worldLogical, primID)
    elif (primType == "Capsule"):
        pass
        #tess = pgh.addCapsule(x, registry, worldLogical, primID)
    elif (primType == "Cylinder"):
        tess = pgh.addCylinder(x, registry, worldLogical, primID)
    elif (primType == "Sphere"):
        tess = pgh.addSphere(x, registry, worldLogical, primID)
    elif (primType == "Mesh"):
        tess = pgh.addMesh(x, registry, worldLogical, primID)
    else:
        print("Missed prim type: " + primType)
        
# ------------------------------------------------------------------------------
# Perform check on geometry

# worldLogical.checkOverlaps( recursive=True,
#                             coplanar=True,
#                             debugIO=False
#                            )

# ------------------------------------------------------------------------------
# Writeout to GDML file

gdmlWriter = pyg4.gdml.Writer()
gdmlWriter.addDetector(registry)
gdmlWriter.write(os.path.join(os.path.dirname(__file__), "test.gdml"))

# ------------------------------------------------------------------------------
# Visualise new layout

viewer = pyg4.visualisation.VtkViewer()
viewer.addLogicalVolume(worldLogical)
#viewer.addAxes(20)
#viewer.setWireframe()
viewer.view()

# ------------------------------------------------------------------------------
# Read GDML file

# import xml.etree.ElementTree as ET
# tree = ET.parse('test.gdml')
# root = tree.getroot()

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

# x = []
# y = []
# z = []

# for el in root.iter('position'):
#     ex = float(el.attrib.get('x'))
#     ey = float(el.attrib.get('y'))
#     ez = float(el.attrib.get('z'))

#     x.append(ex)
#     y.append(ey)
#     z.append(ez)

#     ax.scatter( ex,
#                 ey,
#                 ez,
#                 marker='o'
#                )
