(function () {
  const registry = window.PCB_REGISTRY || [];
  const byId = new Map(registry.map((item) => [item.id, item]));
  const prefix = document.body.dataset.pcbAssetPrefix || '';
  const samples = [
    ['hardware:resistor', 'Resistor / passive component'],
    ['hardware:ceramic_capacitor', 'Ceramic capacitor / passive component'],
    ['hardware:qfp', 'QFP / package outline'],
    ['hardware:bga', 'BGA / package footprint'],
    ['hardware:via', 'Via / plated board feature'],
    ['hardware:cpu', 'CPU / processor package'],
    ['hardware:gpu', 'GPU / expansion card'],
    ['hardware:ddr4_dimm', 'DDR4 DIMM / memory module'],
    ['hardware:pcie_x16_slot', 'PCIe x16 / expansion slot'],
    ['hardware:m2_socket', 'M.2 / socket geometry'],
    ['hardware:nvme_ssd', 'NVMe / storage module'],
    ['hardware:usb_c', 'USB Type-C / connector'],
    ['hardware:atx_24pin', 'ATX 24-pin / power connector']
  ];
  const drawings = [
    ['hardware:atx_motherboard', 'ATX motherboard', 'board / assembly datum'],
    ['hardware:cpu_socket', 'CPU socket', 'package interface / contact field'],
    ['hardware:ddr4_dimm', 'DDR4 DIMM', 'memory module / keyed edge'],
    ['hardware:gpu', 'GPU card', 'expansion board / bracket edge']
  ];

  function record(id) { return byId.get(id); }
  function codepoint(item) { return item.codepoint.replace('U+', ''); }

  function drawingPlate(item, index, note) {
    const figure = document.createElement('figure');
    figure.className = 'patent-plate';
    const head = document.createElement('div');
    head.className = 'patent-plate-head';
    head.innerHTML = `<span>FIG. ${String(index + 1).padStart(2, '0')}</span><code>${item.id}</code>`;
    const views = document.createElement('div');
    views.className = 'patent-plate-views';
    for (const [label, key] of [['TOP', 'technical_top_svg'], ['FRONT', 'technical_front_svg'], ['SIDE', 'technical_side_svg'], ['ISO', 'technical_iso_svg']]) {
      const cell = document.createElement('div');
      cell.className = 'patent-view';
      const image = document.createElement('img');
      image.src = prefix + item[key];
      image.alt = `${item.label}, ${label.toLowerCase()} technical view`;
      cell.append(image);
      const caption = document.createElement('span');
      caption.textContent = label;
      cell.append(caption);
      views.append(cell);
    }
    const caption = document.createElement('figcaption');
    caption.innerHTML = `<strong>${item.label}</strong><span>${note}</span><code>${item.codepoint} · ${item.shortcode}</code>`;
    figure.append(head, views, caption);
    return figure;
  }

  function fontSample(item, label, index) {
    const row = document.createElement('article');
    row.className = 'font-sample-row';
    row.innerHTML = `
      <div class="font-sample-index">${String(index + 1).padStart(2, '0')}</div>
      <div class="font-sample-name"><strong>${label}</strong><code>${item.id}</code></div>
      <div class="font-sample-cell"><span class="sample-label">LIGATURE OUTPUT</span><span class="pcb sample-glyph" aria-label="${item.accessible_label}">${item.shortcode}</span><code class="sample-source">source ${item.shortcode}</code></div>
      <div class="font-sample-cell"><span class="sample-label">DIRECT PUA</span><span class="pcb-emoji sample-glyph" aria-label="${item.accessible_label}">${item.char}</span><code class="sample-source">${item.codepoint}</code></div>
      <div class="font-sample-meta"><code>${item.codepoint}</code><code>${item.shortcode}</code></div>`;
    return row;
  }

  const drawingRoot = document.querySelector('#patent-drawings');
  if (drawingRoot) {
    drawingRoot.replaceChildren(...drawings.map(([id, label, note], index) => {
      const item = record(id);
      return item ? drawingPlate(item, index, note) : document.createComment(`missing ${id}`);
    }));
  }

  const specimenRoot = document.querySelector('#font-specimen');
  if (specimenRoot) {
    const header = document.createElement('div');
    header.className = 'font-specimen-head';
    header.innerHTML = '<span>PART / DESCRIPTION</span><span>SEMANTIC TEXT</span><span>UNICODE-COMPATIBLE GLYPH</span><span>REGISTRY</span>';
    specimenRoot.append(header);
    specimenRoot.append(...samples.map(([id, label], index) => {
      const item = record(id);
      return item ? fontSample(item, label, index) : document.createComment(`missing ${id}`);
    }));
  }
}());
