import bpy


class ObjType(bpy.types.PropertyGroup):
    """Property group containing Blender object types."""
    obj_type: bpy.props.StringProperty(name='Type', default='')
    """Blender object type"""
    obj_name: bpy.props.StringProperty(name='Name', default='')
    icon: bpy.props.StringProperty(name='Icon', default='')
    enabled: bpy.props.BoolProperty(name='Visible', default=False, options=set())