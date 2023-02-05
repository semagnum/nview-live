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


class VertBudget(BaseBudget):
    """Budget manager by setting an upper limit of vertices visible in the scene."""

    def __init__(self):
        self.collection_cache = {}

    def get_vert_count(self, obj: bpy.types.Object):
        """Retrieves triangle count for any given object.

        For instanced collections, it will recursively sum up all child mesh object triangle counts.
        Uses caching in case the same collection is referenced multiple times.

        :param obj: object to retrieve triangle data from
        """
        if obj.type == 'MESH':
            return len(obj.data.vertices)
        elif obj.type == 'EMPTY' and obj.is_instancer and obj.instance_type == 'COLLECTION':
            col_name = obj.instance_collection.name
            if col_name in self.collection_cache:
                return self.collection_cache[col_name]
            instance_cost = sum(self.get_vert_count(o) for o in obj.instance_collection.all_objects)
            self.collection_cache[col_name] = instance_cost
            return instance_cost
        return 0

    def budget_limit(self, context: bpy.types.Context) -> int:
        """Returns the user-specified upper limit of vertices for the scene.

        :param context: Blender context
        """
        return context.window_manager.nl_vert_budget

    def budget_cost(self, context: bpy.types.Context, obj: bpy.types.Object) -> int:
        """Calculates and returns the cost of an object to be visible in the scene.

        :param context: Blender context
        :param obj: Blender object's cost to be counted
        """
        return self.get_vert_count(obj)

    def draw(self, context: bpy.types.Context, layout: bpy.types.UILayout):
        """Draws object budget parameters in panel.

        :param context: Blender context
        :param layout: bpy.types.UILayout
        """
        wm = context.window_manager
        row = layout.row()
        row.prop(wm, 'nl_vert_budget', slider=True)
        row.prop(wm, 'nl_budget_sort_order', expand=True, icon_only=True)
        layout.label(text='Only show up to {} vertices'.format(format_num(wm.nl_vert_budget)))
