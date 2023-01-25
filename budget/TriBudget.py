from .BaseBudget import BaseBudget
import bpy
import bmesh

from .stat_format_util import format_num


def get_bmesh_data(obj: bpy.types.Object, depsgraph: bpy.types.Depsgraph) -> int:
    """Gets bmesh statistics for a given mesh object.

    Currently only returns the evaluated triangle count, but evaluated face and vertex counts could also be retrieved.

    These calculations can be `very` costly, so it's best to use unevaluated data for quicker access.

    :param obj: object to retrieve triangle data from
    :param depsgraph: current scene's dependency graph
    """
    blender_mesh = obj.evaluated_get(depsgraph).to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)

    bm = bmesh.new()
    bm.from_mesh(blender_mesh)
    bm.faces.ensure_lookup_table()

    tris_count = len(bm.calc_loop_triangles())

    bm.free()

    return tris_count


class TriBudget(BaseBudget):
    """Budget manager by setting an upper limit of evaluated triangles visible in the scene."""

    def __init__(self):
        self.collection_cache = {}

    def get_tri_count(self, obj: bpy.types.Object, depsgraph: bpy.types.Depsgraph) -> int:
        """Retrieves triangle count for any given object.

        Uses ``get_bmesh_data`` for mesh objects.
        For instanced collections, it will recursively sum up all child mesh object triangle counts.
        Uses caching in case the same collection is referenced multiple times.

        :param obj: object to retrieve triangle data from
        :param depsgraph: current scene's dependency graph
        """
        if obj.type == 'MESH':
            return get_bmesh_data(obj, depsgraph)
        elif obj.type == 'EMPTY' and obj.is_instancer and obj.instance_type == 'COLLECTION':
            col_name = obj.instance_collection.name
            if col_name in self.collection_cache:
                return self.collection_cache[col_name]
            instance_cost = sum(self.get_tri_count(o, depsgraph) for o in obj.instance_collection.all_objects)
            self.collection_cache[col_name] = instance_cost
            return instance_cost
        return 0

    def budget_limit(self, context: bpy.types.Context) -> int:
        """Returns the user-specified upper limit of objects for the scene.

        :param context: Blender context
        """
        return context.window_manager.nl_tri_budget

    def budget_cost(self, context: bpy.types.Context, obj: bpy.types.Object) -> int:
        """Calculates and returns the cost of an object to be visible in the scene.

        :param context: Blender context
        :param obj: Blender object's cost to be counted
        """
        return self.get_tri_count(obj, context.evaluated_depsgraph_get())

    def draw(self, context: bpy.types.Context, layout: bpy.types.UILayout):
        """Draws object budget parameters in panel.

        :param context: Blender context
        :param layout: bpy.types.UILayout
        """
        wm = context.window_manager
        row = layout.row()
        row.prop(wm, 'nl_tri_budget', slider=True)
        row.prop(wm, 'nl_budget_sort_order', expand=True, icon_only=True)
        layout.label(text='Only show up to {} triangles'.format(format_num(wm.nl_tri_budget)))

