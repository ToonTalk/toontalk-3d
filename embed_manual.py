# Puts a plain-text copy of the manual inside toontalk-3d.html, where Marty can
# read it. He prefers a live fetch of manual.html when one is reachable -- so
# edits show up at once while working -- and falls back to this copy, which is
# what a single-file build (a Claude artifact, say) has.
#
#   python embed_manual.py
#
# Run it whenever manual.html changes. The block sits between the two markers
# below and is inert to the browser (type="text/plain").
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
START = '<script type="text/plain" id="martyManual">'
END = '</script><!-- /martyManual -->'


def manual_text(html):
    """The manual as prose: headings kept, markup and furniture dropped."""
    s = html
    s = re.sub(r'<head>.*?</head>', '', s, flags=re.S | re.I)
    s = re.sub(r'<style.*?</style>', '', s, flags=re.S | re.I)
    s = re.sub(r'<script.*?</script>', '', s, flags=re.S | re.I)
    s = re.sub(r'<nav.*?</nav>', '', s, flags=re.S | re.I)
    s = re.sub(r'<footer.*?</footer>', '', s, flags=re.S | re.I)
    s = re.sub(r'<iframe.*?</iframe>', '', s, flags=re.S | re.I)
    # headings become their own lines, so the sections stay findable
    s = re.sub(r'<h([12])[^>]*>', r'\n\n## ', s, flags=re.I)
    s = re.sub(r'</h[12]>', '\n', s, flags=re.I)
    s = re.sub(r'<li[^>]*>', '\n - ', s, flags=re.I)
    s = re.sub(r'</p>|</div>|<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    # entities the manual actually uses
    for a, b in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&mdash;', '—'),
                 ('&ndash;', '–'), ('&frac12;', '1/2'), ('&times;', '×'),
                 ('&minus;', '−'), ('&nbsp;', ' '), ('&quot;', '"'), ('&#39;', "'"),
                 ('&rarr;', '->'), ('&larr;', '<-'), ('&hellip;', '…'),
                 ('&copy;', '(c)'), ('&sup2;', '^2')]:
        s = s.replace(a, b)
    s = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), s)
    s = re.sub(r'&[a-zA-Z]+;', '', s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r' *\n *', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()


def main():
    manual = io.open(os.path.join(HERE, 'manual.html'), encoding='utf-8').read()
    text = manual_text(manual)
    # a text/plain block cannot contain the closing tag itself
    text = text.replace('</script', '<\\/script')

    app_path = os.path.join(HERE, 'toontalk-3d.html')
    app = io.open(app_path, encoding='utf-8').read()
    block = START + '\n' + text + '\n' + END

    if START in app:
        app = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda _: block, app, flags=re.S)
    else:
        app = app.replace('<div id="loading">', block + '\n<div id="loading">', 1)
    io.open(app_path, 'w', encoding='utf-8').write(app)
    print('embedded %d characters of manual into toontalk-3d.html' % len(text))


if __name__ == '__main__':
    main()
