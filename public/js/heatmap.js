// Heatmap View — maturity heat map across domains

async function initHeatmapView() {
  const container = document.getElementById('view-heatmap')
  container.innerHTML = loading()

  try {
    const [stats, domains] = await Promise.all([API.stats(), API.domains()])
    renderHeatmap(container, stats, domains)
  } catch(e) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><h3>Data loading</h3></div>`
  }
}

function renderHeatmap(container, stats, domains) {
  const maturities = ['emerging', 'developing', 'established', 'mature']
  const maturityColors = {
    emerging:    { bg: 'rgba(239,68,68,0.15)', text: '#f87171', label: 'Emerging' },
    developing:  { bg: 'rgba(245,158,11,0.15)', text: '#fbbf24', label: 'Developing' },
    established: { bg: 'rgba(16,185,129,0.15)', text: '#34d399', label: 'Established' },
    mature:      { bg: 'rgba(59,130,246,0.15)', text: '#60a5fa', label: 'Mature' },
  }

  container.innerHTML = `
    <h1 style="font-size:22px;font-weight:700;margin-bottom:8px">Capability Maturity Heat Map</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:24px">Feature maturity distribution across domains and capability families</p>

    <div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:24px">
      <h2 style="font-size:15px;font-weight:700;margin-bottom:16px">Features by Domain</h2>
      <div style="display:grid;grid-template-columns:1fr auto;gap:20px">
        <div>
          ${(stats.by_domain || []).map(d => {
            const max = Math.max(...(stats.by_domain || []).map(x => x.features))
            const pct = max ? (d.features / max) * 100 : 0
            return `
              <div style="margin-bottom:10px">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                  <span style="font-size:13px">${d.name}</span>
                  <span style="font-size:12px;color:#64748b;font-family:'JetBrains Mono',monospace">${d.features}</span>
                </div>
                <div style="background:var(--surface2);border-radius:4px;height:8px;overflow:hidden">
                  <div style="width:${pct}%;height:100%;background:${d.color || '#3b82f6'};border-radius:4px;transition:width .5s"></div>
                </div>
              </div>`
          }).join('')}
        </div>
        <div style="display:flex;flex-direction:column;gap:8px;align-self:flex-start">
          ${(stats.by_maturity || []).map(m => `
            <div style="background:${(maturityColors[m.maturity] || {bg:'#1e293b'}).bg};padding:10px 16px;border-radius:8px;text-align:center">
              <div style="font-size:20px;font-weight:700;color:${(maturityColors[m.maturity] || {text:'#94a3b8'}).text};font-family:'JetBrains Mono',monospace">${m.count}</div>
              <div style="font-size:11px;color:#64748b;margin-top:2px">${(maturityColors[m.maturity] || {label:m.maturity}).label}</div>
            </div>`).join('')}
        </div>
      </div>
    </div>

    <div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:24px">
      <h2 style="font-size:15px;font-weight:700;margin-bottom:8px">GSIB Digital Asset Maturity Matrix</h2>
      <p style="font-size:12px;color:#64748b;margin-bottom:16px">Self-assessment guide: where is your institution on each capability?</p>
      <div style="overflow-x:auto">
        <table style="width:100%;border-collapse:collapse;font-size:12px">
          <thead>
            <tr>
              <th style="padding:10px;text-align:left;border-bottom:1px solid var(--border);color:#64748b">Domain</th>
              ${maturities.map(m => `<th style="padding:10px;text-align:center;border-bottom:1px solid var(--border);color:${maturityColors[m].text}">${maturityColors[m].label}</th>`).join('')}
            </tr>
          </thead>
          <tbody>
            ${domains.map(d => `
              <tr>
                <td style="padding:10px;border-bottom:1px solid var(--border);font-weight:600">
                  <span style="color:${domainColor(d.id)}">●</span> ${d.name}
                </td>
                ${maturities.map(m => `
                  <td style="padding:10px;border-bottom:1px solid var(--border);text-align:center">
                    <div style="background:${maturityColors[m].bg};border-radius:4px;padding:4px 8px;color:${maturityColors[m].text};font-family:'JetBrains Mono',monospace">
                      —
                    </div>
                  </td>`).join('')}
              </tr>`).join('')}
          </tbody>
        </table>
      </div>
      <p style="font-size:11px;color:#475569;margin-top:12px">Note: Maturity scores per domain will populate automatically as features are tagged during database ingestion.</p>
    </div>`
}
