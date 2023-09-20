bl_info = {
    "name": "3ds Max-like Grouping",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import bmesh
from mathutils import Vector

def center_of_mass(objects):
    total_mass = 0.0
    total_center = Vector((0.0, 0.0, 0.0))

    for obj in objects:
        volume = obj.dimensions.x * obj.dimensions.y * obj.dimensions.z
        center = obj.location
        total_mass += volume
        total_center += volume * center

    return total_center / total_mass if total_mass != 0 else Vector((0, 0, 0))

def bounding_box(objects):
    if not objects:
        return None, None

    min_corner = Vector((float('inf'), float('inf'), float('inf')))
    max_corner = Vector((float('-inf'), float('-inf'), float('-inf')))

    for obj in objects:
        mesh = obj.data
        mat_world = obj.matrix_world

        for vert in mesh.vertices:
            world_coord = mat_world @ vert.co
            min_corner.x = min(min_corner.x, world_coord.x)
            min_corner.y = min(min_corner.y, world_coord.y)
            min_corner.z = min(min_corner.z, world_coord.z)
            max_corner.x = max(max_corner.x, world_coord.x)
            max_corner.y = max(max_corner.y, world_coord.y)
            max_corner.z = max(max_corner.z, world_coord.z)

    return min_corner, max_corner

class OBJECT_OT_max_group(bpy.types.Operator):
    bl_idname = "object.max_group"
    bl_label = "Max Group"

    def execute(self, context):
        selected_objects = context.selected_objects

        # 1. Create Empty
        bpy.ops.object.empty_add(type='CUBE')
        empty = context.active_object

        # 2. Calculate center of mass
        com = center_of_mass(selected_objects)
        empty.location = com

        # 3. Calculate bounding box dimensions
        min_corner, max_corner = bounding_box(selected_objects)
        if min_corner and max_corner:
            empty.dimensions = max_corner - min_corner

        # 4. Parent all objects to the empty
        for obj in selected_objects:
            obj.parent = empty

        # 5. Create new collection
        new_collection = bpy.data.collections.new("MaxGrouped")
        context.scene.collection.children.link(new_collection)

        # Move the objects and the empty to the new collection
        for obj in selected_objects:
            context.collection.objects.unlink(obj)
            new_collection.objects.link(obj)
        
        # Move the empty as well
        context.collection.objects.unlink(empty)
        new_collection.objects.link(empty)

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
