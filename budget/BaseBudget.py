import bpy


class BaseBudget:
    """Abstract class for budget managers."""

    def budget_cost(self, _context: bpy.types.Context, _obj: bpy.types.Object) -> int:
        """Calculates and returns the cost of an object to be visible in the scene.

        :param _context: Blender context
        :param _obj: Blender object's cost to be counted
        """
        return 0

    def budget_limit(self, _context: bpy.types.Context) -> int:
        """Returns the user-specified budget (e.g. 300 objects).

        :param _context: Blender context
        """
        return 0

    def draw(self, _context: bpy.types.Context, layout: bpy.types.UILayout):
        """Draws budget parameters in panel.

        :param _context: Blender context
        :param layout: bpy.types.UILayout
        """
        # empty base case
        layout.label(text="Show all visible objects")
