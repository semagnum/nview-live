# Copyright (C) 2023 Spencer Magnusson
# semagnum@gmail.com
# Created by Spencer Magnusson
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


import bpy
import time

from .obj_config import obj_types
from .ObjType import ObjType
from .coll_util import find_instanced_objs_in_colls
from .frame_handler import viewport_handler, add_viewport_handler, remove_viewport_handler
from .budget import budget_factory
from .BoundBoxCache import BoundBoxCache

allowed_navigation_types = {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'RIGHTMOUSE', 'LEFTMOUSE'}


def build_obj_budget_cost_cache(all_objs: list[bpy.types.Object],
                                context: bpy.types.Context, min_box_size: float) -> tuple[dict, dict]:
    """Returns a tuple of (budget cache, bounding box cache), where the keys are object names.

    :param all_objs: all objects in the scene.
    :param context: Blender context.
    :param min_box_size: minimum allowed bounding box size per object.
    """
    budgeter = budget_factory(context)()
    budget_cache = {obj.name_full: budgeter.budget_cost(context, obj) for obj in all_objs}
    bb_cache_calculator = BoundBoxCache()
    bound_box_cache = {obj.name_full: bb_cache_calculator.bound_box_calc(obj, min_box_size)
                       for obj in all_objs}
    return budget_cache, bound_box_cache


def is_nav_allowed(keyconfigs: bpy.types.KeyConfig, event: bpy.types.Event) -> bool:
    """Returns True if user event is for 3D viewport navigation, False otherwise.

    :param keyconfigs: Blender keymap configuration.
    :param event: user event (pressing a key, moving the mouse, etc.).
    """
    keymaps = ((km.name, km.keymap_items.match_event(event))
               for kc in keyconfigs
               for km in kc.keymaps)
    return any(km is not None and (km.idname.startswith('view3d')
                                   or (km_name == 'Frames' and km.idname.startswith('screen')))
               for km_name, km in keymaps)


class NL_OT_ViewportLive(bpy.types.Operator):
    """Runs a modal in the 3D view. Anything outside the viewport or over the user-specified budget is hidden."""
    bl_idname = 'semagnum_nview_live.viewport'
    bl_label = 'Run nView Live'
    bl_description = 'Automatically hide/show objects in the viewport'
    bl_options = {'REGISTER'}

    playback_mode: bpy.props.BoolProperty(name='Playback Mode',
                                          description='Will constantly refresh viewport based on delay setting,'
                                                      'ideal for previewing animations',
                                          default=False)
    """If True, the operator will update on a scheduled basis determined by the delay setting.
    If False, the operator will only update after the viewport has stopped refreshing.
    
    Playback mode is ideal for previewing animations where the viewport is updating constantly.
    """

    exclude_objs_in_instances: bpy.props.BoolProperty(name='Exclude instanced objects',
                                                      description='Exclude objects in collection instances from '
                                                                  'visibility tests (can make instances seem hidden '
                                                                  'when they are not)',
                                                      default=True)
    """If True, any objects instanced in collections are automatically omitted from evaluation.
    Otherwise, any objects hidden in the instanced collection will be hidden in all instances.
    """

    obj_types: bpy.props.CollectionProperty(type=ObjType)
    """Object types that can be hidden or revealed in the viewport by nView Live."""

    min_box_size: bpy.props.FloatProperty(name='Minimum Bounding Box Size',
                                          description='Minimum bounding box size for objects'
                                                      'without a determinable size'
                                                      '(such as lights or non-instancing empties)',
                                          unit='LENGTH', subtype='DISTANCE',
                                          default=0.1, min=0.001, soft_min=0.1, soft_max=1.0)
    """Minimum bounding box size for objects without a determinable size (e.g. lights)."""

    def draw(self, _context: bpy.types.Context):
        """Draws a UI panel for user to pick settings before running the modal.

        :param _context: Blender context
        """
        layout = self.layout
        layout.prop(self, 'min_box_size')
        layout.prop(self, 'playback_mode')
        layout.prop(self, 'exclude_objs_in_instances')

        layout.label(text='Object types:')
        col = layout.column(align=True)
        for obj_type in self.obj_types.values():
            col.prop(obj_type, 'enabled', text=obj_type.obj_name, toggle=True, icon=obj_type.icon)

    def update_caches(self, context: bpy.types.Context):
        """Updates bounding box and budget caches for objects.

        :param context: Blender context
        """
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
        """Cleanup function before canceling the modal operator."""
        context.window_manager.nl_is_running = False
        context.area.header_text_set(text=None)
        remove_viewport_handler(self._handler)
        return {'CANCELLED'}

    def modal(self, context, event):
        """Code triggered on a regular basis while the modal is running."""
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
        """Code run on initial execution of modal operator."""
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
            header_text = 'nView Live (playback mode) enabled. RMB, ESC: cancel'
        else:
            header_text = 'nView Live enabled. RMB, ESC: cancel'

        context.area.header_text_set(header_text)

        self._handler = add_viewport_handler(self)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        """Opens dialog box for users to choose operator settings."""
        for obj_type, obj_name, icon, enabled in obj_types:
            new_type = self.obj_types.add()
            new_type.obj_type = obj_type
            new_type.obj_name = obj_name
            new_type.icon = icon
            new_type.enabled = enabled
        return context.window_manager.invoke_props_dialog(self)
