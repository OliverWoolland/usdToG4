import math
import numpy as np

## Geant4
import pyg4ometry as pyg4

## Local
import usdHelpers as uh

def _addVolumes ( tess,
                  material,
                  position,
                  rotation,
                  registry,
                  worldLogical,
                  primID):
    
    # ----------------------------------------------------------------------
    # Create volumes and append to world geometry
    print(position)
    try:            
        tess_l = pyg4.geant4.LogicalVolume( tess,
                                            material,
                                            "tess_l_"+str(primID),
                                            registry
                                           )
            
        tess_p = pyg4.geant4.PhysicalVolume( rotation,
                                             position,
                                             tess_l,
                                             "tess_p_"+str(primID),
                                             worldLogical,
                                             registry
                                            )
        return 0
    except Exception as e:
        print("Error creating Geant4 solid! " + str(e))
        return -1

def addCube (cube, registry, worldLogical, primID):
    #print(cube.GetPropertyNames())    
    
    sideLength = uh.getValidProperty(cube,"size")
    rotation = list(uh.getValidProperty(cube,"xformOp:rotateXYZ"))
    position = list(uh.getValidProperty(cube,"xformOp:translate"))
    
    tess = pyg4.geant4.solid.Box( 'box_'+str(primID),
                                  sideLength, # x
                                  sideLength, # y
                                  sideLength, # z
                                  registry )
        
    success = _addVolumes( tess,
                           "G4_Fe",
                           position, 
                           rotation,
                           registry,
                           worldLogical,
                           primID
                          )
    
    return success

def addCone (cone, registry, worldLogical, primID):
    #print(cone.GetPropertyNames())    

    height = uh.getValidProperty(cone,"height")
    radius = uh.getValidProperty(cone,"radius")
    rotation = list(uh.getValidProperty(cone,"xformOp:rotateXYZ"))
    position = list(uh.getValidProperty(cone,"xformOp:translate"))

    tess = pyg4.geant4.solid.Cons( 'cone_'+str(primID),
                                   0, radius, # inner, outer radius at start
                                   0, 0, # inner, outer radius at end
                                   height, # length along z
                                   0, 2*math.pi, # starting, finishing phi
                                   registry)
                                  
    success = _addVolumes( tess,
                           "G4_Fe",
                           position, 
                           rotation,
                           registry,
                           worldLogical,
                           primID
                          )
    return success    

def addCapsule (capsule, registry, worldLogical, primID):
    print(capsule.GetPropertyNames())    
    print("CAPSULE NOT IMPLEMENTED")
    success = 0
    return success

def addCylinder (cylinder, registry, worldLogical, primID):
    #print(cylinder.GetPropertyNames())    

    height = uh.getValidProperty(cylinder,"height")
    radius = uh.getValidProperty(cylinder,"radius")
    rotation = list(uh.getValidProperty(cylinder,"xformOp:rotateXYZ"))
    position = list(uh.getValidProperty(cylinder,"xformOp:translate"))

    tess = pyg4.geant4.solid.Tubs( 'cylinder_'+str(primID),
                                   0, radius, # inner, outer radius at start
                                   height, # length along z
                                   0, 2*math.pi, # starting, finishing phi
                                   registry)
                                  
    success = _addVolumes( tess,
                           "G4_Fe",
                           position, 
                           rotation,
                           registry,
                           worldLogical,
                           primID
                          )
    return success

def addSphere (sphere, registry, worldLogical, primID):
    #print(sphere.GetPropertyNames())    

    radius = uh.getValidProperty(sphere,"radius")
    rotation = list(uh.getValidProperty(sphere,"xformOp:rotateXYZ"))
    position = list(uh.getValidProperty(sphere,"xformOp:translate"))

    tess = pyg4.geant4.solid.Orb( 'sphere_'+str(primID),
                                   radius, # inner, outer radius at start
                                   registry)
                                  
    success = _addVolumes( tess,
                           "G4_Fe",
                           position, 
                           rotation,
                           registry,
                           worldLogical,
                           primID
                          )
    return success

def addMesh (x, registry, worldLogical, primID):
    print(x.GetPropertyNames())    

    ## Get number of vertices in elements
    allVertexSpans   = uh.getValidProperty(x,"faceVertexCounts")
    allVertexIndices = uh.getValidProperty(x,"faceVertexIndices")
    allVertexPoints  = uh.getValidProperty(x,"points")

    print(uh.propertyIsValid(x,"xformOp:rotateXYZ"))
    #rotation = list(uh.getProperty(x,"xformOp:rotateXYZ")) if uh.propertyIsValid(x,"xformOp:rotateXYZ") else [0,0,0]
    rotation = [0,0,0] if not uh.propertyIsValid(x,"xformOp:rotateXYZ") else list(uh.getProperty(x,"xformOp:rotateXYZ"))
    position = [0,0,0] if not uh.propertyIsValid(x,"xformOp:translate") else list(uh.getProperty(x,"xformOp:translate"))

    # ----------------------------------------------------------------------
    # Iterate through vertices collecting polygons

    facets = []

    indexTracker = 0
    for span in allVertexSpans:
        ## Get relevent indices
        indices = allVertexIndices[indexTracker:indexTracker+span]

        ## Build list of polygons
        idx = [indices[ii] for ii in range(0,span)]
        
        if (span > 4): # break quadrilateral into two triangle
            print("Cannot yet handle > 4 vertexes!")
            continue
        
        elif (span == 4): # break quadrilateral into two triangle
            firstIndices  = [indices[ii] for ii in [2,1,0]] #[0,2,1]] # [2,1,0] at least good in py
            vertex = _getPointsDict (allVertexPoints, firstIndices)
            facets.append([vertex])

            secondIndices = [indices[ii] for ii in [0,3,2]] #[1,3,0]] # [2,3,0] at least good in py            
            vertex = _getPointsDict (allVertexPoints, secondIndices)
            facets.append([vertex])

        elif (span == 3):
           revIndices = [indices[ii] for ii in [2,1,0]] 
           vertex = _getPointsDict (allVertexPoints, revIndices)
           facets.append([vertex])
        else:
           raise Exception("Error: Incorrect number of vertices! nVert: " + str(span))
    
        ## Update Tracker
        indexTracker = indexTracker + span
        
    tess = pyg4.geant4.solid.TessellatedSolid( 'mesh_'+str(primID),
                                               facets,
                                               registry,
                                               3
                                              ) 
    
    # tess = pyg4.geant4.solid.createTessellatedSolid( 'mesh_'+str(primID),
    #                                                  sortedPolygons,
    #                                                  registry )

    # tess = pyg4.geant4.solid.TessellatedSolid( 'mesh_'+str(primID),
    #                                            sortedPolygons,
    #                                            registry,
    #                                            3
    #                                           ) 

    success = _addVolumes( tess,
                           "G4_Fe",
                           position, 
                           rotation,
                           registry,
                           worldLogical,
                           primID
                          )
    
    return success

def _getPointsDict ( allVertexPoints, indices ):

    if ( len(indices) != 3 ):
        raise Exception("Error: Incorrect number of indices! nInd: " + str(len(indices)))

    ## Create dict representing three vector for each vertex point
    points = [ ( allVertexPoints[ii][0],  # x
                 allVertexPoints[ii][1],  # y
                 allVertexPoints[ii][2] ) # z
               for ii in indices ]

    return points

def orderPoints ( polygons ):
    npPolygons = np.array(polygons)
    
    sortedPolys = []
    for poly in npPolygons:
        x = poly[:,0]
        y = poly[:,1]
        z = poly[:,2]

        # Find heighest point
        highestZ_idx = np.argmax(z)

        # Get angle from highest point
        dx = x - x[highestZ_idx]
        dy = y - y[highestZ_idx]

        theta = np.arctan2(dy,dx)

        # Perform sort
        sortOrder = np.argsort(theta)
        sortedPoly = []
        for pos in sortOrder:
            sortedPoly.append(tuple(poly[pos,:]))
        sortedPolys.append(sortedPoly)

    print(sortedPolys)
    return sortedPolys

def makePlot (polygons):
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # x = []
    # y = []
    # z = []
    # for poly in polygons:
    #     for point in poly:
    #         x.append(point[0])
    #         y.append(point[1])
    #         z.append(point[2])
    #     # x.append(poly[0][0])
    #     # y.append(poly[0][1])
    #     # z.append(poly[0][2])
    # ax.plot(x,y,z)

    for poly in polygons:
        x = []
        y = []
        z = []

        for point in poly:
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])

            ax.scatter( point[0],
                        point[1],
                        point[2],
                        marker='o'
                       )

        x.append(poly[0][0])
        y.append(poly[0][1])
        z.append(poly[0][2])

        ax.plot(x,y,z)

    #ax.plot_surface(polygons, cmap='jet')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.draw()
    plt.show()

    return
