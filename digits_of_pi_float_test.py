# tested with Blender 2.78c

import bpy
from mathutils import Vector

print()
pi42 = "314159265358979323846264338327950288419716"
for i in range(0, len(pi42)):
    pi_flt = float(pi42[:i] + '.' + pi42[i:])
    pi_vec = Vector((i, pi_flt))
    print('%2d' % pi_vec[0], pi_vec[1])
