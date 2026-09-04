// Static file server for the tt3d demo, plus a capture sink.
//
// POST /capture?name=foo with a data: URL as the body writes
// captures/foo.<ext> — that lets the page hand rendered frames back to disk so
// they can be inspected without a visible browser window.
//
//   node serve.js [port]

const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const CAPTURES = path.join(ROOT, 'captures');
const PORT = Number(process.argv[2]) || 8311;

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json',
  '.glb': 'model/gltf-binary',
  '.gltf': 'model/gltf+json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.css': 'text/css; charset=utf-8',
};

function readBody(req) {
  return new Promise((resolve, reject) => {
    let n = 0;
    const chunks = [];
    req.on('data', (c) => {
      n += c.length;
      if (n > 64 * 1024 * 1024) { reject(new Error('body too large')); req.destroy(); return; }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  if (req.method === 'POST' && url.pathname === '/capture') {
    try {
      const body = await readBody(req);
      const safe = (url.searchParams.get('name') || 'frame').replace(/[^\w.-]/g, '_');
      fs.mkdirSync(CAPTURES, { recursive: true });
      let out;
      const m = /^data:image\/(png|jpeg);base64,/.exec(body);
      if (m) {
        out = path.join(CAPTURES, safe + (m[1] === 'jpeg' ? '.jpg' : '.png'));
        fs.writeFileSync(out, Buffer.from(body.slice(m[0].length), 'base64'));
      } else {
        // a JSON body: how the regression runner's make-goldens mode hands
        // its dumps back (JSON.parse is the validation)
        JSON.parse(body);
        out = path.join(CAPTURES, safe + '.json');
        fs.writeFileSync(out, body);
      }
      console.log('captured', out);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, file: out }));
    } catch (e) {
      console.error('capture failed:', e.message);
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // static
  const rel = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname);
  const file = path.resolve(ROOT, '.' + rel);
  // INSIDE THE SERVED DIRECTORY, by relation rather than by prefix: a prefix
  // test let a neighbouring directory whose name merely begins with this
  // one's ("tt3d-private") pass (a reviewer's finding)
  const inside = path.relative(ROOT, file);
  if (!inside || inside.startsWith('..') || path.isAbsolute(inside)) {
    res.writeHead(403).end('forbidden');
    return;
  }
  fs.readFile(file, (err, buf) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain' }).end('not found: ' + rel);
      return;
    }
    res.writeHead(200, {
      'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-store',
    });
    res.end(buf);
  });
});

server.listen(PORT, () => console.log(`tt3d serving ${ROOT} on http://localhost:${PORT}`));
