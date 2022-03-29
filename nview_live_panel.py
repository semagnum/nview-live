import bpy

from .handler_operators import NL_OT_ViewportLive
from .budget import budget_factory


class NL_PT_NViewLive(bpy.types.Panel):
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
        layout.prop(window_manager, 'nl_max_distance', slider=True)
        layout.prop(window_manager, 'nl_exclude_instanced_objects')
        layout.operator('object.hide_view_clear', icon='HIDE_OFF')


class NL_PT_Budgeting(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_label = 'Budgeting'
    bl_category = 'nView'
    bl_region_type = 'UI'
    bl_idname = 'NL_PT_budgeting'
    bl_parent_id = 'NL_PT_nview_live'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        window_manager = context.window_manager
        row = layout.row()
        row.prop(window_manager, 'nl_budget_option')
        row.enabled = not window_manager.nl_is_running

        box = layout.box()
        budget_option = budget_factory(context)()
        budget_option.draw(context, box)
