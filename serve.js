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
      const m = /^data:image\/(png|jpeg);base64,/.exec(body);
      if (!m) throw new Error('expected a data:image/png|jpeg;base64 URL');
      const ext = m[1] === 'jpeg' ? '.jpg' : '.png';
      const safe = (url.searchParams.get('name') || 'frame').replace(/[^\w.-]/g, '_');
      fs.mkdirSync(CAPTURES, { recursive: true });
      const out = path.join(CAPTURES, safe + ext);
      fs.writeFileSync(out, Buffer.from(body.slice(m[0].length), 'base64'));
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
  const file = path.join(ROOT, rel);
  if (!file.startsWith(ROOT)) {           // no climbing out of the served dir
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
