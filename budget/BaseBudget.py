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


class BaseBudget:
    """Abstract class for budget managers."""

    def budget_cost(self, _context: bpy.types.Context, _obj: bpy.types.Object) -> int:
        """Calculates and returns the cost of an object to be visible in the scene.

        :param _context: Blender context
        :param _obj: Blender object's cost to be counted
        """
        return 0

    def budget_limit(self, _context: bpy.types.Context) -> int:
        """Returns the user-specified budget (e.g. 300 objects).

        :param _context: Blender context
        """
        return 0

    def draw(self, _context: bpy.types.Context, layout: bpy.types.UILayout):
        """Draws budget parameters in panel.

        :param _context: Blender context
        :param layout: bpy.types.UILayout
        """
        # empty base case
        layout.label(text="Show all visible objects")
