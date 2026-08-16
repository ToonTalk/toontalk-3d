"""ToonTalk-3D robot, v3.
v2 fixed colour/exposure; this fixes the arms. v2's hands read as pale nubs and
the arms hugged the torso. Now: joint empties (so limbs can be posed/animated),
splayed shoulders, forearms swung forward at the elbow, and a real two-jaw claw
that reads as a gripper -- which is what the pick-up/drop step needs.

  blender --background --factory-startup --python robot_v3.py
"""
import bpy, math, os

OUT = os.path.dirname(os.path.abspath(__file__))
TAG = "v4"

CORAL  = (0.72, 0.14, 0.09, 1)
CREAM  = (0.93, 0.88, 0.75, 1)
SLATE  = (0.075, 0.09, 0.125, 1)
STEEL  = (0.42, 0.45, 0.50, 1)
CYAN   = (0.25, 0.90, 1.00, 1)
AMBER  = (1.00, 0.68, 0.15, 1)

ELBOW_FWD  = -42.0   # deg, swings forearm forward so the claw is visible
SHOULDER_SPLAY = 9.0 # deg outward

def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(name, color, rough=0.42, metal=0.0, emit=None, emit_str=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = emit_str
    return m

def _parent(o, parent):
    if parent:
        bpy.context.view_layer.update()
        o.parent = parent
        o.matrix_parent_inverse = parent.matrix_world.inverted()

def _finish(o, material, bevel, seg, parent, smooth_angle=40.0):
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0:
        bv = o.modifiers.new("Bevel", 'BEVEL')
        bv.width = bevel
        bv.segments = seg
        bv.limit_method = 'ANGLE'
        bv.angle_limit = math.radians(30)
        bv.harden_normals = True
    if material:
        o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    try:
        bpy.ops.object.shade_auto_smooth(angle=math.radians(smooth_angle))
    except Exception:
        pass
    _parent(o, parent)
    return o

def box(name, size, loc, material=None, bevel=0.025, seg=4, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    return _finish(o, material, bevel, seg, parent)

def cyl(name, r, h, loc, material=None, bevel=0.014, seg=3, parent=None, rot=(0, 0, 0), verts=28):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc,
                                        rotation=rot, vertices=verts)
    o = bpy.context.object
    o.name = name
    return _finish(o, material, bevel, seg, parent)

def ball(name, r, loc, material=None, parent=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    return _finish(o, material, 0, 0, parent)

def empty(name, loc, parent=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = 'PLAIN_AXES'
    e.empty_display_size = 0.09
    e.location = loc
    bpy.context.collection.objects.link(e)
    _parent(e, parent)
    return e

clear()
M_SHELL  = mat("shell_coral", CORAL, rough=0.30)
M_CREAM  = mat("shell_cream", CREAM, rough=0.34)
M_DARK   = mat("joint_slate", SLATE, rough=0.48, metal=0.30)
M_STEEL  = mat("steel", STEEL, rough=0.25, metal=0.90)
M_GLOW   = mat("glow_cyan", (0.06, 0.35, 0.45, 1), rough=0.15, emit=CYAN, emit_str=2.2)
M_AMBER  = mat("glow_amber", (0.35, 0.20, 0.03, 1), rough=0.2, emit=AMBER, emit_str=2.0)
M_SCREEN = mat("chest_screen", (0.02, 0.06, 0.09, 1), rough=0.10,
               emit=(0.10, 0.62, 0.85, 1), emit_str=1.05)

# ---------------------------------------------------------------- body
root = empty("ROBOT_root", (0, 0, 0))
pelvis = box("pelvis", (0.42, 0.30, 0.17), (0, 0, 0.705), M_DARK, bevel=0.045, parent=root)
torso  = box("torso",  (0.64, 0.45, 0.58), (0, 0, 1.04), M_SHELL, bevel=0.080, seg=5, parent=root)
box("chest_bezel",  (0.44, 0.07, 0.32), (0, -0.205, 1.09), M_CREAM, bevel=0.022, parent=torso)
box("chest_screen", (0.37, 0.02, 0.25), (0, -0.237, 1.09), M_SCREEN, bevel=0.008, parent=torso)
# back detail -- v3's back was a featureless coral slab from behind
box("back_plate", (0.46, 0.05, 0.36), (0, 0.205, 1.07), M_CREAM, bevel=0.028, parent=torso)
for i, dz in enumerate((-0.09, 0.0, 0.09)):
    box("vent_%d" % i, (0.30, 0.03, 0.032), (0, 0.228, 1.07 + dz), M_DARK,
        bevel=0.010, parent=torso)
ball("back_light", 0.034, (0.155, 0.225, 1.235), M_AMBER, parent=torso)
cyl("belt", 0.225, 0.075, (0, 0, 0.775), M_CREAM, rot=(math.radians(90), 0, 0), parent=torso)
ball("belt_stud", 0.038, (0, -0.205, 0.775), M_AMBER, parent=torso)
box("yoke", (0.74, 0.36, 0.14), (0, 0, 1.305), M_CREAM, bevel=0.055, seg=5, parent=torso)

cyl("neck", 0.095, 0.14, (0, 0, 1.405), M_DARK, parent=torso)
head = box("head", (0.47, 0.44, 0.39), (0, 0, 1.655), M_SHELL, bevel=0.090, seg=6, parent=root)
box("brow", (0.49, 0.31, 0.075), (0, -0.02, 1.808), M_CREAM, bevel=0.032, parent=head)
box("visor", (0.41, 0.06, 0.155), (0, -0.204, 1.655), M_DARK, bevel=0.022, parent=head)
box("head_back", (0.31, 0.04, 0.23), (0, 0.202, 1.650), M_CREAM, bevel=0.024, parent=head)
for s, nm in ((-1, "L"), (1, "R")):
    ball("eye_" + nm, 0.055, (0.108 * s, -0.229, 1.655), M_GLOW, parent=head, scale=(1, 0.55, 1))
    cyl("ear_" + nm, 0.065, 0.055, (0.243 * s, 0, 1.645), M_STEEL,
        rot=(0, math.radians(90), 0), parent=head)
cyl("antenna", 0.023, 0.17, (0, 0.055, 1.925), M_STEEL, parent=head)
ball("antenna_tip", 0.052, (0, 0.055, 2.02), M_AMBER, parent=head)

# ---------------------------------------------------------------- arms
def arm(side, nm):
    x = 0.405 * side                       # further out than v2 (0.355)
    sh_p = empty("shoulderP_" + nm, (x, 0, 1.215), parent=torso)
    ball("shoulder_" + nm, 0.128, (x, 0, 1.215), M_DARK, parent=sh_p)
    cyl("upperarm_" + nm, 0.094, 0.27, (x, 0, 1.070), M_SHELL, parent=sh_p)

    el_p = empty("elbowP_" + nm, (x, 0, 0.935), parent=sh_p)
    ball("elbow_" + nm, 0.100, (x, 0, 0.935), M_DARK, parent=el_p)
    cyl("forearm_" + nm, 0.086, 0.25, (x, 0, 0.815), M_CREAM, parent=el_p)
    ball("wrist_" + nm, 0.082, (x, 0, 0.700), M_DARK, parent=el_p)

    # claw: solid palm, two opposing jaws reaching forward (-Y)
    pa = box("palm_" + nm, (0.175, 0.17, 0.175), (x, -0.015, 0.610), M_SHELL,
             bevel=0.038, seg=5, parent=el_p)
    for js, jnm in ((-1, "a"), (1, "b")):
        jw = box("jaw_%s_%s" % (nm, jnm), (0.062, 0.215, 0.150),
                 (x + 0.056 * js, -0.200, 0.610), M_CREAM, bevel=0.026, seg=4, parent=pa)
        box("jawpad_%s_%s" % (nm, jnm), (0.030, 0.150, 0.105),
            (x + 0.032 * js, -0.215, 0.610), M_DARK, bevel=0.016, parent=jw)
    empty("grip_" + nm, (x, -0.255, 0.610), parent=pa)

    sh_p.rotation_euler = (0, math.radians(-side * SHOULDER_SPLAY), 0)
    el_p.rotation_euler = (math.radians(ELBOW_FWD), 0, 0)

arm(-1, "L")
arm(1, "R")

# ---------------------------------------------------------------- legs
def leg(side, nm):
    x = 0.19 * side
    hp = ball("hip_" + nm, 0.108, (x, 0, 0.645), M_DARK, parent=root)
    cyl("thigh_" + nm, 0.098, 0.25, (x, 0, 0.515), M_SHELL, parent=hp)
    kn = ball("knee_" + nm, 0.100, (x, 0, 0.390), M_DARK, parent=hp)
    cyl("shin_" + nm, 0.088, 0.25, (x, 0, 0.260), M_CREAM, parent=kn)
    box("foot_" + nm, (0.22, 0.34, 0.14), (x, -0.045, 0.078), M_DARK, bevel=0.050, seg=5, parent=kn)

leg(-1, "L")
leg(1, "R")

# ---------------------------------------------------------------- scene
robot_col = bpy.data.collections.new("RobotRig")
for o in list(bpy.context.scene.collection.objects):
    robot_col.objects.link(o)
    bpy.context.scene.collection.objects.unlink(o)

def add_instance(name, loc, rot_z):
    e = bpy.data.objects.new(name, None)
    e.instance_type = 'COLLECTION'
    e.instance_collection = robot_col
    e.location = loc
    e.rotation_euler = (0, 0, math.radians(rot_z))
    bpy.context.scene.collection.objects.link(e)
    return e

scn = bpy.context.scene
scn.render.engine = 'CYCLES'
scn.cycles.use_denoising = True
scn.view_settings.view_transform = 'Standard'
scn.view_settings.look = 'None'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    scn.cycles.device = 'GPU'
except Exception as e:
    print("CYCLES DEVICE: CPU (%s)" % e)

world = bpy.data.worlds.new("W")
scn.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.035, 0.042, 0.055, 1)

M_FLOOR = mat("floor", (0.105, 0.115, 0.135, 1), rough=0.42)
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
bpy.context.object.name = "floor"
bpy.context.object.data.materials.append(M_FLOOR)

def area_light(name, loc, rot, energy, size, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, 'AREA')
    d.energy, d.size, d.color = energy, size, color
    o = bpy.data.objects.new(name, d)
    o.location, o.rotation_euler = loc, rot
    bpy.context.scene.collection.objects.link(o)
    return o

area_light("key",  (3.2, -3.6, 4.4), (math.radians(46), 0, math.radians(41)), 340, 4.0)
area_light("fill", (-4.2, -2.6, 2.2), (math.radians(72), 0, math.radians(-58)), 110, 5.0,
           color=(0.72, 0.82, 1.0))
area_light("rim",  (-1.8, 4.4, 3.4), (math.radians(122), 0, math.radians(-22)), 220, 3.0,
           color=(0.80, 0.90, 1.0))

def make_cam(name, loc, target_z, lens=None, ortho_scale=None):
    d = bpy.data.cameras.new(name)
    if ortho_scale:
        d.type = 'ORTHO'
        d.ortho_scale = ortho_scale
    else:
        d.lens = lens or 70
    c = bpy.data.objects.new(name, d)
    c.location = loc
    scn.collection.objects.link(c)
    tgt = bpy.data.objects.new(name + "_tgt", None)
    tgt.location = (0, 0, target_z)
    scn.collection.objects.link(tgt)
    con = c.constraints.new('TRACK_TO')
    con.target = tgt
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    return c

def render(path, res_x, res_y, samples):
    scn.cycles.samples = samples
    scn.render.resolution_x, scn.render.resolution_y = res_x, res_y
    scn.render.resolution_percentage = 100
    scn.render.image_settings.file_format = 'PNG'
    scn.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("WROTE", path)

sheet = [add_instance("inst_%d" % i, (i * 1.6 - 2.4, 0, 0), a)
         for i, a in enumerate((0, 45, 90, 180))]
cam1 = make_cam("cam_ortho", (0, -16, 1.06), 1.06, ortho_scale=7.1)
scn.camera = cam1
render(os.path.join(OUT, "robot_%s_sheet.png" % TAG), 1500, 660, 110)

for e in sheet:
    scn.collection.objects.unlink(e)
# rot 0: v3 rotated the instance ~34deg, cancelling the camera azimuth and
# flattening the "hero" shot back to a front view.
add_instance("inst_hero", (0, 0, 0), 0)
cam2 = make_cam("cam_hero", (3.3, -4.6, 2.15), 1.00, lens=80)
scn.camera = cam2
render(os.path.join(OUT, "robot_%s_hero.png" % TAG), 880, 880, 190)

scn.collection.children.link(robot_col)
bpy.ops.object.select_all(action='DESELECT')
for o in robot_col.objects:
    o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "robot_%s.glb" % TAG),
                          export_format='GLB', use_selection=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "robot_%s.blend" % TAG))
print("DONE")
