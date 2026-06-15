#!/usr/bin/env python3
"""Augment DA Capability Map DB with:
  1. Expanded jurisdictions (20 markets)
  2. Periodic table positions for all L1s
  3. Roles + capability_roles mapping
  4. Thematic tags + capability_tags
  5. Priority scores on L3 features
  6. Additional regulatory frameworks for new markets
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'capabilities.db')

# ---------------------------------------------------------------------------
# 1. Additional markets
# ---------------------------------------------------------------------------
NEW_MARKETS = [
    ('in', 'India', 'Asia-Pacific'),
    ('kr', 'South Korea', 'Asia-Pacific'),
    ('br', 'Brazil', 'Americas'),
    ('lu', 'Luxembourg', 'Europe'),
    ('de', 'Germany', 'Europe'),
    ('li', 'Liechtenstein', 'Europe'),
    ('bm', 'Bermuda', 'Americas'),
    ('ky', 'Cayman Islands', 'Americas'),
    ('za', 'South Africa', 'Africa'),
    ('mx', 'Mexico', 'Americas'),
]

# ---------------------------------------------------------------------------
# 2. Additional regulatory frameworks for new markets
# ---------------------------------------------------------------------------
NEW_FRAMEWORKS = [
    ('sebi_crypto', 'SEBI Crypto / VDA Framework (India)', 'SEBI VDA', 'India SEBI regulation of virtual digital assets', 'developing', '2023-03-01', 'SEBI/RBI', 'in', 'in'),
    ('fsc_vaa', 'Financial Services Commission Virtual Asset Act (South Korea)', 'FSC VAA', 'South Korea FSC Virtual Asset User Protection Act', 'in_force', '2024-07-19', 'FSC/FSS', 'kr', 'kr'),
    ('bcb_crypto', 'BCB/CVM Virtual Asset Resolution (Brazil)', 'BCB Crypto', 'Brazil BCB regulation for virtual asset service providers', 'in_force', '2023-06-01', 'BCB/CVM', 'br', 'br'),
    ('cssf_dlt', 'CSSF DLT Pilot and Tokenisation Framework (Luxembourg)', 'CSSF DLT', 'Luxembourg CSSF framework for DLT-based funds and securities', 'in_force', '2023-03-02', 'CSSF', 'lu', 'lu'),
    ('bafin_crypto', 'BaFin Crypto Custody and MiCA Implementation (Germany)', 'BaFin Crypto', 'Germany BaFin crypto custody licence and MiCA implementation', 'in_force', '2023-01-01', 'BaFin', 'de', 'de'),
    ('fma_blockchain', 'FMA Blockchain Act (Liechtenstein)', 'FMA Blockchain Act', 'Liechtenstein FMA Token and Trusted Technology Service Provider Act (TVTG)', 'in_force', '2020-01-01', 'FMA', 'li', 'li'),
    ('bma_daba', 'BMA Digital Asset Business Act (Bermuda)', 'BMA DABA', 'Bermuda Monetary Authority Digital Asset Business Act', 'in_force', '2018-09-10', 'BMA', 'bm', 'bm'),
    ('cima_vasp', 'CIMA Virtual Asset Service Provider Framework (Cayman)', 'CIMA VASP', 'Cayman Islands CIMA VASP registration and regulation', 'in_force', '2020-10-31', 'CIMA', 'ky', 'ky'),
    ('fsca_casp', 'FSCA Crypto Asset Service Provider (South Africa)', 'FSCA CASP', 'South Africa FSCA mandatory CASP registration regime', 'in_force', '2023-06-01', 'FSCA', 'za', 'za'),
    ('cnbv_fintech', 'CNBV Fintech Law Virtual Assets (Mexico)', 'CNBV Fintech', 'Mexico CNBV Fintech Law virtual asset regulation', 'in_force', '2018-03-09', 'CNBV/Banxico', 'mx', 'mx'),
]

# New market mappings for existing domains
NEW_DOMAIN_MARKET_MAP = {
    'custody': ['in', 'kr', 'lu', 'de', 'bm'],
    'wallets': ['in', 'kr', 'bm'],
    'stablecoins': ['in', 'kr', 'br', 'lu', 'bm'],
    'cbdc': ['in', 'kr', 'br'],
    'settlement': ['in', 'kr', 'lu', 'de'],
    'tokenisation': ['lu', 'de', 'li', 'bm', 'ky'],
    'defi_protocols': ['bm', 'ky', 'kr'],
    'security': ['in', 'kr', 'bm'],
    'ai_agentic': ['in', 'kr'],
    'compliance_regulation': ['in', 'kr', 'br', 'lu', 'de', 'li', 'bm', 'ky', 'za', 'mx'],
}

# ---------------------------------------------------------------------------
# 3. Periodic table positions for L1s
# Domain layout: assign L1s sequentially, 18 columns, domain as category
# ---------------------------------------------------------------------------
def build_periodic_positions(c):
    # Get all L1s ordered by domain sort_order then l1 sort_order
    c.execute('''SELECT l1.id, l1.name, l1.domain_id, d.sort_order as dord, l1.sort_order as lord
                 FROM capabilities_l1 l1 JOIN domains d ON l1.domain_id=d.id
                 ORDER BY d.sort_order, l1.sort_order''')
    l1s = c.fetchall()

    COLS = 18

    # Generate 2-char abbreviations from L1 name
    def abbr(name):
        words = name.upper().split()
        # Remove common filler words
        stop = {'AND','&','OF','FOR','IN','THE','A','AN','TO','AT','WITH','BY'}
        words = [w for w in words if w not in stop]
        if len(words) >= 2:
            return words[0][0] + words[1][0]
        return name[:2].upper()

    positions = []
    row, col = 1, 1
    prev_domain = None

    for l1_id, l1_name, domain_id, dord, lord in l1s:
        # Force domain boundary alignment: if new domain and not at start of row, break
        if prev_domain and domain_id != prev_domain:
            if col > 1:
                row += 1
                col = 1
        prev_domain = domain_id

        positions.append({
            'id': l1_id,
            'symbol': abbr(l1_name),
            'period': row,
            'group_num': col,
            'category': domain_id,
        })

        col += 1
        if col > COLS:
            col = 1
            row += 1

    return positions

# ---------------------------------------------------------------------------
# 4. Roles definition and mapping rules
# ---------------------------------------------------------------------------
ROLES = [
    ('cto', 'Chief Technology Officer', 'Infrastructure, architecture, protocol integration, and platform decisions'),
    ('cro', 'Chief Risk Officer', 'Market, credit, liquidity, operational and technology risk'),
    ('cco', 'Chief Compliance Officer', 'AML/CFT, KYC, Travel Rule, regulatory reporting across jurisdictions'),
    ('cfo', 'CFO / Treasury', 'Reserve management, collateral, liquidity, treasury, accounting'),
    ('front_office', 'Front Office / Trading', 'Trading infrastructure, DeFi access, tokenised product distribution'),
    ('operations', 'Operations / COO', 'Settlement workflows, custody ops, reconciliation, client servicing'),
    ('product', 'Product & Strategy', 'Capability roadmap, new product development, market strategy'),
    ('audit', 'Internal Audit / Second Line', 'Assurance, control testing, regulatory examination support'),
]

# Domain → primary roles
DOMAIN_ROLE_MAP = {
    'custody': ['cto', 'cro', 'operations', 'audit'],
    'wallets': ['cto', 'operations', 'product'],
    'stablecoins': ['cfo', 'cco', 'product', 'cro'],
    'cbdc': ['product', 'cfo', 'cco', 'cto'],
    'settlement': ['operations', 'cro', 'cfo', 'cto'],
    'tokenisation': ['product', 'front_office', 'cfo', 'operations'],
    'defi_protocols': ['front_office', 'cro', 'cco', 'product'],
    'security': ['cto', 'cro', 'audit'],
    'ai_agentic': ['cto', 'cro', 'product', 'cco'],
    'compliance_regulation': ['cco', 'cro', 'audit', 'cfo'],
}

# ---------------------------------------------------------------------------
# 5. Tags definition and keyword-to-tag mapping
# ---------------------------------------------------------------------------
TAGS = [
    'MPC', 'HSM', 'ZK-Proof', 'CBDC', 'DeFi', 'AI-ML', 'Staking',
    'Tokenisation', 'AML-CFT', 'Sanctions', 'Travel-Rule', 'Basel-III',
    'MiCA', 'DORA', 'Smart-Contract', 'Cross-Chain', 'Settlement',
    'Collateral', 'Stablecoin', 'Key-Management', 'Custody', 'Wallet',
    'Security', 'Compliance', 'Analytics', 'NFT', 'PoS', 'DvP', 'FX',
    'Reporting', 'KYC', 'Lending', 'Derivatives', 'Insurance', 'Oracle',
    'MEV', 'Bridge', 'Liquidity', 'Governance', 'Privacy', 'Encryption',
    'API', 'Audit', 'Risk', 'FATF',
]

# Tag → keywords (match against L3 name)
TAG_KEYWORDS = {
    'MPC':           ['mpc', 'multi-party', 'threshold signing', 'tss'],
    'HSM':           ['hsm', 'hardware security module', 'fips'],
    'ZK-Proof':      ['zk', 'zero-knowledge', 'zk-snark', 'zk-proof', 'merkle proof'],
    'CBDC':          ['cbdc', 'digital pound', 'digital euro', 'cbdc', 'digital currency', 'wCBDC', 'e-hkd'],
    'DeFi':          ['defi', 'amm', 'dex', 'liquidity pool', 'protocol', 'uniswap', 'aave', 'yield', 'dao'],
    'AI-ML':         ['ai', 'ml', 'machine learning', 'llm', 'neural network', 'nlp', 'model', 'mlops'],
    'Staking':       ['staking', 'validator', 'pos', 'proof of stake', 'slashing', 'liquid staking'],
    'Tokenisation':  ['tokenis', 'tokeniz', 'rwa', 'real world asset', 'digital bond', 'tokenised'],
    'AML-CFT':       ['aml', 'cft', 'money laundering', 'typology', 'sar', 'str', 'fiu'],
    'Sanctions':     ['sanction', 'ofac', 'sdl', 'sdn', 'ofsi', 'un sanctions', 'eu sanctions'],
    'Travel-Rule':   ['travel rule', 'fatf', 'r16', 'vasp data', 'openvasp', 'trust protocol'],
    'Basel-III':     ['basel', 'rwa', 'pillar 3', 'ccar', 'dfast', 'tier 1'],
    'MiCA':          ['mica', 'casp', 'emt', 'ard', 'esma', 'eba'],
    'DORA':          ['dora', 'ict resilience', 'tlpt', 'digital operational'],
    'Smart-Contract':['smart contract', 'erc-20', 'erc-1400', 'erc-4337', 'gnosis safe', 'solidity'],
    'Cross-Chain':   ['cross-chain', 'bridge', 'ibc', 'htlc', 'interoperability', 'multi-chain'],
    'Settlement':    ['settlement', 'dvp', 'pvp', 'finality', 'fail', 'ssi', 't+0'],
    'Collateral':    ['collateral', 'margin', 'haircut', 'rehypothecation', 'variation margin', 'initial margin'],
    'Stablecoin':    ['stablecoin', 'usdc', 'usdt', 'eurc', 'peg', 'reserve', 'mint', 'burn'],
    'Key-Management':['key manage', 'key ceremony', 'key derivation', 'bip32', 'bip39', 'shamir', 'key backup', 'key recovery'],
    'Custody':       ['custody', 'custodian', 'safekeep', 'vault', 'cold storage'],
    'Wallet':        ['wallet', 'hot wallet', 'warm wallet', 'address', 'utxo'],
    'Security':      ['security', 'penetration', 'red team', 'vulnerability', 'exploit', 'cyber'],
    'Compliance':    ['compliance', 'regulatory', 'regulation', 'licence', 'registration'],
    'Analytics':     ['analytics', 'dashboard', 'reporting', 'monitoring', 'kpi', 'metrics', 'insight'],
    'NFT':           ['nft', 'erc-721', 'non-fungible', 'collectible'],
    'PoS':           ['proof of stake', 'validator', 'ethereum staking', 'eth2'],
    'DvP':           ['dvp', 'delivery versus', 'delivery-versus'],
    'FX':            ['fx', 'foreign exchange', 'pvp', 'herstatt', 'cross-border'],
    'Reporting':     ['report', 'disclosure', 'fil', 'return', 'submission'],
    'KYC':           ['kyc', 'know your customer', 'customer due diligence', 'cdd', 'edd', 'ubo'],
    'Lending':       ['lending', 'borrowing', 'loan', 'credit', 'repo', 'securities lending'],
    'Derivatives':   ['derivative', 'futures', 'options', 'swap', 'perpetual', 'structured product'],
    'Insurance':     ['insurance', 'indemnity', 'cover', 'premium', 'parametric'],
    'Oracle':        ['oracle', 'price feed', 'chainlink', 'off-chain data'],
    'MEV':           ['mev', 'maximal extractable', 'front-run', 'sandwich', 'mempool'],
    'Bridge':        ['bridge', 'cross-chain', 'htlc', 'ibc', 'lock-and-mint'],
    'Liquidity':     ['liquidity', 'liquid', 'slippage', 'depth', 'market making', 'market maker'],
    'Governance':    ['governance', 'voting', 'proposal', 'multisig approval', 'dao'],
    'Privacy':       ['privacy', 'gdpr', 'pii', 'data protection', 'anonymity', 'zero-knowledge'],
    'Encryption':    ['encrypt', 'decrypt', 'aes', 'tls', 'cipher', 'at rest'],
    'API':           ['api', 'rest', 'graphql', 'webhook', 'sdk', 'endpoint'],
    'Audit':         ['audit', 'soc 2', 'iso 27001', 'control testing', 'assurance'],
    'Risk':          ['risk', 'exposure', 'limit', 'stress', 'scenario'],
    'FATF':          ['fatf', 'financial action task force', 'travel rule', 'r16'],
}


def get_tags_for_name(name_lower):
    matched = set()
    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                matched.add(tag)
                break
    return matched


# ---------------------------------------------------------------------------
# Priority mapping
# ---------------------------------------------------------------------------
MATURITY_PRIORITY = {
    'mature': 5,
    'established': 4,
    'developing': 3,
    'emerging': 1,
}


# ---------------------------------------------------------------------------
# Main augment function
# ---------------------------------------------------------------------------
def augment(conn):
    c = conn.cursor()

    # ── 1. New markets ─────────────────────────────────────────────────────
    print('Adding new markets...')
    for row in NEW_MARKETS:
        c.execute('INSERT OR IGNORE INTO markets (id, name, region) VALUES (?,?,?)', row)

    # ── 2. New regulatory frameworks ───────────────────────────────────────
    print('Adding new regulatory frameworks...')
    for row in NEW_FRAMEWORKS:
        c.execute('''INSERT OR IGNORE INTO regulatory_frameworks
                     (id, name, short_name, description, status, effective_date, regulator, jurisdiction, jurisdiction_id)
                     VALUES (?,?,?,?,?,?,?,?,?)''', row)

    # ── 2b. Link new markets to L3 features ────────────────────────────────
    print('Linking new markets to capabilities...')
    c.execute('SELECT id, domain_id FROM capabilities_l3')
    all_l3 = c.fetchall()
    for l3_id, domain_id in all_l3:
        for mid in NEW_DOMAIN_MARKET_MAP.get(domain_id, []):
            c.execute('INSERT OR IGNORE INTO capability_markets VALUES (?,?)', (l3_id, mid))

    # Link new frameworks to capabilities by domain
    new_fw_by_domain = {
        'custody': ['bafin_crypto', 'cssf_dlt', 'fma_blockchain', 'bma_daba'],
        'wallets': ['fsc_vaa', 'sebi_crypto'],
        'stablecoins': ['fsc_vaa', 'sebi_crypto', 'bcb_crypto', 'bma_daba'],
        'cbdc': ['sebi_crypto', 'fsc_vaa', 'bcb_crypto'],
        'settlement': ['cssf_dlt', 'bafin_crypto'],
        'tokenisation': ['cssf_dlt', 'fma_blockchain', 'bma_daba', 'cima_vasp'],
        'defi_protocols': ['bma_daba', 'cima_vasp', 'fsc_vaa'],
        'security': ['bafin_crypto'],
        'ai_agentic': ['sebi_crypto', 'fsc_vaa'],
        'compliance_regulation': ['sebi_crypto', 'fsc_vaa', 'bcb_crypto', 'cssf_dlt',
                                   'bafin_crypto', 'fma_blockchain', 'bma_daba', 'cima_vasp',
                                   'fsca_casp', 'cnbv_fintech'],
    }
    for l3_id, domain_id in all_l3:
        for fid in new_fw_by_domain.get(domain_id, []):
            c.execute('INSERT OR IGNORE INTO capability_regulations VALUES (?,?)', (l3_id, fid))

    # ── 3. Periodic table positions ─────────────────────────────────────────
    print('Building periodic positions...')
    c.execute('DELETE FROM periodic_positions')
    positions = build_periodic_positions(c)
    for p in positions:
        c.execute('''INSERT OR REPLACE INTO periodic_positions
                     (capability_id, element_symbol, period, group_num, category)
                     VALUES (?,?,?,?,?)''',
                  (p['id'], p['symbol'], p['period'], p['group_num'], p['category']))
    print(f'  Assigned {len(positions)} L1s to periodic positions')

    # ── 4. Roles ────────────────────────────────────────────────────────────
    print('Setting up roles...')
    c.execute('''CREATE TABLE IF NOT EXISTS roles (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS capability_roles (
        capability_id TEXT NOT NULL,
        role_id TEXT NOT NULL REFERENCES roles(id),
        PRIMARY KEY (capability_id, role_id)
    )''')

    for role_id, role_name, role_desc in ROLES:
        c.execute('INSERT OR REPLACE INTO roles (id, name, description) VALUES (?,?,?)',
                  (role_id, role_name, role_desc))

    c.execute('DELETE FROM capability_roles')
    # Map L3 features to roles via domain
    for l3_id, domain_id in all_l3:
        for role_id in DOMAIN_ROLE_MAP.get(domain_id, []):
            c.execute('INSERT OR IGNORE INTO capability_roles VALUES (?,?)', (l3_id, role_id))

    # ── 5. Tags ─────────────────────────────────────────────────────────────
    print('Setting up tags...')
    c.execute('DELETE FROM capability_tags')
    c.execute('DELETE FROM tags')

    tag_id_map = {}
    for tag_name in TAGS:
        c.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
        tag_id_map[tag_name] = c.lastrowid

    # Tag L3 features by keyword matching
    c.execute('SELECT id, name, description FROM capabilities_l3')
    l3_features = c.fetchall()
    tag_links = 0
    for l3_id, name, desc in l3_features:
        text = (name or '').lower() + ' ' + (desc or '').lower()
        matched_tags = get_tags_for_name(text)
        for tag in matched_tags:
            tid = tag_id_map.get(tag)
            if tid:
                c.execute('INSERT OR IGNORE INTO capability_tags VALUES (?,3,?)', (l3_id, tid))
                tag_links += 1
    print(f'  Created {tag_links} tag links across {len(l3_features)} features')

    # ── 6. Priority scores ──────────────────────────────────────────────────
    print('Adding priority scores...')
    try:
        c.execute('ALTER TABLE capabilities_l3 ADD COLUMN priority INTEGER DEFAULT 3')
        print('  Added priority column')
    except Exception:
        print('  Priority column already exists')

    for maturity, priority in MATURITY_PRIORITY.items():
        c.execute('UPDATE capabilities_l3 SET priority = ? WHERE maturity = ?', (priority, maturity))

    # Add priority to export query: also update periodic_positions
    try:
        c.execute('ALTER TABLE capabilities_l3 ADD COLUMN implementation_notes TEXT')
    except Exception:
        pass

    conn.commit()


def report(conn):
    c = conn.cursor()
    print('\n── Augmentation Report ──')
    c.execute('SELECT COUNT(*) FROM markets')
    print(f'Markets: {c.fetchone()[0]}')
    c.execute('SELECT COUNT(*) FROM regulatory_frameworks')
    print(f'Regulatory frameworks: {c.fetchone()[0]}')
    c.execute('SELECT COUNT(*) FROM periodic_positions')
    print(f'Periodic positions: {c.fetchone()[0]}')
    try:
        c.execute('SELECT COUNT(*) FROM roles')
        print(f'Roles: {c.fetchone()[0]}')
        c.execute('SELECT COUNT(*) FROM capability_roles')
        print(f'Capability-role links: {c.fetchone()[0]}')
    except Exception:
        pass
    c.execute('SELECT COUNT(*) FROM tags')
    print(f'Tags: {c.fetchone()[0]}')
    c.execute('SELECT COUNT(*) FROM capability_tags')
    print(f'Tag links: {c.fetchone()[0]}')
    c.execute('SELECT priority, COUNT(*) FROM capabilities_l3 GROUP BY priority ORDER BY priority DESC')
    print('Priority distribution:')
    for r in c.fetchall():
        print(f'  P{r[0]}: {r[1]} features')
    c.execute('SELECT COUNT(*) FROM capability_markets')
    print(f'Total market links: {c.fetchone()[0]}')
    c.execute('SELECT COUNT(*) FROM capability_regulations')
    print(f'Total regulation links: {c.fetchone()[0]}')


if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    print('Augmenting DA Capability Map...')
    augment(conn)
    report(conn)
    conn.close()
    print('\nDone.')
