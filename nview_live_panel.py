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

from .handler_operators import NL_OT_ViewportLive
from .budget import budget_factory


class NL_PT_NViewLive(bpy.types.Panel):
    """nView Live panel, located in the 3D View."""
    bl_space_type = 'VIEW_3D'
    bl_label = 'nView Live'
    bl_category = 'nView'
    bl_region_type = 'UI'
    bl_idname = 'NL_PT_nview_live'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        window_manager = context.window_manager

        layout.operator(NL_OT_ViewportLive.bl_idname)

        layout.separator()
        layout.prop(window_manager, 'nl_run_delay')
        layout.prop(window_manager, 'nl_max_distance')
        layout.operator('object.hide_view_clear', icon='HIDE_OFF')


class NL_PT_Budgeting(bpy.types.Panel):
    """nView Live subpanel for budget managing."""
    bl_space_type = 'VIEW_3D'
    bl_label = 'Budgeting'
    bl_category = 'nView'
    bl_region_type = 'UI'
    bl_idname = 'NL_PT_budgeting'
    bl_parent_id = 'NL_PT_nview_live'
    bl_context = 'objectmode'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        layout = self.layout
        window_manager = context.window_manager
        layout.enabled = not window_manager.nl_is_running
        layout.prop(window_manager, 'nl_use_budget', text='')

    def draw(self, context):
        layout = self.layout
        window_manager = context.window_manager
        row = layout.row()
        row.prop(window_manager, 'nl_budget_option')
        row.enabled = not window_manager.nl_is_running

        box = layout.box()
        budget_option = budget_factory(context, is_layout=True)()
        budget_option.draw(context, box)
