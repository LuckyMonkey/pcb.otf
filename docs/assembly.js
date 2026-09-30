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

  let view = scene.default_view || 'isometric';
  let selected = null;
  const groups = [...new Set(scene.layers.map((layer) => layer.group))];
  const visibleGroups = new Set(groups);
  const prefix = document.body.dataset.pcbAssetPrefix || '';
  const byInstance = new Map(scene.layers.map((layer) => [layer.instance, layer]));
  stage.style.aspectRatio = `${scene.viewBox[0]} / ${scene.viewBox[1]}`;

  const sceneRoot = document.createElement('div');
  sceneRoot.className = 'assembly-scene';
  const plane = document.createElement('div');
  plane.className = 'assembly-plane';
  const traces = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  traces.classList.add('assembly-traces');
  traces.setAttribute('aria-hidden', 'true');
  sceneRoot.append(plane);
  stage.replaceChildren(sceneRoot);

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
    const viewName = view === 'isometric' ? 'technical_iso_svg' : `technical_${view}_svg`;
    return `${prefix}${record[viewName] || record.color_svg}`;
  }

  function positionOf(layer, isExploded) {
    const dx = isExploded ? layer.explode[0] : 0;
    const dy = isExploded ? layer.explode[1] : 0;
    return { x: layer.x + dx, y: layer.y + dy, cx: layer.x + dx + layer.width / 2, cy: layer.y + dy + layer.height / 2 };
  }

  function renderConnections(isExploded) {
    traces.setAttribute('viewBox', `0 0 ${scene.viewBox[0]} ${scene.viewBox[1]}`);
    traces.innerHTML = (scene.connections || []).map((connection) => {
      const fromLayer = byInstance.get(connection.from);
      const toLayer = byInstance.get(connection.to);
      if (!fromLayer || !toLayer) return '';
      const from = positionOf(fromLayer, isExploded);
      const to = positionOf(toLayer, isExploded);
      const elbow = from.cx + (to.cx - from.cx) * 0.52;
      const color = connection.kind === 'power' ? '#c77645' : connection.kind === 'cooling' ? '#5b83a0' : '#7b9a8c';
      return `<path class="assembly-trace ${connection.kind || 'signal'}" d="M ${from.cx} ${from.cy} L ${elbow} ${from.cy} L ${elbow} ${to.cy} L ${to.cx} ${to.cy}" stroke="${color}"/><circle cx="${from.cx}" cy="${from.cy}" r="9" stroke="${color}"/><circle cx="${to.cx}" cy="${to.cy}" r="9" stroke="${color}"/><text x="${elbow + 10}" y="${(from.cy + to.cy) / 2 - 8}" fill="${color}">${connection.label || connection.id}</text>`;
    }).join('');
    plane.append(traces);
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
    const isExploded = explode.checked;
    stage.classList.toggle('isometric', view === 'isometric');
    stage.classList.toggle('front-view', view === 'front');
    stage.classList.toggle('side-view', view === 'side');
    plane.dataset.view = view;
    plane.replaceChildren();
    renderConnections(isExploded);
    const factor = Number(opacity.value || 78) / 100;
    [...scene.layers].sort((a, b) => a.z - b.z).forEach((layer) => {
      if (!visibleGroups.has(layer.group)) return;
      const record = byId.get(layer.object);
      if (!record) return;
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'assembly-layer'; button.dataset.instance = layer.instance;
      const position = positionOf(layer, isExploded);
      button.style.left = `${(position.x / scene.viewBox[0]) * 100}%`;
      button.style.top = `${(position.y / scene.viewBox[1]) * 100}%`;
      button.style.width = `${(layer.width / scene.viewBox[0]) * 100}%`;
      button.style.height = `${(layer.height / scene.viewBox[1]) * 100}%`;
      button.style.zIndex = layer.z;
      button.style.opacity = Math.max(0.12, layer.opacity * factor);
      button.style.transform = `translateZ(${(isExploded ? layer.z * 12 : layer.z * 3)}px)`;
      button.setAttribute('aria-label', `${record.label}, ${layer.instance}, ${view} view`);
      const image = document.createElement('img'); image.src = assetFor(record); image.alt = '';
      button.append(image);
      button.addEventListener('click', () => selectLayer(layer, record, button));
      plane.append(button);
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
