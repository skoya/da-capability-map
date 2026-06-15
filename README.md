# Digital Asset Capability Map

A comprehensive 4-level capability map for digital assets at GSIBs, covering 1000+ features across custody, wallets, stablecoins, CBDC, settlement, regulation, DeFi, security, AI/agentic, tokenisation, RWA, and market infrastructure.

## Structure

- **Level 0** — Enterprise Competencies (e.g. Custody of Digital Assets)
- **Level 1** — Business Capabilities (services across use cases)
- **Level 2** — Technical Capabilities (technology requirements)
- **Level 3** — Features (lowest-level, 1000+)

## Views

- **Periodic Table** — capabilities grouped by domain, similar to element families
- **Tree Navigator** — hierarchical drill-down from L0 → L3
- **Role Dashboard** — filtered views by GSIB role (COO, CTO, Compliance, Risk, Front Office)
- **Regulation Matrix** — capabilities mapped to jurisdictions and regulations
- **Heat Map** — maturity / priority heat map view

## Markets Covered

G7 + extended western: US, UK, EU (MiCA), Switzerland, Singapore, Hong Kong, UAE, Japan, Canada, Australia

## Running Locally

```bash
npm install
npm start
# → http://localhost:3847
```

## Data

- `data/capabilities.db` — SQLite database
- `data/capabilities.json` — full JSON export
- Export to Excel via the website UI (filtered or full)

## Phases

- Phase 1: Research + data model
- Phase 2: Data generation (1000+ features)
- Phase 3: Database + API
- Phase 4: Website (periodic table, tree, role views)
- Phase 5: Excel export + weekly DA integration
