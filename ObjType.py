import bpy


class ObjType(bpy.types.PropertyGroup):
    obj_type: bpy.props.StringProperty(name='Type', default='')
    obj_name: bpy.props.StringProperty(name='Name', default='')
    icon: bpy.props.StringProperty(name='Icon', default='')
    enabled: bpy.props.BoolProperty(name='Visible', default=False, options=set())