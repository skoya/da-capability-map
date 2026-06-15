-- DA Capability Map Schema

CREATE TABLE IF NOT EXISTS domains (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  color TEXT,
  icon TEXT,
  sort_order INTEGER
);

CREATE TABLE IF NOT EXISTS capabilities_l0 (
  id TEXT PRIMARY KEY,
  domain_id TEXT NOT NULL REFERENCES domains(id),
  name TEXT NOT NULL,
  description TEXT,
  sort_order INTEGER
);

CREATE TABLE IF NOT EXISTS capabilities_l1 (
  id TEXT PRIMARY KEY,
  l0_id TEXT NOT NULL REFERENCES capabilities_l0(id),
  domain_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  sort_order INTEGER
);

CREATE TABLE IF NOT EXISTS capabilities_l2 (
  id TEXT PRIMARY KEY,
  l1_id TEXT NOT NULL REFERENCES capabilities_l1(id),
  l0_id TEXT NOT NULL,
  domain_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  sort_order INTEGER
);

CREATE TABLE IF NOT EXISTS capabilities_l3 (
  id TEXT PRIMARY KEY,
  l2_id TEXT NOT NULL REFERENCES capabilities_l2(id),
  l1_id TEXT NOT NULL,
  l0_id TEXT NOT NULL,
  domain_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  maturity TEXT CHECK(maturity IN ('emerging','developing','established','mature')),
  sort_order INTEGER
);

CREATE TABLE IF NOT EXISTS tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS capability_tags (
  capability_id TEXT NOT NULL,
  capability_level INTEGER NOT NULL,
  tag_id INTEGER NOT NULL REFERENCES tags(id),
  PRIMARY KEY (capability_id, capability_level, tag_id)
);

CREATE TABLE IF NOT EXISTS markets (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  region TEXT
);

CREATE TABLE IF NOT EXISTS capability_markets (
  capability_id TEXT NOT NULL,
  market_id TEXT NOT NULL REFERENCES markets(id),
  PRIMARY KEY (capability_id, market_id)
);

CREATE TABLE IF NOT EXISTS regulatory_frameworks (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  short_name TEXT,
  description TEXT,
  status TEXT,
  effective_date TEXT,
  regulator TEXT,
  jurisdiction TEXT,
  jurisdiction_id TEXT
);

CREATE TABLE IF NOT EXISTS capability_regulations (
  capability_id TEXT NOT NULL,
  framework_id TEXT NOT NULL REFERENCES regulatory_frameworks(id),
  PRIMARY KEY (capability_id, framework_id)
);

-- Periodic table positioning
CREATE TABLE IF NOT EXISTS periodic_positions (
  capability_id TEXT PRIMARY KEY,
  element_symbol TEXT NOT NULL,
  period INTEGER NOT NULL,
  group_num INTEGER NOT NULL,
  category TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_l1_l0 ON capabilities_l1(l0_id);
CREATE INDEX IF NOT EXISTS idx_l2_l1 ON capabilities_l2(l1_id);
CREATE INDEX IF NOT EXISTS idx_l3_l2 ON capabilities_l3(l2_id);
CREATE INDEX IF NOT EXISTS idx_l3_domain ON capabilities_l3(domain_id);
CREATE INDEX IF NOT EXISTS idx_l3_maturity ON capabilities_l3(maturity);
