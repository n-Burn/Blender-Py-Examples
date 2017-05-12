#==========================================================
#
# Distance Button Example
# 
# distance_button.py
# 
# Tracks the mouse cursor's location in relation to two
# points drawn on screen. These points will change
# color depending on the cursor's location:
#   The point the cursor is closest to is green
#   The point the cursor is furthest from is grey
# 
# When a Left Mouse Click is detected, a specific message 
# will be printed to the console depending on which point
# the mouse cursor is closest to.
# 
# Tested with Blender 2.78c
#  
#==========================================================

import bpy
import bgl
import blf

from mathutils import Vector
from mathutils.geometry import intersect_line_line_2d
from math import fmod, sqrt

print("\n\n  Loaded: distance_button\n")  # debug


def get_dist_2D(x1,y1,x2,y2):
    return sqrt( abs( ((x2-x1)**2) + ((y2-y1)**2) ) )


def draw_pt_2D(pt_co, pt_color):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glPointSize(16)
    bgl.glColor4f(*pt_color)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(*pt_co)
    bgl.glEnd()
    return


def drawBox(boxCo, color):
    bgl.glColor4f(*color)  #black or white?
    bgl.glBegin(bgl.GL_LINE_STRIP)
    for coord in boxCo:
        bgl.glVertex2f( coord[0], coord[1] )
    bgl.glVertex2f( boxCo[0][0], boxCo[0][1] )
    bgl.glEnd()

    return


def get_box_coor(origin,rWidth,rHeight,xOffset,yOffset):
    coBL = (origin[0] + xOffset), (origin[1] + yOffset)
    coTL = (origin[0] + xOffset), (rHeight - yOffset)
    coTR = (rWidth - xOffset), (rHeight - yOffset)
    coBR = (rWidth - xOffset), (origin[1] + yOffset)
    return [coBL, coTL, coTR, coBR]


def draw_callback_px(self, context):
    colorGrey = [1.0, 1.0, 1.0, 0.25]
    colorGreen  = [0.0, 1.0, 0.0, 0.5]

    mouseLoc = self.mouse

    region = bpy.context.region
    offsetPerc = 0.8
    width = region.width
    height = region.height
    widthOffs = width * offsetPerc
    heightOffs = height / 2

    X1 = width - widthOffs
    X2 = widthOffs
    co1 = [X1, heightOffs]
    co2 = [X2, heightOffs]

    ms_co1_dis = get_dist_2D(*co1, *mouseLoc)
    ms_co2_dis = get_dist_2D(*co2, *mouseLoc)

    if   ms_co1_dis < ms_co2_dis:
        draw_pt_2D(co1, colorGreen)
        draw_pt_2D(co2, colorGrey)
        if self.L_click == True:
            print("Closer to Coor 1!")
    elif ms_co2_dis < ms_co1_dis:
        draw_pt_2D(co1, colorGrey)
        draw_pt_2D(co2, colorGreen)
        if self.L_click == True:
            print("Closer to Coor 2!")
    else:
        draw_pt_2D(co1, colorGrey)
        draw_pt_2D(co2, colorGrey)

    self.L_click = False


class ModalDrawOperator(bpy.types.Operator):
    '''Draw a line with the mouse'''
    bl_idname = "view3d.modal_operator"
    bl_label = "Simple Modal View3D Operator"

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_4', 'NUMPAD_6', 'NUMPAD_7', 'NUMPAD_8', 'NUMPAD_9', 'NUMPAD_5'}:
            return {'PASS_THROUGH'}

        if event.type == 'MOUSEMOVE':
            self.mouse = (event.mouse_region_x, event.mouse_region_y)

        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            self.L_click = True

        if event.type == 'ESC':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = (self, context)

            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            
            # initialize these with negative values to prevent false positives
            self.mouse = (-5000,-5000)
            self.L_click = False

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalDrawOperator)

def unregister():
    bpy.utils.unregister_class(ModalDrawOperator)

if __name__ == "__main__":
    register()
