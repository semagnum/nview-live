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


class ObjType(bpy.types.PropertyGroup):
    """Property group containing Blender object types."""
    obj_type: bpy.props.StringProperty(name='Type', default='')
    """Blender object type"""
    obj_name: bpy.props.StringProperty(name='Name', default='')
    icon: bpy.props.StringProperty(name='Icon', default='')
    enabled: bpy.props.BoolProperty(name='Visible', default=False, options=set())