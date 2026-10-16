document.addEventListener('DOMContentLoaded', async () => {
  if (window.renderMathInElement) {
    renderMathInElement(document.body, {
      delimiters: [{ left: '$$', right: '$$', display: true }],
      throwOnError: false,
    });
  }
  const diagrams = [...document.querySelectorAll('pre.mermaid')];
  if (diagrams.length && window.mermaid) {
    // Disable the automatic pass before waiting for the local font.
    mermaid.initialize({
      startOnLoad: false, securityLevel: 'strict', theme: 'base',
      fontFamily: 'Paper Sans, PingFang SC, sans-serif',
      themeVariables: {
        primaryColor: '#eaf3ee', primaryTextColor: '#173b38', primaryBorderColor: '#9abdaf',
        lineColor: '#7c9b90', secondaryColor: '#f5f1e8', tertiaryColor: '#f8f8f5', fontSize: '16px',
      },
      flowchart: { useMaxWidth: true, htmlLabels: false, nodeSpacing: 24, rankSpacing: 30, padding: 14, curve: 'linear' },
    });
    await document.fonts.ready;
    for (const diagram of diagrams) {
      if (innerWidth < 680) diagram.textContent = diagram.textContent.replace('flowchart LR', 'flowchart TB');
    }
    await mermaid.run({ nodes: diagrams });
  }

  const storageKey = 'opd-paper-read-v1';
  let read = [];
  try {
    const stored = JSON.parse(localStorage.getItem(storageKey) || '[]');
    if (Array.isArray(stored)) read = stored.filter(item => typeof item === 'string').map(item => item.replace(/^\d+-/, ''));
  } catch (_) {}
  const button = document.querySelector('.readbtn');
  if (button) {
    const id = button.dataset.paper;
    const paint = () => {
      const done = read.includes(id);
      button.classList.toggle('done', done);
      button.textContent = done ? '已读 ✓' : '标记为已读';
      button.setAttribute('aria-pressed', String(done));
    };
    paint();
    button.addEventListener('click', () => {
      read = read.includes(id) ? read.filter(item => item !== id) : [...read, id];
      try { localStorage.setItem(storageKey, JSON.stringify(read)); } catch (_) {}
      paint();
    });
  }
  const cards = [...document.querySelectorAll('.card')];
  for (const card of cards) {
    if (read.includes(card.dataset.paper)) card.querySelector('.go').textContent = '已读 ✓ · 再看一遍 →';
  }

  let category = '全部';
  const search = document.querySelector('.search');
  const filterCards = () => {
    const query = (search?.value || '').trim().toLowerCase();
    let visible = 0;
    for (const card of cards) {
      const match = (category === '全部' || category === card.dataset.group) && card.textContent.toLowerCase().includes(query);
      card.hidden = !match;
      if (match) visible += 1;
    }
    const empty = document.querySelector('.noresults');
    if (empty) empty.hidden = visible > 0;
  };
  for (const filter of document.querySelectorAll('.filter')) {
    filter.addEventListener('click', () => {
      category = filter.textContent;
      for (const item of document.querySelectorAll('.filter')) {
        item.classList.toggle('active', item === filter);
        item.setAttribute('aria-pressed', String(item === filter));
      }
      filterCards();
    });
  }
  search?.addEventListener('input', filterCards);
  await document.fonts.ready;
  document.body.dataset.ready = 'true';
});
