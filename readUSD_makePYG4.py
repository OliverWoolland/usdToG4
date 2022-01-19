# ------------------------------------------------------------------------------
# Libraries

# Pixar
from pxr import Usd

# General
import os
import argparse
import sys

# Geant4
import pyg4ometry as pyg4

# Local
import pyg4Helpers as pgh

# ------------------------------------------------------------------------------
# Support functions

# ------------------------------------------------------------------------------
# Process command line options

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('usd_input', type=str, 
                    help='The USD file to convert to GDML')
args = parser.parse_args()

stage_file = args.usd_input
stage = Usd.Stage.Open(f'{stage_file}')

# ------------------------------------------------------------------------------
# Set up G4 env

# registry to store gdml data
registry = pyg4.geant4.Registry()

# world solid and logical
worldSolid  = pyg4.geant4.solid.Box("worldSolid",  # name
                                    100000,        # x size
                                    100000,        # y size
                                    100000,        # z size
                                    registry)      # registry
worldLogical = pyg4.geant4.LogicalVolume(worldSolid,      # solid volume
                                         "G4_Galactic",   # material
                                         "worldLogical",  # name
                                         registry)        # registry
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
gdmlWriter.write("test.gdml")

# ------------------------------------------------------------------------------
# Visualise new layout

# viewer = pyg4.visualisation.VtkViewer()
# viewer.addLogicalVolume(worldLogical)
# #viewer.addAxes(20)
# #viewer.setWireframe()
# viewer.view()
