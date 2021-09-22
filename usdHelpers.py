from pxr import Usd

def getValidProperty (primative, parameterName):
    # Get param
    prop = primative.GetProperty(parameterName)
    
    # Test validity
    if ( type(prop) == type(Usd.Attribute())): # is valid
        return prop
    else: # is not
        raise Exception("Requested parameter is not valid!")
    
