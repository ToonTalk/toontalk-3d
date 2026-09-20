# Builds toontalk-3d.chat.html -- the workshop as a claude.ai CHAT artifact,
# plus toontalk-3d-pack.json, the pack it asks the reader for once.
#
#   python build_chat_artifact.py
#
# WHY A THIRD BUILD. There are two artifact runtimes and they are not alike
# (measured 2026-08-23):
#
#   Claude Code artifact   `fetch` is the browser's own and a call to Anthropic
#                          is refused by the frame -- so Marty gets no keyless
#                          brain there -- but a 2.4 MB page publishes happily.
#   claude.ai CHAT artifact  carries the keyless call, which is the only way a
#                          reader gets a talking Marty with no key and no
#                          account -- but the publish size is far tighter
#                          (about 950 KB measured), and one inline script may
#                          not pass about 800 KB.
#
# So this build trades size for a brain. Three things make the packed build
# 3.7 MB and the source 1.4 MB, and it sheds them all:
#
#   three.js    fetched from cdn.jsdelivr.net, which the chat frame's own
#               content-security policy allows (unpkg, which the source uses,
#               is NOT on that list -- swapping the importmap is the change).
#   the prose   the module is 1.25 MB of which half is comment; MINIFIED
#               (terser: comments out, whitespace out, local names shortened)
#               it is about 535 KB. Nothing else about it changes: the same
#               source, the same behaviour, checked by the suite against the
#               minified page.
#   the data    the models (~730 KB), Marty's manual (108 KB) and the puzzle
#               set (25 KB) go in ONE PACK handed over by the READER: dropped
#               on the page or chosen from a picker, then kept in this browser
#               (gzipped, in localStorage) so it is asked for once. Ken's
#               technique, from Comic Chat (September 2026: "the first time
#               the user used the artifact they would be instructed to upload a
#               file that would be cached in the browser's storage").
#
# What is left is about 560 KB, which fits with room to grow. The CODE stays in
# the page: running code out of a dropped file needs eval, and whether the chat
# frame's policy allows it is unmeasured -- the prose was the fat, not the code.
#
# The loader is a plain script BEFORE the module, and the module waits on the
# promise it leaves behind. loadModel already prefers window.__TT_MODELS over
# fetching; the manual and the puzzles are put back as the two <script
# type="text/plain"> blocks the app reads them from, so once the pack is in
# nothing in the app knows the difference.
#
# terser: `npx --yes terser@5` (node is needed; the first run downloads it).
import io, os, re, json, base64, subprocess, sys, shutil, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toontalk-3d.html')
OUT = os.path.join(HERE, 'toontalk-3d.chat.html')
PACK = os.path.join(HERE, 'toontalk-3d-pack.json')
MODELS = ['robot_v4.glb', 'dusty_v11.glb', 'mimi_v1.glb']
THREE_VERSION = '0.185.0'
PACK_FORMAT = 'toontalk-3d-pack-2'
PACK_URL = 'https://toontalk.github.io/toontalk-3d/toontalk-3d-pack.json'
# ...and gzipped beside it: a click on a .gz DOWNLOADS where a .json opens as
# a page of text the reader then has to save (Ken's chat session, 20 Sep).
# The builder writes both; commit both.

s = io.open(SRC, encoding='utf-8').read()


def block(id_):
    """A <script type="text/plain" id=...> block: (whole tag, its text, its attributes)."""
    m = re.search(r'<script type="text/plain" id="%s"([^>]*)>(.*?)</script>(<!-- /%s -->)?' % (id_, id_), s, re.S)
    assert m, id_ + ' block not found'
    return m.group(0), m.group(2), m.group(1)


# ---------------------------------------------------------------- the pack
pack = {'format': PACK_FORMAT, 'three': THREE_VERSION, 'models': {}}
for name in MODELS:
    raw = io.open(os.path.join(HERE, name), 'rb').read()
    pack['models'][name] = base64.b64encode(raw).decode('ascii')
    print('  packed %s (%d KB)' % (name, len(raw) // 1024))
manual_tag, manual_text, _ = block('martyManual')
puzzles_tag, puzzles_text, puzzles_attrs = block('puzzleSet')
pack['manual'] = manual_text.strip()
pack['puzzles'] = puzzles_text.strip()
pack['puzzlesGzip'] = 'data-gzip' in puzzles_attrs
print('  packed the manual (%d KB) and the puzzle set (%d KB)' % (len(pack['manual']) // 1024, len(pack['puzzles']) // 1024))
io.open(PACK, 'w', encoding='utf-8').write(json.dumps(pack))
print('wrote %s (%.1f MB)' % (os.path.basename(PACK), os.path.getsize(PACK) / 1048576))
import gzip
with gzip.GzipFile(PACK + '.gz', 'wb', compresslevel=9, mtime=0) as gz:   # mtime 0: the same bytes for the same pack
    gz.write(io.open(PACK, 'rb').read())
print('wrote %s (%d KB)' % (os.path.basename(PACK) + '.gz', os.path.getsize(PACK + '.gz') // 1024))

# ---------------------------------------------------------------- the shell
# 1. the data blocks come out (the pack puts them back)
s = s.replace(manual_tag, '<!-- martyManual: in the pack -->')
s = s.replace(puzzles_tag, '<!-- puzzleSet: in the pack -->')

# 2. three.js from a host the chat frame allows
old_map = '"three": "https://unpkg.com/three@%s/build/three.module.js",' % THREE_VERSION
assert s.count(old_map) == 1, 'importmap not found'
s = s.replace(old_map, '"three": "https://cdn.jsdelivr.net/npm/three@%s/build/three.module.js",' % THREE_VERSION)
old_addons = '"three/addons/": "https://unpkg.com/three@%s/examples/jsm/"' % THREE_VERSION
assert s.count(old_addons) == 1, 'addons path not found'
s = s.replace(old_addons, '"three/addons/": "https://cdn.jsdelivr.net/npm/three@%s/examples/jsm/"' % THREE_VERSION)

# 3. the module holds until the pack is in, and is minified
mod_head = "<script type=\"module\">\nimport * as THREE from 'three';"
assert s.count(mod_head) == 1, 'module head not found'
m = re.search(r'<script type="module">\n(import \* as THREE from \'three\';.*?)</script>', s, re.S)
assert m, 'module not found'
module_src = m.group(1).replace(
    "import * as THREE from 'three';",
    "import * as THREE from 'three';\n"
    "// nothing here can run until the reader has handed over the pack\n"
    "await window.__TT_PACK_READY;", 1)


def minify(src):
    tmp = tempfile.mkdtemp()
    inp, outp = os.path.join(tmp, 'app.mjs'), os.path.join(tmp, 'app.min.mjs')
    io.open(inp, 'w', encoding='utf-8').write(src)
    terser = shutil.which('terser') or os.path.join(HERE, 'node_modules', '.bin', 'terser' + ('.cmd' if os.name == 'nt' else ''))
    cmd = [terser] if os.path.exists(terser) else ['npx', '--yes', 'terser@5']
    if os.name == 'nt' and cmd[0] == 'npx':
        cmd[0] = 'npx.cmd'
    r = subprocess.run(cmd + [inp, '--module', '--compress', '--mangle', '--comments', 'false', '-o', outp],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('terser failed:\n' + r.stderr)
    out = io.open(outp, encoding='utf-8').read()
    shutil.rmtree(tmp, ignore_errors=True)
    return out


print('minifying the module (%d KB)...' % (len(module_src.encode('utf-8')) // 1024))
module_min = minify(module_src)
print('  -> %d KB' % (len(module_min.encode('utf-8')) // 1024))
s = s[:m.start(1)] + module_min + '\n' + s[m.end(1):]

LOADER = r'''<script>
// The pack -- the characters' models, Marty's manual, the puzzle set -- is not
// in this file: it would not publish if it were. It is asked for once, kept
// here afterwards, and handed to the app before it starts. Everything below
// runs before the module, which waits on the promise left in
// window.__TT_PACK_READY.
//
// Kept GZIPPED: the pack is over a megabyte of base64 and an artifact's
// storage quota is tight enough to refuse that; compressed it is about half.
// If the browser refuses even so, that is not a failure -- the workshop runs
// perfectly well having to ask again -- but the reader is told, rather than
// left to wonder why it asks every time.
(function () {
  var KEY = 'tt3d.pack.__FORMAT__.gz';
  var PACK_URL = '__PACK_URL__';
  var PACK_GZ_URL = PACK_URL + '.gz';
  var el = document.getElementById('loading');
  var say = function (html) { if (el) el.innerHTML = html; };
  var note = function (m) {
    var e = document.getElementById('ttErr');
    if (e) e.textContent = m;
  };

  var b64 = {
    from: function (bytes) {
      var s = '', CH = 0x8000;                 // apply() dies on a long array
      for (var i = 0; i < bytes.length; i += CH) {
        s += String.fromCharCode.apply(null, bytes.subarray(i, i + CH));
      }
      return btoa(s);
    },
    to: function (str) {
      var bin = atob(str), out = new Uint8Array(bin.length);
      for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
      return out;
    },
  };
  var gzip = function (text) {
    return new Response(new Blob([text]).stream()
      .pipeThrough(new CompressionStream('gzip'))).arrayBuffer();
  };
  var gunzip = function (bytes) {
    return new Response(new Blob([bytes]).stream()
      .pipeThrough(new DecompressionStream('gzip'))).text();
  };

  // the two text blocks the app reads at boot, put back where it looks for them
  var plant = function (id, text, gz) {
    var old = document.getElementById(id);
    if (old) old.remove();
    var sc = document.createElement('script');
    sc.type = 'text/plain'; sc.id = id;
    if (gz) sc.dataset.gzip = '1';
    sc.textContent = text;
    document.head.appendChild(sc);
  };
  function unpack(text) {
    var data = JSON.parse(text);
    if (!data || data.format !== '__FORMAT__' || !data.models) {
      throw new Error('that is not the ToonTalk 3D pack (toontalk-3d-pack.json)');
    }
    window.__TT_MODELS = data.models;
    if (data.manual) plant('martyManual', data.manual, false);
    if (data.puzzles) plant('puzzleSet', data.puzzles, !!data.puzzlesGzip);
    return data;
  }

  window.__TT_PACK_READY = new Promise(function (done) {
    var kept = null;
    try { kept = localStorage.getItem(KEY); } catch (e) {}

    var fresh = function () {
      say(
        '<div style="max-width:30rem;margin:0 auto;text-align:center;line-height:1.55">'
        + '<div style="font-size:15px;color:#e6ecf7;margin-bottom:10px">'
        + 'ToonTalk 3D needs its pack</div>'
        + '<div style="margin-bottom:14px">Robby, Dusty and Mimi’s 3D models, Marty’s '
        + 'manual and the puzzles are about a megabyte — more than an artifact may '
        + 'carry. Hand them over once and this browser will remember them.</div>'
        + '<div style="margin-bottom:14px">Save <a href="' + PACK_GZ_URL + '" '
        + 'download="toontalk-3d-pack.json.gz" style="color:#7fd3c6">'
        + 'toontalk-3d-pack.json.gz</a> (a click downloads it) and drop the saved '
        + 'file anywhere on this page, or</div>'
        + '<button id="ttPick" style="font:inherit;font-size:13px;color:#eafff0;'
        + 'background:#2f6b43;border:none;border-radius:8px;padding:8px 16px;'
        + 'cursor:pointer">Choose the file…</button>'
        + '<div id="ttErr" style="margin-top:12px;color:#f0b429;min-height:1.2em">'
        + '</div>'
        + '<div style="margin-top:18px;font-size:12px;color:#8b93a1">It comes '
        + 'with the source, at<br>' + PACK_URL + '</div>'
        + '</div>');
    };

    var accept = function (text) {
      unpack(text);                                   // throws if it is wrong
      say('Loading…');
      done();
      // the keep happens after the app has what it needs, so a refusal here
      // delays nothing
      gzip(text)
        .then(function (buf) {
          localStorage.setItem(KEY, b64.from(new Uint8Array(buf)));
        })
        .catch(function (e) {
          console.warn('the pack was not kept in this browser:', e && e.message);
        });
    };
    window.__ttAcceptPack = accept;                   // for a test harness, which cannot drop a file

    if (kept) {
      gunzip(b64.to(kept))
        .then(function (text) { unpack(text); say('Loading…'); done(); })
        .catch(function () {
          try { localStorage.removeItem(KEY); } catch (e) {}
          fresh();
        });
      return;
    }
    // FETCH IT FIRST, and ask only if that fails: a page served from the site
    // (or a chat preview) gets the pack with no gesture at all. A published
    // artifact's policy refuses the fetch (connect-src 'self' and the font
    // hosts), and there the drop screen is what a reader sees.
    say('Fetching the pack…');
    var fetched = null;
    try { fetched = fetch(PACK_URL, { cache: 'force-cache' }); } catch (e) {}
    Promise.resolve(fetched)
      .then(function (r) { if (!r || !r.ok) throw new Error('no pack at ' + PACK_URL); return r.text(); })
      .then(accept)
      .catch(function () { fresh(); });

    // a dropped file may be the .json or the .gz: the gzip magic says which
    var read = function (file) {
      if (!file) return;
      note('Reading…');
      file.arrayBuffer().then(function (buf) {
        var bytes = new Uint8Array(buf);
        if (bytes.length > 2 && bytes[0] === 0x1f && bytes[1] === 0x8b) return gunzip(bytes);
        return new TextDecoder().decode(bytes);
      }).then(accept).catch(function (e) {
        note(String((e && e.message) || e));
      });
    };

    // A dynamically created, never-attached input: a static hidden one never
    // opens a picker in the app's own web view.
    document.addEventListener('click', function (ev) {
      if (!ev.target || ev.target.id !== 'ttPick') return;
      var inp = document.createElement('input');
      inp.type = 'file';
      inp.accept = '.json,.gz,application/json,application/gzip';
      inp.onchange = function () { read(inp.files && inp.files[0]); };
      inp.click();
    });
    // Drag and drop is desktop only; the button above is the path everywhere else.
    addEventListener('dragover', function (ev) { ev.preventDefault(); });
    addEventListener('drop', function (ev) {
      ev.preventDefault();
      read(ev.dataTransfer && ev.dataTransfer.files && ev.dataTransfer.files[0]);
    });
  });
})();
</script>
'''.replace('__FORMAT__', PACK_FORMAT).replace('__PACK_URL__', PACK_URL)

# the loader goes immediately before the importmap, so it runs first
anchor = '<script type="importmap">'
assert s.count(anchor) == 1
s = s.replace(anchor, LOADER + anchor)

io.open(OUT, 'w', encoding='utf-8').write(s)
print('wrote %s (%.0f KB)' % (os.path.basename(OUT), os.path.getsize(OUT) / 1024))
print('\nUpload the .html to claude.ai and ask Claude to copy it into an artifact,')
print('PUBLISHED WITH capabilities: { sample: {}, downloads: true } -- sample is the')
print('keyless Marty there (the viewer\'s own Claude, with their consent), downloads')
print('is Save. A published artifact cannot fetch the pack, so the reader drops')
print('toontalk-3d-pack.json.gz on it the first time; served from the site the')
print('page fetches it itself. Commit both pack files.')
