# -*- coding: utf-8 -*-
"""Extract every script block from a build and parse it. One process, no shell.

    python tests/check_syntax.py [file.html ...]      (default: toontalk-3d.html)

The old two-command version -- extract in a heredoc, then `node --check` on the
next line -- once reported "ok" on a file whose main block had an invalid
unicode escape in it, and the app would not boot at all. A gate that can say ok
when it has not looked is worse than no gate. So: one process does both, prints
the size of what it actually parsed, and fails loudly.

It lived in a session scratchpad for a while, which is its own version of the
same bug -- a gate you cannot run tomorrow. It lives here now.
"""
import io, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The suite is gated too, and by its own marker. A patch that put a real
# newline inside a JS string literal left regress.html unparseable: the page
# loaded, logged nothing, and looked for all the world like an app that would
# not boot -- twenty minutes of watching an empty log.
MARKERS = ['switchScene', 'lookStraightOn', 'processDirtyRooms']
SUITE_MARKERS = ['runOne', 'slowSettle', 'markdownCheck']
targets = sys.argv[1:] or [os.path.join(ROOT, 'toontalk-3d.html'),
                           os.path.join(ROOT, 'tests', 'regress.html')]

bad = False
for path in targets:
    name = os.path.basename(path)
    src = io.open(path, encoding='utf-8').read()
    blocks = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', src, re.S)
    want = SUITE_MARKERS if name == 'regress.html' else MARKERS
    main = next((b for b in blocks if all(m in b for m in want)), None)
    if main is None:
        print('FAIL %s: no script block holds %s' % (name, want))
        bad = True
        continue
    # .mjs, NOT .js. The block is <script type="module">, and node given a .js
    # file parses it as CommonJS, fails on the import, and falls back to a
    # detection pass that reports success without a strict parse -- so an
    # invalid unicode escape sailed through a gate that ran all session.
    tmp = os.path.join(tempfile.gettempdir(), 'tt3d_check.mjs')
    io.open(tmp, 'w', encoding='utf-8').write(main)
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    if r.returncode != 0:
        print('FAIL %s: the main block does not parse' % name)
        print(r.stderr.strip()[:1200])
        bad = True
        continue
    print('ok   %-28s %d chars in the main block, %d script blocks'
          % (name, len(main), len(blocks)))

sys.exit(1 if bad else 0)
