from pxr import Usd, Vt
stage = Usd.Stage.Open('HelloWorld.usda')

for x in stage.Traverse():
    print(x.GetTypeName())
