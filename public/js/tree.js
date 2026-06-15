// Tree Navigator View

let treeState = {
  selectedDomain: null,
  selectedL0: null,
  selectedL1: null,
  selectedL2: null,
  expanded: new Set(),
}

async function initTreeView() {
  const container = document.getElementById('view-tree')
  container.innerHTML = `
    <h2 style="font-size:18px;font-weight:700;margin-bottom:16px">Capability Tree Navigator</h2>
    <div class="tree-container">
      <div class="tree-sidebar" id="tree-sidebar">${loading()}</div>
      <div class="tree-main" id="tree-main">
        <div class="empty-state">
          <div class="empty-icon">🌳</div>
          <h3>Select a domain to explore</h3>
          <p>Use the sidebar to navigate the capability hierarchy</p>
        </div>
      </div>
    </div>`

  try {
    const domains = await API.domains()
    renderTreeSidebar(domains)
  } catch(e) {
    document.getElementById('tree-sidebar').innerHTML = `<div class="empty-state"><p>No data yet</p></div>`
  }
}

function renderTreeSidebar(domains) {
  const sidebar = document.getElementById('tree-sidebar')
  sidebar.innerHTML = `
    <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.05em;padding:4px 10px;margin-bottom:8px">Domains</div>
    ${domains.map(d => `
      <div class="tree-node" data-id="${d.id}" onclick="selectDomain('${d.id}','${d.name.replace(/'/g,"\\'")}')">
        <div class="node-icon" style="color:${domainColor(d.id)}">⬡</div>
        <div class="node-label">${d.name}</div>
        <div class="node-count">${d.feature_count || 0}</div>
      </div>`).join('')}
  `
}

async function selectDomain(id, name) {
  treeState.selectedDomain = id
  document.querySelectorAll('.tree-sidebar .tree-node').forEach(n => n.classList.remove('selected'))
  document.querySelector(`[data-id="${id}"]`)?.classList.add('selected')

  const main = document.getElementById('tree-main')
  main.innerHTML = loading()

  try {
    const l0s = await API.tree({ domain: id })
    renderL0List(l0s, name)
  } catch(e) {
    main.innerHTML = `<div class="empty-state"><p>Error loading capabilities</p></div>`
  }
}

function renderL0List(l0s, domainName) {
  const main = document.getElementById('tree-main')
  main.innerHTML = `
    <h3 style="font-size:15px;font-weight:700;margin-bottom:16px">${domainName}</h3>
    <div style="display:flex;flex-direction:column;gap:10px">
      ${l0s.map(l0 => `
        <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;overflow:hidden">
          <div style="padding:14px 16px;cursor:pointer;display:flex;align-items:center;gap:10px"
            onclick="toggleL0('${l0.id}','${l0.name.replace(/'/g,"\\'")}')">
            <span style="font-size:13px;color:#64748b" id="l0-arrow-${l0.id}">▶</span>
            <div>
              <div style="font-size:14px;font-weight:600">${l0.name}</div>
              <div style="font-size:12px;color:#64748b;margin-top:2px">${l0.description || ''}</div>
            </div>
            <span style="margin-left:auto;font-size:11px;color:#475569;background:var(--surface);padding:2px 8px;border-radius:99px">L0</span>
          </div>
          <div id="l0-children-${l0.id}" style="display:none;padding:0 16px 14px;padding-left:36px">
            ${loading()}
          </div>
        </div>`).join('')}
    </div>`
}

async function toggleL0(id, name) {
  const children = document.getElementById(`l0-children-${id}`)
  const arrow = document.getElementById(`l0-arrow-${id}`)
  if (!children) return

  if (children.style.display === 'none') {
    children.style.display = 'block'
    arrow.textContent = '▼'
    if (children.innerHTML.includes('loading-spinner')) {
      try {
        const l1s = await API.tree({ l0: id })
        children.innerHTML = l1s.map(l1 => `
          <div style="margin-bottom:8px;background:var(--surface);border:1px solid var(--border);border-radius:6px;overflow:hidden">
            <div style="padding:10px 14px;cursor:pointer;display:flex;align-items:center;gap:8px"
              onclick="toggleL1('${l1.id}','${l1.name.replace(/'/g,"\\'")}')">
              <span style="font-size:12px;color:#64748b" id="l1-arrow-${l1.id}">▶</span>
              <div>
                <div style="font-size:13px;font-weight:600">${l1.name}</div>
                <div style="font-size:11px;color:#64748b;margin-top:1px">${l1.description || ''}</div>
              </div>
              <span style="margin-left:auto;font-size:10px;color:#6366f1;background:rgba(99,102,241,0.1);padding:1px 7px;border-radius:99px">L1</span>
            </div>
            <div id="l1-children-${l1.id}" style="display:none;padding:0 14px 10px;padding-left:28px">${loading()}</div>
          </div>`).join('') || '<p style="color:#64748b;font-size:12px">No business capabilities</p>'
      } catch(e) {
        children.innerHTML = '<p style="color:#64748b;font-size:12px">Error loading</p>'
      }
    }
  } else {
    children.style.display = 'none'
    arrow.textContent = '▶'
  }
}

async function toggleL1(id, name) {
  const children = document.getElementById(`l1-children-${id}`)
  const arrow = document.getElementById(`l1-arrow-${id}`)
  if (!children) return

  if (children.style.display === 'none') {
    children.style.display = 'block'
    arrow.textContent = '▼'
    if (children.innerHTML.includes('loading-spinner')) {
      try {
        const l2s = await API.tree({ l1: id })
        children.innerHTML = l2s.map(l2 => `
          <div style="margin-bottom:6px;border-left:2px solid var(--border);padding-left:10px">
            <div style="display:flex;align-items:center;gap:6px;cursor:pointer;padding:6px 0"
              onclick="toggleL2('${l2.id}','${l2.name.replace(/'/g,"\\'")}')">
              <span style="font-size:11px;color:#64748b" id="l2-arrow-${l2.id}">▶</span>
              <div>
                <div style="font-size:12px;font-weight:600">${l2.name}</div>
                <div style="font-size:11px;color:#64748b">${l2.description || ''}</div>
              </div>
              <span style="margin-left:auto;font-size:10px;color:#14b8a6;background:rgba(20,184,166,0.1);padding:1px 6px;border-radius:99px">L2</span>
            </div>
            <div id="l2-children-${l2.id}" style="display:none;margin-top:4px">${loading()}</div>
          </div>`).join('') || '<p style="color:#64748b;font-size:11px">No technical capabilities</p>'
      } catch(e) {
        children.innerHTML = '<p style="color:#64748b;font-size:11px">Error loading</p>'
      }
    }
  } else {
    children.style.display = 'none'
    arrow.textContent = '▶'
  }
}

async function toggleL2(id, name) {
  const children = document.getElementById(`l2-children-${id}`)
  const arrow = document.getElementById(`l2-arrow-${id}`)
  if (!children) return

  if (children.style.display === 'none') {
    children.style.display = 'block'
    arrow.textContent = '▼'
    if (children.innerHTML.includes('loading-spinner')) {
      try {
        const features = await API.tree({ l2: id })
        children.innerHTML = `
          <div style="display:flex;flex-direction:column;gap:4px">
            ${features.map(f => `
              <div style="background:var(--surface2);border-radius:4px;padding:7px 10px;font-size:11px;border-left:2px solid #1e293b">
                <div style="font-weight:600;margin-bottom:2px">${f.name}</div>
                <div style="color:#64748b;line-height:1.4">${f.description || ''}</div>
                ${maturityTag(f.maturity)}
              </div>`).join('')}
          </div>` || '<p style="color:#64748b;font-size:11px">No features</p>'
      } catch(e) {
        children.innerHTML = '<p style="color:#64748b;font-size:11px">Error loading</p>'
      }
    }
  } else {
    children.style.display = 'none'
    arrow.textContent = '▶'
  }
}
