# Puts the puzzle set inside toontalk-3d.html, where the Puzzle Game button
# can find it without fetching anything -- which is what a single-file build
# (a Claude artifact, say) has to live with. p1 carries every later puzzle in
# its library, so one file is the whole set.
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
    rec = json.load(io.open(os.path.join(HERE, 'examples', 'puzzles', 'p1.world.json'),
                            encoding='utf-8'))
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
    names = ['p1'] + list((rec.get('library') or {}).keys())
    print('embedded the puzzle set (%d bytes of JSON -> %d of base64 gzip): %s'
          % (len(raw), len(body), ', '.join(names)))


if __name__ == '__main__':
    main()
