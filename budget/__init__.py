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


from typing import Type

import bpy

from . import BaseBudget, ObjBudget, VertBudget, TriBudget
from .BaseBudget import BaseBudget
from .ObjBudget import ObjBudget
from .TriBudget import TriBudget
from .VertBudget import VertBudget


def budget_factory(context: bpy.types.Context, is_layout: bool = False) -> Type[BaseBudget]:
    """Factory pattern for choosing budget manager based on context parameters

    :param context: Blender context
    :param is_layout: whether the chosen budget for drawing in the UI layout, or for calculations
    """
    wm = context.window_manager
    curr_option = wm.nl_budget_option

    if not wm.nl_use_budget and not is_layout:
        return BaseBudget

    if curr_option == 'objects':
        return ObjBudget
    elif curr_option == 'verts':
        return VertBudget
    elif curr_option == 'tris':
        return TriBudget

    raise ValueError('Unknown budget option: {}'.format(curr_option))
