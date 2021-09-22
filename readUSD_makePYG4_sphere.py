from pxr import Usd, Vt
import pyg4ometry, math

import usdHelpers as uh

# ------------------------------------------------------------------------------
# Set up USD env

stage = Usd.Stage.Open('../USDExamples/Kitchen_set/assets/Ball/Ball.usd')

# ------------------------------------------------------------------------------
# Set up G4 env

# registry to store gdml data
registry  = pyg4ometry.geant4.Registry()

# world solid and logical
ws   = pyg4ometry.geant4.solid.Box("ws",2,2,2,registry)
wl   = pyg4ometry.geant4.LogicalVolume(ws,"G4_Galactic","wl",registry)
registry.setWorld(wl.name)

# ------------------------------------------------------------------------------
# Begin traversing USD

for x in stage.Traverse():
    primType = x.GetTypeName()
    print("PRIM: " + str(primType))
    
    if (primType == "Sphere"):
        radius = uh.getValidProperty(x,"radius")
        print(radius.Get())
        sph = pyg4ometry.geant4.solid.Orb("orb",           # name  
                                          math.pi,         # radius
                                          registry,        # registry
                                          lunit='mm',      # length unit
                                          nslice=None,     # number of phi segs
                                          nstack=None,     # number of theta segs
                                          addRegistry=True # 
                                          )
        sph_l = pyg4ometry.geant4.LogicalVolume(sph,
                                                "G4_Fe",
                                                "sph_l",
                                                registry)
        sph_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                 [0,0,0],
                                                 sph_l,
                                                 "sph_p",
                                                 wl,
                                                 registry)

# ------------------------------------------------------------------------------
# Visualise new layout

# visualise geometry
v = pyg4ometry.visualisation.VtkViewer()
v.addLogicalVolume(wl)
v.addAxes(20)
v.view()

# ------------------------------------------------------------------------------
# Writeout to GDML file

# gdml output
# w = _gd.Writer()
# w.addDetector(reg)
# w.write(_os.path.join(_os.path.dirname(__file__), "T033_TessellatedSolid.gdml"))
# w.writeGmadTester(_os.path.join(_os.path.dirname(__file__), "T033_TessellatedSolid.gmad"), "T033_TessellatedSolid.gdml")
