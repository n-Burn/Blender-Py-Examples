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
# the mouse cursor was closest to.
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


def get_dist_2D(x1, y1, x2, y2):
    return sqrt( abs( ((x2-x1)**2) + ((y2-y1)**2) ) )


def draw_pt_2D(pt_co, pt_color):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glPointSize(16)
    bgl.glColor4f(*pt_color)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(*pt_co)
    bgl.glEnd()
    return


def draw_callback_px(self, context):
    color_grey = 1.0, 1.0, 1.0, 0.25
    color_green = 0.0, 1.0, 0.0, 0.5

    region = bpy.context.region
    offset_perc = 0.8
    width = region.width
    height = region.height
    width_offs = width * offset_perc
    height_offs = height / 2

    x1 = width - width_offs
    x2 = width_offs
    co1 = x1, height_offs
    co2 = x2, height_offs

    ms_co1_dis = get_dist_2D(*co1, *self.mouse_co)
    ms_co2_dis = get_dist_2D(*co2, *self.mouse_co)

    if   ms_co1_dis < ms_co2_dis:
        draw_pt_2D(co1, color_green)
        draw_pt_2D(co2, color_grey)
        if self.left_mouse is True:
            print("Closer to Coor 1!")
    elif ms_co2_dis < ms_co1_dis:
        draw_pt_2D(co1, color_grey)
        draw_pt_2D(co2, color_green)
        if self.left_mouse is True:
            print("Closer to Coor 2!")
    else:
        draw_pt_2D(co1, color_grey)
        draw_pt_2D(co2, color_grey)

    self.left_mouse = False


class ModalDisBtnOperator(bpy.types.Operator):
    '''Highlight which of 2 drawn points is closer to the mouse'''
    bl_idname = "view3d.modal_disbtn_operator"
    bl_label = "Basic Distance Button Operator"

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE',
                          'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3',
                          'NUMPAD_4', 'NUMPAD_5', 'NUMPAD_6',
                          'NUMPAD_7', 'NUMPAD_8', 'NUMPAD_9',}:
            return {'PASS_THROUGH'}

        if event.type == 'MOUSEMOVE':
            self.mouse_co = event.mouse_region_x, event.mouse_region_y

        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            self.left_mouse = True

        if event.type in {'ESC', 'RIGHTMOUSE'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = self, context

            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            
            # initialize these with negative values to prevent false positives
            self.mouse_co = -5000, -5000
            self.left_mouse = False

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalDisBtnOperator)

def unregister():
    bpy.utils.unregister_class(ModalDisBtnOperator)

if __name__ == "__main__":
    register()
