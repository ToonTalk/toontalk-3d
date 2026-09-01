# Packs ToonTalk 3D into ONE self-contained file that will run as a Claude
# artifact, where nothing may be fetched -- not another host, not a sibling
# file, not even a data: URI the page made itself.
#
#   python build_artifact.py            -> toontalk-3d.artifact.html
#
# What it does:
#   * downloads three.js, OrbitControls and GLTFLoader (the versions the import
#     map names) and bundles them into the page, replacing the import map;
#   * carries robot_v4.glb and dusty_v1.glb as base64 in the page itself, for
#     loadModel() to parse out of memory;
#   * spreads all of that over several <script type="module"> blocks, because a
#     single inline script over about a megabyte is silently dropped by the
#     artifact host (measured: 800 KB runs, 1.2 MB does not);
#   * leaves toontalk-3d.html itself untouched -- that stays the source. Run
#     embed_manual.py first if manual.html has changed.
#
# The bundling is deliberately dumb and therefore trustworthy: every module
# becomes an IIFE that RETURNS its exports onto `window`, and every import
# becomes a `const` read off the namespace an earlier block produced. No
# renaming, no hoisting tricks, no chance of two modules' helpers colliding --
# and being on `window` is what lets the blocks be separate scripts at all.
#
# Downloads are cached in .artifact-cache/, so a rebuild is offline and quick.
import base64, io, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, '.artifact-cache')
SRC = os.path.join(HERE, 'toontalk-3d.html')
OUT = os.path.join(HERE, 'toontalk-3d.artifact.html')
MODELS = ['robot_v4.glb', 'dusty_v11.glb']
BLOCK_MAX = 700 * 1024          # comfortably under what the host will run

# name -> (path inside the three package, JS identifier for its namespace).
# Order matters: a module may only import from ones already listed.
MODULES = [
    ('three.core', 'build/three.core.min.js', '__m_core'),
    ('three', 'build/three.module.min.js', 'THREE'),
    ('OrbitControls', 'examples/jsm/controls/OrbitControls.js', '__m_orbit'),
    ('BufferGeometryUtils', 'examples/jsm/utils/BufferGeometryUtils.js', '__m_bgu'),
    ('SkeletonUtils', 'examples/jsm/utils/SkeletonUtils.js', '__m_skel'),
    ('GLTFLoader', 'examples/jsm/loaders/GLTFLoader.js', '__m_gltf'),
]


def fetch(url, name):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name)
    if os.path.exists(path):
        return io.open(path, encoding='utf-8').read()
    print('  downloading', url)
    req = urllib.request.Request(url, headers={'User-Agent': 'tt3d-build'})
    text = urllib.request.urlopen(req, timeout=120).read().decode('utf-8')
    io.open(path, 'w', encoding='utf-8').write(text)
    return text


def resolve(spec):
    """Which of MODULES does this import specifier mean?"""
    stem = 'three' if spec == 'three' else spec.rsplit('/', 1)[-1]
    stem = stem.replace('.min', '').replace('.js', '')
    if stem == 'three.module':
        stem = 'three'
    for name, _, ns in MODULES:
        if name == stem:
            return ns
    sys.exit('unbundled import: ' + spec)


def parse_names(block):
    """'A, B as C' -> [(A, A), (B, C)] -- (name in the source, name out)."""
    out = []
    for piece in block.replace('\n', ' ').split(','):
        piece = piece.strip()
        if not piece:
            continue
        m = re.match(r'^(\S+)\s+as\s+(\S+)$', piece)
        out.append((m.group(1), m.group(2)) if m else (piece, piece))
    return out


# Rollup's output -- minified or not -- puts every import at the top and the
# lone export list at the very end. Minified files are one enormous line, so
# these cannot be anchored to line starts; a statement boundary will do.
IMPORT = re.compile(r'(^|[;\n}])import\s*\{([^}]*)\}\s*from\s*[\'"]([^\'"]+)[\'"]\s*;?')
REEXPORT = re.compile(r'(^|[;\n}])export\s*\{([^}]*)\}\s*from\s*[\'"]([^\'"]+)[\'"]\s*;?')
EXPORT = re.compile(r'(^|[;\n}])export\s*\{([^}]*)\}\s*;?')


def wrap(js, ns):
    """Turn one ES module into `window.ns = (function () { ... })();`"""
    binds, exports = [], []

    def imp(match):
        src = resolve(match.group(3).strip())
        for a, b in parse_names(match.group(2)):
            binds.append((b, src, a))
        return match.group(1)

    def reexp(match):
        src = resolve(match.group(3).strip())
        for a, b in parse_names(match.group(2)):
            binds.append((b, src, a))
            exports.append(b)
        return match.group(1)

    def exp(match):
        for a, b in parse_names(match.group(2)):
            exports.append('%s: %s' % (b, a) if a != b else a)
        return match.group(1)

    body = IMPORT.sub(imp, js)
    body = REEXPORT.sub(reexp, body)
    body = EXPORT.sub(exp, body)
    for leftover in ('\nimport ', '\nexport ', ';import', ';export'):
        if leftover in body:
            sys.exit('unhandled module syntax in %s: %s' % (ns, leftover.strip()))
    if not exports:
        sys.exit('no exports found in ' + ns)
    # one plain const per imported name: no destructuring, so a name that
    # arrives twice (imported AND re-exported) simply collapses
    seen, head = set(), []
    for local, src, orig in binds:
        if local in seen:
            continue
        seen.add(local)
        head.append('const %s = %s.%s;' % (local, src, orig))
    return ('window.%s = (function () {\n%s\n%s\nreturn { %s };\n})();\n'
            % (ns, '\n'.join(head), body, ', '.join(exports)))


# WHAT A PUBLISHED ARTIFACT WILL AND WILL NOT DO -- measured 2026-08-20, with
# probe pages, against claude.ai's artifact frame:
#
#   works:  2.5 MB pages; inline module scripts up to 800 KB; WebGL2; canvas
#           textures; localStorage; the downloads capability; a full-screen
#           three.js scene RENDERED ONCE (alive after 20 s of watching); a
#           trivial scene animated by setAnimationLoop if the loop starts 8 s
#           after load.
#   fails:  a single inline script of 1.2 MB (silently dropped); fetch of any
#           kind, including a data: URI the page made itself and any outside
#           host; and -- the wall -- this workshop's own animation loop. The
#           frame goes white, markup and all, however long the boot is delayed
#           (6 s and 12 s both die). A live 3D workshop is more than the frame
#           will carry; the file below still runs perfectly when opened from
#           disk or served from anywhere else.
GATE = 'bootWorkshop();\n'


def script(js):
    """One inline module block, refused if it is too big to survive."""
    if len(js.encode('utf-8')) > BLOCK_MAX:
        sys.exit('a script block came to %.0f KB, over the %d KB the host will run'
                 % (len(js.encode('utf-8')) / 1024, BLOCK_MAX / 1024))
    return '<script type="module">\n' + js + '\n</script>\n'


def main():
    src = io.open(SRC, encoding='utf-8').read()

    m = re.search(r'"three":\s*"https://unpkg\.com/three@([\d.]+)/', src)
    if not m:
        sys.exit('could not find the three.js version in the import map')
    ver = m.group(1)
    print('three.js', ver)

    blocks = []
    # the models first: loadModel() reads them straight out of __TT_MODELS
    for i, name in enumerate(MODELS):
        mpath = os.path.join(HERE, name)
        if not os.path.exists(mpath):
            sys.exit('missing model: ' + name)
        if "'%s'" % name not in src:
            sys.exit('the page no longer names ' + name)
        b64 = base64.b64encode(io.open(mpath, 'rb').read()).decode('ascii')
        blocks.append(('window.__TT_MODELS = window.__TT_MODELS || {};\n'
                       'window.__TT_MODELS[%s] = "%s";' % (json.dumps(name), b64)))
        print('  packed %s (%.0f KB -> %.0f KB)'
              % (name, os.path.getsize(mpath) / 1024, len(b64) / 1024))

    # then three.js, one block per module, in dependency order
    small = []
    for name, path, ns in MODULES:
        js = fetch('https://unpkg.com/three@%s/%s' % (ver, path),
                   '%s-%s%s.js' % (name, ver, '.min' if '.min.' in path else ''))
        js = '/* ---- %s ---- */\n' % name + wrap(js, ns)
        # the big two get a block each; the addons share one
        if len(js) > BLOCK_MAX // 2:
            blocks.append(js)
        else:
            small.append(js)
    small.append('window.OrbitControls = __m_orbit.OrbitControls;\n'
                 'window.GLTFLoader = __m_gltf.GLTFLoader;')
    blocks.append('\n'.join(small))

    # the page's own module: the import map and its three imports both go, and
    # what they named is on `window` by the time this block runs
    out = re.sub(r'<script type="importmap">[\s\S]*?</script>\s*', '', src, count=1)
    out, n = re.subn(r'^import\s+[\s\S]*?from\s+[\'"]three(?:/addons/[^\'"]*)?[\'"];\s*$',
                     '', out, flags=re.M)
    if n != 3:
        sys.exit('expected 3 imports in the page, replaced %d' % n)
    head, sep, rest = out.partition('<script type="module">')
    appjs, sep2, tail = rest.partition('</script>')
    if not sep or not sep2:
        sys.exit("could not find the page's own module")
    out = (head + ''.join(script(b) for b in blocks)
           + '<script type="module">\n'
           + '/* ---- the workshop ---- */\n'
           + 'const THREE = window.THREE;\n'
           + 'const OrbitControls = window.OrbitControls;\n'
           + 'const GLTFLoader = window.GLTFLoader;\n'
           + 'const bootWorkshop = () => {\n' + appjs + '\n};\n'
           + GATE + '</script>' + tail)

    # The artifact host supplies the document skeleton and wraps what we give
    # it, so the page must hand over its contents, not a whole document. The
    # <title> stays: that is the artifact's name.
    for tag in ('<!doctype html>', '<html lang="en">', '<head>', '</head>',
                '<body>', '</body>', '</html>'):
        if tag not in out:
            sys.exit('expected to strip ' + tag)
        out = out.replace(tag, '', 1)
    out = out.lstrip()

    # Marty's manual: manual.html cannot be fetched in an artifact, so the
    # embedded copy is the only one he gets
    if 'id="martyManual"' not in out:
        sys.exit('run embed_manual.py first: the artifact would have no manual')

    biggest = max(len(b.encode('utf-8')) for b in re.findall(
        r'<script type="module">([\s\S]*?)</script>', out))
    io.open(OUT, 'w', encoding='utf-8').write(out)
    print('wrote %s (%.1f MB, %d script blocks, biggest %.0f KB)'
          % (os.path.basename(OUT), len(out.encode('utf-8')) / 1048576,
             len(blocks) + 1, biggest / 1024))


if __name__ == '__main__':
    main()
