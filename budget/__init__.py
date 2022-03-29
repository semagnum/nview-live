from .BaseBudget import BaseBudget
from .ObjBudget import ObjBudget
from .TriBudget import TriBudget
from .VertBudget import VertBudget

def budget_factory(context):
    wm = context.window_manager
    curr_option = wm.nl_budget_option

    if curr_option == 'objects':
        return ObjBudget
    elif curr_option == 'verts':
        return VertBudget
    elif curr_option == 'tris':
        return TriBudget
    elif curr_option == 'none':
        return BaseBudget
    raise ValueError('Unknown budget option: {}'.format(curr_option))