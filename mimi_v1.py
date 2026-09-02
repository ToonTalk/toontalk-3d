"""Mimi the copier, v1 -- a MIME, because her name says what she is.

  blender --background --factory-startup --python mimi_v1.py

Ken: "I'm wondering if we can make Mimi more of a character (e.g. with a
face). Do you have any ideas what kind of character and why it would make
sense for it to make copies of things?"

A mime copies what she is shown. That is the whole of her act, and it is the
whole of what the copier does: you set a thing in front of her, she studies
it, and a copy appears. So she is a mime the way the workshop's other helpers
are people -- Marty a Martian, Ruby an eraser with a face, Dusty a vacuum with
a mouth -- and her platform and tray stay as her little stage.

What is HERE, and why:
  * the classic silhouette, because it must read at toy scale from across
    the table: white face, black beret, black-and-white striped top, white
    gloves. Three colours and a shape everyone knows.
  * a face that MEETS your eye: Marty's own eye -- a pale ball with a small
    dark pupil standing just proud -- not googly, not a spark; and a small
    red mouth, closed, because a mime does not talk.
  * hands held up, palms out, the "invisible wall" pose: it says COPYING
    without a word, and it is the pose she will hold a copy in one day.
  * a body with the same proportions as Dusty (about half a metre), so she
    sits at the same scale beside the platform she serves.
"""
import bpy, math, os

OUT = os.path.dirname(os.path.abspath(__file__))
TAG = "v1"

WHITE = (0.93, 0.92, 0.88, 1)
BLACK = (0.03, 0.03, 0.035, 1)
SKIN = (0.96, 0.93, 0.86, 1)
RED = (0.72, 0.10, 0.12, 1)
EYE_BLUE = (0.35, 0.78, 1.00, 1)
PUPIL = (0.03, 0.06, 0.26, 1)
STEEL = (0.42, 0.45, 0.50, 1)
AMBER = (1.00, 0.68, 0.15, 1)


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def mat(name, color, rough=0.42, metal=0.0, emit=None, emit_str=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if emit is not None:
        bsdf.inputs["Emission Color"].default_value = emit
        bsdf.inputs["Emission Strength"].default_value = emit_str
    return m


def _parent(o, parent):
    if parent is not None:
        o.parent = parent


def _finish(o, material, bevel, seg, parent):
    if bevel:
        b = o.modifiers.new("bevel", 'BEVEL')
        b.width = bevel
        b.segments = seg
    if material is not None:
        o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    _parent(o, parent)
    return o


def box(name, size, loc, material=None, bevel=0.02, seg=4, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    return _finish(o, material, bevel, seg, parent)


def cyl(name, r, h, loc, material=None, bevel=0.012, seg=3, parent=None,
        rot=(0, 0, 0), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc,
                                        rotation=rot, vertices=verts)
    o = bpy.context.object
    o.name = name
    return _finish(o, material, bevel, seg, parent)


def ball(name, r, loc, material=None, parent=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=12)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    return _finish(o, material, 0, 0, parent)


def torus(name, R, r, loc, material=None, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc,
                                     rotation=rot, major_segments=22, minor_segments=10)
    o = bpy.context.object
    o.name = name
    return _finish(o, material, 0, 0, parent)


def empty(name, loc, parent=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = 'PLAIN_AXES'
    e.empty_display_size = 0.06
    e.location = loc
    bpy.context.collection.objects.link(e)
    _parent(e, parent)
    return e


clear()
M_WHITE = mat("mimi_white", WHITE, rough=0.55)
M_BLACK = mat("mimi_black", BLACK, rough=0.6)
M_SKIN = mat("mimi_skin", SKIN, rough=0.5)
M_RED = mat("mimi_red", RED, rough=0.4)
M_EYE = mat("mimi_eye", EYE_BLUE, rough=0.22)
M_PUPIL = mat("mimi_pupil", PUPIL, rough=0.28)
M_STEEL = mat("mimi_steel", STEEL, rough=0.25, metal=0.9)
M_AMBER = mat("mimi_amber", (0.35, 0.20, 0.03, 1), rough=0.2, emit=AMBER, emit_str=2.2)

root = empty("mimi", (0, 0, 0))

# --- the body: a striped top over a slim black trunk ---------------------------
# The stripes are bands of white laid over a black trunk, not a texture: the
# glb carries no images, and at this size five bands read as a stripe.
trunk = cyl("trunk", 0.085, 0.24, (0, 0, 0.30), M_BLACK, bevel=0.01, parent=root)
for i, z in enumerate((0.215, 0.265, 0.315, 0.365)):
    cyl("stripe_%d" % i, 0.088, 0.022, (0, 0, z), M_WHITE, bevel=0.004, parent=root)
# a black skirt of a hem, so the top ends somewhere
torus("hem", 0.085, 0.014, (0, 0, 0.185), M_BLACK, parent=root)
# legs and feet: short, black, and set a little apart -- she is standing
for s2, nm in ((-1, "L"), (1, "R")):
    cyl("leg_" + nm, 0.03, 0.15, (0.045 * s2, 0, 0.10), M_BLACK, bevel=0.008, parent=root)
    box("foot_" + nm, (0.055, 0.10, 0.03), (0.045 * s2, 0.025, 0.02), M_BLACK, bevel=0.01, parent=root)

# --- the head ----------------------------------------------------------------
head = ball("head", 0.10, (0, 0, 0.53), M_SKIN, parent=root, scale=(1, 0.95, 1.05))
# the beret: a flat disc, tilted, with a stalk -- the hat everybody knows
beret = cyl("beret", 0.115, 0.03, (0.01, 0, 0.615), M_BLACK, bevel=0.012, seg=4, parent=root,
            rot=(0, math.radians(-8), 0))
ball("beret_stalk", 0.012, (0.02, 0, 0.638), M_BLACK, parent=root)
# Marty's eye, in her colours: a pale ball, a small pupil standing proud
for s2, nm in ((-1, "L"), (1, "R")):
    ball("eye_" + nm, 0.026, (0.04 * s2, -0.085, 0.545), M_EYE, parent=root)
    ball("pupil_" + nm, 0.011, (0.041 * s2, -0.108, 0.545), M_PUPIL, parent=root)
    # a painted brow, the one line of make-up that says "mime"
    torus("brow_" + nm, 0.024, 0.004, (0.04 * s2, -0.086, 0.573), M_BLACK, parent=root,
          rot=(math.radians(90), 0, 0))
# a small closed red mouth: a mime does not talk
ball("mouth", 0.018, (0, -0.096, 0.492), M_RED, parent=root, scale=(1.4, 0.5, 0.55))
# the tear, painted, on one cheek
ball("tear", 0.007, (-0.052, -0.09, 0.515), M_BLACK, parent=root, scale=(1, 1, 1.8))

# --- the arms: up, palms out, the invisible wall -------------------------------
for s2, nm in ((-1, "L"), (1, "R")):
    # upper arm out to the side, forearm up, glove at the top: an L
    cyl("arm_" + nm, 0.024, 0.13, (0.13 * s2, 0, 0.34), M_BLACK, bevel=0.008, parent=root,
        rot=(0, math.radians(90), 0))
    cyl("forearm_" + nm, 0.022, 0.15, (0.195 * s2, -0.02, 0.41), M_BLACK, bevel=0.008,
        parent=root, rot=(math.radians(15), 0, 0))
    # the glove: a white ball flattened toward you, palm out
    ball("glove_" + nm, 0.04, (0.195 * s2, -0.045, 0.50), M_WHITE, parent=root,
         scale=(1.0, 0.55, 1.15))
    # a black cuff, which is what turns a ball into a glove
    torus("cuff_" + nm, 0.026, 0.008, (0.195 * s2, -0.02, 0.475), M_BLACK, parent=root)

# the family badge every helper wears
cyl("antenna", 0.007, 0.06, (-0.04, 0, 0.66), M_STEEL, bevel=0.003, parent=root)
ball("blinker", 0.02, (-0.04, 0, 0.695), M_AMBER, parent=root)

# --- render and export ------------------------------------------------------
col = bpy.data.collections.new("mimi")
bpy.context.scene.collection.children.link(col)
for o in list(bpy.context.scene.collection.objects):
    bpy.context.scene.collection.objects.unlink(o)
    col.objects.link(o)

scn = bpy.context.scene
scn.render.engine = 'CYCLES'
scn.cycles.device = 'CPU'
scn.render.film_transparent = False
world = bpy.data.worlds.new("w")
scn.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.12, 0.13, 0.16, 1)
bg.inputs[1].default_value = 0.6

M_FLOOR = mat("floor", (0.105, 0.115, 0.135, 1), rough=0.42)
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
floor = bpy.context.object
floor.data.materials.append(M_FLOOR)

def light(name, loc, energy, size=1.0):
    bpy.ops.object.light_add(type='AREA', location=loc)
    L = bpy.context.object
    L.name = name
    L.data.energy = energy
    L.data.size = size
    L.rotation_euler = (math.atan2(math.hypot(loc[0], loc[1]), loc[2]) , 0, math.atan2(loc[1], loc[0]) + math.pi / 2)
    return L

light("key", (1.2, -1.4, 1.8), 250, 1.2)
light("fill", (-1.6, -1.0, 1.0), 90, 2.0)
light("rim", (0.3, 1.6, 1.4), 120, 1.0)


def make_cam(name, loc, aim_z, lens=50, ortho_scale=None):
    """A camera that LOOKS AT a point, by constraint rather than by angles."""
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.name = name
    if ortho_scale:
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = ortho_scale
    cam.data.lens = lens
    target = bpy.data.objects.new(name + "_aim", None)
    target.location = (0, 0, aim_z)
    scn.collection.objects.link(target)
    c = cam.constraints.new('TRACK_TO')
    c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'
    return cam


def add_instance(name, loc, yaw_deg):
    inst = bpy.data.objects.new(name, None)
    inst.instance_type = 'COLLECTION'
    inst.instance_collection = col
    inst.location = loc
    inst.rotation_euler = (0, 0, math.radians(yaw_deg))
    scn.collection.objects.link(inst)
    return inst


def render(path, x, y, samples):
    scn.cycles.samples = samples
    scn.render.resolution_x, scn.render.resolution_y = x, y
    scn.render.resolution_percentage = 100
    scn.render.image_settings.file_format = 'PNG'
    scn.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("WROTE", path)


sheet = [add_instance("inst_%d" % i, (i * 0.62 - 0.93, 0, 0), a)
         for i, a in enumerate((0, 45, 90, 180))]
cam1 = make_cam("cam_ortho", (0, -8, 0.36), 0.36, ortho_scale=2.75)
scn.camera = cam1
render(os.path.join(OUT, "mimi_%s_sheet.png" % TAG), 1500, 620, 110)

for e in sheet:
    scn.collection.objects.unlink(e)
add_instance("inst_hero", (0, 0, 0), 0)
cam2 = make_cam("cam_hero", (1.05, -1.6, 0.75), 0.36, lens=80)
scn.camera = cam2
render(os.path.join(OUT, "mimi_%s_hero.png" % TAG), 880, 880, 190)

bpy.ops.object.select_all(action='DESELECT')
for o in col.objects:
    o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "mimi_%s.glb" % TAG),
                          export_format='GLB', use_selection=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "mimi_%s.blend" % TAG))
print("DONE")
