// Gap analysis view — self-assessment mode
// Shows L3 features by priority, domain coverage summary, and coverage toggle

window.GapView = {
  coverage: {},  // capability_id → 'yes' | 'partial' | 'no'
  data: null,

  async render(container) {
    container.innerHTML = `
      <div class="gap-header">
        <h2>Gap Analysis</h2>
        <p class="gap-sub">Rate your institution's coverage of each capability to identify gaps. Select a filter to focus.</p>
        <div class="gap-controls">
          <select id="gap-domain" onchange="GapView.reload()">
            <option value="">All Domains</option>
          </select>
          <select id="gap-role" onchange="GapView.reload()">
            <option value="">All Roles</option>
            <option value="cto">CTO</option>
            <option value="cro">CRO</option>
            <option value="cco">CCO</option>
            <option value="cfo">CFO</option>
            <option value="front_office">Front Office</option>
            <option value="operations">Operations</option>
            <option value="product">Product</option>
            <option value="audit">Audit</option>
          </select>
          <button class="btn-secondary" onclick="GapView.resetCoverage()">Reset Coverage</button>
          <button class="btn-export" onclick="GapView.exportGapReport()">⬇ Export Gap Report</button>
        </div>
      </div>
      <div id="gap-summary-bar"></div>
      <div id="gap-domain-grid"></div>
      <div id="gap-priority-sections"></div>
    `

    await this.loadDomains()
    await this.reload()
  },

  async loadDomains() {
    const domains = await api('/api/domains')
    const sel = document.getElementById('gap-domain')
    for (const d of domains) {
      const opt = document.createElement('option')
      opt.value = d.id
      opt.textContent = d.name
      sel.appendChild(opt)
    }
  },

  async reload() {
    const domain = document.getElementById('gap-domain')?.value || ''
    const role = document.getElementById('gap-role')?.value || ''
    const params = new URLSearchParams()
    if (domain) params.set('domain', domain)
    if (role) params.set('role', role)
    this.data = await api('/api/gap?' + params.toString())
    this.renderSummaryBar()
    this.renderDomainGrid()
    this.renderPrioritySections()
  },

  getCoverage(id) {
    return this.coverage[id] || 'no'
  },

  setCoverage(id, value) {
    this.coverage[id] = value
    this.renderSummaryBar()
    this.renderDomainGrid()
    // update just the badge on this row
    const row = document.querySelector(`[data-cap-id="${id}"]`)
    if (row) {
      const badges = row.querySelectorAll('.coverage-btn')
      badges.forEach(b => b.classList.toggle('active', b.dataset.val === value))
    }
  },

  resetCoverage() {
    this.coverage = {}
    this.renderSummaryBar()
    this.renderDomainGrid()
    this.renderPrioritySections()
  },

  summaryStats() {
    if (!this.data) return { total: 0, covered: 0, partial: 0, gap: 0 }
    const features = this.data.features
    const covered = features.filter(f => this.getCoverage(f.id) === 'yes').length
    const partial = features.filter(f => this.getCoverage(f.id) === 'partial').length
    const gap = features.length - covered - partial
    return { total: features.length, covered, partial, gap }
  },

  renderSummaryBar() {
    const { total, covered, partial, gap } = this.summaryStats()
    const pct = total ? Math.round((covered + partial * 0.5) / total * 100) : 0
    document.getElementById('gap-summary-bar').innerHTML = `
      <div class="gap-summary">
        <div class="gap-metric"><span class="gm-num">${total}</span><span class="gm-label">Total</span></div>
        <div class="gap-metric green"><span class="gm-num">${covered}</span><span class="gm-label">Covered</span></div>
        <div class="gap-metric amber"><span class="gm-num">${partial}</span><span class="gm-label">Partial</span></div>
        <div class="gap-metric red"><span class="gm-num">${gap}</span><span class="gm-label">Gap</span></div>
        <div class="gap-coverage-bar">
          <div class="gcb-track">
            <div class="gcb-fill green" style="width:${total ? Math.round(covered/total*100) : 0}%"></div>
            <div class="gcb-fill amber" style="width:${total ? Math.round(partial/total*100) : 0}%"></div>
          </div>
          <span class="gcb-pct">${pct}% effective coverage</span>
        </div>
      </div>
    `
  },

  renderDomainGrid() {
    if (!this.data) return
    const html = this.data.domain_summary.map(d => {
      const covered = this.data.features
        .filter(f => f.domain_id === d.domain_id && this.getCoverage(f.id) === 'yes').length
      const partial = this.data.features
        .filter(f => f.domain_id === d.domain_id && this.getCoverage(f.id) === 'partial').length
      const pct = d.total ? Math.round((covered + partial * 0.5) / d.total * 100) : 0
      const col = d.color || '#888'
      return `<div class="gap-domain-card" style="border-left:4px solid ${col}">
        <div class="gdc-name">${d.name}</div>
        <div class="gdc-stats">
          <span class="gdc-pct" style="color:${col}">${pct}%</span>
          <span class="gdc-sub">${covered}/${d.total} covered</span>
        </div>
        <div class="gdc-bar">
          <div class="gdb-fill" style="width:${pct}%;background:${col}"></div>
        </div>
      </div>`
    }).join('')
    document.getElementById('gap-domain-grid').innerHTML = `<div class="gap-domain-row">${html}</div>`
  },

  renderPrioritySections() {
    if (!this.data) return
    const PRIORITY_LABELS = {
      5: { label: 'P5 — Mature / Critical', cls: 'p5' },
      4: { label: 'P4 — Established', cls: 'p4' },
      3: { label: 'P3 — Developing', cls: 'p3' },
      1: { label: 'P1 — Emerging', cls: 'p1' },
    }
    let html = ''
    for (const p of [5, 4, 3, 1]) {
      const features = this.data.by_priority[p] || []
      if (!features.length) continue
      const { label, cls } = PRIORITY_LABELS[p]
      const rows = features.map(f => {
        const cov = this.getCoverage(f.id)
        return `<tr data-cap-id="${f.id}" class="gap-row ${cov}">
          <td class="gc-domain" style="color:${f.domain_color}">${f.domain_name}</td>
          <td class="gc-l1">${f.l1_name}</td>
          <td class="gc-l2">${f.l2_name}</td>
          <td class="gc-name">${f.name}</td>
          <td class="gc-maturity mat-${f.maturity}">${f.maturity}</td>
          <td class="gc-actions">
            <button class="coverage-btn ${cov==='yes'?'active':''}" data-val="yes"
              onclick="GapView.setCoverage('${f.id}','yes')">✓ Yes</button>
            <button class="coverage-btn amber ${cov==='partial'?'active':''}" data-val="partial"
              onclick="GapView.setCoverage('${f.id}','partial')">~ Partial</button>
            <button class="coverage-btn red ${cov==='no'?'active':''}" data-val="no"
              onclick="GapView.setCoverage('${f.id}','no')">✗ Gap</button>
          </td>
        </tr>`
      }).join('')
      html += `<div class="gap-section ${cls}">
        <div class="gap-section-header" onclick="this.parentElement.classList.toggle('collapsed')">
          <span class="gs-label">${label}</span>
          <span class="gs-count">${features.length} features</span>
          <span class="gs-toggle">▾</span>
        </div>
        <div class="gap-section-body">
          <table class="gap-table">
            <thead><tr>
              <th>Domain</th><th>L1</th><th>L2</th><th>Feature</th><th>Maturity</th><th>Coverage</th>
            </tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>`
    }
    document.getElementById('gap-priority-sections').innerHTML = html
  },

  exportGapReport() {
    if (!this.data) return
    const rows = [['Domain','L1','L2','Feature','Maturity','Priority','Coverage']]
    for (const f of this.data.features) {
      rows.push([f.domain_name, f.l1_name, f.l2_name, f.name, f.maturity, f.priority, this.getCoverage(f.id)])
    }
    const csv = rows.map(r => r.map(v => `"${(v||'').toString().replace(/"/g,'""')}"`).join(',')).join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = 'da-gap-analysis.csv'
    a.click()
  }
}
