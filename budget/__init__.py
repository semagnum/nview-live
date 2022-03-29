from .BaseBudget import BaseBudget
from .ObjBudget import ObjBudget
from .TriBudget import TriBudget
from .VertBudget import VertBudget

def budget_factory(context, is_layout=False):
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