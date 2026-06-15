// Periodic Table View
// Layout: 18 columns (groups), rows are periods
// Each L1 Business Capability becomes an "element"
// Domain = element category (like noble gases, metals etc)
// Gaps/placeholders fill the standard periodic table layout

const PERIODIC_CATEGORIES = {
  custody:        { label: 'Custody & Safekeeping', color: '#f59e0b', short: 'CU' },
  wallets:        { label: 'Wallet Infrastructure', color: '#10b981', short: 'WA' },
  stablecoins:    { label: 'Stablecoins',           color: '#6366f1', short: 'SC' },
  cbdc:           { label: 'CBDC & Digital Money',  color: '#ec4899', short: 'CB' },
  settlement:     { label: 'Settlement & Clearing', color: '#14b8a6', short: 'ST' },
  tokenisation:   { label: 'Tokenisation & RWA',    color: '#f97316', short: 'TK' },
  defi_protocols: { label: 'DeFi & Protocols',      color: '#8b5cf6', short: 'DE' },
  security:       { label: 'Security & Risk',        color: '#ef4444', short: 'SE' },
  ai_agentic:     { label: 'AI & Agentic',           color: '#06b6d4', short: 'AI' },
  compliance_regulation: { label: 'Compliance & Regulation', color: '#84cc16', short: 'CO' },
}

async function initPeriodicView() {
  const container = document.getElementById('view-periodic')
  container.innerHTML = loading()

  try {
    const [elements, stats] = await Promise.all([API.periodic(), API.stats()])
    renderPeriodicView(container, elements, stats)
  } catch(e) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><h3>Data not yet loaded</h3><p>The capability database is still being built. Check back shortly.</p></div>`
  }
}

function renderPeriodicView(container, elements, stats) {
  // Build periodic table positions
  // If elements have positions from DB, use them; otherwise auto-assign
  const positioned = buildPeriodicLayout(elements)

  const statsHtml = `
    <div class="stats-bar">
      <div class="stat-chip"><strong>${stats.l3 || 0}</strong>L3 Features</div>
      <div class="stat-chip"><strong>${stats.l1 || 0}</strong>L1 Capabilities</div>
      <div class="stat-chip"><strong>${stats.domains || 0}</strong>Domains</div>
      <div class="stat-chip"><strong>${stats.regulatory_frameworks || 0}</strong>Reg Frameworks</div>
    </div>`

  const legendHtml = `
    <div class="periodic-legend">
      ${Object.entries(PERIODIC_CATEGORIES).map(([k, v]) =>
        `<div class="legend-item"><div class="legend-dot" style="background:${v.color}"></div>${v.label}</div>`
      ).join('')}
    </div>`

  // Render grid
  const maxPeriod = Math.max(...positioned.map(e => e.period), 8)
  const maxGroup = 18

  let gridCells = []
  const cellMap = {}
  positioned.forEach(el => { cellMap[`${el.period}-${el.group}`] = el })

  for (let p = 1; p <= maxPeriod; p++) {
    for (let g = 1; g <= maxGroup; g++) {
      const el = cellMap[`${p}-${g}`]
      if (el) {
        const cat = PERIODIC_CATEGORIES[el.domain_id] || { color: '#64748b', label: el.domain_name }
        const bg = cat.color + '30'
        const border = cat.color + '80'
        gridCells.push(`
          <div class="element"
            style="background:${bg};border-color:${border};grid-column:${g};grid-row:${p}"
            onclick="showElementDetail('${el.id}')"
            title="${el.name}"
            data-id="${el.id}">
            <span class="el-num">${el.id ? el.id.split('-').pop() : ''}</span>
            <span class="el-symbol" style="color:${cat.color}">${generateSymbol(el.name)}</span>
            <span class="el-name">${el.name}</span>
            <span class="el-count">${el.feature_count || 0}f</span>
          </div>`)
      } else {
        gridCells.push(`<div class="element placeholder" style="grid-column:${g};grid-row:${p}"></div>`)
      }
    }
  }

  container.innerHTML = `
    <div class="periodic-header">
      <h1>Digital Asset Periodic Table</h1>
      <p>Business capabilities arranged by domain family — click any element to explore its technical capabilities and features</p>
    </div>
    ${statsHtml}
    ${legendHtml}
    <div class="periodic-table" style="grid-template-rows:repeat(${maxPeriod},1fr)">
      ${gridCells.join('')}
    </div>`
}

function generateSymbol(name) {
  const words = name.trim().split(/\s+/)
  if (words.length === 1) return words[0].slice(0, 2)
  return (words[0][0] + (words[1][0] || '')).toUpperCase()
}

function buildPeriodicLayout(elements) {
  // If DB has positions, use them
  const hasPositions = elements.some(e => e.period && e.group_num)
  if (hasPositions) {
    return elements.map(e => ({ ...e, group: e.group_num }))
  }

  // Auto-assign: group elements by domain, spread across 18 columns
  const domainOrder = Object.keys(PERIODIC_CATEGORIES)
  const byDomain = {}
  domainOrder.forEach(d => { byDomain[d] = [] })

  elements.forEach(el => {
    const d = el.domain_id
    if (!byDomain[d]) byDomain[d] = []
    byDomain[d].push(el)
  })

  // Assign layout: each domain gets a band of columns
  // Layout approach: two main blocks (like s/p block and d/f block)
  // Domains 1-2: columns 1-2 (s-block analogy: Custody, Wallets)
  // Domains 3-4: columns 3-4 (Stablecoins, CBDC)
  // Domains 5-6: columns 5-8 (d-block: Settlement, Tokenisation)
  // Domains 7-8: columns 9-12 (DeFi, Security)
  // Domains 9-10: columns 13-18 (AI, Compliance)

  const domainColumns = {
    custody:               [1,2],
    wallets:               [3,4],
    stablecoins:           [5,6],
    cbdc:                  [7,8],
    settlement:            [9,10],
    tokenisation:          [11,12],
    defi_protocols:        [13,14],
    security:              [15,16],
    ai_agentic:            [17],
    compliance_regulation: [18],
  }

  const positioned = []
  const colPeriod = {} // track current period per column

  for (const domainId of domainOrder) {
    const caps = byDomain[domainId] || []
    const cols = domainColumns[domainId] || [1]

    let colIdx = 0
    for (const cap of caps) {
      const col = cols[colIdx % cols.length]
      if (!colPeriod[col]) colPeriod[col] = 1
      positioned.push({ ...cap, period: colPeriod[col], group: col })
      colPeriod[col]++
      colIdx++
    }
  }

  return positioned
}

async function showElementDetail(id) {
  openModal(loading())
  try {
    const [l2s, all] = await Promise.all([
      API.tree({ l1: id }),
      API.features({ limit: 5 })  // placeholder; will get actual features
    ])

    // Get the element info from the periodic table
    const el = document.querySelector(`[data-id="${id}"]`)
    const name = el ? el.querySelector('.el-name')?.textContent : id

    const l2Html = l2s.map(l2 => `
      <li style="cursor:pointer" onclick="showL2Detail('${l2.id}','${l2.name.replace(/'/g,"\\'")}')">
        <div>
          <strong>${l2.name}</strong>
          <div style="font-size:11px;color:#64748b;margin-top:2px">${l2.description || ''}</div>
        </div>
      </li>`).join('')

    openModal(`
      <div class="modal-domain-badge" style="background:rgba(59,130,246,0.15);color:#60a5fa">Business Capability (L1)</div>
      <h2>${name}</h2>
      <div class="modal-section">
        <h4>Technical Capabilities (L2)</h4>
        <ul class="sub-feature-list">${l2Html || '<li>No technical capabilities loaded yet</li>'}</ul>
      </div>`)
  } catch(e) {
    openModal(`<div class="empty-state"><div class="empty-icon">⚠️</div><h3>Could not load detail</h3></div>`)
  }
}

async function showL2Detail(id, name) {
  openModal(loading())
  try {
    const features = await API.tree({ l2: id })
    const featureHtml = features.slice(0, 40).map(f => `
      <li>
        <div>
          <strong>${f.name}</strong>
          ${f.description ? `<div style="font-size:11px;color:#64748b;margin-top:2px">${f.description}</div>` : ''}
          ${maturityTag(f.maturity)}
        </div>
      </li>`).join('')

    openModal(`
      <div class="modal-domain-badge" style="background:rgba(16,185,129,0.15);color:#34d399">Technical Capability (L2)</div>
      <h2>${name}</h2>
      <div class="modal-section">
        <h4>Features (L3) — ${features.length} total</h4>
        <ul class="sub-feature-list">${featureHtml || '<li>No features loaded yet</li>'}</ul>
        ${features.length > 40 ? `<p style="font-size:12px;color:#64748b;margin-top:8px">...and ${features.length - 40} more — use Search view for full list</p>` : ''}
      </div>`)
  } catch(e) {
    openModal(`<div class="empty-state"><div class="empty-icon">⚠️</div><h3>Could not load features</h3></div>`)
  }
}
