(function () {
  const registry = window.PCB_REGISTRY || [];
  const relations = window.PCB_RELATIONS || [];
  const byShortcode = new Map(registry.map((item) => [item.shortcode, item]));
  const search = document.querySelector('#search');
  const cards = document.querySelector('#cards');
  const counts = document.querySelector('#counts');
  const assetPrefix = document.body.dataset.pcbAssetPrefix || '';
  let filter = 'all';
  const categories = [...new Set(registry.map((item) => item.category))].sort();
  document.querySelector('#filters').insertAdjacentHTML('beforeend', categories.map((category) => `<button data-filter="${category}">${category.replaceAll('_', ' ')}</button>`).join(''));

  function copy(value, button) { navigator.clipboard?.writeText(value); const original = button.textContent; button.textContent = 'Copied'; setTimeout(() => { button.textContent = original; }, 900); }
  function searchable(item) { return [item.id, item.label, item.shortcode, item.codepoint, ...item.aliases, ...Object.entries(item.attributes || {}).flat(), ...Object.entries(item.external_ids || {}).flat(), ...item.sources].map(String); }
  function filtered() { const query = (search.value || '').toLowerCase(); return registry.filter((item) => (filter === 'all' || item.category === filter) && searchable(item).some((value) => value.toLowerCase().includes(query))); }
  function relationText(item) { const edges = relations.filter((edge) => edge.from === item.id || edge.to === item.id).slice(0, 3); return edges.map((edge) => `<div><strong>${edge.relation}</strong> ${edge.from === item.id ? edge.to : edge.from}</div>`).join(''); }
  function render() {
    const items = filtered(); counts.textContent = `${items.length} of ${registry.length} objects`;
    cards.replaceChildren(...items.map((item) => {
      const card = document.createElement('article'); card.className = 'card';
      const attrs = Object.entries(item.attributes || {}).slice(0, 3).map(([key, value]) => `${key}: ${value}`).join(' · ');
      card.innerHTML = `<div class="card-views"><div><div class="card-view"><img src="${assetPrefix}${item.color_svg}" alt=""></div><div class="view-label">TOP-DOWN</div></div><div><div class="card-view iso"><img src="${assetPrefix}${item.iso_svg}" alt=""></div><div class="view-label">ISOMETRIC</div></div></div><h3>${item.label}</h3><div class="meta">${item.id}<br>${item.codepoint} · ${item.shortcode}</div><div class="attributes">${attrs}</div><div class="relation-note">${relationText(item)}</div><div class="card-actions"><button data-copy="${item.shortcode}">Copy shortcode</button><button data-copy="${item.char}">Copy character</button></div>`;
      card.querySelectorAll('[data-copy]').forEach((button) => button.addEventListener('click', () => copy(button.dataset.copy, button))); return card;
    }));
  }
  document.querySelectorAll('[data-filter]').forEach((button) => button.addEventListener('click', () => { document.querySelectorAll('[data-filter]').forEach((candidate) => candidate.classList.toggle('active', candidate === button)); filter = button.dataset.filter; render(); }));
  search.addEventListener('input', render);
  const playground = document.querySelector('#playground'); const ligatureOutput = document.querySelector('#ligature-output'); const unicodeOutput = document.querySelector('#unicode-output');
  function shape(value) { return value.replace(/:[a-z0-9_]+:/g, (token) => byShortcode.has(token) ? byShortcode.get(token).char : token); }
  function updatePlayground() { ligatureOutput.textContent = playground.value; unicodeOutput.textContent = shape(playground.value); }
  playground.addEventListener('input', updatePlayground); updatePlayground(); render();
}());
