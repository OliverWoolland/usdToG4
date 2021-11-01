from pxr import Usd

def propertyIsValid (primative, parameterName):
    # Get param
    prop = primative.GetProperty(parameterName)
    
    # Test validity
    if ( type(prop) == type(Usd.Attribute())): # is valid
        return True
    else:
        return False

def getProperty (primative, parameterName): # Unsafe 
    # Get param
    prop = primative.GetProperty(parameterName).Get()

    return prop

def getValidProperty (primative, parameterName):
    # Get param
    prop = primative.GetProperty(parameterName)
    
    # Test validity
    if ( type(prop) == type(Usd.Attribute())): # is valid
        return prop.Get()
    else: # is not
        print("Requested parameter is not valid!")
        return None
        #raise Exception("Requested parameter is not valid!")
    
