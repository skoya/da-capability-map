const API = {
  base: '',

  async get(path) {
    const r = await fetch(this.base + path)
    if (!r.ok) throw new Error(`API error: ${r.status}`)
    return r.json()
  },

  domains: () => API.get('/api/domains'),
  stats: () => API.get('/api/stats'),
  periodic: () => API.get('/api/periodic'),
  tree: (params = {}) => API.get('/api/tree?' + new URLSearchParams(params)),
  regulations: (params = {}) => API.get('/api/regulations?' + new URLSearchParams(params)),
  features: (params = {}) => API.get('/api/features?' + new URLSearchParams(params)),

  exportUrl(params = {}) {
    return '/api/export?' + new URLSearchParams(params)
  }
}

function exportExcel() {
  const params = window.currentSearchParams || {}
  window.location.href = API.exportUrl(params)
}

const DOMAIN_COLORS = {
  custody:       '#f59e0b',
  wallets:       '#10b981',
  stablecoins:   '#6366f1',
  cbdc:          '#ec4899',
  settlement:    '#14b8a6',
  tokenisation:  '#f97316',
  defi_protocols:'#8b5cf6',
  security:      '#ef4444',
  ai_agentic:    '#06b6d4',
  compliance_regulation: '#84cc16',
}

function domainColor(id) {
  return DOMAIN_COLORS[id] || '#64748b'
}

function maturityTag(m) {
  if (!m) return ''
  return `<span class="tag tag-maturity-${m}">${m}</span>`
}

function openModal(html) {
  document.getElementById('modal-content').innerHTML = html
  document.getElementById('modal-overlay').classList.remove('hidden')
}

function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden')
}

function loading() {
  return `<div class="loading-spinner"><div class="spinner"></div> Loading...</div>`
}
