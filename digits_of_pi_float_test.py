# tested with Blender 2.78, 2.79, 2.80

import bpy
from mathutils import Vector

print()
pi42 = "314159265358979323846264338327950288419716"
print(pi42, '\n')
pi_vec = Vector()
for i in range(len(pi42)):
    pi_vec[0] = float(pi42[:i] + '.' + pi42[i:])
    matched = 0
    for d in str(pi_vec[0]).replace('.', '').strip('0'):
        if pi42[matched] != d:
            break
        matched += 1
    print("%2d " % i, "%2d " % matched, pi_vec[0])
print()
