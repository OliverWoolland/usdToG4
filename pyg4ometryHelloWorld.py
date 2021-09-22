import pyg4ometry

# registry to store gdml data
reg  = pyg4ometry.geant4.Registry()

# world solid and logical
ws   = pyg4ometry.geant4.solid.Box("ws",50,50,50,reg)
wl   = pyg4ometry.geant4.LogicalVolume(ws,"G4_Galactic","wl",reg)
reg.setWorld(wl.name)

# box placed at origin
b1   = pyg4ometry.geant4.solid.Box("b1",10,10,10,reg)
b1_l = pyg4ometry.geant4.LogicalVolume(b1,"G4_Fe","b1_l",reg)
b1_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,0],b1_l,"b1_p",wl,reg)

# visualise geometry
v = pyg4ometry.visualisation.VtkViewer()
v.addLogicalVolume(wl)
v.addAxes(20)
v.view()
