"""Dusty the vacuum, v6 -- a character rather than an appliance.

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
TAG = "v6"

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



def cut(target, cutter):
    """Subtract `cutter` from `target` and throw the cutter away.

    AN OPENING HAS TO BE CUT. Every earlier Dusty faked its mouth by laying a
    dark ellipsoid over the shell, and every one read as a lump stuck on rather
    than a hole -- because that is exactly what it was. A boolean removes
    material, so the eye gets a rim, a wall and a shadow, which is what says
    "this goes inwards".
    """
    bpy.context.view_layer.objects.active = target
    m = target.modifiers.new("cut", 'BOOLEAN')
    m.operation = 'DIFFERENCE'
    m.solver = 'EXACT'
    m.object = cutter
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    return target


clear()
M_SHELL = mat("dusty_shell", CORAL, rough=0.30)
M_CREAM = mat("dusty_cream", CREAM, rough=0.34)
M_DARK  = mat("dusty_slate", SLATE, rough=0.48, metal=0.30)
M_STEEL = mat("dusty_steel", STEEL, rough=0.25, metal=0.90)
M_GLOW  = mat("dusty_glow", (0.06, 0.35, 0.45, 1), rough=0.15, emit=CYAN, emit_str=2.0)
M_AMBER = mat("dusty_amber", (0.35, 0.20, 0.03, 1), rough=0.2, emit=AMBER, emit_str=2.2)
M_WHITE = mat("dusty_white", (1, 1, 1, 1), rough=0.12, emit=(1, 1, 1, 1), emit_str=1.1)

# ONE SHAPE PLUS A FACE, which is why Marty works and why v2 and v3 did not.
# Both were assemblies -- a head on a neck, a visor, a snout, a skirt -- and
# every seam was somewhere for the eye to catch. Dusty is a single rounded
# body, and the vacuum idea is carried by his MOUTH: he is the fellow who
# takes things away, so the intake IS the mouth and he eats what you give him.
# Nothing bolted on that a face cannot explain.
root = empty("DUSTY_root", (0, 0, 0))
body = ball("body", 0.22, (0, 0, 0.20), M_SHELL, parent=root, scale=(1.0, 0.92, 0.85))

# THE MOUTH IS CUT INTO HIM, not laid on top. The cutter is a wide flat
# ellipsoid pushed through the front; what is left is a cavity with coral walls
# and a real edge, with the suction glowing in the dark of it.
mouth_cutter = ball("mouth_cut", 0.115, (0, -0.205, 0.146), None,
                    scale=(1.25, 0.92, 0.52))
cut(body, mouth_cutter)
ball("throat", 0.098, (0, -0.120, 0.146), M_DARK, parent=body, scale=(1.22, 0.85, 0.50))
ball("gulp", 0.068, (0, -0.135, 0.146), M_GLOW, parent=body, scale=(1.10, 0.55, 0.42))

# ...and the eyes sit IN shallow sockets, so they belong to the head instead of
# being stuck to it. The socket's shadow is what does the work.
for s2, nm in ((-1, "L"), (1, "R")):
    cut(body, ball("sock_" + nm, 0.056, (0.076 * s2, -0.196, 0.300), None))
for s2, nm in ((-1, "L"), (1, "R")):
    ball("eye_" + nm, 0.055, (0.076 * s2, -0.168, 0.300), M_CREAM, parent=body)
    ball("iris_" + nm, 0.032, (0.079 * s2, -0.205, 0.298), M_GLOW, parent=body,
         scale=(1, 0.55, 1))
    ball("spark_" + nm, 0.013, (0.091 * s2, -0.214, 0.314), M_WHITE, parent=body,
         scale=(1, 0.6, 1))

torus("bumper", 0.168, 0.030, (0, 0, 0.030), M_DARK, parent=root)
ball("chin", 0.078, (0, -0.170, 0.078), M_CREAM, parent=body, scale=(1.15, 0.30, 0.50))

# the family badge Marty and the robots wear
cyl("antenna", 0.009, 0.08, (0, 0.02, 0.400), M_STEEL, bevel=0.004, parent=body)
ball("blinker", 0.026, (0, 0.02, 0.448), M_AMBER, parent=body)

# little mitts: he should look as though he can carry off what he takes
for s2, nm in ((-1, "L"), (1, "R")):
    cyl("arm_" + nm, 0.020, 0.050, (0.190 * s2, -0.035, 0.180), M_DARK, bevel=0.008,
        parent=body, rot=(0, math.radians(74 * s2), 0))
    ball("mitt_" + nm, 0.042, (0.216 * s2, -0.035, 0.168), M_CREAM, parent=body,
         scale=(1, 0.94, 0.88))

# the bag rides on his back like a satchel, with a window so you can see he
# really is keeping what he took
ball("bag", 0.105, (0, 0.168, 0.255), M_SHELL, parent=body, scale=(0.90, 0.75, 0.95))
torus("bag_strap", 0.092, 0.016, (0, 0.150, 0.255), M_CREAM, parent=body,
      rot=(math.radians(90), 0, math.radians(90)))
cyl("bag_window", 0.044, 0.018, (0, 0.238, 0.262), M_GLOW, parent=body,
    rot=(math.radians(90), 0, 0), bevel=0.006)
empty("intake", (0, -0.30, 0.15), parent=body)     # where he points when working

# wheels, mostly tucked behind the bumper
for s2, nm in ((-1, "L"), (1, "R")):
    cyl("wheel_" + nm, 0.046, 0.032, (0.140 * s2, 0.01, 0.046), M_DARK,
        rot=(0, math.radians(90), 0), parent=root)
ball("caster", 0.034, (0, 0.140, 0.038), M_STEEL, parent=root)

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
