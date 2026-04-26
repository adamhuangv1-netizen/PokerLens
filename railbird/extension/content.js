const WS_URL = 'ws://localhost:9234';

const SUIT = { clubs: 'c', diamonds: 'd', hearts: 'h', spades: 's' };
const RANK = {
  '10': 'T', 'A': 'A', 'K': 'K', 'Q': 'Q', 'J': 'J',
  '2': '2', '3': '3', '4': '4', '5': '5',
  '6': '6', '7': '7', '8': '8', '9': '9',
};

function parseCard(el) {
  const s = el.className.match(/\b(clubs|diamonds|hearts|spades)\b/);
  const r = el.className.match(/\bval-(\w+)\b/);
  return (s && r && RANK[r[1]]) ? RANK[r[1]] + SUIT[s[1]] : null;
}

function getState() {
  const heroEl = document.querySelector('.is-this-player');
  const hero = heroEl
    ? [...heroEl.querySelectorAll('.card')]
        .filter(c => c.dataset.faceUp === 'true')
        .map(parseCard).filter(Boolean)
    : [];

  const community = [...document.querySelectorAll('.card')]
    .filter(c => c.dataset.faceUp === 'true' && !c.closest('.player'))
    .map(parseCard).filter(Boolean);

  const activeOpp = [...document.querySelectorAll('.player')]
    .filter(p => !p.classList.contains('is-this-player')
              && p.classList.contains('playing')
              && !p.classList.contains('folded')).length;

  const callBtn = [...document.querySelectorAll('.btn')]
    .find(b => b.innerText?.includes('CALL') && !b.innerText?.includes('FOLD'));
  const callText = callBtn?.innerText?.match(/\$([\d,]+)/)?.[1]?.replace(',', '');

  const potEl = document.querySelector('[class*="pot"]');
  const potText = potEl?.innerText?.trim()?.match(/\$([\d,]+)/)?.[1]?.replace(',', '');

  return {
    hero,
    community,
    activeOpp,
    toCall: callText ? parseFloat(callText) : null,
    pot: potText ? parseFloat(potText) : null,
  };
}

// --- WebSocket with auto-reconnect ---
let ws = null;

function connect() {
  ws = new WebSocket(WS_URL);

  ws.onopen = () => console.log('[PokerLens] connected');

  ws.onclose = () => {
    ws = null;
    setTimeout(connect, 3000);
  };

  ws.onerror = () => ws?.close();
}

function poll() {
  if (ws?.readyState === WebSocket.OPEN) {
    try { ws.send(JSON.stringify(getState())); } catch (_) {}
  }
}

connect();
setInterval(poll, 200);
