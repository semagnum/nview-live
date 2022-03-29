import bpy
import time

from .obj_config import obj_types
from .ObjType import ObjType
from .coll_util import find_instanced_objs_in_colls
from .frame_handler import viewport_handler, add_viewport_handler, remove_viewport_handler
from .budget import budget_factory

allowed_navigation_types = {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'MIDDLEMOUSE',
                            'RIGHTMOUSE', 'LEFTMOUSE',
                            'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'MOUSESMARTZOOM', 'TRACKPADZOOM', 'TRACKPADPAN',
                            'MOUSEROTATE', 'WHEELINMOUSE', 'WHEELOUTMOUSE',
                            'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_4', 'NUMPAD_5', 'NUMPAD_6',
                            'NUMPAD_7', 'NUMPAD_8', 'NUMPAD_9', 'NUMPAD_0', 'NUMPAD_PERIOD'}


class NL_OT_ViewportLive(bpy.types.Operator):
    bl_idname = 'semagnum_nview_live.viewport'
    bl_label = 'Run nView Live'
    bl_description = 'Automatically hide/show objects in the viewport'
    bl_options = {'REGISTER'}

    run_delay: bpy.props.FloatProperty(
        name='Update delay',
        description='Delay before nView starts updating after view change (in seconds)',
        default=1.0,
        min=0.1,
        subtype='TIME',
        unit='TIME',
        soft_min=0.1,
        soft_max=2.0,
    )

    obj_types: bpy.props.CollectionProperty(type=ObjType)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'run_delay', slider=True)

        layout.label(text='Object types:')
        col = layout.column(align=True)
        for obj_type in self.obj_types.values():
            col.prop(obj_type, 'enabled', text=obj_type.obj_name, toggle=True, icon=obj_type.icon)

    def modal(self, context, event):
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            context.window_manager.nl_is_running = False
            context.area.header_text_set(text=None)
            remove_viewport_handler(self._handler)
            return {'CANCELLED'}

        if self.last_call > self.run_delay and not self.has_updated:
            self.has_updated = True
            try:
                viewport_handler(context, self.viable_objs)
            except Exception as e:
                self.report({'ERROR'}, 'Exiting due to internal error: {}'.format(str(e)))
                context.window_manager.nl_is_running = False
                return {'CANCELLED'}

        if event.type in allowed_navigation_types:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        if context.area.type == 'VIEW_3D':
            self.last_call = time.time()
            self.has_updated = True
            wm = context.window_manager
            excluded_objs = {}

            wm.nl_is_running = True

            if wm.nl_exclude_instanced_objects:
                excluded_objs = set(find_instanced_objs_in_colls(context.scene.collection))

            valid_obj_types = {o_type.obj_type for o_type in self.obj_types.values() if o_type.enabled}

            self.viable_objs = {o for o in context.scene.objects if o.type in valid_obj_types} - excluded_objs

            context.area.header_text_set("nView Live enabled. RMB, ESC: cancel")

            self._handler = add_viewport_handler(self)
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            context.window_manager.nl_is_running = False
            return {'CANCELLED'}

    def invoke(self, context, event):
        for obj_type, obj_name, icon, enabled in obj_types:
            new_type = self.obj_types.add()
            new_type.obj_type = obj_type
            new_type.obj_name = obj_name
            new_type.icon = icon
            new_type.enabled = enabled
        return context.window_manager.invoke_props_dialog(self)

