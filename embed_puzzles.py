# Puts the puzzle set inside toontalk-3d.html, where the Puzzle Game button
# can find it without fetching anything -- which is what a single-file build
# (a Claude artifact, say) has to live with. Every examples/puzzles/*.world.json
# goes in, by name.
#
#   python embed_puzzles.py
#
# Run it whenever examples/puzzles/*.world.json change (after make_puzzles.py).
# The block sits between the two markers below; the page reads it at boot and
# remembers every world in it by name. When a server is reachable the app can
# also fetch the files, so edits show up without re-embedding while working.
import io, os, json, gzip, base64

HERE = os.path.dirname(os.path.abspath(__file__))
# GZIP AND BASE64, not plain JSON: the chat-artifact build lives under a size
# cap it was already near, and the set is mostly repeated structure -- it
# packs to a fraction. The page inflates it at boot with DecompressionStream.
START = '<script type="text/plain" id="puzzleSet" data-gzip="1">'
END = '</script><!-- /puzzleSet -->'
AFTER = '</script><!-- /martyManual -->'


def main():
    page = os.path.join(HERE, 'toontalk-3d.html')
    html = io.open(page, encoding='utf-8').read()
    # EVERY puzzle file, by name -- one block, { worlds: { p1: ..., p2: ... } }.
    # Ken: stop bundling the later puzzles inside each earlier one; a file is
    # one puzzle, and the page carries the set.
    folder = os.path.join(HERE, 'examples', 'puzzles')
    worlds = {}
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith('.world.json'):
            continue
        w = json.load(io.open(os.path.join(folder, fn), encoding='utf-8'))
        w.pop('library', None)
        worlds[w.get('name') or fn[:-len('.world.json')]] = w
    rec = {'worlds': worlds}
    # compact, and safe inside a script element
    raw = json.dumps(rec, separators=(',', ':')).encode('utf-8')
    body = base64.b64encode(gzip.compress(raw, 9)).decode('ascii')
    block = START + body + END
    if START in html:
        a = html.index(START)
        b = html.index(END, a) + len(END)
        html = html[:a] + block + html[b:]
    else:
        assert AFTER in html, 'the manual block is the anchor'
        html = html.replace(AFTER, AFTER + '\n' + block, 1)
    io.open(page, 'w', encoding='utf-8', newline='').write(html)
    names = list(worlds.keys())
    print('embedded the puzzle set (%d bytes of JSON -> %d of base64 gzip): %s'
          % (len(raw), len(body), ', '.join(names)))


if __name__ == '__main__':
    main()
