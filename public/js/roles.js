// Role Views — filtered capability views for different GSIB roles

const GSIB_ROLES = [
  {
    id: 'cto',
    title: 'Chief Technology Officer',
    icon: '🏗️',
    desc: 'Infrastructure, architecture, technical capabilities, protocol integration, and platform decisions',
    domains: ['wallets', 'security', 'settlement', 'defi_protocols', 'ai_agentic'],
    focus: 'L2 Technical Capabilities — what technology stack is required and at what maturity',
  },
  {
    id: 'cro',
    title: 'Chief Risk Officer',
    icon: '⚖️',
    desc: 'Market, credit, liquidity, operational and technology risk across the digital asset stack',
    domains: ['security', 'custody', 'stablecoins', 'settlement', 'defi_protocols'],
    focus: 'Risk features, attack vectors, counterparty exposure, settlement risk',
  },
  {
    id: 'cco',
    title: 'Chief Compliance Officer',
    icon: '📋',
    desc: 'Regulatory obligations, AML/CFT, KYC, Travel Rule, reporting across all G7+ jurisdictions',
    domains: ['compliance_regulation', 'stablecoins', 'cbdc'],
    focus: 'Regulatory requirements, compliance features, jurisdiction mapping',
  },
  {
    id: 'cfo',
    title: 'Chief Financial Officer / Treasury',
    icon: '💰',
    desc: 'Treasury management, stablecoin liquidity, reserve management, collateral optimisation, accounting',
    domains: ['stablecoins', 'cbdc', 'settlement', 'tokenisation'],
    focus: 'Financial capabilities, reserve management, cross-border efficiency',
  },
  {
    id: 'front_office',
    title: 'Front Office / Trading',
    icon: '📈',
    desc: 'Trading infrastructure, DeFi access, tokenised product distribution, market making',
    domains: ['defi_protocols', 'tokenisation', 'settlement', 'custody'],
    focus: 'Trading, liquidity, yield, structured products on digital rails',
  },
  {
    id: 'operations',
    title: 'Operations / COO',
    icon: '⚙️',
    desc: 'Operational processes, settlement workflows, custody operations, client servicing',
    domains: ['custody', 'wallets', 'settlement', 'compliance_regulation'],
    focus: 'Operational efficiency, SLAs, reconciliation, straight-through processing',
  },
  {
    id: 'product',
    title: 'Product & Strategy',
    icon: '🎯',
    desc: 'Strategic capability planning, new product development, market opportunity mapping',
    domains: ['tokenisation', 'cbdc', 'stablecoins', 'defi_protocols', 'ai_agentic'],
    focus: 'Enterprise competencies and business capabilities for roadmap planning',
  },
  {
    id: 'digital_assets',
    title: 'Digital Assets Division Head',
    icon: '🔷',
    desc: 'Full DA stack overview: custody, stablecoins, CBDC, tokenisation, settlement, DeFi',
    domains: ['custody', 'wallets', 'stablecoins', 'cbdc', 'settlement', 'tokenisation', 'defi_protocols', 'security', 'ai_agentic', 'compliance_regulation'],
    focus: 'Full 4-level taxonomy — strategic to feature level',
  },
]

async function initRolesView() {
  const container = document.getElementById('view-roles')
  container.innerHTML = `
    <h1 style="font-size:22px;font-weight:700;margin-bottom:8px">Role-Based Capability Views</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:24px">Filtered views of the capability map for key GSIB roles</p>
    <div class="roles-grid">
      ${GSIB_ROLES.map(r => `
        <div class="role-card" onclick="showRoleView('${r.id}')">
          <div class="role-icon">${r.icon}</div>
          <div class="role-title">${r.title}</div>
          <div class="role-desc">${r.desc}</div>
          <div class="role-domains">
            ${r.domains.map(d => `<span class="domain-pill" style="background:${domainColor(d)}20;color:${domainColor(d)}">${d.split('_')[0]}</span>`).join('')}
          </div>
        </div>`).join('')}
    </div>
    <div id="role-detail"></div>`
}

async function showRoleView(roleId) {
  const role = GSIB_ROLES.find(r => r.id === roleId)
  if (!role) return

  const detail = document.getElementById('role-detail')
  detail.innerHTML = `
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:24px;margin-top:24px">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
        <span style="font-size:32px">${role.icon}</span>
        <div>
          <h2 style="font-size:18px;font-weight:700">${role.title}</h2>
          <p style="font-size:13px;color:#64748b;margin-top:2px">${role.focus}</p>
        </div>
        <button onclick="window.location.href='/api/export?domain=${role.domains[0]}'" class="btn-export" style="margin-left:auto">⬇ Export View</button>
      </div>
      ${loading()}
    </div>`

  detail.scrollIntoView({ behavior: 'smooth' })

  try {
    const results = await Promise.all(
      role.domains.map(d => API.features({ domain: d, limit: 100 }))
    )

    let html = ''
    role.domains.forEach((d, i) => {
      const data = results[i]
      if (!data || !data.features.length) return
      const color = domainColor(d)
      html += `
        <div style="margin-bottom:20px">
          <h3 style="font-size:14px;font-weight:700;color:${color};margin-bottom:10px;display:flex;align-items:center;gap:8px">
            <span style="width:8px;height:8px;background:${color};border-radius:50%;display:inline-block"></span>
            ${data.features[0]?.domain_name || d}
            <span style="font-size:11px;color:#64748b;font-weight:400">${data.total} features</span>
          </h3>
          <div class="feature-grid">
            ${data.features.slice(0, 12).map(f => `
              <div class="feature-card">
                <h4>${f.name}</h4>
                <p>${f.description || ''}</p>
                <div class="feature-meta">
                  ${maturityTag(f.maturity)}
                  <span style="font-size:10px;color:#64748b">${f.l1_name || ''}</span>
                </div>
              </div>`).join('')}
            ${data.features.length > 12 ? `<div class="feature-card" style="display:flex;align-items:center;justify-content:center;color:#64748b;font-size:13px">+${data.features.length - 12} more → <a href="/search" onclick="switchView('search')" style="color:#3b82f6;margin-left:4px">Search</a></div>` : ''}
          </div>
        </div>`
    })

    const inner = detail.querySelector('div')
    const p = inner.querySelector('.loading-spinner')?.parentElement || inner
    if (p) p.innerHTML += html
    detail.querySelector('.loading-spinner')?.remove()
    inner.innerHTML = inner.innerHTML.replace(loading(), html)
    // Re-render cleanly
    detail.innerHTML = `
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:24px;margin-top:24px">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
          <span style="font-size:32px">${role.icon}</span>
          <div>
            <h2 style="font-size:18px;font-weight:700">${role.title}</h2>
            <p style="font-size:13px;color:#64748b;margin-top:2px">${role.focus}</p>
          </div>
          <a href="${API.exportUrl({ domain: role.domains.join(',') })}" class="btn-export" style="margin-left:auto;text-decoration:none">⬇ Export View</a>
        </div>
        ${html || '<div class="empty-state"><p>No features loaded yet — database building</p></div>'}
      </div>`
  } catch(e) {
    detail.innerHTML += `<p style="color:#64748b;font-size:13px;margin-top:10px">Data not yet available</p>`
  }
}
