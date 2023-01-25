import bpy

from .BaseBudget import BaseBudget
from .stat_format_util import format_num


class ObjBudget(BaseBudget):
    """Budget manager by setting an upper limit of objects visible in the scene."""

    def budget_cost(self, _context: bpy.types.Context, _obj: bpy.types.Object) -> int:
        """Calculates and returns the cost of an object to be visible in the scene.

        :param _context: Blender context
        :param _obj: Blender object's cost to be counted
        """
        return 1

    def budget_limit(self, context: bpy.types.Context) -> int:
        """Returns the user-specified upper limit of objects for the scene.

        :param context: Blender context
        """
        return context.window_manager.nl_max_objects

    def draw(self, context: bpy.types.Context, layout: bpy.types.UILayout):
        """Draws object budget parameters in panel.

        :param context: Blender context
        :param layout: bpy.types.UILayout
        """
        layout.prop(context.window_manager, 'nl_max_objects', slider=True)
        layout.label(text='Only show up to {} objects'.format(format_num(context.window_manager.nl_max_objects)))
