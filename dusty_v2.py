"""Dusty the vacuum, v2 -- a character rather than an appliance.

  blender --background --factory-startup --python dusty_v2.py

Ken, of v1: "I'm not very happy with how Dusty looks. It doesn't have the
charm of marty, ruby, and robots."

What was wrong, looking at the v1 hero render beside them:

  * The face was STUCK ON. A dark slab of visor sat proud of the dome with two
    flat discs in it, overlapping the collar -- eyes applied to an appliance,
    not a face the shell has. Marty's eyes sit IN his head; the robots' faces
    are a recessed screen.
  * No gaze. Flat emissive discs cannot look at you: what makes an eye alive is
    a bright iris with a highlight off-centre, and a lid or brow above it.
  * The nozzle ate him. A 0.16-deep cone at 0.10 radius, hung out front and
    down, read as a funnel or a cup and broke the silhouette in half.
  * One undifferentiated canister: no head, no shoulders, nothing to tell you
    which part is which from across a table.

What v2 does about it, keeping the palette, the size and the vacuum idea:

  * A HEAD that reads as a head -- a smaller dome set on the shoulders with the
    collar as a neck, so the silhouette has two masses instead of one.
  * Eyes sunk into a recessed dark visor band that WRAPS the head, each a
    cream ball with a cyan iris and an off-centre white highlight, set close
    together and large for their head, which is what makes a face read young
    and friendly. A cream brow-ridge over them gives him an expression.
  * A SNOUT, not a funnel: short, wide, tucked under the chin and angled
    forward, so it reads as a nose-and-mouth on a face rather than a machine
    part bolted to a barrel. The intake glow becomes a soft smile inside it.
  * Little cream mitts on stubby arms: he is the fellow who takes things away,
    so he should look as though he can hold something.
  * A weeble body -- wide at the base, tapering up -- which is stable-looking
    and inherently charming, with the dust bag a friendly cream pouch on his
    back rather than a lump.
  * An amber blinker on a short antenna, echoing Marty's and the robots', so
    the three of them look like they come from the same workshop.
"""
import bpy, math, os

OUT = os.path.dirname(os.path.abspath(__file__))
TAG = "v2"

CORAL = (0.72, 0.14, 0.09, 1)
CREAM = (0.93, 0.88, 0.75, 1)
SLATE = (0.075, 0.09, 0.125, 1)
STEEL = (0.42, 0.45, 0.50, 1)
CYAN = (0.25, 0.90, 1.00, 1)
AMBER = (1.00, 0.68, 0.15, 1)


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


def _finish(o, material, bevel, seg, parent):
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
        bpy.ops.object.shade_auto_smooth(angle=math.radians(40))
    except Exception:
        pass
    _parent(o, parent)
    return o


def box(name, size, loc, material=None, bevel=0.02, seg=4, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    return _finish(o, material, bevel, seg, parent)


def cyl(name, r, h, loc, material=None, bevel=0.012, seg=3, parent=None,
        rot=(0, 0, 0), verts=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc,
                                        rotation=rot, vertices=verts)
    o = bpy.context.object
    o.name = name
    return _finish(o, material, bevel, seg, parent)


def cone(name, r1, r2, h, loc, material=None, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=h, location=loc,
                                    rotation=rot, vertices=32)
    o = bpy.context.object
    o.name = name
    return _finish(o, material, 0, 0, parent)


def ball(name, r, loc, material=None, parent=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=40, ring_count=20)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    return _finish(o, material, 0, 0, parent)


def torus(name, R, r, loc, material=None, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc,
                                     rotation=rot, major_segments=40, minor_segments=16)
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
M_SHELL = mat("dusty_shell", CORAL, rough=0.30)
M_CREAM = mat("dusty_cream", CREAM, rough=0.34)
M_DARK = mat("dusty_slate", SLATE, rough=0.48, metal=0.30)
M_STEEL = mat("dusty_steel", STEEL, rough=0.25, metal=0.90)
M_GLOW = mat("dusty_glow", (0.06, 0.35, 0.45, 1), rough=0.15, emit=CYAN, emit_str=2.2)
M_AMBER = mat("dusty_amber", (0.35, 0.20, 0.03, 1), rough=0.2, emit=AMBER, emit_str=2.2)
M_WHITE = mat("dusty_white", (1, 1, 1, 1), rough=0.12, emit=(1, 1, 1, 1), emit_str=1.1)

root = empty("DUSTY_root", (0, 0, 0))

# ---------------------------------------------------------------- body
# A WEEBLE: widest at the hem, tapering up to the shoulders. Round and
# bottom-heavy reads as friendly and stable where a straight barrel reads as
# equipment.
skirt = cone("skirt", 0.215, 0.185, 0.16, (0, 0, 0.08), M_SHELL, parent=root)
torus("hem", 0.212, 0.028, (0, 0, 0.022), M_DARK, parent=root)
body = cyl("body", 0.185, 0.13, (0, 0, 0.225), M_SHELL, bevel=0.05, seg=6, parent=root)
cyl("belly_band", 0.190, 0.055, (0, 0, 0.196), M_CREAM, bevel=0.02, parent=body)

# ---------------------------------------------------------------- head
# Set on a short neck so there are two masses in the silhouette. Smaller than
# the body, which is what makes him look like a small person rather than a bin.
neck = cyl("neck", 0.105, 0.05, (0, 0, 0.305), M_DARK, bevel=0.014, parent=body)
head = ball("head", 0.155, (0, 0, 0.405), M_SHELL, parent=body, scale=(1, 0.95, 0.92))

# THE VISOR IS A GROOVE, NOT A SLAB: a dark band sunk into the head, wrapping
# round it, with the eyes sitting inside the groove.
torus("visor_groove", 0.150, 0.030, (0, 0, 0.418), M_DARK, parent=head,
      rot=(math.radians(90), 0, 0))
box("visor_face", (0.20, 0.055, 0.075), (0, -0.118, 0.418), M_DARK, bevel=0.022, parent=head)

# EYES WITH A GAZE: a cream ball, a cyan iris, and an off-centre white
# highlight. The highlight is the whole trick -- it is what makes an eye look
# wet and alive instead of like a lamp.
for s, nm in ((-1, "L"), (1, "R")):
    ball("eye_" + nm, 0.047, (0.055 * s, -0.128, 0.420), M_CREAM, parent=head,
         scale=(1, 0.72, 1))
    ball("iris_" + nm, 0.030, (0.058 * s, -0.158, 0.418), M_GLOW, parent=head,
         scale=(1, 0.42, 1))
    ball("spark_" + nm, 0.011, (0.070 * s, -0.170, 0.432), M_WHITE, parent=head,
         scale=(1, 0.5, 1))
# a cream brow gives him an expression -- slightly raised, which reads as
# willing rather than cross
box("brow", (0.20, 0.05, 0.026), (0, -0.116, 0.472), M_CREAM, bevel=0.011, parent=head,
    rot=(math.radians(-9), 0, 0))

# antenna and blinker, the family badge Marty and the robots wear
cyl("antenna", 0.011, 0.10, (0, 0.01, 0.545), M_STEEL, bevel=0.004, parent=head)
ball("blinker", 0.030, (0, 0.01, 0.605), M_AMBER, parent=head)

# ---------------------------------------------------------------- snout
# SHORT, WIDE AND TUCKED UNDER THE CHIN, angled forward and slightly down: a
# nose and mouth, not a funnel. v1's cone was two thirds as long as he was
# tall and hung off the front like a traffic cone.
snout = cone("snout", 0.095, 0.072, 0.075, (0, -0.205, 0.315), M_CREAM, parent=body,
             rot=(math.radians(99), 0, 0))
torus("snout_lip", 0.090, 0.020, (0, -0.238, 0.309), M_DARK, parent=body,
      rot=(math.radians(99), 0, 0))
# the intake glow, shaped as a soft smile inside the snout
ball("smile", 0.070, (0, -0.232, 0.307), M_GLOW, parent=body, scale=(1, 0.30, 0.62))
empty("intake", (0, -0.33, 0.29), parent=body)     # where he points when working

# ---------------------------------------------------------------- arms
# He is the fellow who takes things away: give him something to take them with.
for s, nm in ((-1, "L"), (1, "R")):
    cyl("arm_" + nm, 0.028, 0.12, (0.175 * s, -0.02, 0.245), M_DARK, bevel=0.01,
        parent=body, rot=(0, math.radians(64 * s), 0))
    ball("mitt_" + nm, 0.052, (0.232 * s, -0.02, 0.205), M_CREAM, parent=body,
         scale=(1, 0.92, 0.86))

# ---------------------------------------------------------------- bag + wheels
# The bag rides high on his back like a satchel, with a cream patch so you can
# see it is a bag and not a hump.
bag = ball("bag", 0.115, (0, 0.165, 0.315), M_SHELL, parent=body, scale=(0.92, 0.78, 1.0))
torus("bag_strap", 0.100, 0.018, (0, 0.150, 0.315), M_CREAM, parent=body,
      rot=(math.radians(90), 0, math.radians(90)))
cyl("bag_window", 0.052, 0.02, (0, 0.243, 0.325), M_GLOW, parent=body,
    rot=(math.radians(90), 0, 0), bevel=0.006)

# small wheels, tucked under the skirt so the silhouette stays clean
for s, nm in ((-1, "L"), (1, "R")):
    cyl("wheel_" + nm, 0.050, 0.036, (0.150 * s, 0.01, 0.048), M_DARK,
        rot=(0, math.radians(90), 0), parent=root)
    cyl("hub_" + nm, 0.020, 0.040, (0.150 * s, 0.01, 0.048), M_STEEL,
        rot=(0, math.radians(90), 0), parent=root)
ball("caster", 0.038, (0, 0.145, 0.040), M_STEEL, parent=root)

# ---------------------------------------------------------------- collection
col = bpy.data.collections.new("DustyRig")
for o in list(bpy.context.scene.collection.objects):
    col.objects.link(o)
    bpy.context.scene.collection.objects.unlink(o)


def add_instance(name, loc, rot_z):
    e = bpy.data.objects.new(name, None)
    e.instance_type = 'COLLECTION'
    e.instance_collection = col
    e.location = loc
    e.rotation_euler = (0, 0, math.radians(rot_z))
    bpy.context.scene.collection.objects.link(e)
    return e


# ---------------------------------------------------------------- studio
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


area_light("key", (1.6, -1.8, 2.2), (math.radians(46), 0, math.radians(41)), 90, 2.0)
area_light("fill", (-2.1, -1.3, 1.1), (math.radians(72), 0, math.radians(-58)), 30, 2.5,
           color=(0.72, 0.82, 1.0))
area_light("rim", (-0.9, 2.2, 1.7), (math.radians(122), 0, math.radians(-22)), 60, 1.5,
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
cam1 = make_cam("cam_ortho", (0, -8, 0.32), 0.32, ortho_scale=2.75)
scn.camera = cam1
render(os.path.join(OUT, "dusty_%s_sheet.png" % TAG), 1500, 620, 110)

for e in sheet:
    scn.collection.objects.unlink(e)
add_instance("inst_hero", (0, 0, 0), 0)
cam2 = make_cam("cam_hero", (1.15, -1.75, 0.82), 0.30, lens=80)
scn.camera = cam2
render(os.path.join(OUT, "dusty_%s_hero.png" % TAG), 880, 880, 190)

scn.collection.children.link(col)
bpy.ops.object.select_all(action='DESELECT')
for o in col.objects:
    o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "dusty_%s.glb" % TAG),
                          export_format='GLB', use_selection=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "dusty_%s.blend" % TAG))
print("DONE")
