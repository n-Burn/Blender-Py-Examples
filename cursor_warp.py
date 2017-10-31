import bpy
import bgl
from mathutils import Vector
print("\nadd-on loaded.")


def draw_pt_2D(pt_co, pt_color, pt_size):
	if pt_co is not None:
		bgl.glEnable(bgl.GL_BLEND)
		bgl.glPointSize(pt_size)
		bgl.glColor4f(*pt_color)
		bgl.glBegin(bgl.GL_POINTS)
		bgl.glVertex2f(*pt_co)
		bgl.glEnd()
	return


def draw_callback_px(self, context):
	rgn, rv3d = self.rgn_rv3d
	
	size = 10
	colr = 0.0, 1.0, 0.0, 1.0  # green
	draw_pt_2D(self.mouse_co, colr, size)
	
	size = 1
	colr = 0.0, 0.0, 0.0, 1.0  # black
	draw_pt_2D(self.mouse_co, colr, size)
	
	size = 10
	colr = 1.0, 0.0, 0.0, 1.0  # red
	draw_pt_2D(self.mouse_prev, colr, size)
	
	size = 1
	colr = 0.0, 0.0, 0.0, 1.0  # black 
	draw_pt_2D(self.mouse_prev, colr, size)
	#__import__('code').interact(local=dict(globals(), **locals()))


class WarpTest(bpy.types.Operator):
	bl_idname = "object.warp_test"
	bl_label = "Warp Test"

	def modal(self, context, event):
		context.area.tag_redraw()
		
		if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
			# allow navigation
			return {'PASS_THROUGH'}
			
		if event.type == 'MOUSEMOVE':
			self.mouse_co = Vector((event.mouse_region_x, event.mouse_region_y))
			
		if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
			#print('left_click = True')
			area = context.area
			self.mouse_co = Vector((event.mouse_region_x, event.mouse_region_y))
			ms_back = self.mouse_prev.copy()
			win = None
			for i in area.regions:
				if i.type == "WINDOW":
					win = i
					break
			warpco = ms_back[0]+win.x, ms_back[1]+win.y
			context.window.cursor_warp(*warpco)
			#bpy.context.window.cursor_warp(*ms_back)
			self.mouse_prev = self.mouse_co.copy()

		if event.type == 'D' and event.value == 'RELEASE':
			# call debugger
			#self.debug_flag = True
			__import__('code').interact(local=dict(globals(), **locals()))

		if event.type in {'ESC', 'RIGHTMOUSE'}:
			print("add-on stopped.\n")
			bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		if context.area.type == 'VIEW_3D':
			print("add-on running.\n")  # debug
			args = (self, context)
			self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px,
					args, 'WINDOW', 'POST_PIXEL')

			self.mouse_co = Vector((event.mouse_region_x, event.mouse_region_y))
			self.mouse_prev = self.mouse_co.copy()
			self.left_click = False
			self.pts = []
			self.mous_hist = []
			self.debug_flag = False
			self.rgn_rv3d = context.region, context.region_data

			context.window_manager.modal_handler_add(self)

			return {'RUNNING_MODAL'}
		else:
			self.report({'WARNING'}, "View3D not found, cannot run operator")
			return {'CANCELLED'}


def register():
	bpy.utils.register_class(WarpTest)

def unregister():
	bpy.utils.unregister_class(WarpTest)

if __name__ == "__main__":
	register()

