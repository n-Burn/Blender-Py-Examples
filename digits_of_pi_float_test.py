import bpy
from mathutils import Vector

print()
pi42 = "314159265358979323846264338327950288419716"
for i in range( 0, len(pi42) ):
    piFlt = float( pi42[:i] + '.' + pi42[i:] )
    piVec = Vector(( i, piFlt ))
    print( '%2d' % int(piVec[0]), piVec[1] )
