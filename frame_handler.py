import bpy
import time
import bpy_extras
from .budget import budget_factory


def vert_count(obj, collection_tri_count_cache: dict):
    if obj.type == 'MESH':
        return len(obj.data.vertices)
    elif obj.type == 'EMPTY' and obj.is_instancer and obj.instance_type == 'COLLECTION':
        col_name = obj.instance_collection.name
        if col_name in collection_tri_count_cache:
            return collection_tri_count_cache[col_name]
        return sum(vert_count(o, collection_tri_count_cache) for o in obj.instance_collection.all_objects)
    return 0


def close_to_camera(camera_location, locs, max_dist):
    return any((loc - camera_location).length < max_dist for loc in locs)


def dist_to_camera(camera_location, locs: list):
    return min((loc - camera_location).length for loc in locs)


def is_visible_to_camera(context, location_coords):
    region_3d = context.space_data.region_3d
    region = context.region
    region_relative_locs = [bpy_extras.view3d_utils.location_3d_to_region_2d(region, region_3d, location_coord)
                            for location_coord in location_coords]

    region_xs = [loc[0]
                 for loc in region_relative_locs
                 if loc is not None]
    region_ys = [loc[1]
                 for loc in region_relative_locs
                 if loc is not None]

    # empty lists, ie all are invisible or behind camera
    if len(region_xs) == 0 or len(region_ys) == 0:
        return False

    if all(x < 0 for x in region_xs) or all(y < 0 for y in region_ys):
        return False
    if all(x > region.width for x in region_xs) or all(y > region.height for y in region_ys):
        return False
    return True


def filter_viable_objs(context, viewport_location, max_distance, viable_objs: set, bb_cache: dict):
    for o in viable_objs:
        bb_locs = bb_cache.get(o.name_full)
        if close_to_camera(viewport_location, bb_locs, max_distance) and is_visible_to_camera(context, bb_locs):
            yield o
        elif not o.hide_get():
            try:
                o.hide_set(True)
            except Exception as e:
                print('Could not hide {}: {}'.format(o.name, e))


def parse_optimal_objs(context, viable_objects, budget_cache: dict):
    my_budget = budget_factory(context)().budget_limit(context)
    curr_count = 0
    for idx, o in enumerate(viable_objects):
        o_cost = budget_cache.get(o.name_full, 0)
        above_budget = (curr_count + o_cost) > my_budget
        if above_budget:
            return idx

        if o.hide_get():
            try:
                o.hide_set(False)
            except Exception as e:
                print('Could not unhide {}: {}'.format(o.name, e))
        curr_count += o_cost
    return len(viable_objects)


def viewport_handler(context, viable_objs, budget_cache: dict, bb_cache: dict):
    wm = context.window_manager

    viewport_location = context.region_data.view_matrix.to_translation()

    max_distance = wm.nl_max_distance

    filtered_objs = list(filter_viable_objs(context, viewport_location, max_distance, viable_objs, bb_cache))
    if wm.nl_use_budget:
        if wm.nl_budget_option != 'objects':
            budget_sort_reverse = -1 if wm.nl_budget_sort_order == 'ascending' else 1
            filtered_objs.sort(key=lambda obj: (
                budget_sort_reverse * budget_cache.get(obj.name_full, 0),
                dist_to_camera(viewport_location, bb_cache.get(obj.name_full, []))
            ))
        else:
            filtered_objs.sort(key=lambda obj: dist_to_camera(viewport_location, bb_cache.get(obj.name_full, []) + [obj.matrix_world.to_translation()]))

    split_index = parse_optimal_objs(context, filtered_objs, budget_cache)

    objs_to_reveal = (o for o in filtered_objs[:split_index] if o.hide_get())

    for o in objs_to_reveal:
        try:
            o.hide_set(False)
        except Exception as e:
            print('Could not unhide {}: {}'.format(o.name, e))

    if split_index >= len(filtered_objs):
        return

    objs_to_hide = (o for o in filtered_objs[split_index:] if not o.hide_get())

    for o in objs_to_hide:
        try:
            o.hide_set(True)
        except Exception as e:
            print('Could not hide {}: {}'.format(o.name, e))


def viewport_draw_handler(self):
    self.last_call = time.time()
    self.has_updated = False


def add_viewport_handler(self):
    return bpy.types.SpaceView3D.draw_handler_add(viewport_draw_handler, (self,), 'WINDOW', 'POST_PIXEL')


def remove_viewport_handler(handler):
    bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
