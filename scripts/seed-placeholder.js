#!/usr/bin/env node
// Seed a placeholder database so the website works while research workflow completes

const Database = require('better-sqlite3')
const fs = require('fs')
const path = require('path')

const DB_PATH = path.join(__dirname, '../data/capabilities.db')
const SCHEMA_PATH = path.join(__dirname, '../src/schema.sql')
const schema = fs.readFileSync(SCHEMA_PATH, 'utf8')

if (!fs.existsSync(path.dirname(DB_PATH))) {
  fs.mkdirSync(path.dirname(DB_PATH), { recursive: true })
}
if (fs.existsSync(DB_PATH)) fs.unlinkSync(DB_PATH)

const db = new Database(DB_PATH)
db.exec(schema)

const DOMAINS = [
  { id: 'custody', name: 'Digital Asset Custody', color: '#f59e0b', icon: '🏦', sort: 1 },
  { id: 'wallets', name: 'Wallet Infrastructure', color: '#10b981', icon: '👛', sort: 2 },
  { id: 'stablecoins', name: 'Stablecoins', color: '#6366f1', icon: '💵', sort: 3 },
  { id: 'cbdc', name: 'CBDC & Digital Money', color: '#ec4899', icon: '🏛️', sort: 4 },
  { id: 'settlement', name: 'Settlement & Clearing', color: '#14b8a6', icon: '⚡', sort: 5 },
  { id: 'tokenisation', name: 'Tokenisation & RWA', color: '#f97316', icon: '🔖', sort: 6 },
  { id: 'defi_protocols', name: 'DeFi & Protocols', color: '#8b5cf6', icon: '🔗', sort: 7 },
  { id: 'security', name: 'Security & Risk', color: '#ef4444', icon: '🛡️', sort: 8 },
  { id: 'ai_agentic', name: 'AI & Agentic Systems', color: '#06b6d4', icon: '🤖', sort: 9 },
  { id: 'compliance_regulation', name: 'Compliance & Regulation', color: '#84cc16', icon: '📋', sort: 10 },
]

// Sample capability data (subset — full data from workflow will replace this)
const SAMPLE = {
  custody: {
    l0: [
      { name: 'Institutional Digital Asset Custody', desc: 'Bank-grade safekeeping of digital assets for institutional clients', l1s: [
        { name: 'Qualified Custodian Services', desc: 'SEC/CFTC qualified custodian for digital assets', l2s: [
          { name: 'Regulatory Compliance Infrastructure', desc: 'Systems to maintain qualified custodian status', l3s: [
            { name: 'SEC Rule 17f-1 Digital Asset Compliance', desc: 'Custody of digital assets under Rule 17f-1 safekeeping requirements', maturity: 'developing' },
            { name: 'CFTC DCO Custodian Registration', desc: 'Registration as derivatives clearing organisation custodian for crypto', maturity: 'emerging' },
            { name: 'OCC Non-Depository Trust Charter', desc: 'National trust charter for crypto custody under OCC interpretive letters 2020/21', maturity: 'established' },
            { name: 'State Trust Charter (Wyoming SPDI)', desc: 'Special Purpose Depository Institution charter for digital asset custody', maturity: 'established' },
            { name: 'FCA CASS 7 Digital Asset Compliance', desc: 'UK client asset custody rules adapted for cryptoassets', maturity: 'developing' },
            { name: 'MiCA Article 70-76 Custody Requirements', desc: 'EU MiCA custody obligations for CASPs', maturity: 'developing' },
          ]}
        ]},
        { name: 'Cold Storage Management', desc: 'Offline key and asset storage for maximum security', l2s: [
          { name: 'Air-Gapped Signing Infrastructure', desc: 'Physically isolated signing systems for cold storage', l3s: [
            { name: 'Air-Gap Hardware Wallet Integration', desc: 'Integration with Ledger Enterprise, Trezor Model T for cold signing', maturity: 'established' },
            { name: 'Faraday Cage Key Storage', desc: 'Physical electromagnetic shielding for hardware security modules', maturity: 'mature' },
            { name: 'Geographic Redundancy (N+1 Vaults)', desc: 'Multi-jurisdiction cold storage vault replication', maturity: 'established' },
            { name: 'Multi-Person Authorisation (MPA)', desc: 'Quorum-based approval for cold wallet operations', maturity: 'established' },
          ]}
        ]},
      ]}
    ]
  },
  compliance_regulation: {
    l0: [
      { name: 'AML/CFT Compliance for Digital Assets', desc: 'Anti-money laundering and counter-terrorist financing across the digital asset stack', l1s: [
        { name: 'Travel Rule Compliance', desc: 'FATF Recommendation 16 implementation for virtual asset transfers', l2s: [
          { name: 'VASP Data Exchange Platform', desc: 'Technology for sharing originator/beneficiary data between VASPs', l3s: [
            { name: 'IVMS101 Message Standard Implementation', desc: 'InterVASP Messaging Standard v1.0 for Travel Rule data', maturity: 'established' },
            { name: 'OpenVASP Protocol Integration', desc: 'Decentralised Travel Rule protocol integration', maturity: 'developing' },
            { name: 'Notabene Network Integration', desc: 'Third-party Travel Rule compliance network', maturity: 'established' },
            { name: 'TRP (Travel Rule Protocol) Adoption', desc: 'Industry-standard Travel Rule protocol by TRISA', maturity: 'developing' },
            { name: 'Sygna Bridge Integration', desc: 'CoolBitX Sygna Bridge for Travel Rule', maturity: 'established' },
            { name: 'VerifyVASP Network Connection', desc: 'Korean-origin VASP verification and Travel Rule network', maturity: 'developing' },
          ]}
        ]},
      ]}
    ]
  },
}

const insertDomain = db.prepare(`INSERT INTO domains VALUES (?,?,?,?,?,?)`)
const insertL0 = db.prepare(`INSERT INTO capabilities_l0 VALUES (?,?,?,?,?)`)
const insertL1 = db.prepare(`INSERT INTO capabilities_l1 VALUES (?,?,?,?,?,?)`)
const insertL2 = db.prepare(`INSERT INTO capabilities_l2 VALUES (?,?,?,?,?,?,?)`)
const insertL3 = db.prepare(`INSERT INTO capabilities_l3 VALUES (?,?,?,?,?,?,?,?,?)`)
const insertPos = db.prepare(`INSERT INTO periodic_positions VALUES (?,?,?,?,?)`)

const seed = db.transaction(() => {
  let l3Count = 0
  const DOMAIN_COLS = {
    custody:[1,2], wallets:[3,4], stablecoins:[5,6], cbdc:[7,8],
    settlement:[9,10], tokenisation:[11,12], defi_protocols:[13,14],
    security:[15,16], ai_agentic:[17], compliance_regulation:[18],
  }
  const colPeriod = {}

  for (const d of DOMAINS) {
    insertDomain.run(d.id, d.name, null, d.color, d.icon, d.sort)

    const sampleDomain = SAMPLE[d.id]
    if (sampleDomain) {
      let l0Idx = 0
      for (const l0 of sampleDomain.l0) {
        const l0id = `${d.id}-l0-${l0Idx}`
        insertL0.run(l0id, d.id, l0.name, l0.desc, l0Idx)

        let l1Idx = 0
        for (const l1 of l0.l1s) {
          const l1id = `${l0id}-l1-${l1Idx}`
          insertL1.run(l1id, l0id, d.id, l1.name, l1.desc, l1Idx)

          const cols = DOMAIN_COLS[d.id] || [1]
          const col = cols[l1Idx % cols.length]
          if (!colPeriod[col]) colPeriod[col] = 1
          const sym = l1.name.split(/\s+/).slice(0,2).map(w=>w[0]).join('').toUpperCase()
          insertPos.run(l1id, sym, colPeriod[col], col, d.id)
          colPeriod[col]++

          let l2Idx = 0
          for (const l2 of l1.l2s) {
            const l2id = `${l1id}-l2-${l2Idx}`
            insertL2.run(l2id, l1id, l0id, d.id, l2.name, l2.desc, l2Idx)

            let l3Idx = 0
            for (const l3 of l2.l3s) {
              const l3id = `${l2id}-l3-${l3Idx}`
              insertL3.run(l3id, l2id, l1id, l0id, d.id, l3.name, l3.desc, l3.maturity, l3Idx)
              l3Count++
              l3Idx++
            }
            l2Idx++
          }
          l1Idx++
        }
        l0Idx++
      }
    }
  }

  console.log(`Placeholder seed: ${l3Count} L3 features`)
})

seed()
db.close()
console.log('Placeholder DB ready:', DB_PATH)
