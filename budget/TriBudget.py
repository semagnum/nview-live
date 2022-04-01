from .BaseBudget import BaseBudget
import bmesh

from .stat_format_util import format_num


def get_bmesh_data(obj, depsgraph):
    """
    Gets bmesh stats for object
    :param obj: bpy.types.Object
    :param depsgraph: current scene depsgraph
    :return: faces, tris, verts
    """
    blender_mesh = obj.evaluated_get(depsgraph).to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)

    bm = bmesh.new()
    bm.from_mesh(blender_mesh)
    bm.faces.ensure_lookup_table()

    tris_count = len(bm.calc_loop_triangles())

    bm.free()

    return tris_count


class TriBudget(BaseBudget):

    def __init__(self):
        self.collection_cache = {}

    def get_tri_count(self, obj, depsgraph):
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

    def budget_limit(self, context) -> int:
        return context.window_manager.nl_tri_budget

    def budget_cost(self, context, obj) -> int:
        return self.get_tri_count(obj, context.evaluated_depsgraph_get())

    def draw(self, context, layout):
        wm = context.window_manager
        row = layout.row()
        row.prop(wm, 'nl_tri_budget', slider=True)
        row.prop(wm, 'nl_budget_sort_order', expand=True, icon_only=True)
        layout.label(text='Only show up to {} triangles'.format(format_num(wm.nl_tri_budget)))

