// Search & Filter View
let searchTimeout = null
window.currentSearchParams = {}

async function initSearchView() {
  const container = document.getElementById('view-search')
  let domains = []
  try { domains = await API.domains() } catch(e) {}

  container.innerHTML = `
    <div class="search-container">
      <div class="search-header">
        <h1>Search Features</h1>
        <p style="color:#64748b;font-size:14px;margin-top:4px">Search and filter all 1000+ digital asset capabilities</p>
      </div>
      <div class="search-bar">
        <input type="text" class="search-input" id="search-q" placeholder="Search capabilities, features, descriptions..." oninput="triggerSearch()">
        <select class="search-select" id="search-domain" onchange="triggerSearch()">
          <option value="">All Domains</option>
          ${domains.map(d => `<option value="${d.id}">${d.name}</option>`).join('')}
        </select>
        <select class="search-select" id="search-maturity" onchange="triggerSearch()">
          <option value="">All Maturity</option>
          <option value="emerging">Emerging</option>
          <option value="developing">Developing</option>
          <option value="established">Established</option>
          <option value="mature">Mature</option>
        </select>
        <button class="btn-export" onclick="exportCurrentSearch()">⬇ Export</button>
      </div>
      <div class="search-results" id="search-results">
        <div class="empty-state">
          <div class="empty-icon">🔍</div>
          <h3>Start searching</h3>
          <p>Type a keyword or select a filter above</p>
        </div>
      </div>
    </div>`

  // Auto-search on load to show all
  runSearch()
}

function triggerSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(runSearch, 300)
}

async function runSearch() {
  const q = document.getElementById('search-q')?.value || ''
  const domain = document.getElementById('search-domain')?.value || ''
  const maturity = document.getElementById('search-maturity')?.value || ''

  const params = {}
  if (q) params.q = q
  if (domain) params.domain = domain
  if (maturity) params.maturity = maturity
  params.limit = 500

  window.currentSearchParams = params

  const results = document.getElementById('search-results')
  if (!results) return
  results.innerHTML = loading()

  try {
    const data = await API.features(params)
    renderSearchResults(data)
  } catch(e) {
    results.innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><h3>Error</h3><p>Could not load features. Database may still be loading.</p></div>`
  }
}

function renderSearchResults(data) {
  const results = document.getElementById('search-results')
  if (!data || !data.features) {
    results.innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><h3>No data</h3></div>`
    return
  }

  if (data.features.length === 0) {
    results.innerHTML = `<div class="empty-state"><div class="empty-icon">🔍</div><h3>No results</h3><p>Try different search terms</p></div>`
    return
  }

  results.innerHTML = `
    <div class="result-count">${data.total} features found${data.total > data.features.length ? ` (showing first ${data.features.length})` : ''}</div>
    <table class="result-table">
      <thead>
        <tr>
          <th>Domain</th>
          <th>L0 Competency</th>
          <th>L1 Business</th>
          <th>L2 Technical</th>
          <th>L3 Feature</th>
          <th>Description</th>
          <th>Maturity</th>
        </tr>
      </thead>
      <tbody>
        ${data.features.map(f => `
          <tr>
            <td><span class="domain-pill" style="background:${f.domain_color || '#64748b'}20;color:${f.domain_color || '#64748b'}">${f.domain_name || f.domain_id}</span></td>
            <td style="font-size:12px;color:#94a3b8">${f.l0_name || ''}</td>
            <td style="font-size:12px;color:#94a3b8">${f.l1_name || ''}</td>
            <td style="font-size:12px;color:#94a3b8">${f.l2_name || ''}</td>
            <td style="font-weight:600;font-size:13px">${f.name}</td>
            <td style="font-size:12px;color:#94a3b8;max-width:300px">${f.description || ''}</td>
            <td>${maturityTag(f.maturity)}</td>
          </tr>`).join('')}
      </tbody>
    </table>`
}

function exportCurrentSearch() {
  const q = document.getElementById('search-q')?.value || ''
  const domain = document.getElementById('search-domain')?.value || ''
  const maturity = document.getElementById('search-maturity')?.value || ''
  const params = {}
  if (q) params.q = q
  if (domain) params.domain = domain
  if (maturity) params.maturity = maturity
  window.location.href = API.exportUrl(params)
}
