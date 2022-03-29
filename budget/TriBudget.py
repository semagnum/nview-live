from .BaseBudget import BaseBudget
import bmesh

from .stat_format_util import format_num


def get_tri_count(obj, depsgraph, collection_tri_count_cache: dict):
    if obj.type == 'MESH':
        return get_bmesh_data(obj, depsgraph)
    elif obj.type == 'EMPTY' and obj.is_instancer and obj.instance_type == 'COLLECTION':
        col_name = obj.instance_collection.name
        if col_name in collection_tri_count_cache:
            return collection_tri_count_cache[col_name]
        return sum(get_tri_count(o, depsgraph, collection_tri_count_cache) for o in obj.instance_collection.all_objects)
    return 0


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

    def budget_limit(self, context) -> int:
        return context.window_manager.nl_tri_budget

    def budget_cost(self, context, obj) -> int:
        return get_tri_count(obj, context.evaluated_depsgraph_get(), {}) if obj.type == 'MESH' else 0

    def draw(self, context, layout):
        layout.prop(context.window_manager, 'nl_tri_budget', slider=True)
        layout.label(text='Only show up to {} triangles'.format(format_num(context.window_manager.nl_tri_budget)))
