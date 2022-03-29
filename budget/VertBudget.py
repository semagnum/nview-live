from .BaseBudget import BaseBudget
from .stat_format_util import format_num


class VertBudget(BaseBudget):

    def budget_limit(self, context) -> int:
        return context.window_manager.nl_vert_budget

    def budget_cost(self, context, obj) -> int:
        return len(obj.data.vertices) if obj.type == 'MESH' else 0

    def draw(self, context, layout):
        layout.prop(context.window_manager, 'nl_vert_budget', slider=True)
        layout.label(text='Only show up to {} vertices'.format(format_num(context.window_manager.nl_vert_budget)))