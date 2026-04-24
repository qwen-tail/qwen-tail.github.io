import bpy
import math
from mathutils import Vector, Euler

# === БАЗОВЫЕ ПРИМИТИВЫ ===

def add_cube(location=(0, 0, 0), size=1, name="Cube", rotation=(0, 0, 0)):
    """Создаёт куб с заданными параметрами"""
    bpy.ops.mesh.primitive_cube_add(size=size, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def add_sphere(location=(0, 0, 0), radius=1, name="Sphere", segments=32):
    """Создаёт сферу"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location, 
                                         segments=segments, ring_count=segments)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def add_cylinder(location=(0, 0, 0), radius=1, depth=2, name="Cylinder", vertices=32):
    """Создаёт цилиндр (вертикальный по умолчанию)"""
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, 
                                        location=location, vertices=vertices)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def add_cone(location=(0, 0, 0), radius1=1, radius2=0, depth=2, name="Cone", vertices=32):
    """Создаёт конус или усечённый конус"""
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=radius2, 
                                    depth=depth, location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def add_plane(location=(0, 0, 0), size=10, name="Ground"):
    """Создаёт плоскость-основание"""
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

# === БАЗОВЫЕ ПРИМИТИВЫ ===

add_cylinder(location=(0, 7,  0), radius=3, depth=2, name="Cylinder_1", vertices=6)
add_cone(     (0, 15, 0), 3, 2, 4, "Cone_1", vertices=8)
add_sphere(   (0, 25, 0), radius=2, name="Sphere_1", segments=12)

add_plane((0, 0, 0), size=30, "Ground_1")

# add_cube((0, 3, 0), size=1, name="Cube", rotation=(45, 0, 0))
add_cube((0, 0, 0), size=1)
add_cube((3, 3, 0), size=2)
add_cube((7, 3, 0), size=3)
add_cube((15, 5, 0), size=4)

#add_grid_floor()
#enable_shadows()
