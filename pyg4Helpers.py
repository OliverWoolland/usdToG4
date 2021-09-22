def getPointsDict ( allVertexPoints, indices ):

    if ( len(indices) != 3 ):
        raise Exception("Error: Incorrect number of indices! nInd: " + str(len(indices)))

    ## Create dict representing three vector for each vertex point
    points = [ ( allVertexPoints[ii][0],  # x
                 allVertexPoints[ii][1],  # y
                 allVertexPoints[ii][2] ) # z
               for ii in indices ]

    return points
