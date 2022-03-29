def coll_iter(curr_coll):
    """
    Iterate through hierarchy of collections
    :param curr_coll: current collection
    :return: generator of collections
    """
    yield curr_coll
    for child in curr_coll.children:
        yield from coll_iter(child)


def has_coll_instancers(curr_coll):
    """
    Find all objects that instance collections
    :param curr_coll: current collection
    :return: generator of objects that instance collections
    """
    return any(obj for obj in curr_coll.all_objects if obj.is_instancer and obj.instance_type == 'COLLECTION')


def find_coll_instancers(curr_coll):
    """
    Find all objects that instance collections
    :param curr_coll: current collection
    :return: generator of objects that instance collections
    """
    return {obj for obj in curr_coll.all_objects if obj.is_instancer and obj.instance_type == 'COLLECTION'}


def find_instanced_colls(curr_coll):
    """
    Iterate over collections instanced by objects
    :param curr_coll: current collection
    :return: generator of collections that are instanced by objects
    """
    return {o.instance_collection for o in find_coll_instancers(curr_coll)}


# example: find_instanced_colls(context.view_layer.layer_collection)
def find_instanced_objs_in_colls(curr_coll):
    """
    Iterate over objects that are in collections instanced by objects
    :param curr_coll: current collection
    :return: generator of objects in collections instanced by objects
    """
    objs_dict = {}
    for coll in find_instanced_colls(curr_coll):
        for obj in coll.all_objects:
            if obj not in objs_dict:
                objs_dict[obj] = True
                yield obj
