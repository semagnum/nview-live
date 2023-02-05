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
