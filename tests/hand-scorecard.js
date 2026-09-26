// THE HAND-BY-WORDS SCORECARD, for any brain -- a key's, Nano, a model in this
// browser. Open toontalk-3d-next.html, choose the brain under "How Marty
// thinks" (and load it, for a model in this browser), tick "Move my hand by
// words", then in the browser's console:
//
//   await import('./tests/hand-scorecard.js'); const r = await __score('ABCDEFH'); console.log(r.rows.join('\n')); r
//
// Each section starts from an empty table (a fresh world; the brain stays
// loaded). A sentence passes only if the WORKSHOP ends up right -- what is on
// the table, the desk, Mimi's platform and in the hand -- whatever the brain
// said about it. Sections: A fresh things, B "a"/"the", C Mimi and Dusty,
// D robots, E inside a bubble, F refusals, H names/yard/the thought.
window.__score = async (sections = 'ABCDEFH', log = []) => {
  const D = window.__nano;
  const B = () => { const o = []; for (let i = 0; i < 80; i++) { const t = D.bench(i); if (!t) break; o.push(t); } return o; };
  const v = (t) => t?.userData?.kind === 'number' ? String(t.userData.value.n) + (t.userData.value.d !== 1n ? '/' + t.userData.value.d : '') : null;
  const held = () => window.__handHeld();
  const mode = () => D.sched().mode;
  const desk = () => D.stations.stand?.occupant ?? null;
  const plat = () => D.stations.copyIn?.occupant ?? null;
  const kind = (k) => B().filter(t => t.userData.kind === k);
  const nums = () => B().filter(t => t.userData.kind === 'number').map(v);
  const holes = (t) => (t?.userData?.holes || []).map(h => h.thing ? (v(h.thing) ?? h.thing.userData.kind) : '-');
  const spots = () => Object.values(D.stations).filter(st => /^s\d+$/.test(st?.id || '') && st.occupant).map(st => st.occupant);
  const wait = (ms) => new Promise(r => setTimeout(r, ms));
  const fresh = async (bench = []) => { D.worldIn({ kind: 'world', v: 4, stations: {}, active: null, bench }); await wait(1200); D.showStacks(true); };
  const settleRun = async () => { for (let i = 0; i < 120 && mode() === 'replay'; i++) await wait(250); };
  const S = {
    A: { setup: () => fresh(), rows: [
      ['A1', 'put a box on the table', () => kind('box').length === 1 && holes(kind('box')[0]).length === 2],
      ['A2', 'pick up a 1 and put it in a 3-hole box', () => kind('box').some(b => holes(b).join() === '1,-,-') && kind('box').some(b => holes(b).length === 2)],
      ['A3', 'create a text pad with ToonTalk on it', () => kind('text').some(t => t.userData.text === 'ToonTalk')],
      ['A4', 'make a 12', () => nums().includes('12')],
      ['A5', 'put a -5 on the table', () => nums().includes('-5')],
      ['A6', 'give a robot a scale with 1 and 100 on it', () => desk()?.userData.kind === 'scale' && holes(desk()).join() === '1,100' && mode() === 'training'],
      ['A7', 'leave', () => mode() === 'world' && desk()?.userData.kind === 'scale'],
    ] },
    B: { setup: () => fresh([{ x: 0, z: 1.7, thing: { kind: 'box', holes: [null, null] } }]), rows: [
      ['B1', 'put a 1 in the box', () => kind('box').length === 1 && holes(kind('box')[0]).join() === '1,-'],
      ['B2', 'put a 3 in the box', () => kind('box').length === 1 && holes(kind('box')[0]).join() === '1,3'],
      ['B3', 'pick up the box and put it down again', () => kind('box').length === 1 && holes(kind('box')[0]).join() === '1,3' && !held()],
      ['B4', 'put the 3 on the 1', () => holes(kind('box')[0]).join() === '4,-'],
      ['B5', 'take a 1 and add it to the 4', () => holes(kind('box')[0]).join() === '5,-'],
    ] },
    C: { setup: () => fresh(), rows: [
      ['C1', 'make a 7', () => nums().includes('7')],
      ['C2', 'copy the 7', () => v(plat()) === '7' && (nums().includes('7') || v(held()) === '7')],
      ['C3', 'take the original back', () => !plat() && [...nums(), v(held())].filter(x => x === '7').length === 2],
      ['C4', 'vacuum one of the 7s', () => [...nums(), v(held())].filter(x => x === '7').length === 1],
      ['C5', 'give the 7 to Mimi', () => v(plat()) === '7' && [...nums(), v(held())].filter(x => x === '7').length === 1],
    ] },
    D: { setup: () => fresh(), rows: [
      ['D1', 'put a robot on the table', () => kind('robot').length === 1],
      ['D2', 'give it a 1', () => mode() === 'training' && v(desk()) === '1'],
      ['D3', 'add a 1 to the number on the desk', () => mode() === 'training' && v(desk()) === '2'],
      ['D4', 'leave', () => mode() === 'world' && v(desk()) === '1'],
      ['D5', 'run the robot', async () => { await settleRun(); return v(desk()) === '2'; }],
    ] },
    E: { setup: async () => { await fresh(); await D.hand('put a robot on the table'); await D.hand('give it a 1'); }, rows: [
      ['E1', 'copy it', () => v(plat()) === '1' && (spots().some(t => v(t) === '1') || v(held()) === '1')],
      ['E2', 'put a 2 in a box', () => spots().some(t => t.userData.kind === 'box' && holes(t).includes('2'))],
      ['E3', 'take a robot', (r) => !r.ok && mode() === 'training'],
      ['E4', 'leave', () => mode() === 'world'],
    ] },
    F: { setup: () => fresh(), rows: [
      ['F1', 'drop it on the table', (r) => !r.ok && B().length === 0],
      ['F2', 'put a 1 in the box', (r) => (!r.ok && B().length === 0) || kind('box').some(b => holes(b).includes('1'))],
      ['F3', 'vacuum the robot', (r) => !r.ok],
      ['F4', 'what is a nest?', () => B().filter(t => t.userData.kind !== 'box' && t.userData.kind !== 'number').length === 0 && !held()],
      ['F5', 'put a bird on the table', async () => { for (let i = 0; i < 20 && !kind('bird').length; i++) await wait(300); return kind('nest').length >= 1 && kind('bird').length >= 1; }],   // the egg hatches a moment later
    ] },
    H: { setup: () => fresh(), rows: [
      ['H1', 'take a nest and call it orders', () => held()?.userData.kind === 'nest' && held()?.userData.label === 'orders'],
      ['H4', 'go out to the yard', (r) => r.ok],
      ['H5', 'come back in', (r) => r.ok],
      ['H6', 'put a robot on the table and give it a 3', () => mode() === 'training' && v(desk()) === '3'],
      ['H7', 'erase the 3 so it works for any number', (r) => r.ok],
      ['H7b', 'add a 1 to the 3 on the desk', () => v(desk()) === '4'],
      ['H8', 'leave', () => mode() === 'world'],
    ] },
  };
  const out = { rows: [], ok: 0, n: 0, ms: [] };
  for (const sec of sections) {
    const s = S[sec]; if (!s) continue;
    await s.setup();
    for (const [id, said, check] of s.rows) {
      const t0 = performance.now();
      let r;
      try { r = await D.hand(said); } catch (e) { r = { ok: false, say: 'threw ' + e }; }
      await wait(600);
      const ms = Math.round(performance.now() - t0);
      let pass = false;
      try { pass = !!(await check(r)); } catch (e) { pass = false; }
      out.n++; if (pass) out.ok++; out.ms.push(ms);
      const brain = window.__localLast?.ms;
      const plan = window.__handLastPlan?.said === said ? String(window.__handLastPlan.raw).replace(/\s+/g, ' ') : '';
      const line = (pass ? 'OK  ' : 'BAD ') + id + ' ' + said + ' -> ' + (r.ok ? '✓ ' : '✗ ') + String(r.say || '').slice(0, 140) + ' [' + ms + ' ms' + (brain ? ', brain ' + brain : '') + ']'
        + (pass ? '' : ' || PLAN ' + plan.slice(0, 400));
      window.__localLast = null;
      out.rows.push(line); log.push(line);
    }
  }
  out.ms.sort((a, b) => a - b);
  out.median = out.ms[Math.floor(out.ms.length / 2)];
  delete out.ms;
  return out;
};
