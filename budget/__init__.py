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
