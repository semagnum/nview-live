from .BaseBudget import BaseBudget
from .stat_format_util import format_num


class VertBudget(BaseBudget):

    def __init__(self):
        self.collection_cache = {}

    def get_vert_count(self, obj):
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

    def budget_limit(self, context) -> int:
        return context.window_manager.nl_vert_budget

    def budget_cost(self, context, obj) -> int:
        return self.get_vert_count(obj)

    def draw(self, context, layout):
        layout.prop(context.window_manager, 'nl_vert_budget', slider=True)
        layout.label(text='Only show up to {} vertices'.format(format_num(context.window_manager.nl_vert_budget)))