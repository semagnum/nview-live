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
from typing import Iterator


def find_coll_instancers(curr_coll: bpy.types.Collection) -> set[bpy.types.Collection]:
    """Returns all objects that instance collections

    :param curr_coll: current collection
    """
    return {obj for obj in curr_coll.all_objects if obj.is_instancer and obj.instance_type == 'COLLECTION'}


def find_instanced_colls(curr_coll: bpy.types.Collection) -> set[bpy.types.Collection]:
    """Returns an iterator of collections that are instanced by objects.

    :param curr_coll: current collection
    """
    return {o.instance_collection for o in find_coll_instancers(curr_coll)}


# example: find_instanced_colls(context.view_layer.layer_collection)
def find_instanced_objs_in_colls(curr_coll: bpy.types.Collection) -> Iterator[bpy.types.Object]:
    """Returns an iterator of objects in collections instanced by objects.

    Example: ``find_instanced_colls(context.view_layer.layer_collection)``

    :param curr_coll: current collection
    """
    objs_dict = {}
    for coll in find_instanced_colls(curr_coll):
        for obj in coll.all_objects:
            if obj not in objs_dict:
                objs_dict[obj] = True
                yield obj
