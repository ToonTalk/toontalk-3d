# Builds toontalk-3d.chat.html -- the workshop as a claude.ai CHAT artifact,
# plus toontalk-3d-models.json, the pack of models it asks the reader for.
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
#                          account -- but the publish size is far tighter.
#
# So this build trades size for a brain. It sheds the two things that make the
# packed build 2.4 MB:
#
#   three.js   fetched from cdn.jsdelivr.net, which the chat frame's own
#              content-security policy allows (unpkg, which the source uses, is
#              NOT on that list -- swapping the importmap is the whole change).
#   the models  ~730 KB of them, handed over by the READER: dropped on the page
#              or chosen from a picker, then kept in this browser so it is asked
#              for once. The technique is Ken's, from Comic Chat.
#
# What is left is about 500 KB, which fits.
#
# The loader is a plain script BEFORE the module, and the module waits on the
# promise it leaves behind -- loadModel already prefers window.__TT_MODELS over
# fetching, so once the pack is in nothing else in the app knows the difference.
import io, os, re, json, base64

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toontalk-3d.html')
OUT = os.path.join(HERE, 'toontalk-3d.chat.html')
PACK = os.path.join(HERE, 'toontalk-3d-models.json')
MODELS = ['robot_v4.glb', 'dusty_v10.glb']
THREE_VERSION = '0.185.0'
PACK_FORMAT = 'toontalk-3d-models-1'

# ---------------------------------------------------------------- the pack
pack = {'format': PACK_FORMAT, 'three': THREE_VERSION, 'models': {}}
for name in MODELS:
    raw = io.open(os.path.join(HERE, name), 'rb').read()
    pack['models'][name] = base64.b64encode(raw).decode('ascii')
    print('  packed %s (%d KB)' % (name, len(raw) // 1024))
io.open(PACK, 'w', encoding='utf-8').write(json.dumps(pack))
print('wrote %s (%.1f MB)' % (os.path.basename(PACK), os.path.getsize(PACK) / 1048576))

# ---------------------------------------------------------------- the shell
s = io.open(SRC, encoding='utf-8').read()

# 1. three.js from a host the chat frame allows
old_map = '"three": "https://unpkg.com/three@%s/build/three.module.js",' % THREE_VERSION
assert s.count(old_map) == 1, 'importmap not found'
s = s.replace(
    old_map,
    '"three": "https://cdn.jsdelivr.net/npm/three@%s/build/three.module.js",' % THREE_VERSION)
old_addons = '"three/addons/": "https://unpkg.com/three@%s/examples/jsm/"' % THREE_VERSION
assert s.count(old_addons) == 1, 'addons path not found'
s = s.replace(
    old_addons,
    '"three/addons/": "https://cdn.jsdelivr.net/npm/three@%s/examples/jsm/"' % THREE_VERSION)

LOADER = r'''<script>
// The models are not in this file -- it would not publish if they were. They
// are asked for once, kept here afterwards, and handed to the app before it
// starts. Everything below runs before the module, which waits on the promise
// left in window.__TT_PACK_READY.
//
// Kept GZIPPED: the pack is 973 KB of base64 and an artifact's storage quota is
// tight enough to refuse that; compressed it is about 412 KB. If the browser
// refuses even so, that is not a failure -- the workshop runs perfectly well
// having to ask again -- but the reader is told, rather than left to wonder
// why it asks every time.
(function () {
  var KEY = 'tt3d.models.__FORMAT__.gz';
  var PACK_URL =
    'https://raw.githubusercontent.com/ToonTalk/toontalk-3d/main/toontalk-3d-models.json';
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

  function unpack(text) {
    var data = JSON.parse(text);
    if (!data || data.format !== '__FORMAT__' || !data.models) {
      throw new Error('that is not the ToonTalk 3D model pack');
    }
    window.__TT_MODELS = data.models;
    return data;
  }

  window.__TT_PACK_READY = new Promise(function (done) {
    var kept = null;
    try { kept = localStorage.getItem(KEY); } catch (e) {}

    var fresh = function () {
      say(
        '<div style="max-width:30rem;margin:0 auto;text-align:center;line-height:1.55">'
        + '<div style="font-size:15px;color:#e6ecf7;margin-bottom:10px">'
        + 'ToonTalk 3D needs its characters</div>'
        + '<div style="margin-bottom:14px">Robby the robot and Dusty the vacuum are '
        + 'about 700&nbsp;KB of 3D models — more than an artifact may carry. '
        + 'Hand them over once and this browser will remember them.</div>'
        + '<div style="margin-bottom:14px">Drop <a href="' + PACK_URL + '" '
        + 'target="_blank" rel="noopener" style="color:#7fd3c6">'
        + 'toontalk-3d-models.json</a> anywhere on this page, or</div>'
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
          console.warn('models not kept in this browser:', e && e.message);
        });
    };

    if (kept) {
      gunzip(b64.to(kept))
        .then(function (text) { unpack(text); say('Loading…'); done(); })
        .catch(function () {
          try { localStorage.removeItem(KEY); } catch (e) {}
          fresh();
        });
      return;
    }
    fresh();

    var read = function (file) {
      if (!file) return;
      note('Reading…');
      file.text().then(accept).catch(function (e) {
        note(String((e && e.message) || e));
      });
    };

    // A dynamically created, never-attached input: a static hidden one never
    // opens a picker in the app's own web view.
    document.addEventListener('click', function (ev) {
      if (!ev.target || ev.target.id !== 'ttPick') return;
      var inp = document.createElement('input');
      inp.type = 'file';
      inp.accept = '.json,application/json';
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
'''.replace('__FORMAT__', PACK_FORMAT)

# the loader goes immediately before the importmap, so it runs first
anchor = '<script type="importmap">'
assert s.count(anchor) == 1
s = s.replace(anchor, LOADER + anchor)

# and the module holds until the pack is in
mod = "<script type=\"module\">\nimport * as THREE from 'three';"
assert s.count(mod) == 1, 'module head not found'
s = s.replace(mod, mod.replace(
    "import * as THREE from 'three';",
    "import * as THREE from 'three';\n"
    "// nothing here can run until the reader has handed over the models\n"
    "await window.__TT_PACK_READY;"))

io.open(OUT, 'w', encoding='utf-8').write(s)
print('wrote %s (%.0f KB)' % (os.path.basename(OUT), os.path.getsize(OUT) / 1024))
print('\nUpload the .html to claude.ai and ask Claude to copy it into an artifact;')
print('the reader drops the .json on it the first time.')
