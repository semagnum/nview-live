# Copyright (C) 2023 Spencer Magnusson
# semagnum@gmail.com
# Created by Spencer Magnusson
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


import bpy
from mathutils import Vector

bound_box_base = [(-1.0, -1.0, -1.0), (-1.0, -1.0, 1.0), (-1.0, 1.0, 1.0), (-1.0, 1.0, -1.0),
                  (1.0, -1.0, -1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, -1.0)]


def valid_bound_box(obj: bpy.types.Object) -> bool:
    """Returns if object has a valid bounding box.

    For objects that do not take up space (e.g. light), it may set all the box corners to be a single point.
    In these cases, they are invalid and we need to calculate the box or set a default ourselves.
    
    :param obj: object to be checked
    """
    return not all([obj.bound_box[0][0] == obj.bound_box[i][j] for i in range(8) for j in range(3)])


class BoundBoxCache:
    """Blender object wrapper to hold cache of bounding boxes."""

    def __init__(self):
        self.collection_cache = {}
        self.object_cache = {}

    def bound_box_calc(self, obj: bpy.types.Object, min_box_size: float) -> list[Vector]:
        """Returns - as a list of corners - an object's existing bounding box,
        otherwise calculates one based on object type.

        If the object is instancing a collection,
        the function recursively calculates an enclosing box around all the instance's objects.

        :param obj:
        :param min_box_size:
        """
        if obj.name_full in self.object_cache:
            return self.object_cache[obj.name_full]

        # coalesce bound box based on collection
        # cannot cache with matrix_world, so that will need to be calculated each time
        if obj.is_instancer and obj.instance_type == 'COLLECTION':
            coll_name = obj.instance_collection.name
            if coll_name in self.collection_cache:
                coalesced_bb = self.collection_cache[obj.instance_collection.name]
                return [obj.matrix_world @ v for v in coalesced_bb]
            coll_instance_offset = Vector(obj.instance_collection.instance_offset)
            coll_instance_offset.negate()
            bound_boxes = [
                              [v + coll_instance_offset for v in
                               self.bound_box_calc(coll_obj, min_box_size)]
                              for coll_obj
                              in obj.instance_collection.all_objects] + [obj.bound_box]
            x1, x2 = min((x for b in bound_boxes for x, _, _ in b)), max((x for b in bound_boxes for x, _, _ in b))
            y1, y2 = min((y for b in bound_boxes for _, y, _ in b)), max((y for b in bound_boxes for _, y, _ in b))
            z1, z2 = min((z for b in bound_boxes for _, _, z in b)), max((z for b in bound_boxes for _, _, z in b))
            coalesced_bb = [Vector((x1, y1, z1)), Vector((x1, y1, z2)), Vector((x1, y2, z2)), Vector((x1, y2, z1)),
                            Vector((x2, y1, z1)), Vector((x2, y1, z2)), Vector((x2, y2, z2)), Vector((x2, y2, z1))]
            self.collection_cache[coll_name] = coalesced_bb
            obj_box = [obj.matrix_world @ v for v in coalesced_bb]
            self.object_cache[obj.name_full] = obj_box
            return obj_box

        if valid_bound_box(obj):
            obj_box = [obj.matrix_world @ Vector((v[0], v[1], v[2])) for v in obj.bound_box]
        else:
            obj_box = [obj.matrix_world @ Vector((x * min_box_size, y * min_box_size, z * min_box_size))
                       for x, y, z in bound_box_base]
        self.object_cache[obj.name_full] = obj_box
        return obj_box
