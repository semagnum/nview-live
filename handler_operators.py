import bpy
import time

from .obj_config import obj_types
from .ObjType import ObjType
from .coll_util import find_instanced_objs_in_colls
from .frame_handler import viewport_handler, add_viewport_handler, remove_viewport_handler
from .budget import budget_factory
from .BoundBoxCache import BoundBoxCache

allowed_navigation_types = {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'MIDDLEMOUSE',
                            'RIGHTMOUSE', 'LEFTMOUSE',
                            'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'MOUSESMARTZOOM', 'TRACKPADZOOM', 'TRACKPADPAN',
                            'MOUSEROTATE', 'WHEELINMOUSE', 'WHEELOUTMOUSE',
                            'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_4', 'NUMPAD_5', 'NUMPAD_6',
                            'NUMPAD_7', 'NUMPAD_8', 'NUMPAD_9', 'NUMPAD_0', 'NUMPAD_PERIOD'}


def build_obj_budget_cost_cache(all_objs, context):
    budgeter = budget_factory(context)()
    budget_cache = {obj.name_full: budgeter.budget_cost(context, obj) for obj in all_objs}
    bb_cache_calculator = BoundBoxCache()
    bound_box_cache = {obj.name_full: bb_cache_calculator.bound_box_calc(obj) for obj in all_objs}
    return budget_cache, bound_box_cache


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

    exclude_objs_in_instances: bpy.props.BoolProperty(name='Exclude instanced objects',
                                                      description='Exclude objects in collection instances from '
                                                                  'visibility tests (can make instances seem hidden '
                                                                  'when they are not)',
                                                      default=True)

    obj_types: bpy.props.CollectionProperty(type=ObjType)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'run_delay', slider=True)
        layout.prop(self, 'exclude_objs_in_instances')

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
                viewport_handler(context, self.viable_objs, self.cost_cache, self.bb_cache)
            except Exception as e:
                self.report({'ERROR'}, 'Exiting due to internal error: {}'.format(str(e)))
                context.window_manager.nl_is_running = False
                return {'CANCELLED'}

        if event.type in allowed_navigation_types:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

        self.last_call = time.time()
        self.has_updated = False
        wm = context.window_manager
        excluded_objs = set()

        wm.nl_is_running = True

        if self.exclude_objs_in_instances:
            excluded_objs = {o.name_full for o in find_instanced_objs_in_colls(context.scene.collection)}

        valid_obj_types = {o_type.obj_type for o_type in self.obj_types.values() if o_type.enabled}

        self.viable_objs = {o
                            for o in context.scene.objects
                            if o.type in valid_obj_types
                            and o.name_full not in excluded_objs}

        self.cost_cache, self.bb_cache = build_obj_budget_cost_cache(self.viable_objs, context)

        context.area.header_text_set("nView Live enabled. RMB, ESC: cancel")

        self._handler = add_viewport_handler(self)
        context.window_manager.modal_handler_add(self)

        self.report({'INFO'}, 'Initialization done, ready to navigate 3D view')
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        for obj_type, obj_name, icon, enabled in obj_types:
            new_type = self.obj_types.add()
            new_type.obj_type = obj_type
            new_type.obj_name = obj_name
            new_type.icon = icon
            new_type.enabled = enabled
        return context.window_manager.invoke_props_dialog(self)
