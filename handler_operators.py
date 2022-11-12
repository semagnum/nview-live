import bpy
import time

from .obj_config import obj_types
from .ObjType import ObjType
from .coll_util import find_instanced_objs_in_colls
from .frame_handler import viewport_handler, add_viewport_handler, remove_viewport_handler
from .budget import budget_factory
from .BoundBoxCache import BoundBoxCache

allowed_navigation_types = {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'RIGHTMOUSE', 'LEFTMOUSE'}


def build_obj_budget_cost_cache(all_objs, context, min_box_size):
    budgeter = budget_factory(context)()
    budget_cache = {obj.name_full: budgeter.budget_cost(context, obj) for obj in all_objs}
    bb_cache_calculator = BoundBoxCache()
    bound_box_cache = {obj.name_full: bb_cache_calculator.bound_box_calc(obj, min_box_size)
                       for obj in all_objs}
    return budget_cache, bound_box_cache


def is_nav_allowed(keyconfigs, event):
    keymaps = ((km.name, km.keymap_items.match_event(event))
               for kc in keyconfigs
               for km in kc.keymaps)
    return any(km is not None and (km.idname.startswith('view3d')
                                   or (km_name == 'Frames' and km.idname.startswith('screen')))
               for km_name, km in keymaps)


class NL_OT_ViewportLive(bpy.types.Operator):
    bl_idname = 'semagnum_nview_live.viewport'
    bl_label = 'Run nView Live'
    bl_description = 'Automatically hide/show objects in the viewport'
    bl_options = {'REGISTER'}

    playback_mode: bpy.props.BoolProperty(name='Playback Mode',
                                          description='Will constantly refresh viewport based on delay setting,'
                                                      'ideal for previewing animations',
                                          default=False)

    exclude_objs_in_instances: bpy.props.BoolProperty(name='Exclude instanced objects',
                                                      description='Exclude objects in collection instances from '
                                                                  'visibility tests (can make instances seem hidden '
                                                                  'when they are not)',
                                                      default=True)

    obj_types: bpy.props.CollectionProperty(type=ObjType)

    min_box_size: bpy.props.FloatProperty(name='Minimum Bounding Box Size',
                                          description='Minimum bounding box size for objects'
                                                      'without a determinable size'
                                                      '(such as lights or non-instancing empties)',
                                          unit='LENGTH', subtype='DISTANCE',
                                          default=0.1, min=0.001, soft_min=0.1, soft_max=1.0)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'min_box_size')
        layout.prop(self, 'playback_mode')
        layout.prop(self, 'exclude_objs_in_instances')

        layout.label(text='Object types:')
        col = layout.column(align=True)
        for obj_type in self.obj_types.values():
            col.prop(obj_type, 'enabled', text=obj_type.obj_name, toggle=True, icon=obj_type.icon)

    def update_caches(self, context):
        excluded_objs = set()
        if self.exclude_objs_in_instances:
            excluded_objs = {o.name_full for o in find_instanced_objs_in_colls(context.scene.collection)}

        valid_obj_types = {o_type.obj_type for o_type in self.obj_types.values() if o_type.enabled}

        self.viable_objs = {o
                            for o in context.scene.objects
                            if o.type in valid_obj_types
                            and o.name_full not in excluded_objs
                            and not o.hide_viewport}

        self.cost_cache, self.bb_cache = build_obj_budget_cost_cache(self.viable_objs, context, self.min_box_size)
        self.report({'INFO'}, 'Caching done, ready to use')

    def cancel(self, context):
        context.window_manager.nl_is_running = False
        context.area.header_text_set(text=None)
        remove_viewport_handler(self._handler)
        return {'CANCELLED'}

    def modal(self, context, event):
        window_manager = context.window_manager
        if is_nav_allowed(window_manager.keyconfigs, event):
            return {'PASS_THROUGH'}

        if event.type in {'ESC', 'RIGHTMOUSE'}:
            return self.cancel(context)

        run_delay = window_manager.nl_run_delay
        curr_time = time.time()
        should_update_playback_mode = self.playback_mode and (curr_time - self.last_run) > run_delay
        should_update_normal_mode = ((curr_time - self.last_call) > run_delay and not self.has_updated)
        if should_update_playback_mode or should_update_normal_mode:
            self.last_run = curr_time
            self.has_updated = True
            try:
                viewport_handler(context, self.viable_objs, self.cost_cache, self.bb_cache)
            except Exception as e:
                self.report({'ERROR'}, 'Exiting due to internal error: {}'.format(str(e)))
                return self.cancel(context)

        return {'PASS_THROUGH'}

    def execute(self, context):
        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

        self.last_call = time.time()
        self.last_run = time.time()
        self.has_updated = False
        wm = context.window_manager

        wm.nl_is_running = True

        self.update_caches(context)

        if self.playback_mode:
            header_text = 'nView Live playback mode. RMB, ESC: cancel'
        else:
            header_text = 'nView Live enabled. RMB, ESC: cancel'

        context.area.header_text_set(header_text)

        self._handler = add_viewport_handler(self)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        for obj_type, obj_name, icon, enabled in obj_types:
            new_type = self.obj_types.add()
            new_type.obj_type = obj_type
            new_type.obj_name = obj_name
            new_type.icon = icon
            new_type.enabled = enabled
        return context.window_manager.invoke_props_dialog(self)
