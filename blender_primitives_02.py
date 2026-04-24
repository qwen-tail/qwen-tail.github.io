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

# === НАПРАВЛЯЮЩИЕ ПЕРСПЕКТИВЫ ===

def add_vanishing_point(location=(0, 50, 1.6), name="VP", color=(1, 0, 0)):
    """Создаёт маркер точки схода (красная сфера)"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=location, segments=16)
    vp = bpy.context.active_object
    vp.name = name
    # Материал для видимости
    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.diffuse_color = (*color, 1)
    mat.specular_intensity = 0
    if vp.data.materials:
        vp.data.materials[0] = mat
    else:
        vp.data.materials.append(mat)
    return vp

def add_horizon_line(y_pos=50, z_height=1.6, length=100, name="Horizon"):
    """Горизонтальная линия на уровне глаз"""
    bpy.ops.mesh.primitive_curve_bezier_add(location=(0, y_pos, z_height))
    curve = bpy.context.active_object
    curve.name = name
    # Выпрямляем кривую в линию
    spline = curve.data.splines[0]
    spline.points[0].co = (-length/2, 0, 0, 1)
    spline.points[1].co = (length/2, 0, 0, 1)
    # Материал линии
    mat = bpy.data.materials.new(name="GuideLine_Mat")
    mat.diffuse_color = (0, 1, 1, 1)  # Циан
    curve.data.materials.append(mat)
    return curve

def add_projection_line(start, end, name="ProjLine", dashed=False):
    """Линия проекции от объекта к точке схода"""
    bpy.ops.mesh.primitive_curve_bezier_add(location=start)
    curve = bpy.context.active_object
    curve.name = name
    spline = curve.data.splines[0]
    spline.points[0].co = (0, 0, 0, 1)
    spline.points[1].co = (Vector(end) - Vector(start)).to_4d()
    # Стиль
    mat = bpy.data.materials.new(name="ProjLine_Mat")
    mat.diffuse_color = (0.5, 0.5, 0.5, 0.7)  # Полупрозрачный серый
    curve.data.materials.append(mat)
    if dashed:
        curve.data.bevel_depth = 0.02  # Тонкая линия
    return curve

def add_grid_floor(size=20, subdivisions=10, location=(0, 0, 0), name="PerspectiveGrid"):
    """Сетка пола для отсчёта перспективы"""
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=subdivisions, 
                                    y_subdivisions=subdivisions,
                                    size=size, location=location)
    grid = bpy.context.active_object
    grid.name = name
    # Wireframe-материал
    mat = bpy.data.materials.new(name="Grid_Mat")
    mat.blend_method = 'BLEND'
    mat.show_wireframe = True
    mat.diffuse_color = (0.3, 0.3, 0.3, 0.3)
    grid.data.materials.append(mat)
    return grid

# === ОСВЕЩЕНИЕ И ТЕНИ ===

def setup_study_lighting(key_pos=(10, -10, 15), fill_pos=(-10, -10, 5), rim_pos=(0, 10, 10)):
    """Трёхточечное освещение для чётких теней"""
    # Key light (основной)
    bpy.ops.object.light_add(type='SUN', location=key_pos)
    key = bpy.context.active_object
    key.name = "KeyLight"
    key.data.energy = 3.0
    key.rotation_euler = Euler((math.radians(45), math.radians(-30), math.radians(45)), 'XYZ')
    
    # Fill light (заполняющий)
    bpy.ops.object.light_add(type='SUN', location=fill_pos)
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 1.0
    fill.data.color = (0.8, 0.9, 1.0)  # Холодный оттенок
    
    # Rim light (контровой)
    bpy.ops.object.light_add(type='SUN', location=rim_pos)
    rim = bpy.context.active_object
    rim.name = "RimLight"
    rim.data.energy = 2.0
    rim.data.color = (1.0, 0.9, 0.7)  # Тёплый оттенок
    
    return key, fill, rim

def enable_shadows(render_engine='CYCLES'):
    """Включает тени и настраивает рендер"""
    scene = bpy.context.scene
    scene.render.engine = render_engine
    
    if render_engine == 'CYCLES':
        scene.cycles.samples = 128
        scene.cycles.use_denoising = True
    else:  # EEVEE
        scene.eevee.use_shadows = True
        scene.eevee.use_soft_shadows = True
        scene.eevee.shadow_cube_size = '2048'
    
    # Включаем тени для всех источников
    for light in bpy.data.objects:
        if light.type == 'LIGHT':
            light.data.use_shadow = True
    
    return scene

# === КАМЕРА И ЭКСПОРТ ===

def setup_camera_for_perspective(target=(0, 0, 0), distance=30, height=5, name="StudyCam"):
    """Камера с видом в перспективе, направленная на центр"""
    bpy.ops.object.camera_add(location=(0, -distance, height))
    cam = bpy.context.active_object
    cam.name = name
    cam.rotation_euler = Euler((math.radians(75), 0, 0), 'XYZ')  # Наклон вниз
    cam.data.lens = 35  # Умеренный широкоугольник для перспективы
    bpy.context.scene.camera = cam
    return cam

def setup_orthographic_camera(size=20, axis='FRONT', name="OrthoCam"):
    """Ортографическая камера для чертежей (вид спереди/сбоку/сверху)"""
    bpy.ops.object.camera_add(location=(0, -30, 10))
    cam = bpy.context.active_object
    cam.name = name
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = size
    if axis == 'TOP':
        cam.location = (0, 0, 30)
        cam.rotation_euler = Euler((0, 0, 0), 'XYZ')
    elif axis == 'SIDE':
        cam.location = (30, 0, 10)
        cam.rotation_euler = Euler((math.radians(90), 0, math.radians(90)), 'XYZ')
    else:  # FRONT
        cam.location = (0, -30, 10)
        cam.rotation_euler = Euler((math.radians(90), 0, 0), 'XYZ')
    bpy.context.scene.camera = cam
    return cam

def configure_render_for_print(resolution=(2480, 3508), dpi=300, format='PNG'):
    """Настройки рендера для печати на A4 (300 DPI)"""
    scene = bpy.context.scene
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = format
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.compression = 15
    scene.render.film_transparent = False  # Белый фон для печати
    # Белый фон
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    return scene

def render_and_save(filepath="//perspective_study.png"):
    """Рендерит сцену и сохраняет"""
    bpy.ops.render.render(write_still=True)
    bpy.data.images['Render Result'].save_render(filepath=bpy.path.abspath(filepath))
    print(f"✓ Рендер сохранён: {filepath}")

#add_horizon_line()
#add_grid_floor()

def scene_one_point_perspective():
    """Учебная сцена: кубы, уходящие к одной точке схода"""
    # Очистка
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Настройки
    setup_study_lighting()
    enable_shadows()
    configure_render_for_print()
    
    # Пол и горизонт
    add_grid_floor(size=40, subdivisions=20)
    add_horizon_line(y_pos=30, z_height=1.6)
    
    # Точка схода
    vp = add_vanishing_point(location=(0, 30, 1.6), name="VP1")
    
    # Кубы в перспективе
    for i, x in enumerate([-6, -3, 0, 3, 6]):
        cube = add_cube(location=(x, i*3, 1), size=1.5 - i*0.2, name=f"Cube_{i}")
        # Линии к точке схода (опционально)
        add_projection_line(cube.location, vp.location, name=f"Line_{i}")
    
    # Камера
    setup_camera_for_perspective(target=(0, 10, 1), distance=40, height=8)
    
    # Рендер
    render_and_save("//one_point_study.png")
    print("✓ Сцена 'Одна точка схода' готова")

# Запуск: scene_one_point_perspective()
#scene_one_point_perspective()

def scene_two_point_perspective():
    """Сцена с двумя точками схода для архитектуры"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    setup_study_lighting()
    enable_shadows('CYCLES')
    configure_render_for_print()
    
    # Горизонт и две точки схода
    add_horizon_line(y_pos=40, z_height=1.6)
    vp_left = add_vanishing_point(location=(-25, 40, 1.6), name="VP_Left", color=(1, 0, 0))
    vp_right = add_vanishing_point(location=(25, 40, 1.6), name="VP_Right", color=(0, 0, 1))
    
    # «Здания» из кубов и цилиндров
    add_cube(location=(-4, 5, 2), size=3, name="Building_A")
    add_cylinder(location=(4, 8, 2.5), radius=1.5, depth=5, name="Tower_B")
    add_cone(location=(0, 12, 4), radius1=2, depth=4, name="Roof_C")
    
    # Направляющие от углов к точкам схода
    for obj_name in ["Building_A", "Tower_B", "Roof_C"]:
        obj = bpy.data.objects.get(obj_name)
        if obj:
            add_projection_line(obj.location, vp_left.location, name=f"{obj_name}_to_VPL")
            add_projection_line(obj.location, vp_right.location, name=f"{obj_name}_to_VPR")
    
    setup_camera_for_perspective(target=(0, 10, 2), distance=50, height=10)
    render_and_save("//two_point_study.png")
    print("✓ Сцена 'Две точки схода' готова")

# Запуск: scene_two_point_perspective()
#scene_two_point_perspective()

def scene_ortho_template():
    """Компоновка: 3 орто-вида + перспектива для печати-шаблона"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Создаём «машинку» из примитивов
    body = add_cube(location=(0, 0, 1), size=4, name="CarBody")
    cabin = add_cube(location=(0, 0, 2.5), size=2, name="Cabin")
    wheel = add_cylinder(location=(1.5, 2, 0.5), radius=0.6, depth=0.4, name="Wheel_FL")
    wheel.rotation_euler = Euler((math.radians(90), 0, 0), 'XYZ')
    
    setup_study_lighting()
    enable_shadows()
    
    # Рендерим 4 вида в один файл (упрощённо — последовательно)
    views = [
        ("//view_perspective.png", setup_camera_for_perspective, (0, 0, 1), 25, 8),
        ("//view_front.png", setup_orthographic_camera, None, None, None),
        ("//view_side.png", setup_orthographic_camera, None, None, None), 
        ("//view_top.png", setup_orthographic_camera, None, None, None),
    ]
    
    for filepath, cam_func, target, dist, height in views:
        if cam_func == setup_camera_for_perspective:
            cam_func(target=target, distance=dist, height=height)
        else:
            # Определяем ось по имени файла
            axis = 'FRONT' if 'front' in filepath else ('SIDE' if 'side' in filepath else 'TOP')
            cam_func(size=15, axis=axis)
        configure_render_for_print(resolution=(1240, 1754))  # A5 для экономии
        render_and_save(filepath)
    
    print("✓ Набор орто-шаблонов готов")

# Запуск: scene_ortho_template()

#scene_ortho_template()
# === МИКРО-УПРАЖНЕНИЯ ===

def exercise_draw_cubes_in_row(count=5, spacing=3, size_decay=0.8):
    """Упражнение: ряд кубов с уменьшением размера в перспективе"""
    for i in range(count):
        size = 2 * (size_decay ** i)
        add_cube(location=(0, i*spacing, 1), size=size, name=f"Cube_Exercise_{i}")
    print(f"✓ Создано {count} кубов для упражнения")

def exercise_sphere_shadows():
    """Упражнение: сфера с акцентом на светотень"""
    add_sphere(location=(0, 0, 1.5), radius=2)
    # Жёсткий ключевой свет для чёткой тени
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 20))
    light = bpy.context.active_object
    light.data.energy = 5.0
    light.data.angle = 0.01  # Почти параллельные лучи
    print("✓ Сфера для изучения светотени готова")

def exercise_cone_perspective():
    """Упражнение: конус в 1-точечной перспективе"""
    vp = add_vanishing_point((0, 30, 1.6))
    add_cone(location=(0, 5, 1), radius1=1.5, depth=3)
    add_projection_line((0, 5, 2.5), vp.location, name="ConeAxis")
    print("✓ Конус с направляющей к точке схода готов")
    
#exercise_draw_cubes_in_row()
#exercise_sphere_shadows()
#exercise_cone_perspective()

#add_cube((2, 5, 1), size=1)
#add_cube((2, 5, 3), size=3)
#add_cube((2, 5, 5), size=5)

# === БАЗОВЫЕ ПРИМИТИВЫ ===

add_cube((0, 3, 0), size=1, name="Cube", rotation=(45, 0, 0))
add_cylinder((0, 7, 0), 3, 2, "Cylinder_1", vertices=6)
add_cone( (0, 15, 0), 3, 2, 4, "Cone_1", vertices=8)
add_sphere((0,25, 0), radius=2, name="Sphere", segments=12)

#add_plane((0, 0, 0), size=10, "Ground")

#add_cube((0, 0, 0), size=1)
add_cube((3, 3, 0), size=2)
add_cube((7, 3, 0), size=3)
add_cube((15, 5, 0), size=4)

#add_grid_floor()
#enable_shadows()
