# ------------------------------------------------------------------------------
# Libraries

## Pixar
from pxr import Usd, Vt

## Geant4
import pyg4ometry as pyg4

## General
import math, os

## Local
import usdHelpers as uh
import pyg4Helpers as pgh

# ------------------------------------------------------------------------------
# Set up USD env

#stage = Usd.Stage.Open('../USDExamples/Kitchen_set/assets/Ball/Ball.usd')
stage = Usd.Stage.Open('../USDExamples/Kitchen_set/assets/GarlicRope/GarlicRope.usd')
#stage = Usd.Stage.Open('../USDExamples/Kitchen_set/Kitchen_set.usd')

# ------------------------------------------------------------------------------
# Set up G4 env

# registry to store gdml data
registry = pyg4.geant4.Registry()

# world solid and logical
worldSolid  = pyg4.geant4.solid.Box( "wordlSolid", # name
                                      2000,         # x size
                                      2000,         # y size
                                      2000,         # z size
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
    
    if (primType == "Mesh"):
        ## Get number of vertices in elements
        allVertexSpans   = uh.getValidProperty(x,"faceVertexCounts").Get()
        allVertexIndices = uh.getValidProperty(x,"faceVertexIndices").Get()
        allVertexPoints  = uh.getValidProperty(x,"points").Get()

        # ----------------------------------------------------------------------
        # Iterate through vertices collecting polygons
        
        polygons = []
        indexTracker = 0 
        for span in allVertexSpans:
            if (primID != 5):
                continue
            ## Get relevent indices
            indices = allVertexIndices[indexTracker:indexTracker+span]

            ## Build list of polygons
            if (span == 4): # break quadrilateral into two triangle
                firstIndices  = [indices[ii] for ii in [1,2,0]]
                #secondIndices = [indices[ii] for ii in [1,2,0]]

                polygons.append(pgh.getPointsDict (allVertexPoints, firstIndices))
                #polygons.append(pgh.getPointsDict (allVertexPoints, secondIndices))
            elif (span == 3):
                revIndices = [indices[ii] for ii in [0,2,1]] 
                polygons.append(pgh.getPointsDict (allVertexPoints, revIndices))
            else:
                raise Exception("Error: Incorrect number of vertices! nVert: " + str(span))

            ## Update Tracker
            indexTracker = indexTracker + span

        # ----------------------------------------------------------------------
        # Create volumes and append to world geometry

        try:            
            tess = pyg4.geant4.solid.createTessellatedSolid( 'mesh_'+str(primID),
                                                             polygons,
                                                             registry )
        
            tess_l = pyg4.geant4.LogicalVolume( tess,
                                                "G4_Fe",
                                                "tess_l_"+str(primID),
                                                registry
                                               )
            
            tess_p = pyg4.geant4.PhysicalVolume( [0, 0, 0],
                                                 [0, 0, 0],
                                                 tess_l,
                                                 "tess_p_"+str(primID),
                                                 worldLogical,
                                                 registry
                                                )
        except:
            print("Error creating Geant4 solid!")

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
