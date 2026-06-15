// Regulation View

const JURISDICTIONS = [
  { id: 'us', name: '🇺🇸 United States', color: '#3b82f6' },
  { id: 'uk', name: '🇬🇧 United Kingdom', color: '#ef4444' },
  { id: 'eu', name: '🇪🇺 European Union', color: '#f59e0b' },
  { id: 'apac', name: '🌏 Asia-Pacific', color: '#10b981' },
  { id: 'ch_uae', name: '🇨🇭🇦🇪 CH / UAE', color: '#8b5cf6' },
]

async function initRegulationView() {
  const container = document.getElementById('view-regulation')
  container.innerHTML = `
    <h1 style="font-size:22px;font-weight:700;margin-bottom:8px">Regulatory Frameworks</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:24px">Digital asset regulations across G7+ markets mapped to capabilities</p>
    <div class="reg-filters" id="reg-filters">
      <button class="btn-export" onclick="filterReg('')" style="background:#334155">All Jurisdictions</button>
      ${JURISDICTIONS.map(j => `<button class="btn-export" onclick="filterReg('${j.id}')" style="background:${j.color}30;color:${j.color};border:1px solid ${j.color}50">${j.name}</button>`).join('')}
    </div>
    <div id="reg-content">${loading()}</div>`

  loadRegulations('')
}

async function filterReg(jurisdiction) {
  document.getElementById('reg-content').innerHTML = loading()
  loadRegulations(jurisdiction)
}

async function loadRegulations(jurisdiction) {
  try {
    const frameworks = await API.regulations(jurisdiction ? { jurisdiction } : {})
    renderRegulations(frameworks)
  } catch(e) {
    document.getElementById('reg-content').innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><h3>Regulation data loading</h3><p>Framework data will be available once the database build completes.</p></div>`
  }
}

function renderRegulations(frameworks) {
  const content = document.getElementById('reg-content')
  if (!frameworks.length) {
    content.innerHTML = `<div class="empty-state"><div class="empty-icon">📋</div><h3>No frameworks loaded yet</h3><p>Regulatory data is still being ingested into the database.</p></div>`
    return
  }

  // Group by jurisdiction
  const byJurisdiction = {}
  frameworks.forEach(f => {
    const j = f.jurisdiction || 'Other'
    if (!byJurisdiction[j]) byJurisdiction[j] = []
    byJurisdiction[j].push(f)
  })

  content.innerHTML = Object.entries(byJurisdiction).map(([j, fws]) => `
    <div style="margin-bottom:28px">
      <h2 style="font-size:16px;font-weight:700;margin-bottom:12px;color:#94a3b8">${j}</h2>
      ${fws.map(f => `
        <div class="reg-card">
          <h3>${f.name} ${f.short_name ? `<span style="font-size:11px;color:#64748b;font-weight:400">(${f.short_name})</span>` : ''}</h3>
          <div class="reg-meta">
            ${f.regulator ? `<span>Regulator: ${f.regulator}</span>` : ''}
            ${f.status ? `<span style="margin-left:12px">Status: <span style="color:${f.status === 'In Force' ? '#34d399' : '#fbbf24'}">${f.status}</span></span>` : ''}
            ${f.effective_date ? `<span style="margin-left:12px">Effective: ${f.effective_date}</span>` : ''}
          </div>
          <p>${f.description || ''}</p>
        </div>`).join('')}
    </div>`).join('')
}
