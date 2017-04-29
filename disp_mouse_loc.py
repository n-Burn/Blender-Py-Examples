#################################################
#
#  Display Mouse Location Example
#
#  disp_mouse_loc.py
#
#  Left clicking places a point
#    The mouse's 2D location and distance from
#    the last point are displayed on the bottom
#    left of the 3D View.
#  
#  If you click the mouse within 80 pixels of a
#  point, the point will be relocated to where
#  you just clicked.
#  
#  Tested with Blender 2.78c
#  
#################################################

import bpy
import bgl
import blf
from math import sqrt

print("\n\n\n  Add-on Loaded!\n") # debug


def get_dist_2D(pt1,pt2):
    x1, y1, x2, y2 = pt1[0], pt1[1], pt2[0], pt2[1]
    return sqrt( abs( ((x2-x1)**2) + ((y2-y1)**2) ) )


def draw_font_at_pt(text, pt_co, pt_color):
    font_id = 0
    bgl.glColor4f(*pt_color)
    blf.position(font_id, pt_co[0], pt_co[1], 0)
    blf.size(font_id, 32, 48)
    blf.draw(font_id, text)
    w, h = blf.dimensions(font_id, text)
    return [w, h]


def draw_pt_2D(pt_co, pt_color):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glPointSize(7)
    bgl.glColor4f(*pt_color)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(*pt_co)
    bgl.glEnd()
    return


def draw_callback_px(self, context):
    colorWhite  = [1.0, 1.0, 1.0, 1.0]
    colorGreen  = [0.0, 1.0, 0.0, 0.5]
    colorYellow = [1.0, 1.0, 0.5, 1.0]

    draw_font_at_pt("Mouse Loc: "+str(self.mouse[0])+', '+str(self.mouse[1]), [70,64], colorGreen )
    
    if self.ptStr != []:
        draw_pt_2D( self.ptStr, colorWhite )
        self.distFrClick = get_dist_2D( self.ptStr, self.mouse )
    
    draw_font_at_pt ( "Dist from point: " + format(self.distFrClick, '.2f'), [70,40], colorYellow )    
    #draw_font_at_pt ( "Dist from point: " + str(distFrClick), [70,40], colorYellow )    


class MouseLocDispOperator(bpy.types.Operator):
    """Draw dots with the mouse"""
    bl_idname = "view3d.display_ms_loc"
    bl_label = "Display Mouse Location"

    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'A', 'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_4', 'NUMPAD_6', 'NUMPAD_7', 'NUMPAD_8', 'NUMPAD_9', 'NUMPAD_5'}:
            return {'PASS_THROUGH'}

        if event.type == 'MOUSEMOVE':
            self.mouse = (event.mouse_region_x, event.mouse_region_y)

        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            click_loc = (event.mouse_region_x, event.mouse_region_y)
            if abs( self.distFrClick) < 80:
                self.ptStr = [ *click_loc ]

        if event.type == 'ESC':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            self.ptStr = []
            self.mouse = (-5000,-5000)
            self.distFrClick = -1.0

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(MouseLocDispOperator)

def unregister():
    bpy.utils.unregister_class(MouseLocDispOperator)

if __name__ == "__main__":
    register()