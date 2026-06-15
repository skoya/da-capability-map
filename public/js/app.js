// Router & App Initialisation

const VIEWS = {
  '/':           { id: 'periodic',   init: initPeriodicView },
  '/tree':       { id: 'tree',       init: initTreeView },
  '/search':     { id: 'search',     init: initSearchView },
  '/roles':      { id: 'roles',      init: initRolesView },
  '/regulation': { id: 'regulation', init: initRegulationView },
  '/heatmap':    { id: 'heatmap',    init: initHeatmapView },
}

const initialized = new Set()

function switchView(name) {
  const path = name === 'periodic' ? '/' : `/${name}`
  navigate(path)
}

function navigate(path) {
  // Update nav links
  document.querySelectorAll('.nav-link').forEach(l => {
    const lv = l.dataset.view
    const lp = lv === 'periodic' ? '/' : `/${lv}`
    l.classList.toggle('active', lp === path)
  })

  // Show correct view
  const viewDef = VIEWS[path] || VIEWS['/']
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'))
  const viewEl = document.getElementById(`view-${viewDef.id}`)
  if (viewEl) viewEl.classList.add('active')

  // Init view if not yet done
  if (!initialized.has(viewDef.id)) {
    initialized.add(viewDef.id)
    viewDef.init()
  }

  // Update URL without reload
  history.pushState({ path }, '', path)
}

// Nav link clicks
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault()
    const view = link.dataset.view
    const path = view === 'periodic' ? '/' : `/${view}`
    navigate(path)
  })
})

// Browser back/forward
window.addEventListener('popstate', e => {
  navigate(e.state?.path || '/')
})

// Keyboard shortcut: Escape to close modal
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal()
})

// Init on load
navigate(location.pathname || '/')
