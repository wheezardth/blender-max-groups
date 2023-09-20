bl_info = {
    "name": "3ds Max-like Grouping",
    "blender": (3, 6, 0),
    "category": "Object",
}

import bpy
from mathutils import Vector

def bounding_box(objects):
    if not objects:
        return None, None

    min_corner = Vector((float('inf'), float('inf'), float('inf')))
    max_corner = Vector((float('-inf'), float('-inf'), float('-inf')))

    for obj in objects:
        bb_world = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        for coord in bb_world:
            min_corner.x = min(min_corner.x, coord.x)
            min_corner.y = min(min_corner.y, coord.y)
            min_corner.z = min(min_corner.z, coord.z)
            max_corner.x = max(max_corner.x, coord.x)
            max_corner.y = max(max_corner.y, coord.y)
            max_corner.z = max(max_corner.z, coord.z)

    return min_corner, max_corner

class OBJECT_OT_max_group(bpy.types.Operator):
    bl_idname = "object.max_group"
    bl_label = "Max Group"

    def execute(self, context):
        selected_objects = context.selected_objects

        # Calculate bounding box dimensions
        min_corner, max_corner = bounding_box(selected_objects)
        if not min_corner or not max_corner:
            return {'CANCELLED'}

        # Enlarge the bounding box dimensions by 2%
        scale_factor = 1.02
        size_adjust = (max_corner - min_corner) * (scale_factor - 1) / 2
        min_corner -= size_adjust
        max_corner += size_adjust

        # Calculate the center for the cube
        cube_center = (min_corner + max_corner) / 2

        # Calculate the dimensions for the cube
        cube_dimensions = max_corner - min_corner

        # Add a cube to act as the "empty"
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=cube_center)
        cube = context.active_object

        # Set the scale to match the calculated dimensions
        cube.scale = cube_dimensions  # Cube has a default size of 2 units in all dimensions
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Set display mode to WIRE for the bounding box cube
        cube.display_type = 'WIRE'

        # Parent all objects to the cube
        for obj in selected_objects:
            obj.select_set(True)
            cube.select_set(True)
            bpy.context.view_layer.objects.active = cube
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        return {'FINISHED'}

class OBJECT_PT_max_group_panel(bpy.types.Panel):
    bl_label = "3ds Max-like Grouping"
    bl_idname = "OBJECT_PT_max_group"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.max_group")

def register():
    bpy.utils.register_class(OBJECT_OT_max_group)
    bpy.utils.register_class(OBJECT_PT_max_group_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_max_group)
    bpy.utils.unregister_class(OBJECT_PT_max_group_panel)

if __name__ == "__main__":
    register()
