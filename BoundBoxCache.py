from mathutils import Vector

bound_box_base = [(-1.0, -1.0, -1.0), (-1.0, -1.0, 1.0), (-1.0, 1.0, 1.0), (-1.0, 1.0, -1.0),
                  (1.0, -1.0, -1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, -1.0)]


def valid_bound_box(obj):
    return not all([obj.bound_box[0][0] == obj.bound_box[i][j] for i in range(8) for j in range(3)])


class BoundBoxCache:

    def __init__(self):
        self.collection_cache = {}
        self.object_cache = {}

    def bound_box_calc(self, obj, min_box_size):
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
