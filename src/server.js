const express = require('express')
const path = require('path')
const cors = require('cors')
const Database = require('better-sqlite3')
const ExcelJS = require('exceljs')
const fs = require('fs')

const app = express()
const PORT = 3847
const DB_PATH = path.join(__dirname, '../data/capabilities.db')

app.use(cors())
app.use(express.json())
app.use(express.static(path.join(__dirname, '../public')))

function getDb() {
  return new Database(DB_PATH, { readonly: true })
}

// --- API Routes ---

// GET /api/domains
app.get('/api/domains', (req, res) => {
  const db = getDb()
  const domains = db.prepare(`
    SELECT d.*,
      COUNT(DISTINCT l0.id) as l0_count,
      COUNT(DISTINCT l3.id) as feature_count
    FROM domains d
    LEFT JOIN capabilities_l0 l0 ON l0.domain_id = d.id
    LEFT JOIN capabilities_l1 l1 ON l1.l0_id = l0.id
    LEFT JOIN capabilities_l2 l2 ON l2.l1_id = l1.id
    LEFT JOIN capabilities_l3 l3 ON l3.l2_id = l2.id
    GROUP BY d.id ORDER BY d.sort_order
  `).all()
  db.close()
  res.json(domains)
})

// GET /api/tree?domain=&l0=&l1=&l2=
app.get('/api/tree', (req, res) => {
  const db = getDb()
  const { domain, l0, l1, l2 } = req.query

  if (l2) {
    const features = db.prepare(`SELECT * FROM capabilities_l3 WHERE l2_id = ? ORDER BY sort_order`).all(l2)
    db.close()
    return res.json(features)
  }
  if (l1) {
    const techs = db.prepare(`SELECT * FROM capabilities_l2 WHERE l1_id = ? ORDER BY sort_order`).all(l1)
    db.close()
    return res.json(techs)
  }
  if (l0) {
    const bizCaps = db.prepare(`SELECT * FROM capabilities_l1 WHERE l0_id = ? ORDER BY sort_order`).all(l0)
    db.close()
    return res.json(bizCaps)
  }
  if (domain) {
    const competencies = db.prepare(`SELECT * FROM capabilities_l0 WHERE domain_id = ? ORDER BY sort_order`).all(domain)
    db.close()
    return res.json(competencies)
  }

  const domains = db.prepare(`SELECT * FROM domains ORDER BY sort_order`).all()
  db.close()
  res.json(domains)
})

// GET /api/features — search/filter for features
app.get('/api/features', (req, res) => {
  const db = getDb()
  const { q, domain, maturity, market, limit = 200, offset = 0 } = req.query

  let where = []
  let params = []

  if (q) {
    where.push(`(l3.name LIKE ? OR l3.description LIKE ?)`)
    params.push(`%${q}%`, `%${q}%`)
  }
  if (domain) {
    where.push(`l3.domain_id = ?`)
    params.push(domain)
  }
  if (maturity) {
    where.push(`l3.maturity = ?`)
    params.push(maturity)
  }

  const whereClause = where.length ? `WHERE ${where.join(' AND ')}` : ''

  const total = db.prepare(`
    SELECT COUNT(*) as count FROM capabilities_l3 l3 ${whereClause}
  `).get(...params)

  const features = db.prepare(`
    SELECT l3.*,
      l2.name as l2_name, l2.description as l2_desc,
      l1.name as l1_name, l1.description as l1_desc,
      l0.name as l0_name, l0.description as l0_desc,
      d.name as domain_name, d.color as domain_color
    FROM capabilities_l3 l3
    JOIN capabilities_l2 l2 ON l3.l2_id = l2.id
    JOIN capabilities_l1 l1 ON l3.l1_id = l1.id
    JOIN capabilities_l0 l0 ON l3.l0_id = l0.id
    JOIN domains d ON l3.domain_id = d.id
    ${whereClause}
    ORDER BY l3.domain_id, l3.sort_order
    LIMIT ? OFFSET ?
  `).all(...params, parseInt(limit), parseInt(offset))

  db.close()
  res.json({ total: total.count, features, limit: parseInt(limit), offset: parseInt(offset) })
})

// GET /api/periodic — data for periodic table view
app.get('/api/periodic', (req, res) => {
  const db = getDb()
  const elements = db.prepare(`
    SELECT
      l1.id, l1.name, l1.description,
      l1.l0_id, l0.name as l0_name,
      l1.domain_id, d.name as domain_name, d.color as domain_color,
      COUNT(l3.id) as feature_count,
      pp.element_symbol, pp.period, pp.group_num, pp.category
    FROM capabilities_l1 l1
    JOIN capabilities_l0 l0 ON l1.l0_id = l0.id
    JOIN domains d ON l1.domain_id = d.id
    LEFT JOIN capabilities_l2 l2 ON l2.l1_id = l1.id
    LEFT JOIN capabilities_l3 l3 ON l3.l2_id = l2.id
    LEFT JOIN periodic_positions pp ON pp.capability_id = l1.id
    GROUP BY l1.id
    ORDER BY pp.period, pp.group_num
  `).all()
  db.close()
  res.json(elements)
})

// GET /api/stats
app.get('/api/stats', (req, res) => {
  const db = getDb()
  const stats = {
    domains: db.prepare(`SELECT COUNT(*) as c FROM domains`).get().c,
    l0: db.prepare(`SELECT COUNT(*) as c FROM capabilities_l0`).get().c,
    l1: db.prepare(`SELECT COUNT(*) as c FROM capabilities_l1`).get().c,
    l2: db.prepare(`SELECT COUNT(*) as c FROM capabilities_l2`).get().c,
    l3: db.prepare(`SELECT COUNT(*) as c FROM capabilities_l3`).get().c,
    regulatory_frameworks: db.prepare(`SELECT COUNT(*) as c FROM regulatory_frameworks`).get().c,
    by_domain: db.prepare(`
      SELECT d.name, d.color, COUNT(l3.id) as features
      FROM domains d
      LEFT JOIN capabilities_l0 l0 ON l0.domain_id = d.id
      LEFT JOIN capabilities_l1 l1 ON l1.l0_id = l0.id
      LEFT JOIN capabilities_l2 l2 ON l2.l1_id = l1.id
      LEFT JOIN capabilities_l3 l3 ON l3.l2_id = l2.id
      GROUP BY d.id ORDER BY features DESC
    `).all(),
    by_maturity: db.prepare(`
      SELECT maturity, COUNT(*) as count FROM capabilities_l3 GROUP BY maturity
    `).all(),
  }
  db.close()
  res.json(stats)
})

// GET /api/export?domain=&maturity=&q= — Excel export
app.get('/api/export', async (req, res) => {
  const db = getDb()
  const { q, domain, maturity } = req.query

  let where = []
  let params = []
  if (q) { where.push(`(l3.name LIKE ? OR l3.description LIKE ?)`); params.push(`%${q}%`, `%${q}%`) }
  if (domain) { where.push(`l3.domain_id = ?`); params.push(domain) }
  if (maturity) { where.push(`l3.maturity = ?`); params.push(maturity) }
  const whereClause = where.length ? `WHERE ${where.join(' AND ')}` : ''

  const features = db.prepare(`
    SELECT
      d.name as Domain,
      l0.name as "Enterprise Competency (L0)",
      l1.name as "Business Capability (L1)",
      l2.name as "Technical Capability (L2)",
      l3.id as "Feature ID",
      l3.name as "Feature (L3)",
      l3.description as Description,
      l3.maturity as Maturity
    FROM capabilities_l3 l3
    JOIN capabilities_l2 l2 ON l3.l2_id = l2.id
    JOIN capabilities_l1 l1 ON l3.l1_id = l1.id
    JOIN capabilities_l0 l0 ON l3.l0_id = l0.id
    JOIN domains d ON l3.domain_id = d.id
    ${whereClause}
    ORDER BY d.sort_order, l3.sort_order
  `).all(...params)

  db.close()

  const workbook = new ExcelJS.Workbook()
  const sheet = workbook.addWorksheet('DA Capability Map')

  sheet.columns = [
    { header: 'Domain', key: 'Domain', width: 25 },
    { header: 'L0 Enterprise Competency', key: 'Enterprise Competency (L0)', width: 35 },
    { header: 'L1 Business Capability', key: 'Business Capability (L1)', width: 35 },
    { header: 'L2 Technical Capability', key: 'Technical Capability (L2)', width: 35 },
    { header: 'Feature ID', key: 'Feature ID', width: 15 },
    { header: 'L3 Feature', key: 'Feature (L3)', width: 45 },
    { header: 'Description', key: 'Description', width: 60 },
    { header: 'Maturity', key: 'Maturity', width: 15 },
  ]

  const headerRow = sheet.getRow(1)
  headerRow.font = { bold: true, color: { argb: 'FFFFFFFF' } }
  headerRow.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF1a237e' } }
  headerRow.height = 22

  features.forEach(f => sheet.addRow(f))

  sheet.autoFilter = { from: 'A1', to: 'H1' }

  res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  res.setHeader('Content-Disposition', `attachment; filename="da-capability-map-${Date.now()}.xlsx"`)
  await workbook.xlsx.write(res)
  res.end()
})

// GET /api/roles
app.get('/api/roles', (req, res) => {
  const db = getDb()
  const roles = db.prepare(`SELECT * FROM roles ORDER BY id`).all()
  db.close()
  res.json(roles)
})

// GET /api/roles/:roleId/capabilities
app.get('/api/roles/:roleId/capabilities', (req, res) => {
  const db = getDb()
  const { domain, maturity } = req.query
  let where = [`cr.role_id = ?`]
  let params = [req.params.roleId]
  if (domain) { where.push(`l3.domain_id = ?`); params.push(domain) }
  if (maturity) { where.push(`l3.maturity = ?`); params.push(maturity) }
  const features = db.prepare(`
    SELECT l3.*, l2.name as l2_name, l1.name as l1_name, l0.name as l0_name,
           d.name as domain_name, d.color as domain_color
    FROM capability_roles cr
    JOIN capabilities_l3 l3 ON cr.capability_id = l3.id
    JOIN capabilities_l2 l2 ON l3.l2_id = l2.id
    JOIN capabilities_l1 l1 ON l3.l1_id = l1.id
    JOIN capabilities_l0 l0 ON l3.l0_id = l0.id
    JOIN domains d ON l3.domain_id = d.id
    WHERE ${where.join(' AND ')}
    ORDER BY l3.domain_id, l3.priority DESC, l3.sort_order
  `).all(...params)
  db.close()
  res.json(features)
})

// GET /api/tags
app.get('/api/tags', (req, res) => {
  const db = getDb()
  const tags = db.prepare(`
    SELECT t.id, t.name, COUNT(ct.capability_id) as usage_count
    FROM tags t
    LEFT JOIN capability_tags ct ON ct.tag_id = t.id
    GROUP BY t.id ORDER BY usage_count DESC
  `).all()
  db.close()
  res.json(tags)
})

// GET /api/gap?domain= — gap analysis: L3s grouped by priority with coverage placeholder
app.get('/api/gap', (req, res) => {
  const db = getDb()
  const { domain, role } = req.query
  let where = []
  let params = []
  if (domain) { where.push(`l3.domain_id = ?`); params.push(domain) }
  if (role) {
    where.push(`EXISTS (SELECT 1 FROM capability_roles cr WHERE cr.capability_id = l3.id AND cr.role_id = ?)`)
    params.push(role)
  }
  const wc = where.length ? `WHERE ${where.join(' AND ')}` : ''

  const features = db.prepare(`
    SELECT l3.id, l3.name, l3.description, l3.maturity, l3.priority,
           l3.domain_id, d.name as domain_name, d.color as domain_color,
           l2.name as l2_name, l1.name as l1_name, l0.name as l0_name
    FROM capabilities_l3 l3
    JOIN capabilities_l2 l2 ON l3.l2_id = l2.id
    JOIN capabilities_l1 l1 ON l3.l1_id = l1.id
    JOIN capabilities_l0 l0 ON l3.l0_id = l0.id
    JOIN domains d ON l3.domain_id = d.id
    ${wc}
    ORDER BY l3.priority DESC, l3.domain_id, l3.sort_order
  `).all(...params)

  const by_priority = { 5: [], 4: [], 3: [], 1: [] }
  for (const f of features) {
    const p = f.priority || 3
    const bucket = p >= 5 ? 5 : p >= 4 ? 4 : p >= 3 ? 3 : 1
    by_priority[bucket].push(f)
  }

  const domain_summary = db.prepare(`
    SELECT l3.domain_id, d.name, d.color,
           COUNT(l3.id) as total,
           SUM(CASE WHEN l3.priority >= 4 THEN 1 ELSE 0 END) as high_priority,
           SUM(CASE WHEN l3.maturity IN ('mature','established') THEN 1 ELSE 0 END) as mature_count
    FROM capabilities_l3 l3
    JOIN domains d ON l3.domain_id = d.id
    ${wc}
    GROUP BY l3.domain_id ORDER BY d.sort_order
  `).all(...params)

  db.close()
  res.json({ features, by_priority, domain_summary })
})

// GET /api/regulations
app.get('/api/regulations', (req, res) => {
  const db = getDb()
  const { jurisdiction } = req.query
  let frameworks
  if (jurisdiction) {
    frameworks = db.prepare(`SELECT * FROM regulatory_frameworks WHERE jurisdiction_id = ? ORDER BY name`).all(jurisdiction)
  } else {
    frameworks = db.prepare(`SELECT * FROM regulatory_frameworks ORDER BY jurisdiction, name`).all()
  }
  db.close()
  res.json(frameworks)
})

// Serve index for all non-API routes (SPA)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'))
})

app.listen(PORT, () => {
  console.log(`DA Capability Map running at http://localhost:${PORT}`)
})
