(function () {
  const scene = (window.PCB_ASSEMBLIES || [])[0];
  const registry = window.PCB_REGISTRY || [];
  const relations = window.PCB_RELATIONS || [];
  const byId = new Map(registry.map((item) => [item.id, item]));
  const stage = document.querySelector('#assembly-stage');
  const inspector = document.querySelector('#assembly-inspector');
  const opacity = document.querySelector('#assembly-opacity');
  const explode = document.querySelector('#assembly-explode');
  const groupBar = document.querySelector('#assembly-groups');
  if (!scene || !stage || !inspector) return;

  let view = scene.default_view || 'top';
  let selected = null;
  const groups = [...new Set(scene.layers.map((layer) => layer.group))];
  const visibleGroups = new Set(groups);
  const prefix = document.body.dataset.pcbAssetPrefix || '';
  stage.style.aspectRatio = `${scene.viewBox[0]} / ${scene.viewBox[1]}`;

  groupBar.replaceChildren(...groups.map((group) => {
    const label = document.createElement('label');
    label.innerHTML = `<input type="checkbox" checked data-assembly-group="${group}"> ${group.toUpperCase()}`;
    label.querySelector('input').addEventListener('change', (event) => {
      event.target.checked ? visibleGroups.add(group) : visibleGroups.delete(group);
      render();
    });
    return label;
  }));

  function assetFor(record) {
    const viewName = view === 'isometric' ? 'isometric' : view;
    return `${prefix}glyphs/technical/${viewName}/${record.glyph_base}.svg`;
  }

  function selectLayer(layer, record, element) {
    selected = layer.instance;
    stage.querySelectorAll('.assembly-layer').forEach((node) => node.classList.toggle('selected', node === element));
    const edgeText = relations.filter((edge) => edge.from === record.id || edge.to === record.id).slice(0, 5).map((edge) => `${edge.relation}: ${edge.from === record.id ? edge.to : edge.from}`).join(' · ');
    inspector.innerHTML = '';
    const eyebrow = document.createElement('p'); eyebrow.className = 'eyebrow'; eyebrow.textContent = 'OBJECT INSPECTOR'; inspector.append(eyebrow);
    const heading = document.createElement('h3'); heading.textContent = record.label; inspector.append(heading);
    const description = document.createElement('p'); description.textContent = `${layer.instance} · ${record.category}`; inspector.append(description);
    const id = document.createElement('code'); id.textContent = record.id; inspector.append(id);
    const shortcode = document.createElement('code'); shortcode.textContent = `${record.codepoint} · ${record.shortcode}`; inspector.append(shortcode);
    const details = document.createElement('dl');
    for (const [term, value] of [['View', view], ['Attributes', Object.entries(record.attributes || {}).map(([key, item]) => `${key}: ${item}`).join(' · ')], ['Relations', edgeText || 'No explicit edges']]) {
      const dt = document.createElement('dt'); dt.textContent = term; const dd = document.createElement('dd'); dd.textContent = value; details.append(dt, dd);
    }
    inspector.append(details);
  }

  function render() {
    stage.classList.toggle('isometric', view === 'isometric');
    stage.replaceChildren();
    const factor = Number(opacity.value || 78) / 100;
    const isExploded = explode.checked;
    [...scene.layers].sort((a, b) => a.z - b.z).forEach((layer) => {
      if (!visibleGroups.has(layer.group)) return;
      const record = byId.get(layer.object);
      if (!record) return;
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'assembly-layer'; button.dataset.instance = layer.instance;
      const dx = isExploded ? layer.explode[0] : 0; const dy = isExploded ? layer.explode[1] : 0;
      button.style.left = `${((layer.x + dx) / scene.viewBox[0]) * 100}%`;
      button.style.top = `${((layer.y + dy) / scene.viewBox[1]) * 100}%`;
      button.style.width = `${(layer.width / scene.viewBox[0]) * 100}%`;
      button.style.height = `${(layer.height / scene.viewBox[1]) * 100}%`;
      button.style.zIndex = layer.z;
      button.style.opacity = Math.max(0.12, layer.opacity * factor);
      button.setAttribute('aria-label', `${record.label}, ${layer.instance}`);
      const image = document.createElement('img'); image.src = assetFor(record); image.alt = '';
      button.append(image);
      button.addEventListener('click', () => selectLayer(layer, record, button));
      stage.append(button);
      if (selected === layer.instance) button.classList.add('selected');
    });
  }

  document.querySelectorAll('[data-assembly-view]').forEach((button) => button.addEventListener('click', () => {
    view = button.dataset.assemblyView;
    document.querySelectorAll('[data-assembly-view]').forEach((candidate) => candidate.classList.toggle('active', candidate === button));
    render();
  }));
  opacity.addEventListener('input', render); explode.addEventListener('change', render); render();
}());
