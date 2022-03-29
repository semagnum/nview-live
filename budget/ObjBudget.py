from .BaseBudget import BaseBudget
from .stat_format_util import format_num

class ObjBudget(BaseBudget):

    def budget_cost(self, context, obj) -> int:
        return 1

    def budget_limit(self, context) -> int:
        return context.window_manager.nl_max_objects

    def draw(self, context, layout):
        layout.prop(context.window_manager, 'nl_max_objects', slider=True)
        layout.label(text='Only show up to {} objects'.format(format_num(context.window_manager.nl_max_objects)))
