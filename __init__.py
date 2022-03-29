import bpy

from .ObjType import ObjType
from .handler_operators import NL_OT_ViewportLive
from .nview_live_panel import NL_PT_NViewLive, NL_PT_Budgeting

bl_info = {
    "name": 'nView Live Blender Addon',
    "author": 'Spencer Magnusson',
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "description": 'Gives live updates of visibility of mesh objects',
    "location": 'View 3D > Tools',
    "support": 'COMMUNITY',
    "category": '3D View'
}

classes = [ObjType, NL_OT_ViewportLive, NL_PT_NViewLive, NL_PT_Budgeting]
properties = [
    ('nl_max_distance', bpy.props.FloatProperty(name='Max Distance',
                                                description='Maximum distance of objects allowed to be visible',
                                                default=100.0,
                                                min=0.0, soft_min=0.0, soft_max=1000.0, step=100)),
    ('nl_tri_budget', bpy.props.IntProperty(name='Max Tris',
                                            description='Maximum allowed number of triangles to show in viewport',
                                            default=300000, min=1, soft_min=1000, soft_max=10000000)),
    ('nl_vert_budget', bpy.props.IntProperty(name='Max Vertices',
                                             description='Maximum allowed number of vertices to show in viewport',
                                             default=1000000, min=1, soft_min=1000, soft_max=10000000)),
    ('nl_budget_option', bpy.props.EnumProperty(name='Budget Option',
                                                description='Option to use when budget is exceeded',
                                                items=[('none', 'None', 'Just do distance culling, no budgeting'),
                                                       ('objects', 'Objects', 'Budget visible objects'),
                                                       ('verts', 'Vertices', 'Budget visible vertices (meshes only)'),
                                                       ('tris', 'Triangles', 'Budget triangles (meshes only), slowest'),
                                                       ],
                                                default='verts')),
    ('nl_max_objects', bpy.props.IntProperty(name='Max objects',
                                             description='Max number of viable objects to show at a time',
                                             default=100, min=1, soft_min=10, soft_max=10000)),
    ('nl_exclude_instanced_objects', bpy.props.BoolProperty(name='Exclude instanced objects',
                                                            description='Exclude objects that are instanced',
                                                            default=True)),
    ('nl_is_running', bpy.props.BoolProperty(options={'HIDDEN'}, default=False))
]


def register():
    window_manager = bpy.types.WindowManager

    for cls in classes:
        bpy.utils.register_class(cls)

    for name, prop in properties:
        setattr(window_manager, name, prop)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    window_manager = bpy.types.WindowManager
    for name, prop in properties[::-1]:
        try:
            delattr(window_manager, name)
        except AttributeError:
            pass


if __name__ == '__main__':
    register()