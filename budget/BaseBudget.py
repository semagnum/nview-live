class BaseBudget:

    def is_viable_obj(self, obj) -> bool:
        return True

    def budget_cost(self, context, obj) -> int:
        return 0

    def budget_limit(self, context) -> int:
        return 0

    def draw(self, context, layout):
        # empty base case
        pass