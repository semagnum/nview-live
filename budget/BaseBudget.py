class BaseBudget:

    def budget_cost(self, context, obj) -> int:
        return 0

    def budget_limit(self, context) -> int:
        return 0

    def draw(self, context, layout):
        # empty base case
        layout.label(text="Show all visible objects")
