import bpy
from mathutils import Vector

print()
x = "314159265358979323846264338327950288419716"
for i in range( 0, len(x) ):
	y = float( x[:i] + '.' + x[i:] )
	z = Vector(( i, y ))
	print( '%2d' % int(z[0]), z[1] )
