#!/usr/bin/env python3
"""Full seed for DA Capability Map — 1000+ L3 features across 10 domains.

Structure: domain -> [L0] -> [L1] -> [L2] -> [L3]
Each level item: (suffix, name, description, children_or_maturity)
L3 items: (suffix, name, description, maturity_key)
maturity_key: 'e'=emerging, 'd'=developing, 's'=established, 'm'=mature
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'capabilities.db')
M = {'e': 'emerging', 'd': 'developing', 's': 'established', 'm': 'mature'}

# ---------------------------------------------------------------------------
# Domain data  (L0 > L1 > L2 > L3)
# ---------------------------------------------------------------------------

DOMAINS = {

# ── CUSTODY ──────────────────────────────────────────────────────────────────
'custody': [
  ('01', 'Institutional Digital Asset Custody', 'Safekeeping and administration of digital assets for institutional clients', [
    ('01', 'Regulatory Compliance & Licensing', 'Obtaining and maintaining custody licences across jurisdictions', [
      ('01', 'Jurisdiction Licensing', 'Regulatory licence applications and maintenance per market', [
        ('01', 'NYDFS BitLicense custody qualification', 'New York DFS custody licence application and ongoing compliance', 'm'),
        ('02', 'MAS Major Payment Institution licence (DPT)', 'Singapore MAS MPL licence for digital payment token custody', 's'),
        ('03', 'HKMA VASP custody authorisation', 'Hong Kong VASP registration for custody services', 'd'),
        ('04', 'FINMA VQF/SRO membership for custody', 'Swiss regulatory membership for digital asset custody operations', 's'),
        ('05', 'MiCA CASP registration for custody', 'EU MiCA CASP registration for custody across EEA', 'd'),
        ('06', 'FCA cryptoasset business registration', 'UK FCA registration for custody under MLR 2017', 's'),
        ('07', 'SEC qualified custodian rule compliance', 'Meeting SEC proposed qualified custodian rule for investment advisers', 'd'),
        ('08', 'VARA custody licence (Dubai)', 'Dubai VARA licence for digital asset custody operations', 'd'),
        ('09', 'Multi-jurisdiction licence matrix management', 'Tracking and renewing custody licences across 10+ jurisdictions', 'd'),
      ]),
      ('02', 'Client Asset Segregation', 'Holding client assets separately from proprietary assets', [
        ('01', 'On-chain wallet segregation per client', 'Unique wallet addresses assigned per client for on-chain segregation', 'm'),
        ('02', 'Omnibus sub-ledger reconciliation', 'Internal sub-ledger tracking of client balances within pooled wallets', 's'),
        ('03', 'Insolvency-remote structure for client assets', 'Legal structures protecting client assets in custodian insolvency', 's'),
        ('04', 'Real-time segregation audit trail', 'Continuous audit log proving segregation status per client per asset', 'd'),
        ('05', 'Regulatory segregation reporting', 'Automated reports confirming asset segregation ratios to regulators', 'd'),
      ]),
    ]),
    ('02', 'Cold Storage & Key Management', 'Offline key storage systems and cryptographic key lifecycle management', [
      ('01', 'Air-Gapped Signing Infrastructure', 'Hardware and procedures for signing transactions on offline devices', [
        ('01', 'HSM-based air-gapped signing ceremony', 'Structured key ceremony using HSMs in air-gapped environment with M-of-N quorum', 'm'),
        ('02', 'Faraday cage vault operations', 'Electromagnetic shielded vault for hardware key devices', 's'),
        ('03', 'QR-code PSBT relay between online/offline', 'Partially-signed transaction relay via QR codes avoiding network exposure', 's'),
        ('04', 'Video-recorded key ceremony', 'Tamper-evident video documentation of key generation and signing', 's'),
        ('05', 'Dual-control four-eyes signing policy', 'Minimum two authorised operators required for every cold signing event', 'm'),
        ('06', 'Time-locked cold withdrawal queues', 'Enforced time delays on cold-to-hot withdrawals for fraud detection', 's'),
        ('07', 'Geographic distribution of cold vaults', 'Geographically dispersed vault locations for disaster recovery', 's'),
      ]),
      ('02', 'HSM Integration', 'HSM provisioning, clustering, and lifecycle management', [
        ('01', 'FIPS 140-3 Level 3 HSM provisioning', 'Procurement and certification of FIPS 140-3 Level 3 HSMs', 'm'),
        ('02', 'HSM cluster failover and replication', 'High-availability HSM cluster with synchronised state and failover', 's'),
        ('03', 'Blockchain-specific HSM firmware', 'Custom HSM firmware supporting ED25519, secp256k1, BLS12-381', 's'),
        ('04', 'HSM key import and export controls', 'Strict controls and audit trails for key material entering or leaving HSMs', 'm'),
        ('05', 'HSM tamper-evidence monitoring', 'Continuous monitoring for HSM tampering, battery failure, firmware drift', 's'),
      ]),
      ('03', 'MPC Key Management', 'Multi-party computation threshold signing without full key assembly', [
        ('01', 'MPC threshold signing ceremony (t-of-n)', 'Distributed key generation and signing using MPC with configurable threshold', 's'),
        ('02', 'MPC key refresh without asset movement', 'Periodic key share rotation limiting exposure window', 's'),
        ('03', 'MPC node geographic distribution', 'MPC signing nodes distributed across multiple jurisdictions', 's'),
        ('04', 'MPC latency optimisation for throughput', 'Protocol tuning to achieve sub-second MPC signing for high volume', 'd'),
        ('05', 'MPC disaster recovery and share reconstruction', 'Procedures for reconstructing keys after MPC node failure', 's'),
        ('06', 'MPC vendor interoperability testing', 'Testing MPC libraries across vendors for interoperability', 'd'),
      ]),
      ('04', 'Key Derivation & Recovery', 'HD wallet derivation standards and key backup procedures', [
        ('01', 'BIP32/44/84/86 HD wallet derivation', 'Hierarchical deterministic wallet derivation per BIP standards', 'm'),
        ('02', 'BIP39 mnemonic seed generation and storage', 'Secure seed phrase generation and encrypted offline storage', 'm'),
        ('03', 'Shamir Secret Sharing for seed backup', 'Splitting seed phrases into Shamir shares for distributed backup', 's'),
        ('04', 'Metal seed backup (Cryptosteel / Bilodeau)', 'Fireproof and waterproof physical seed storage via metal plates', 'm'),
        ('05', 'Key recovery playbook and tabletop drills', 'Documented recovery procedures tested annually', 's'),
        ('06', 'Derivation path policy enforcement', 'Policy engine restricting allowed derivation paths per asset type', 's'),
        ('07', 'Multi-coin derivation path management', 'Managing derivation paths across Bitcoin, Ethereum, Solana, and 50+ chains', 's'),
        ('08', 'Key usage audit log', 'Immutable audit log of every key derivation and signing operation', 'm'),
      ]),
    ]),
    ('03', 'Reconciliation & Reporting', 'Automated reconciliation and regulatory reporting', [
      ('01', 'On-chain Reconciliation', 'Automated matching of on-chain balances against internal ledger', [
        ('01', 'Real-time on-chain balance polling', 'Continuous polling of blockchain nodes for custodied address balances', 'm'),
        ('02', 'Multi-chain reconciliation engine', 'Automated reconciliation across 20+ chains', 's'),
        ('03', 'UTXO-model reconciliation', 'Reconciliation logic for Bitcoin and other UTXO chains', 's'),
        ('04', 'Account-model reconciliation', 'Reconciliation logic for EVM and Solana account model chains', 's'),
        ('05', 'Reconciliation break investigation workflow', 'Automated flagging and investigation of reconciliation breaks', 's'),
        ('06', 'Staking reward reconciliation', 'Tracking and reconciling validator staking rewards and slashing', 'd'),
      ]),
      ('02', 'Regulatory Reporting', 'Structured reports for regulators on custodied assets', [
        ('01', 'MiCA crypto-asset custody reporting', 'Automated MiCA-compliant custody reports for EEA regulators', 'd'),
        ('02', 'FCA annual custody report', 'Annual UK FCA custody return covering client asset reconciliation', 's'),
        ('03', 'Basel III crypto RWA reporting', 'RWA calculations for crypto exposures under Basel III Group 2', 'd'),
        ('04', 'CCAR/DFAST stress test exposure reporting', 'Including digital asset custody in Fed stress test submissions', 'd'),
        ('05', 'Proof of reserves regulatory submission', 'Submitting cryptographic proof of reserves to regulators on request', 'd'),
      ]),
    ]),
    ('04', 'Insurance & Risk Transfer', 'Insurance products covering custody operational risk', [
      ('01', 'Custody Insurance Programme', 'Structured insurance covering theft, loss, and errors in custody', [
        ('01', 'Crime and specie insurance for cold storage', 'Insurance for physical theft and destruction of cold storage media', 'm'),
        ('02', 'Cyber crime coverage for hot wallet', 'Insurance for hot wallet losses from cyber attack and insider fraud', 's'),
        ('03', 'Errors and omissions (E&O) custody coverage', 'Professional indemnity for custody operational errors', 's'),
        ('04', 'Insurance carrier due diligence process', 'Annual review of custody insurance carriers and coverage limits', 's'),
        ('05', 'Client insurance certificate issuance', 'Issuing insurance certificates to institutional clients on request', 'd'),
        ('06', 'Parametric insurance for blockchain events', 'Trigger-based insurance payouts on smart contract exploits or chain halts', 'e'),
      ]),
    ]),
  ]),
],

# ── WALLETS ───────────────────────────────────────────────────────────────────
'wallets': [
  ('01', 'Wallet Infrastructure', 'Core wallet architecture across hot, warm, and cold tiers', [
    ('01', 'Tiered Wallet Architecture', 'Hot, warm, and cold wallet design and operations', [
      ('01', 'Hot Wallet Operations', 'Always-online wallet tier for operational liquidity', [
        ('01', 'Hot wallet HSM integration', 'HSM-secured private keys for hot wallet signing', 'm'),
        ('02', 'Hot wallet spending limit enforcement', 'Per-transaction and per-period spending limits', 'm'),
        ('03', 'Hot wallet address rotation policy', 'Automated rotation of hot wallet deposit addresses for privacy', 's'),
        ('04', 'Hot wallet automated rebalancing', 'Automatic transfer of excess hot wallet funds to warm or cold tiers', 's'),
        ('05', 'Hot wallet multi-chain support', 'Single infrastructure supporting EVM, Solana, Bitcoin, Cosmos', 's'),
      ]),
      ('02', 'Warm Wallet Operations', 'Semi-online wallet tier for accessible, secured liquidity', [
        ('01', 'Scheduled warm-to-hot transfer workflows', 'Time-scheduled approval-gated transfers from warm to hot tier', 's'),
        ('02', 'Warm wallet MPC signing integration', 'MPC threshold signing for warm wallet without full key exposure', 's'),
        ('03', 'Warm wallet liquidity forecasting', 'Predictive models for warm funding based on withdrawal history', 'd'),
        ('04', 'Dual-approval warm wallet withdrawals', 'Minimum two authorised approvers for warm wallet outflows', 'm'),
      ]),
      ('03', 'Multisig Wallet Management', 'Multi-signature wallet setup and governance', [
        ('01', 'Bitcoin P2SH/P2WSH multisig (m-of-n)', 'Native Bitcoin multisig with configurable threshold', 'm'),
        ('02', 'Ethereum Gnosis Safe multisig deployment', 'Smart contract multisig on EVM chains via Gnosis Safe', 'm'),
        ('03', 'Multisig key holder onboarding and rotation', 'Process for adding, removing, and rotating multisig key holders', 's'),
        ('04', 'Multisig transaction simulation', 'Pre-flight simulation of multisig transactions before signing', 'd'),
        ('05', 'Multisig emergency recovery procedure', 'Recovery procedures when multisig signers are unavailable', 's'),
      ]),
    ]),
    ('02', 'Smart Contract Wallets', 'Programmable wallet functionality via smart contracts', [
      ('01', 'Account Abstraction (ERC-4337)', 'ERC-4337 infrastructure for programmable transaction policies', [
        ('01', 'ERC-4337 UserOperation construction', 'Building and submitting UserOperations via bundlers', 'd'),
        ('02', 'Paymaster integration for gas abstraction', 'Sponsoring gas fees via paymasters for institutional UX', 'd'),
        ('03', 'Session key management', 'Short-lived session keys enabling scoped transaction permissions', 'd'),
        ('04', 'Smart account factory deployment', 'Deterministic smart account deployment using CREATE2', 'd'),
        ('05', 'Guardian-based social recovery', 'ERC-4337 guardian social recovery for institutional smart accounts', 'e'),
        ('06', 'On-chain spending policy enforcement', 'Transaction policy rules enforced via account abstraction logic', 'd'),
      ]),
      ('02', 'Smart Contract Wallet Security', 'Security controls for smart contract wallet code', [
        ('01', 'Pre-deployment smart wallet audit', 'Third-party security audit of wallet contract code', 's'),
        ('02', 'Continuous wallet contract monitoring', 'On-chain monitoring for unexpected state changes', 'd'),
        ('03', 'Upgrade governance (time-lock + multi-sig)', 'Governed upgrade process for proxy-pattern wallets', 'd'),
        ('04', 'Reentrancy vulnerability review', 'Specific audit review for reentrancy risks in wallet code', 's'),
      ]),
    ]),
  ]),
  ('02', 'Wallet-as-a-Service', 'API-first embedded wallet platforms for institutional clients', [
    ('01', 'Embedded Wallet API Platform', 'Developer-facing APIs and SDKs for wallet integration', [
      ('01', 'Core Wallet API', 'REST/GraphQL APIs for wallet provisioning and operations', [
        ('01', 'REST API for wallet provisioning', 'Authenticated REST API for creating wallets programmatically', 's'),
        ('02', 'Webhook event streaming for wallet events', 'Real-time webhooks for deposit, withdrawal, balance changes', 's'),
        ('03', 'iOS/Android SDK for wallet embedding', 'Mobile SDK for embedding custody wallet functionality in client apps', 'd'),
        ('04', 'White-label wallet UI components', 'Brandable frontend components for wallet interfaces', 'd'),
        ('05', 'Batch transaction submission API', 'API for submitting and tracking batches of wallet transactions', 's'),
        ('06', 'Wallet API rate limiting and abuse detection', 'Per-client rate limits and anomaly detection on API usage', 's'),
        ('07', 'Non-custodial MPC-TSS client key split', 'Option for clients to hold one MPC share for partial custody', 'd'),
      ]),
      ('02', 'Wallet Compliance Integration', 'Compliance screening integrated into wallet operations', [
        ('01', 'On-chain sanctions screening', 'Real-time OFAC/EU/UN check on every wallet address', 'm'),
        ('02', 'Travel Rule data collection at wallet level', 'Collecting and transmitting VASP data above threshold', 's'),
        ('03', 'Blockchain analytics provider integration', 'Risk scoring via Chainalysis, Elliptic, or TRM Labs', 'm'),
        ('04', 'KYC gating on wallet activation', 'Preventing wallet use until client KYC is approved', 'm'),
      ]),
    ]),
    ('02', 'Transaction Lifecycle Management', 'End-to-end wallet transaction processing', [
      ('01', 'Transaction Processing', 'Core transaction submission and fee management', [
        ('01', 'Transaction pre-flight policy check', 'Automated compliance and policy checks before signing', 's'),
        ('02', 'Gas price estimation and optimisation', 'Dynamic fee estimation balancing cost and confirmation speed', 'm'),
        ('03', 'EIP-1559 fee market management', 'Priority fee and base fee management for EIP-1559 transactions', 's'),
        ('04', 'Transaction replacement (RBF / cancel)', 'Replace-by-fee and cancellation for stuck transactions', 's'),
        ('05', 'Transaction confirmation monitoring', 'Real-time monitoring of pending transactions with timeout alerts', 's'),
        ('06', 'Cross-chain bridge transaction monitoring', 'Tracking in-flight bridge transactions across chains', 'd'),
        ('07', 'Nonce management for high-throughput wallets', 'Sequential nonce management preventing EVM collisions', 's'),
        ('08', 'Failed transaction retry and alerting', 'Retry logic with exponential backoff and operator alerts', 's'),
      ]),
    ]),
  ]),
],

# ── STABLECOINS ───────────────────────────────────────────────────────────────
'stablecoins': [
  ('01', 'Stablecoin Issuance & Reserve Management', 'Technology and operations for stablecoin creation and reserves', [
    ('01', 'Fiat-Backed Stablecoin Operations', 'Issuance and redemption of fiat-collateralised stablecoins', [
      ('01', 'Issuance & Redemption Mechanics', 'Core mint/burn and redemption operations', [
        ('01', 'Reserve account management and segregation', 'Maintaining fiat reserves in segregated bankruptcy-remote accounts', 'm'),
        ('02', 'Mint/burn smart contract deployment', 'Smart contract logic for minting on deposit and burning on redemption', 'm'),
        ('03', 'KYC-gated mint and redemption flows', 'Restricting minting and redemption to KYC-verified counterparties', 'm'),
        ('04', 'Real-time reserve attestation feed', 'Automated data feed showing reserve balances vs circulating supply', 'd'),
        ('05', 'Redemption queue management', 'Handling redemption queues during high-volume or stressed conditions', 's'),
        ('06', 'Cross-chain stablecoin bridge (native vs wrapped)', 'Infrastructure for bridging stablecoins across chains', 'd'),
        ('07', 'Large redemption settlement coordination', 'Procedures for same-day settlement of large institutional redemptions', 's'),
        ('08', 'Stablecoin supply monitoring dashboard', 'Real-time visibility into circulating supply and reserve ratio', 's'),
      ]),
      ('02', 'Reserve Asset Management', 'Managing assets backing stablecoin issuance', [
        ('01', 'Reserve asset allocation policy', 'Governing permitted reserve assets (T-bills, repo, bank deposits)', 'm'),
        ('02', 'Money market fund integration for reserves', 'Routing reserve cash into regulated MMFs for yield', 's'),
        ('03', 'Daily reserve NAV calculation', 'Daily net asset value calculation of reserves vs circulating supply', 'm'),
        ('04', 'Reserve liquidity stress testing', 'Scenario analysis for reserve adequacy under mass redemption', 's'),
        ('05', 'Reserve counterparty credit monitoring', 'Ongoing credit monitoring of reserve counterparties', 's'),
        ('06', 'Reserve geographic diversification policy', 'Distributing reserves across jurisdictions to reduce concentration', 'd'),
      ]),
    ]),
    ('02', 'Reserve Attestation & Audit', 'Third-party verification of stablecoin reserve backing', [
      ('01', 'Third-Party Attestation Programme', 'Independent verification of reserves against circulating supply', [
        ('01', 'Monthly third-party reserve attestation', 'Independent accountant monthly confirmation of reserves', 'm'),
        ('02', 'Big 4 full reserve audit', 'Annual full-scope audit of reserves by Big 4 accounting firm', 's'),
        ('03', 'On-chain proof of reserve oracle', 'Chainlink or similar oracle publishing verified reserve data on-chain', 'd'),
        ('04', 'Public reserve dashboard with API', 'Public-facing reserve dashboard with sub-minute refresh', 'd'),
        ('05', 'SOC 2 Type II for stablecoin operations', 'SOC 2 audit covering stablecoin issuance operation controls', 's'),
      ]),
    ]),
  ]),
  ('02', 'Stablecoin Compliance & Regulation', 'Regulatory compliance for stablecoin issuers', [
    ('01', 'MiCA E-Money Token Compliance', 'Meeting EU MiCA requirements for e-money tokens', [
      ('01', 'MiCA EMT Authorisation', 'Licencing and ongoing MiCA compliance for EMT issuers', [
        ('01', 'EMT issuer authorisation under MiCA', 'Obtaining e-money institution licence as prerequisite for EMT issuance', 'd'),
        ('02', 'MiCA 30% daily transaction limit monitoring', 'Real-time monitoring and enforcement of MiCA non-EUR EMT limits', 'd'),
        ('03', 'MiCA interoperability with EBA guidelines', 'Aligning operations with EBA technical standards under MiCA', 'd'),
        ('04', 'MiCA white paper publication and updates', 'Drafting and publishing MiCA-compliant crypto-asset white paper', 'd'),
        ('05', 'MiCA significance threshold monitoring', 'Monitoring transaction volumes against MiCA significance thresholds', 'd'),
      ]),
    ]),
    ('02', 'AML Compliance', 'AML/CFT controls specific to stablecoin operations', [
      ('01', 'Stablecoin AML Controls', 'Anti-money laundering controls for stablecoin issuers', [
        ('01', 'Travel Rule compliance for stablecoin transfers', 'Originator/beneficiary data transmission above threshold', 's'),
        ('02', 'On-chain stablecoin transaction monitoring', 'AML monitoring of stablecoin transfers for red flags', 'm'),
        ('03', 'Sanctions screening on mint/redeem counterparties', 'OFAC and EU/UN sanctions checks on every counterparty', 'm'),
        ('04', 'SAR filing process for stablecoins', 'Process for filing SARs on suspicious stablecoin activity', 'm'),
      ]),
    ]),
    ('03', 'Tokenised Deposit Programmes', 'Bank-issued tokenised deposits on distributed ledgers', [
      ('01', 'Tokenised Deposit Architecture', 'Technical design for tokenised commercial bank deposits', [
        ('01', 'Core banking ledger integration', 'Linking blockchain token issuance to core banking deposit ledger', 'd'),
        ('02', 'Intraday tokenised deposit settlement', 'Using tokenised deposits for intraday liquidity and finality', 'd'),
        ('03', 'Interoperability with CBDC settlement rail', 'Connecting tokenised deposit platform to wholesale CBDC rails', 'e'),
        ('04', 'Deposit insurance eligibility confirmation', 'Confirming tokenised deposits qualify for FDIC/FSCS/DGS insurance', 'd'),
        ('05', 'Programmable payment conditions on deposits', 'Smart contract conditional payment logic on tokenised deposits', 'e'),
        ('06', 'Multi-bank tokenised deposit interoperability (RLN)', 'Participation in regulated liability network for deposit interop', 'e'),
      ]),
    ]),
  ]),
],

# ── CBDC ─────────────────────────────────────────────────────────────────────
'cbdc': [
  ('01', 'Wholesale CBDC', 'Central bank digital currency for interbank and large-value settlement', [
    ('01', 'wCBDC Settlement Rail', 'Settlement infrastructure using central bank-issued digital currency', [
      ('01', 'RTGS and Settlement Integration', 'Connecting wCBDC to existing settlement infrastructure', [
        ('01', 'RTGS integration with wCBDC settlement', 'Connecting wholesale CBDC to RTGS for interbank settlement', 'e'),
        ('02', 'DvP settlement using wCBDC', 'Delivery-versus-payment for securities using wholesale CBDC', 'e'),
        ('03', 'PvP FX settlement using wCBDC', 'Payment-versus-payment FX settlement eliminating Herstatt risk', 'e'),
        ('04', 'Intraday liquidity with wCBDC credit facilities', 'Intraday liquidity management using wCBDC credit lines', 'e'),
        ('05', 'Multi-CBDC cross-border settlement (mBridge)', 'Participation in multi-CBDC platforms for cross-border flows', 'e'),
        ('06', 'wCBDC interop with commercial bank money', 'Technical bridge between wCBDC and tokenised bank deposits', 'e'),
      ]),
      ('02', 'Programmable CBDC Features', 'Smart contract and programmability for wholesale CBDC', [
        ('01', 'Conditional payment logic on wCBDC', 'Programmable release of wCBDC based on verified conditions', 'e'),
        ('02', 'Atomic swap wCBDC-to-tokenised-asset', 'Simultaneous exchange of wCBDC and tokenised asset', 'e'),
        ('03', 'Expiry and velocity controls on wCBDC', 'Central bank-imposed time limits or velocity controls on holdings', 'e'),
        ('04', 'Tiered interest rate programmability', 'Applying tiered interest rates programmatically to wCBDC balances', 'e'),
      ]),
    ]),
  ]),
  ('02', 'Retail CBDC Distribution', 'Bank-intermediated distribution of retail CBDC to end users', [
    ('01', 'Retail CBDC Wallet & Onboarding', 'Issuing and managing retail CBDC wallets via commercial banks', [
      ('01', 'Retail CBDC Issuance & Operations', 'Core retail CBDC wallet issuance and customer operations', [
        ('01', 'Retail CBDC wallet issuance to bank customers', 'Issuing and managing retail CBDC wallets on behalf of customers', 'e'),
        ('02', 'KYC integration for CBDC onboarding', 'Linking CBDC wallet issuance to existing bank KYC checks', 'e'),
        ('03', 'Retail CBDC-to-bank deposit conversion', 'Seamless conversion between retail CBDC and bank deposits', 'e'),
        ('04', 'Retail CBDC offline payment capability', 'Offline transactions via secure element or hardware wallet', 'e'),
        ('05', 'Retail CBDC holding limit enforcement', 'Enforcing central bank-mandated holding and spending limits', 'e'),
        ('06', 'Retail CBDC mobile banking API integration', 'Embedding retail CBDC features in mobile banking app', 'e'),
      ]),
      ('02', 'CBDC Privacy Architecture', 'Technical approaches to privacy for retail CBDC users', [
        ('01', 'Tiered anonymity for low-value retail CBDC', 'Low KYC requirements for small CBDC balances', 'e'),
        ('02', 'ZK proof for CBDC transaction privacy', 'Zero-knowledge proofs enabling selective disclosure', 'e'),
        ('03', 'CBDC data access governance framework', 'Policies governing which entities can access CBDC data', 'e'),
      ]),
    ]),
  ]),
  ('03', 'CBDC Sandbox & Research', 'Participation in central bank CBDC experiments and sandboxes', [
    ('01', 'Central Bank Sandbox Programmes', 'Engagement with central bank-led CBDC pilot programmes', [
      ('01', 'Sandbox Engagement', 'Active participation in CBDC pilot initiatives globally', [
        ('01', 'Bank of England digital pound sandbox', 'Engaging in BoE digital pound design and experimentation', 'e'),
        ('02', 'ECB digital euro pilot programme', 'Participating in ECB digital euro preparation phase as PSP', 'e'),
        ('03', 'Fed digital dollar research participation', 'Contributing to US Fed research on digital dollar designs', 'e'),
        ('04', 'MAS Project Orchid wCBDC participation', 'Singapore MAS Project Orchid wholesale CBDC pilot', 'e'),
        ('05', 'BIS Innovation Hub collaboration', 'Collaboration with BIS Innovation Hub on cross-border CBDC', 'e'),
        ('06', 'HKMA e-HKD pilot participation', 'Hong Kong e-HKD pilot for retail and wholesale use cases', 'e'),
        ('07', 'JFSA digital yen research engagement', 'Japan digital yen research programme participation', 'e'),
      ]),
    ]),
  ]),
],

# ── SETTLEMENT ────────────────────────────────────────────────────────────────
'settlement': [
  ('01', 'Atomic & Instant Settlement', 'Real-time and atomic settlement using distributed ledger technology', [
    ('01', 'Delivery versus Payment (DvP)', 'Simultaneous exchange of assets and payment on DLT', [
      ('01', 'DvP Implementation', 'Technical implementation of DvP settlement on DLT', [
        ('01', 'On-chain DvP for tokenised securities', 'Atomic swap of tokenised bond vs stablecoin on shared ledger', 'd'),
        ('02', 'Cross-chain DvP via HTLCs', 'Hash time-lock contract DvP across two separate blockchains', 'd'),
        ('03', 'Regulated DvP with licensed intermediary', 'DvP via licenced CSD or settlement agent as intermediary', 'd'),
        ('04', 'DvP settlement finality rules', 'Legal and technical definitions of DvP settlement finality', 's'),
        ('05', 'DvP partial fill and exception handling', 'Handling partial fills, failed legs, and exceptions in DvP', 'd'),
        ('06', 'DvP audit trail and regulatory reporting', 'Complete audit trail of DvP settlement events', 'd'),
      ]),
    ]),
    ('02', 'Payment versus Payment (PvP)', 'Simultaneous exchange of two payment obligations', [
      ('01', 'PvP Settlement', 'PvP infrastructure for FX and multi-currency settlement', [
        ('01', 'On-chain PvP for stablecoin FX', 'Atomic stablecoin exchange eliminating Herstatt risk', 'd'),
        ('02', 'PvP interoperability across CBDC platforms', 'PvP spanning multiple CBDC platforms via bridging protocol', 'e'),
        ('03', 'PvP netting to reduce settlement volumes', 'Multilateral netting of PvP obligations before final settlement', 'd'),
        ('04', 'PvP confirmation and affirmation workflow', 'Pre-settlement affirmation of PvP instructions between counterparties', 'd'),
      ]),
    ]),
  ]),
  ('02', 'Settlement Operations', 'Day-to-day settlement processing and exception management', [
    ('01', 'Pre-Settlement Processing', 'Pre-settlement checks and enrichment workflows', [
      ('01', 'Instruction Enrichment & Matching', 'Automated settlement instruction preparation and matching', [
        ('01', 'Trade affirmation and confirmation matching', 'Automated matching of trade details before settlement', 'm'),
        ('02', 'Settlement instruction enrichment', 'Automatically enriching instructions with SSI and account data', 'm'),
        ('03', 'Settlement date calculation (T+0 to T+2)', 'Calculating settlement dates per instrument and market convention', 'm'),
        ('04', 'Pre-settlement counterparty credit check', 'Verifying counterparty credit limits before committing to settlement', 's'),
        ('05', 'Fails prediction and proactive management', 'Predicting likely settlement fails using inventory data', 'd'),
      ]),
    ]),
    ('02', 'Cross-Chain Settlement', 'Settlement across multiple blockchain networks', [
      ('01', 'Cross-Chain Settlement Infrastructure', 'Technical infrastructure for multi-chain settlement coordination', [
        ('01', 'Cross-chain settlement finality monitoring', 'Monitoring settlement finality across source and destination chains', 'd'),
        ('02', 'Bridge risk assessment framework', 'Risk scoring for cross-chain bridge counterparty and smart contract risk', 'd'),
        ('03', 'Cross-chain settlement reconciliation', 'Automated reconciliation of cross-chain settlement events', 'd'),
        ('04', 'Interoperability hub for multi-chain settlement', 'Central coordination hub routing settlement across networks', 'e'),
        ('05', 'Cross-chain settlement SLA monitoring', 'Real-time tracking of cross-chain completion against SLAs', 'd'),
      ]),
    ]),
    ('03', 'Fails Management', 'Managing and resolving settlement failures', [
      ('01', 'Settlement Fails Resolution', 'Processes and tools for resolving settlement failures', [
        ('01', 'Buy-in process for persistent fails', 'Automated buy-in execution for fails exceeding duration threshold', 's'),
        ('02', 'CSDR mandatory buy-in compliance', 'Compliance with EU CSDR mandatory buy-in regime', 's'),
        ('03', 'Fails penalty calculation and reporting', 'Automated calculation and reporting of cash penalties for fails', 's'),
        ('04', 'Settlement fails root cause analysis', 'Systematic analysis of fails causes for operational improvement', 's'),
        ('05', 'Partial settlement and netting optimisation', 'Using partial settlement and netting to reduce fail rates', 'd'),
      ]),
    ]),
  ]),
  ('03', 'Clearing Infrastructure', 'Central clearing of digital asset transactions', [
    ('01', 'Central Counterparty Clearing', 'CCP-based clearing for digital asset transactions', [
      ('01', 'CCP Membership & Margin', 'CCP membership operations and margin management', [
        ('01', 'CCP membership for digital asset clearing', 'CCP clearing membership for digital asset derivatives and spot', 'd'),
        ('02', 'Digital asset initial margin calculation', 'SIMM or SPAN-based initial margin for digital asset positions', 'd'),
        ('03', 'Real-time variation margin for crypto derivatives', 'Intraday VM calls and collection for crypto derivative positions', 'd'),
        ('04', 'Default fund contribution management', 'Capital contribution and management of default fund share at CCP', 'd'),
        ('05', 'Crypto derivative position netting at CCP', 'Bilateral and multilateral netting of crypto derivative positions', 'd'),
      ]),
    ]),
  ]),
],

# ── TOKENISATION ──────────────────────────────────────────────────────────────
'tokenisation': [
  ('01', 'Real World Asset Tokenisation', 'Converting real-world assets into blockchain tokens', [
    ('01', 'Fixed Income Tokenisation', 'Tokenising bonds, treasuries, and fixed income instruments', [
      ('01', 'Bond Tokenisation Lifecycle', 'End-to-end lifecycle management for tokenised bonds', [
        ('01', 'Government bond tokenisation (T-bill, Gilt)', 'Tokenising sovereign bonds on regulated DLT platforms', 'd'),
        ('02', 'Corporate bond tokenisation and primary issuance', 'Issuing corporate bonds in tokenised form at origination', 'd'),
        ('03', 'Bond coupon payment automation via smart contract', 'Automated coupon distribution to tokenised bond holders', 'd'),
        ('04', 'Bond maturity and principal redemption on-chain', 'On-chain execution of bond maturity and principal return', 'd'),
        ('05', 'Tokenised bond secondary market trading', 'Secondary market infrastructure for trading tokenised bonds', 'd'),
        ('06', 'Repo on tokenised bonds (digital repo)', 'Using tokenised bonds as collateral in digital repo', 'd'),
        ('07', 'Tokenised bond CSD linkage and nominee structure', 'Legal structure linking tokenised bond to underlying at CSD', 'd'),
        ('08', 'Tokenised bond ISIN and LEI mapping', 'Mapping tokenised bond to ISIN, LEI, and legal documentation', 'd'),
      ]),
    ]),
    ('02', 'Equity & Real Estate Tokenisation', 'Tokenising equities, private equity, and real estate', [
      ('01', 'Equity Tokenisation', 'Converting equity instruments to blockchain tokens', [
        ('01', 'Private equity tokenisation and secondary transfer', 'Converting PE interests to tokens enabling secondary trading', 'd'),
        ('02', 'Listed equity tokenisation for settlement efficiency', 'Tokenised representation of listed equities for DvP settlement', 'e'),
        ('03', 'Dividend distribution via smart contract', 'Automated cash dividend payments to tokenised equity holders', 'd'),
        ('04', 'On-chain voting rights management', 'On-chain governance and voting for tokenised equity shareholders', 'd'),
        ('05', 'Cap table management on blockchain', 'On-chain cap table for private companies using tokenised equity', 'd'),
      ]),
      ('02', 'Real Estate Tokenisation', 'Fractional real estate ownership via tokens', [
        ('01', 'Fractional real estate token structure', 'Legal and technical structure for fractional ownership via tokens', 'd'),
        ('02', 'Rental income distribution via smart contract', 'Automated pro-rata rental income distribution to token holders', 'd'),
        ('03', 'Property valuation oracle integration', 'On-chain property valuation feeds for NAV calculation', 'd'),
        ('04', 'SPV-backed real estate token wrapper', 'SPV structure backing real estate tokens with bankruptcy remoteness', 'd'),
      ]),
    ]),
    ('03', 'Fund Tokenisation', 'Tokenising investment fund units for efficiency', [
      ('01', 'Fund Token Lifecycle', 'Subscription, redemption, and distribution for tokenised funds', [
        ('01', 'Tokenised money market fund units', 'Tokenising MMF units for use as collateral and settlement assets', 'd'),
        ('02', 'Tokenised private credit fund interests', 'Converting private credit LP interests to transferable tokens', 'd'),
        ('03', 'Fund subscription and redemption via smart contract', 'Automating fund sub/redeem lifecycle on-chain with compliance', 'd'),
        ('04', 'Fund NAV oracle for tokenised fund pricing', 'On-chain NAV feed for tokenised fund unit pricing', 'd'),
        ('05', 'Transfer agent replacement via DLT', 'Using DLT to replace or augment traditional transfer agent functions', 'd'),
        ('06', 'Tokenised fund regulatory approval (CSSF, FCA, MAS)', 'Obtaining regulatory approval for tokenised fund structures', 'd'),
      ]),
    ]),
  ]),
  ('02', 'Token Issuance & Secondary Markets', 'Platform and market infrastructure for tokenised assets', [
    ('01', 'Token Issuance Platform', 'Technical platform for issuing and managing tokenised assets', [
      ('01', 'Security Token Standards & Controls', 'Standards and transfer restriction controls for security tokens', [
        ('01', 'ERC-1400/ERC-3643 security token standard', 'Implementing security token standards with transfer restrictions', 'd'),
        ('02', 'On-chain transfer restriction enforcement', 'Smart contract enforcement of KYC, jurisdiction, and lock-up rules', 'd'),
        ('03', 'Token lifecycle event management', 'Automated handling of corporate actions and lifecycle events', 'd'),
        ('04', 'Whitelist management for permissioned transfers', 'Maintaining on-chain whitelists of eligible token holders', 'd'),
        ('05', 'Multi-chain token deployment strategy', 'Deploying tokenised assets across multiple chains for liquidity', 'd'),
        ('06', 'Tokenisation platform API for issuers', 'REST/GraphQL API enabling issuers to self-serve token issuance', 'd'),
        ('07', 'Token registry and ownership ledger', 'Authoritative on-chain or hybrid registry of token ownership', 'd'),
      ]),
    ]),
    ('02', 'Secondary Market Infrastructure', 'Infrastructure supporting secondary trading of tokenised assets', [
      ('01', 'Secondary Market Trading', 'Venues and mechanisms for tokenised asset secondary trading', [
        ('01', 'ATS/MTF integration for tokenised asset trading', 'Connecting tokenised assets to Alternative Trading Systems or MTFs', 'd'),
        ('02', 'OTC tokenised asset bilateral trading desk', 'Bilateral OTC trading desk for institutional transactions', 'd'),
        ('03', 'Tokenised asset price discovery mechanism', 'Market making or auction mechanisms for price discovery', 'd'),
        ('04', 'Tokenised asset lending and borrowing', 'Secured lending using tokenised assets as collateral', 'd'),
        ('05', 'On-chain order book for tokenised assets', 'Fully on-chain order matching for tokenised instruments', 'e'),
      ]),
    ]),
  ]),
],

# ── DEFI & PROTOCOLS ─────────────────────────────────────────────────────────
'defi_protocols': [
  ('01', 'Institutional DeFi Access', 'Connecting institutional clients to decentralised finance protocols', [
    ('01', 'Permissioned DeFi Integration', 'Accessing DeFi protocols via compliant, permissioned on-ramps', [
      ('01', 'Compliant DeFi Access', 'KYC-permissioned access to institutional DeFi pools and protocols', [
        ('01', 'KYC-permissioned DeFi pool participation', 'Accessing institutional DeFi pools with on-chain KYC verification', 'd'),
        ('02', 'Aave Arc / institutional lending pool access', 'KYC-gated institutional DeFi lending via permissioned pools', 'd'),
        ('03', 'Compliant DEX aggregator routing', 'DEX aggregators with sanctions screening on route selection', 'd'),
        ('04', 'DeFi protocol smart contract risk assessment', 'Pre-engagement risk scoring of DeFi protocol smart contracts', 'd'),
        ('05', 'DeFi exposure limit and risk appetite framework', 'Internal risk framework setting limits on DeFi exposures', 'd'),
        ('06', 'DeFi protocol governance participation', 'Voting in DeFi governance on behalf of institutional clients', 'e'),
      ]),
      ('02', 'Liquidity Provision', 'Providing liquidity to DeFi protocols for institutional yield', [
        ('01', 'AMM liquidity provision (Uniswap, Curve)', 'Providing liquidity to AMMs for fee generation', 'd'),
        ('02', 'Concentrated liquidity management (Uni v3)', 'Managing Uniswap v3 concentrated liquidity positions', 'd'),
        ('03', 'Impermanent loss monitoring and hedging', 'Real-time IL calculation and hedging strategies for LP positions', 'd'),
        ('04', 'Liquidity mining programme management', 'Tracking and claiming DeFi rewards on behalf of clients', 'd'),
      ]),
    ]),
  ]),
  ('02', 'DeFi Risk Management', 'Risk controls for DeFi protocol exposures', [
    ('01', 'Smart Contract Risk', 'Technical risk assessment for DeFi protocol smart contracts', [
      ('01', 'Protocol Risk Assessment', 'Pre-engagement and ongoing risk evaluation of DeFi protocols', [
        ('01', 'Pre-interaction smart contract audit review', 'Reviewing third-party audit reports before first interaction', 'd'),
        ('02', 'Protocol TVL and concentration monitoring', 'Monitoring total value locked and concentration risk', 'd'),
        ('03', 'DeFi exploit alerting and circuit breaker', 'Real-time exploit monitoring triggering automatic position exits', 'd'),
        ('04', 'Oracle manipulation risk monitoring', 'Detecting price oracle manipulation risks in DeFi protocols', 'd'),
        ('05', 'Flash loan attack risk assessment', 'Assessing DeFi protocol exposure to flash loan attacks', 'd'),
        ('06', 'Protocol upgrade governance risk', 'Assessing risks from DeFi protocol governance upgrades', 'd'),
      ]),
    ]),
    ('02', 'DeFi Position Monitoring', 'Real-time visibility into DeFi positions and exposures', [
      ('01', 'Position Tracking & Reporting', 'Unified monitoring and reporting of DeFi positions', [
        ('01', 'Multi-protocol DeFi position dashboard', 'Unified dashboard for DeFi positions across protocols and chains', 'd'),
        ('02', 'DeFi collateral ratio monitoring', 'Real-time collateral ratio tracking with margin call alerts', 'd'),
        ('03', 'DeFi yield performance reporting', 'Daily yield and fee income reporting across all DeFi positions', 'd'),
        ('04', 'DeFi position regulatory reporting', 'Structured regulatory reporting of DeFi exposures', 'e'),
        ('05', 'Liquidation risk monitoring and alerting', 'Early warning alerts for approaching liquidation thresholds', 'd'),
      ]),
    ]),
  ]),
  ('03', 'Staking & Yield', 'Institutional staking and yield generation services', [
    ('01', 'Proof of Stake Validation', 'Running or delegating PoS validators for institutional clients', [
      ('01', 'Ethereum Staking Operations', 'Ethereum validator node management and reward tracking', [
        ('01', 'Ethereum validator node operation', 'Running Ethereum PoS validator nodes on behalf of institutional stakers', 's'),
        ('02', 'Validator key management and slashing protection', 'Secure key management with slashing protection (e.g. Vouch)', 's'),
        ('03', 'Liquid staking token integration (stETH, rETH)', 'Using liquid staking tokens maintaining staked ETH liquidity', 's'),
        ('04', 'Staking reward reporting and tax lot tracking', 'Tracking rewards per tax lot for institutional tax reporting', 's'),
        ('05', 'Multi-chain staking (Cosmos, Polkadot, Cardano)', 'Validator delegation and staking across multiple PoS networks', 'd'),
        ('06', 'Slashing insurance and risk mitigation', 'Insurance and controls for Ethereum validator slashing risk', 'd'),
        ('07', 'Staking commission and fee management', 'Managing staking commission structures and fee sharing', 's'),
      ]),
    ]),
  ]),
],

# ── SECURITY ─────────────────────────────────────────────────────────────────
'security': [
  ('01', 'Threat & Vulnerability Management', 'Identifying and managing cyber security threats', [
    ('01', 'Offensive Security Testing', 'Penetration testing and red team exercises', [
      ('01', 'Penetration Testing Programme', 'Regular offensive security testing of digital asset infrastructure', [
        ('01', 'Annual red team exercise for custody', 'Full-scope red team attack simulation for custody operations', 'm'),
        ('02', 'Smart contract penetration testing', 'Security testing of proprietary smart contract code', 'm'),
        ('03', 'Social engineering and phishing simulation', 'Regular phishing and vishing simulations for key management staff', 'm'),
        ('04', 'DeFi integration security review', 'Security review before connecting to a new DeFi protocol or bridge', 'd'),
        ('05', 'Bug bounty programme', 'Public or private bug bounty programme for responsible disclosure', 's'),
        ('06', 'Continuous attack surface monitoring', 'Automated discovery of externally exposed assets', 's'),
      ]),
    ]),
    ('02', 'Vulnerability Management', 'Tracking and remediating security vulnerabilities', [
      ('01', 'Vulnerability Tracking & Remediation', 'CVE management and patching for digital asset systems', [
        ('01', 'CVE tracking for digital asset dependencies', 'Monitoring CVEs in blockchain node software, SDKs, and custody deps', 'm'),
        ('02', 'Patch management SLA for critical systems', 'Defined and enforced patch SLAs for custody-critical infrastructure', 'm'),
        ('03', 'Dependency supply chain security review', 'Monitoring third-party dependency supply chain for custody code', 's'),
        ('04', 'SAST/DAST in CI/CD pipeline', 'Static and dynamic analysis integrated into smart contract CI/CD', 's'),
      ]),
    ]),
  ]),
  ('02', 'Operational Security', 'Security controls for day-to-day digital asset operations', [
    ('01', 'Key Ceremony Security', 'Physical and procedural security for key ceremonies', [
      ('01', 'Key Ceremony Controls', 'Controls governing key generation and signing ceremonies', [
        ('01', 'Key ceremony physical security checklist', 'Documented physical security requirements for key ceremonies', 'm'),
        ('02', 'Background checks for ceremony participants', 'Enhanced background checks for key ceremony personnel', 'm'),
        ('03', 'Independent observer programme', 'Observer programme for key generation and signing ceremonies', 's'),
        ('04', 'Tamper-evident seal procedures', 'Tamper-evident sealing of HSMs and storage media post-ceremony', 'm'),
        ('05', 'Split knowledge and dual control enforcement', 'Controls ensuring no single person has complete key access', 'm'),
      ]),
    ]),
    ('02', 'Privileged Access Management', 'Controlling privileged access to digital asset systems', [
      ('01', 'PAM Controls', 'Privileged access controls for custody system administration', [
        ('01', 'Privileged access workstation (PAW)', 'Dedicated hardened workstations for custody system admin', 'm'),
        ('02', 'Just-in-time privileged access provisioning', 'Time-limited privileged access grants with automatic expiry', 's'),
        ('03', 'Privileged session recording', 'Full video and keystroke recording of privileged sessions', 'm'),
        ('04', 'Break-glass emergency access procedures', 'Controlled and audited emergency access for critical systems', 'm'),
        ('05', 'Hardware security key for admin access (FIDO2)', 'FIDO2/WebAuthn hardware key mandatory for admin accounts', 'm'),
      ]),
    ]),
  ]),
  ('03', 'Incident Response', 'Responding to security incidents in digital asset operations', [
    ('01', 'Digital Asset Incident Response', 'IR plan and playbooks specific to digital asset incidents', [
      ('01', 'IR Playbooks & Exercises', 'Documented response procedures and tabletop exercises', [
        ('01', 'Crypto incident classification and severity matrix', 'Severity classification for digital asset security incidents', 'm'),
        ('02', 'Hot wallet compromise runbook', 'Step-by-step response for a compromised hot wallet', 'm'),
        ('03', 'Key compromise response and asset quarantine', 'Emergency procedures for suspected key compromise', 'm'),
        ('04', 'DeFi exploit response playbook', 'Rapid response procedures for losses from DeFi exploits', 'd'),
        ('05', 'Regulatory notification procedures', 'Notification process for material digital asset security incidents', 'm'),
        ('06', 'Quarterly tabletop exercise programme', 'Quarterly tabletop exercises for crypto-specific scenarios', 's'),
        ('07', 'Post-incident chain forensics capability', 'On-chain forensic investigation capability post-incident', 's'),
      ]),
    ]),
  ]),
  ('04', 'Smart Contract Security', 'Security programme for smart contract development and deployment', [
    ('01', 'Smart Contract Audit Programme', 'Formal security auditing of smart contract code', [
      ('01', 'Audit & Formal Verification', 'Multi-party auditing and formal verification for critical contracts', [
        ('01', 'Pre-deployment multi-auditor review', 'Minimum two independent audit firms before deployment', 'm'),
        ('02', 'Formal verification of critical contracts', 'Mathematical formal verification of high-value smart contract logic', 'd'),
        ('03', 'On-chain monitoring for smart contract anomalies', 'Real-time monitoring of deployed contracts for unexpected changes', 'd'),
        ('04', 'Upgrade governance (time-lock + multi-sig)', 'Time-locked, multi-sig gated upgrade process for contracts', 'm'),
        ('05', 'Reentrancy and MEV protection review', 'Specific audit review for reentrancy and MEV risks', 's'),
        ('06', 'Emergency pause and kill switch implementation', 'Circuit breaker functionality for emergency contract halt', 'm'),
      ]),
    ]),
  ]),
],

# ── AI & AGENTIC ─────────────────────────────────────────────────────────────
'ai_agentic': [
  ('01', 'AI-Augmented Compliance', 'Using AI to enhance compliance and regulatory operations', [
    ('01', 'AI Transaction Monitoring', 'Machine learning for AML and fraud transaction monitoring', [
      ('01', 'ML-Based AML Detection', 'Trained models detecting crypto AML typologies and anomalies', [
        ('01', 'ML-based typology detection for crypto', 'Trained ML models detecting known crypto AML typologies', 'd'),
        ('02', 'Unsupervised anomaly detection for blockchain', 'Unsupervised learning for detecting novel laundering patterns', 'd'),
        ('03', 'Graph neural network for on-chain entity clustering', 'GNN-based address clustering to identify connected wallets', 'd'),
        ('04', 'AI-generated SAR narrative drafting', 'LLM assistance in drafting SAR narratives from alert data', 'd'),
        ('05', 'Model explainability for AML decisions (SHAP/LIME)', 'SHAP or LIME-based explanations for AI-flagged AML alerts', 'd'),
        ('06', 'Continuous model retraining on new typologies', 'MLOps pipeline retraining AML models on emerging typology data', 'd'),
      ]),
    ]),
    ('02', 'AI Regulatory Intelligence', 'AI tools for monitoring and interpreting regulatory change', [
      ('01', 'Regulatory Monitoring & Analysis', 'NLP and LLM tools for regulatory monitoring', [
        ('01', 'Regulatory change NLP monitoring', 'NLP pipeline monitoring regulatory publications for material changes', 'd'),
        ('02', 'AI-assisted regulatory gap analysis', 'LLM-powered gap analysis mapping new regulations to controls', 'd'),
        ('03', 'AI regulatory Q&A assistant for compliance staff', 'Internal AI assistant trained on regulatory texts', 'd'),
        ('04', 'Automated regulatory horizon scanning', 'Automated tracking and summarisation of regulatory consultations', 'd'),
      ]),
    ]),
  ]),
  ('02', 'Agentic Workflows', 'Autonomous AI agents for digital asset operations', [
    ('01', 'Autonomous Settlement & Operations Agents', 'AI agents executing settlement and operational workflows', [
      ('01', 'Agentic Workflow Infrastructure', 'Core infrastructure for autonomous agent orchestration', [
        ('01', 'AI settlement exception resolution agent', 'Autonomous agent triaging and resolving settlement exceptions', 'e'),
        ('02', 'AI-assisted trade reconciliation agent', 'AI agent matching and resolving reconciliation breaks', 'e'),
        ('03', 'Multi-agent workflow orchestration', 'Orchestration layer coordinating multiple agents in custody workflows', 'e'),
        ('04', 'Human-in-the-loop override for agent decisions', 'Configurable human approval checkpoints in agentic workflows', 'e'),
        ('05', 'Agent audit trail and decision logging', 'Immutable logs of all AI agent decisions and actions', 'e'),
        ('06', 'Agent tool policy and permission controls', 'Enforced tool access controls for autonomous agents', 'e'),
      ]),
    ]),
    ('02', 'AI Risk Monitoring', 'Continuous risk monitoring powered by AI', [
      ('01', 'AI-Driven Risk Intelligence', 'Machine learning for real-time risk signals', [
        ('01', 'Real-time AI market risk monitoring for crypto', 'AI models providing continuous risk signals on crypto exposure', 'd'),
        ('02', 'AI-powered liquidity stress prediction', 'Predictive models for liquidity stress in digital asset portfolios', 'd'),
        ('03', 'On-chain MEV and front-running detection', 'AI detection of MEV and front-running affecting client orders', 'd'),
        ('04', 'Smart contract rug pull early warning system', 'ML signals detecting early indicators of fraudulent protocols', 'd'),
        ('05', 'AI counterparty risk scoring for DeFi protocols', 'Continuous AI scoring of DeFi counterparty risk', 'd'),
      ]),
    ]),
  ]),
  ('03', 'AI Model Governance', 'Governance framework for AI models in digital asset operations', [
    ('01', 'Model Risk Management', 'MRM framework for AI models in custody and compliance', [
      ('01', 'AI MRM Programme', 'Comprehensive model risk management for digital asset AI', [
        ('01', 'AI model inventory and classification', 'Maintaining an inventory of all AI models with risk classification', 'd'),
        ('02', 'Model validation for compliance AI', 'Independent validation of AML and compliance AI models', 'd'),
        ('03', 'AI model performance monitoring dashboard', 'Tracking model drift, accuracy, and false positive rates', 'd'),
        ('04', 'SR 11-7 model risk guidance application', 'Applying Fed SR 11-7 MRM guidance to AI compliance tools', 'd'),
        ('05', 'EU AI Act high-risk system compliance', 'Compliance with EU AI Act for high-risk AI in financial services', 'd'),
        ('06', 'AI model bias and fairness testing', 'Regular bias and fairness testing of AI models in client decisions', 'd'),
      ]),
    ]),
  ]),
],

# ── COMPLIANCE & REGULATION ───────────────────────────────────────────────────
'compliance_regulation': [
  ('01', 'AML & CFT Programme', 'Anti-money laundering and counter-terrorism financing controls', [
    ('01', 'KYC & Customer Due Diligence', 'Know your customer and enhanced due diligence processes', [
      ('01', 'KYC Onboarding & Refresh', 'KYC processes for digital asset client onboarding and refresh', [
        ('01', 'VASP and institutional KYC onboarding', 'Enhanced KYC for VASP and institutional counterparties', 'm'),
        ('02', 'Beneficial ownership identification for crypto', 'Identifying UBOs of crypto funds, DAOs, and complex entities', 'm'),
        ('03', 'Risk-based KYC tiering for digital asset clients', 'Tiered KYC requirements based on client type and risk profile', 'm'),
        ('04', 'Ongoing KYC refresh programme', 'Periodic KYC refresh and trigger-based re-KYC for material changes', 'm'),
        ('05', 'DAO legal entity classification for KYC', 'Procedures for classifying and KYC-ing DAOs as institutional counterparties', 'd'),
        ('06', 'AI-assisted KYC document review', 'AI-powered document verification and extraction in KYC workflows', 'd'),
      ]),
    ]),
    ('02', 'Travel Rule Compliance', 'FATF Travel Rule data exchange for crypto transfers', [
      ('01', 'Travel Rule Programme', 'End-to-end Travel Rule compliance and data exchange', [
        ('01', 'FATF Travel Rule threshold monitoring', 'Automated detection of transfers exceeding Travel Rule threshold', 'm'),
        ('02', 'VASP counterparty identification and verification', 'Identifying and verifying VASP counterparties for Travel Rule', 'm'),
        ('03', 'Travel Rule protocol integration (TRUST, OpenVASP)', 'Integration with Travel Rule protocol networks for data exchange', 'm'),
        ('04', 'Unhosted wallet Travel Rule risk assessment', 'Risk-based process for unhosted wallet counterparties', 'm'),
        ('05', 'Travel Rule sunrise issue management', 'Procedures for transacting with non-compliant jurisdictions', 's'),
        ('06', 'Travel Rule data retention and record keeping', 'Retaining Travel Rule records per regulatory requirements', 'm'),
      ]),
    ]),
    ('03', 'Transaction Monitoring', 'Ongoing AML monitoring of digital asset transactions', [
      ('01', 'AML Transaction Monitoring Programme', 'AML monitoring controls for digital asset transactions', [
        ('01', 'Real-time on-chain transaction monitoring', 'Continuous AML screening of all blockchain transactions', 'm'),
        ('02', 'Blockchain analytics provider integration', 'Integration with Chainalysis, Elliptic, or TRM Labs', 'm'),
        ('03', 'Sanctions screening for wallet addresses', 'Real-time OFAC, EU, UN, OFSI screening for all addresses', 'm'),
        ('04', 'SAR filing process and workflow', 'End-to-end SAR/STR filing workflow for suspicious activity', 'm'),
        ('05', 'Typology-based alert tuning', 'Configuring TM rules based on FATF crypto typologies', 'm'),
        ('06', 'Alert disposition and investigation workflow', 'Structured workflow for triaging, investigating, and closing alerts', 'm'),
      ]),
    ]),
  ]),
  ('02', 'Regulatory Licensing & Jurisdiction Compliance', 'Managing licences and compliance across operating jurisdictions', [
    ('01', 'Licence Matrix Management', 'Centralised management of regulatory licences', [
      ('01', 'Global Licence Tracking & Renewal', 'Lifecycle management of regulatory licences globally', [
        ('01', 'Global regulatory licence tracker', 'Centralised tracker of licence status, renewal dates, and conditions', 'm'),
        ('02', 'Material change notification process', 'Notifying regulators of material changes to licensed activities', 'm'),
        ('03', 'New jurisdiction licence assessment framework', 'Evaluating licence requirements before entering new markets', 's'),
        ('04', 'Regulatory engagement and lobbying strategy', 'Structured engagement with regulators on policy development', 's'),
        ('05', 'Licence condition monitoring and compliance', 'Ongoing monitoring of compliance with all licence conditions', 'm'),
      ]),
    ]),
    ('02', 'Market-Specific Regulatory Frameworks', 'Compliance programmes for specific regulatory regimes', [
      ('01', 'Jurisdiction-Specific Compliance', 'Dedicated compliance programmes per major regulatory regime', [
        ('01', 'MiCA CASP authorisation and ongoing compliance', 'Full MiCA compliance programme for EU digital asset providers', 'd'),
        ('02', 'MAS Payment Services Act compliance', 'Singapore MAS PSA compliance for MPL licence (DPT)', 's'),
        ('03', 'HKMA VASP licensing compliance', 'Hong Kong SFC/HKMA VASP licensing and ongoing compliance', 'd'),
        ('04', 'VARA Dubai digital asset regulation compliance', 'Dubai VARA licence and ongoing compliance', 'd'),
        ('05', 'FINMA virtual asset guidelines compliance', 'Swiss FINMA banking and AMLA compliance for digital assets', 's'),
        ('06', 'FCA financial promotions compliance for crypto', 'UK FCA financial promotion rules for cryptoasset marketing', 's'),
        ('07', 'SEC/CFTC registration assessment', 'Analysis of SEC and CFTC requirements for digital asset activities', 'd'),
        ('08', 'JFSA crypto asset exchange service compliance', 'Japan FSA registration and compliance for CAES', 's'),
      ]),
    ]),
  ]),
  ('03', 'Market Integrity & Consumer Protection', 'Controls preventing market abuse and protecting clients', [
    ('01', 'Market Abuse Prevention', 'Surveillance controls preventing manipulation in digital asset markets', [
      ('01', 'Trade Surveillance Programme', 'Market surveillance for crypto-specific manipulation patterns', [
        ('01', 'Wash trading detection for digital assets', 'Surveillance for wash trading and fictitious transaction patterns', 's'),
        ('02', 'Insider dealing controls for token listings', 'Information barrier controls around new token listings', 's'),
        ('03', 'Spoofing and layering surveillance', 'Surveillance for spoofing and layering in crypto order books', 's'),
        ('04', 'Front-running and MEV policy', 'Policy and controls preventing front-running of client crypto orders', 's'),
        ('05', 'Trade and transaction reporting (MiCA, MAR)', 'Submitting trade and transaction reports to regulators', 'd'),
      ]),
    ]),
    ('02', 'Client Asset Protection', 'Regulatory requirements protecting client digital assets', [
      ('01', 'Client Protection Controls', 'Controls and disclosures protecting digital asset clients', [
        ('01', 'Client money rules for crypto (FCA CASS)', 'Applying FCA CASS client money rules to crypto custody', 's'),
        ('02', 'Client disclosure and risk warning requirements', 'Required risk warnings and disclosures for digital asset clients', 'm'),
        ('03', 'Client complaint handling for digital assets', 'Complaint handling and redress procedures for DA clients', 'm'),
        ('04', 'Retail investor suitability assessment', 'Assessing retail investor suitability for digital asset products', 's'),
      ]),
    ]),
  ]),
],

}  # end DOMAINS

# ---------------------------------------------------------------------------
# Additional features per domain (merged into DOMAINS at seed time)
# Each entry: domain_id -> list of additional L0 blocks (same format as DOMAINS)
# ---------------------------------------------------------------------------

DOMAINS_EXTRA = {

'custody': [
  ('02', 'Asset Administration & Corporate Actions', 'Managing corporate events and income on custodied digital assets', [
    ('01', 'Corporate Actions Processing', 'Handling lifecycle events on custodied digital assets', [
      ('01', 'On-chain Corporate Action Detection', 'Automated detection and processing of on-chain events', [
        ('01', 'Hard fork detection and replay protection', 'Automated detection of hard forks and replay attack protection', 'm'),
        ('02', 'Airdrop asset custody and eligibility tracking', 'Tracking and securing airdropped assets for eligible custodied holders', 's'),
        ('03', 'Token migration handling (contract upgrade)', 'Managing token migrations when ERC-20 contracts are upgraded', 's'),
        ('04', 'Chain split asset crediting', 'Crediting new chain assets to holders after contentious chain splits', 's'),
        ('05', 'Staking withdrawal queue monitoring (Ethereum)', 'Monitoring Ethereum validator exit and withdrawal queues', 'd'),
        ('06', 'NFT corporate action processing', 'Handling royalties, trait changes, and NFT-related events', 'd'),
      ]),
      ('02', 'Income & Distribution Processing', 'Distributing staking, lending, and fee income to clients', [
        ('01', 'Staking reward distribution to clients', 'Automated distribution of staking rewards to beneficial owners', 's'),
        ('02', 'DeFi yield income collection and distribution', 'Collecting and distributing DeFi protocol income to clients', 'd'),
        ('03', 'Lending fee income reconciliation', 'Reconciling lending fees earned on custodied assets', 'd'),
        ('04', 'Tax lot accounting for digital asset income', 'Per-tax-lot accounting for staking and income events', 's'),
      ]),
    ]),
    ('02', 'Counterparty Settlement & Collateral', 'Settlement and collateral management for custodied assets', [
      ('01', 'Collateral Management', 'Using custodied digital assets as collateral', [
        ('01', 'Digital asset collateral eligibility framework', 'Defining eligible digital assets for use as collateral', 's'),
        ('02', 'Real-time collateral valuation (mark-to-market)', 'Continuous mark-to-market of digital asset collateral values', 's'),
        ('03', 'Margin call processing for digital asset collateral', 'Automated margin call generation and collection for DA collateral', 'd'),
        ('04', 'Collateral substitution and optimisation', 'Automated collateral substitution to optimise funding cost', 'd'),
        ('05', 'Tri-party collateral management integration', 'Integration with tri-party agents for digital asset collateral', 'd'),
        ('06', 'Rehypothecation controls for custodied assets', 'Controls governing permitted rehypothecation of client assets', 's'),
      ]),
      ('02', 'Securities Lending & Borrowing', 'Lending custodied digital assets for income generation', [
        ('01', 'Digital asset securities lending programme', 'Programme for lending custodied digital assets to approved borrowers', 'd'),
        ('02', 'Borrower credit assessment for DA lending', 'Credit assessment framework for digital asset securities borrowers', 'd'),
        ('03', 'Collateral receipt and management for lending', 'Receiving and managing collateral against digital asset loans', 'd'),
        ('04', 'Lending revenue sharing with clients', 'Revenue sharing model for client income from asset lending', 'd'),
        ('05', 'Recall and return process for lent assets', 'Procedures for recalling lent digital assets from borrowers', 'd'),
      ]),
    ]),
  ]),
  ('03', 'Custody Technology Platform', 'Core technology platform supporting custody operations', [
    ('01', 'Blockchain Node Infrastructure', 'Node infrastructure for blockchain connectivity', [
      ('01', 'Full Node Operations', 'Running and maintaining blockchain full nodes', [
        ('01', 'Bitcoin full node cluster management', 'Highly available Bitcoin full node cluster for custody operations', 'm'),
        ('02', 'Ethereum execution and consensus client management', 'Running Geth/Besu and Prysm/Lighthouse node pairs', 'm'),
        ('03', 'Multi-chain node monitoring and alerting', 'Real-time health monitoring for custody blockchain nodes', 'm'),
        ('04', 'Node sync recovery procedures', 'Documented recovery procedures for out-of-sync blockchain nodes', 's'),
        ('05', 'Archival node access for historical queries', 'Archival node access for historical transaction lookups', 's'),
        ('06', 'Private RPC endpoint security', 'Securing internal RPC endpoints from external access', 'm'),
      ]),
      ('02', 'Blockchain Data Indexing', 'Indexing and querying blockchain data for custody operations', [
        ('01', 'Transaction indexing for custodied addresses', 'Indexed transaction history for all custodied wallet addresses', 'm'),
        ('02', 'Token transfer event indexing (ERC-20, ERC-721)', 'Indexed token transfer events for portfolio and reporting', 'm'),
        ('03', 'Block reorganisation detection and handling', 'Automated detection of block reorgs with confirmation depth policies', 'm'),
        ('04', 'Multi-chain data lake for analytics', 'Centralised data lake of on-chain data for custody analytics', 'd'),
      ]),
    ]),
    ('02', 'Custody Platform Resilience', 'Business continuity and disaster recovery for custody platforms', [
      ('01', 'Business Continuity', 'BCP and DR for custody platform operations', [
        ('01', 'RPO/RTO targets for custody systems', 'Defined recovery point and recovery time objectives for custody systems', 'm'),
        ('02', 'Active-active data centre architecture', 'Multi-data-centre active-active deployment for custody platforms', 's'),
        ('03', 'Custody platform DR drill programme', 'Annual disaster recovery drills for custody platform failover', 'm'),
        ('04', 'Immutable offsite backup for custody data', 'Offsite immutable backups for custody ledger and key metadata', 'm'),
        ('05', 'Custody platform change management controls', 'Rigorous change management for custody-critical systems', 'm'),
        ('06', 'DORA ICT resilience compliance for custody', 'EU DORA digital operational resilience requirements for custody', 'd'),
      ]),
    ]),
  ]),
],

'wallets': [
  ('03', 'Network-Specific Wallet Implementations', 'Wallet support optimised per blockchain network', [
    ('01', 'Bitcoin Wallet Features', 'Bitcoin-specific wallet functionality', [
      ('01', 'Bitcoin-Specific Operations', 'Native Bitcoin wallet capabilities', [
        ('01', 'UTXO coin selection algorithms', 'Optimal UTXO coin selection minimising fees and privacy leakage', 'm'),
        ('02', 'Bitcoin fee estimation (mempool-aware)', 'Real-time mempool-aware fee estimation for Bitcoin transactions', 'm'),
        ('03', 'SegWit v0 and Taproot address support', 'Full P2WPKH, P2TR address type support for Bitcoin wallets', 'm'),
        ('04', 'Lightning Network channel management', 'Opening, managing, and closing Lightning Network channels', 'd'),
        ('05', 'PSBT multi-party signing workflow', 'Partially Signed Bitcoin Transaction workflow for cold signing', 'm'),
        ('06', 'Bitcoin RBF fee bumping UX', 'User-facing RBF fee bump for unconfirmed Bitcoin transactions', 's'),
      ]),
    ]),
    ('02', 'EVM Wallet Features', 'Ethereum and EVM-compatible chain wallet functionality', [
      ('01', 'EVM-Specific Operations', 'Native EVM wallet capabilities', [
        ('01', 'EIP-712 structured data signing', 'Typed data signing per EIP-712 for DeFi and NFT interactions', 's'),
        ('02', 'EIP-2612 permit signature handling', 'Gasless token approvals via permit signature support', 'd'),
        ('03', 'EVM chain ID management (multi-chain)', 'Safe chain ID management preventing replay across EVM networks', 'm'),
        ('04', 'Multi-call transaction batching', 'Batching multiple EVM calls into a single transaction', 'd'),
        ('05', 'Smart account migration tooling', 'Migrating assets from EOA to smart account wallet type', 'd'),
        ('06', 'EVM mempool monitoring for pending transactions', 'Monitoring mempool for pending outbound EVM transactions', 's'),
      ]),
    ]),
    ('03', 'Multi-Chain Wallet Integration', 'Cross-chain wallet operations and standards', [
      ('01', 'Chain Abstraction & Interoperability', 'Abstracting chain differences for seamless multi-chain operations', [
        ('01', 'Cross-chain address derivation management', 'Deriving and managing addresses consistently across 20+ chains', 's'),
        ('02', 'Unified balance aggregation across chains', 'Single view of client balances across all supported chains', 's'),
        ('03', 'Chain-agnostic fee estimation API', 'Common API abstraction for fee estimation across different chains', 'd'),
        ('04', 'Native token vs ERC-20 handling abstraction', 'Abstracted handling for native gas tokens vs token assets', 's'),
        ('05', 'Solana SPL token wallet support', 'Native SPL token support for Solana wallet operations', 's'),
        ('06', 'Cosmos IBC transfer support', 'IBC cross-chain transfer support for Cosmos ecosystem wallets', 'd'),
      ]),
    ]),
  ]),
  ('04', 'Wallet Analytics & Reporting', 'Analytics and reporting tools for institutional wallet operations', [
    ('01', 'Wallet Performance Analytics', 'Analytical tools for wallet usage and performance', [
      ('01', 'Wallet Metrics & Dashboard', 'Operational metrics and management dashboards for wallets', [
        ('01', 'Real-time wallet balance dashboard', 'Live dashboard of all wallet balances across tiers and chains', 'm'),
        ('02', 'Transaction throughput and latency reporting', 'Reporting on wallet transaction volumes and confirmation times', 's'),
        ('03', 'Fee spend analysis and optimisation reports', 'Reporting on gas and fee spend with optimisation recommendations', 's'),
        ('04', 'Wallet utilisation heat map', 'Visualisation of wallet activity by time, chain, and client', 'd'),
        ('05', 'Hot/warm/cold tier balance ratio monitoring', 'Monitoring balance distribution across storage tiers', 's'),
        ('06', 'Client-level wallet activity report', 'Per-client wallet activity and balance summary reporting', 's'),
      ]),
    ]),
  ]),
],

'stablecoins': [
  ('03', 'Stablecoin Technology & Interoperability', 'Technical infrastructure for multi-chain stablecoin operations', [
    ('01', 'Multi-Chain Stablecoin Deployment', 'Deploying and managing stablecoins across multiple blockchains', [
      ('01', 'Cross-Chain Stablecoin Architecture', 'Technical design for multi-chain stablecoin availability', [
        ('01', 'Native issuance vs bridged token decision framework', 'Framework for deciding between native issuance and bridging per chain', 'd'),
        ('02', 'CCTP (Circle Cross-Chain Transfer Protocol)', 'Integration with Circle CCTP for native USDC multi-chain transfer', 'd'),
        ('03', 'Canonical bridge lock-and-mint mechanism', 'Lock-and-mint bridge design for controlled cross-chain supply', 'd'),
        ('04', 'Stablecoin supply cap management per chain', 'Governance controls for per-chain stablecoin supply caps', 'd'),
        ('05', 'Bridge exploit monitoring and circuit breaker', 'Real-time monitoring of bridge contracts with emergency pause', 'd'),
        ('06', 'Multi-chain supply reconciliation', 'Reconciling total circulating supply across all chains and bridges', 'd'),
      ]),
    ]),
    ('02', 'Stablecoin Analytics', 'Analytics and monitoring for stablecoin operations', [
      ('01', 'Stablecoin Operational Analytics', 'Dashboards and analytics for stablecoin issuers', [
        ('01', 'Real-time peg deviation monitoring', 'Monitoring secondary market price vs peg with deviation alerts', 'm'),
        ('02', 'Mint/burn volume trend analysis', 'Historical and trend analysis of minting and redemption volumes', 's'),
        ('03', 'Holder concentration analysis', 'Analysing large holder concentration risk in stablecoin distribution', 'd'),
        ('04', 'On-chain velocity and turnover analysis', 'Measuring transaction velocity and turnover of circulating supply', 'd'),
        ('05', 'Reserve yield optimisation reporting', 'Reporting on yield generated from reserve assets', 'd'),
        ('06', 'Stablecoin regulatory dashboard', 'Consolidated dashboard tracking regulatory KPIs for stablecoin issuers', 'd'),
      ]),
    ]),
    ('03', 'Commodity-Backed & Alternative Stablecoins', 'Infrastructure for commodity-backed and hybrid stablecoin structures', [
      ('01', 'Commodity-Backed Stablecoin Operations', 'Operational controls for gold and commodity-backed tokens', [
        ('01', 'Precious metal vault integration for gold-backed tokens', 'Integrating vault custody for gold backing tokenised gold products', 'd'),
        ('02', 'Physical commodity delivery and redemption process', 'Procedures for physical commodity delivery on token redemption', 'd'),
        ('03', 'Commodity valuation oracle integration', 'On-chain commodity price oracle for gold/silver-backed tokens', 'd'),
        ('04', 'Warehouse receipt tokenisation', 'Converting commodity warehouse receipts to on-chain tokens', 'd'),
      ]),
    ]),
  ]),
],

'cbdc': [
  ('04', 'CBDC Technology Architecture', 'Technical architecture and design choices for CBDC platforms', [
    ('01', 'DLT Platform Selection for CBDC', 'Evaluating and implementing DLT platforms for CBDC', [
      ('01', 'CBDC Platform Technology Assessment', 'Technical evaluation of DLT platforms for CBDC implementation', [
        ('01', 'Permissioned blockchain CBDC architecture (Hyperledger, R3)', 'Evaluating permissioned DLT for central bank CBDC', 'e'),
        ('02', 'Programmable CBDC scripting language design', 'Designing safe scripting environments for CBDC programmability', 'e'),
        ('03', 'CBDC consensus mechanism selection', 'Selecting consensus algorithms balancing finality and throughput', 'e'),
        ('04', 'CBDC ledger throughput benchmarking', 'Benchmarking CBDC ledger TPS against payment system requirements', 'e'),
        ('05', 'CBDC node operator governance', 'Governing which entities can run CBDC network nodes', 'e'),
        ('06', 'CBDC data residency and sovereignty controls', 'Enforcing data residency and sovereignty requirements in CBDC design', 'e'),
      ]),
    ]),
    ('02', 'CBDC Integration & APIs', 'APIs and integration patterns for CBDC-connected services', [
      ('01', 'CBDC API & Integration Standards', 'Standardised APIs for CBDC integration with financial services', [
        ('01', 'Open CBDC API specification (REST/gRPC)', 'Standardised CBDC API for commercial bank integration', 'e'),
        ('02', 'ISO 20022 messaging for CBDC transactions', 'Using ISO 20022 message formats for CBDC payment instructions', 'e'),
        ('03', 'CBDC to core banking system integration', 'Connecting CBDC platform to commercial bank core banking systems', 'e'),
        ('04', 'CBDC POS terminal integration for retail', 'Integrating retail CBDC acceptance at point-of-sale terminals', 'e'),
        ('05', 'CBDC interoperability with card networks', 'Bridge between retail CBDC and existing card payment networks', 'e'),
        ('06', 'Open banking API (PSD2/CDR) linkage to CBDC', 'Connecting CBDC to open banking API ecosystems', 'e'),
        ('07', 'CBDC developer sandbox and testnet', 'Developer sandbox environment for CBDC integration testing', 'e'),
      ]),
    ]),
    ('03', 'CBDC Governance & Operations', 'Governance frameworks and operational procedures for CBDC programmes', [
      ('01', 'CBDC Programme Governance', 'Governance structures for CBDC design and deployment', [
        ('01', 'CBDC policy framework and design principles', 'Documenting CBDC design choices and policy rationale', 'e'),
        ('02', 'Central bank-commercial bank role delineation', 'Defining responsibilities between central and commercial bank in CBDC model', 'e'),
        ('03', 'CBDC issuance and destruction policy', 'Governance over CBDC issuance, destruction, and total supply limits', 'e'),
        ('04', 'CBDC system incident response and communication', 'IR and communication procedures for CBDC system outages', 'e'),
        ('05', 'CBDC pilot to production migration plan', 'Managing transition from CBDC pilot to production deployment', 'e'),
      ]),
    ]),
  ]),
],

'settlement': [
  ('04', 'Settlement Technology & Standards', 'Technology infrastructure and industry standards for settlement', [
    ('01', 'Settlement Data Standards', 'Industry data standards for digital asset settlement', [
      ('01', 'ISO Standards for Digital Asset Settlement', 'ISO 20022 and related standards applied to digital asset settlement', [
        ('01', 'ISO 20022 adoption for crypto settlement messages', 'Using ISO 20022 message formats for digital asset settlement', 'd'),
        ('02', 'UTI and USI harmonisation for crypto derivatives', 'Unique Transaction/Swap Identifiers for crypto derivatives reporting', 'd'),
        ('03', 'LEI integration for counterparty identification', 'Legal entity identifier use in digital asset settlement chains', 's'),
        ('04', 'SSI database for digital asset settlement instructions', 'Standard settlement instructions database for digital asset trades', 's'),
        ('05', 'SWIFT gpi integration for stablecoin corridors', 'Linking SWIFT gpi with stablecoin cross-border payment flows', 'd'),
      ]),
    ]),
    ('02', 'Settlement Risk Management', 'Managing and mitigating settlement risk exposures', [
      ('01', 'Settlement Risk Framework', 'Quantifying and managing settlement risk for digital assets', [
        ('01', 'Settlement exposure measurement (PFE for crypto)', 'Measuring settlement exposure including potential future exposure', 'd'),
        ('02', 'Settlement netting and compression', 'Compressing settlement obligations via bilateral and multilateral netting', 'd'),
        ('03', 'Intraday liquidity monitoring for settlement', 'Real-time intraday liquidity monitoring for settlement obligations', 's'),
        ('04', 'Settlement concentration risk monitoring', 'Monitoring concentration of settlement flows through single venues', 'd'),
        ('05', 'Digital asset settlement loss provisioning', 'Provisioning methodology for settlement loss scenarios', 'd'),
        ('06', 'Settlement SLA dashboard and breach alerting', 'Real-time SLA monitoring with automated breach notifications', 's'),
      ]),
    ]),
    ('03', 'Post-Trade Infrastructure', 'Post-trade reporting and lifecycle management', [
      ('01', 'Post-Trade Reporting', 'Regulatory and counterparty post-trade reporting', [
        ('01', 'EMIR crypto derivative trade reporting', 'Reporting crypto derivatives under EU EMIR trade reporting regime', 'd'),
        ('02', 'MiFIR transaction reporting for crypto', 'MiFIR transaction reporting for regulated crypto instruments', 'd'),
        ('03', 'CFTC swap reporting for crypto derivatives', 'CFTC swap data repository reporting for crypto swaps', 'd'),
        ('04', 'Post-trade transparency and public tape', 'Contributing to public post-trade transparency for digital assets', 'e'),
        ('05', 'Trade confirmation and settlement status API', 'API providing real-time settlement status to counterparties', 'd'),
      ]),
    ]),
  ]),
],

'tokenisation': [
  ('03', 'Tokenisation Standards & Interoperability', 'Technical standards and interoperability for tokenised assets', [
    ('01', 'Token Interoperability', 'Cross-platform and cross-chain tokenised asset portability', [
      ('01', 'Cross-Platform Token Standards', 'Standards enabling tokenised asset interoperability', [
        ('01', 'ERC-3525 semi-fungible token for structured products', 'Using ERC-3525 for structured product tokenisation', 'd'),
        ('02', 'ERC-4626 tokenised vault standard for funds', 'Using ERC-4626 for tokenised investment vault structures', 'd'),
        ('03', 'ACTUS financial contract standard on-chain', 'Implementing ACTUS cashflow modelling for tokenised bonds', 'e'),
        ('04', 'Interledger Protocol (ILP) integration', 'Using ILP for atomic cross-platform asset transfers', 'e'),
        ('05', 'Token metadata standards (EIP-1155, ERC-7512)', 'Standardising on-chain token metadata for institutional assets', 'd'),
        ('06', 'Legal document hash anchoring on-chain', 'Anchoring legal agreement hashes on-chain for tokenised assets', 'd'),
      ]),
    ]),
    ('02', 'Alternative Asset Tokenisation', 'Tokenising infrastructure, carbon, and supply chain assets', [
      ('01', 'Infrastructure & Alternatives Tokenisation', 'Tokenised access to infrastructure and alternative investments', [
        ('01', 'Infrastructure debt tokenisation', 'Tokenising infrastructure loan and bond exposures', 'd'),
        ('02', 'Carbon credit tokenisation (Toucan, KlimaDAO frameworks)', 'Tokenising verified carbon credits on-chain', 'd'),
        ('03', 'Supply chain finance receivable tokenisation', 'Converting supply chain receivables to tradeable digital tokens', 'd'),
        ('04', 'Aviation and maritime asset tokenisation', 'Tokenised fractional ownership of aircraft and shipping assets', 'd'),
        ('05', 'Art and collectible tokenisation (authentication)', 'Blockchain-authenticated tokenisation of physical art and collectibles', 'd'),
        ('06', 'Insurance risk tokenisation (ILS/cat bonds)', 'Tokenising insurance-linked securities and catastrophe bonds', 'd'),
      ]),
    ]),
    ('03', 'Tokenisation Operations & Client Services', 'Operational and client-facing services for tokenised asset programmes', [
      ('01', 'Issuer & Investor Services', 'Services supporting tokenised asset issuers and investors', [
        ('01', 'Investor onboarding portal for tokenised assets', 'Self-service investor onboarding and subscription portal', 'd'),
        ('02', 'Tokenised asset investor reporting', 'Periodic NAV, income, and performance reporting for token holders', 'd'),
        ('03', 'Corporate action instruction gateway for tokens', 'Receiving and processing corporate action elections from token holders', 'd'),
        ('04', 'Tokenised asset primary dealer network', 'Network of primary dealers supporting tokenised issuance and distribution', 'd'),
        ('05', 'Tax reporting for tokenised asset holders', 'Annual tax reporting for investors in tokenised fund and asset structures', 'd'),
      ]),
    ]),
  ]),
],

'defi_protocols': [
  ('04', 'DeFi Treasury & Structured Products', 'DeFi-based treasury management and structured product access', [
    ('01', 'DeFi Yield Strategies', 'Institutional yield generation via DeFi protocols', [
      ('01', 'Structured DeFi Yield Products', 'Packaged DeFi yield strategies for institutional clients', [
        ('01', 'Principal protected DeFi yield note', 'Structured product combining DeFi yield with principal protection', 'd'),
        ('02', 'DeFi yield aggregator integration (Yearn, Convex)', 'Using yield aggregators for optimised DeFi strategy returns', 'd'),
        ('03', 'Real yield vs inflationary reward differentiation', 'Distinguishing protocol real yield from token emission rewards', 'd'),
        ('04', 'Basis trading via DeFi (cash and carry)', 'Crypto cash-and-carry basis trade execution via DeFi protocols', 'd'),
        ('05', 'DeFi options vault (DOV) strategies', 'Covered call and put option vault strategies via DeFi', 'd'),
        ('06', 'Fixed rate DeFi lending (Notional, Yield Protocol)', 'Accessing fixed interest rates via DeFi fixed rate protocols', 'd'),
      ]),
    ]),
    ('02', 'DeFi Derivatives & Hedging', 'Derivatives and hedging via decentralised protocols', [
      ('01', 'DeFi Derivatives Access', 'Institutional access to DeFi-based derivatives instruments', [
        ('01', 'Perpetual swap trading on decentralised platforms', 'Trading crypto perpetuals on dYdX, GMX, and similar protocols', 'd'),
        ('02', 'On-chain options (Lyra, Premia) integration', 'Accessing DeFi options protocols for hedging and yield', 'd'),
        ('03', 'Interest rate swap via DeFi (Pendle)', 'Hedging interest rate exposure via DeFi rate swap protocols', 'd'),
        ('04', 'Synthetic asset exposure via DeFi (Synthetix)', 'Accessing synthetic off-chain asset exposure via DeFi', 'd'),
        ('05', 'On-chain volatility index monitoring', 'Tracking implied and realised volatility via on-chain sources', 'd'),
      ]),
    ]),
    ('03', 'DeFi Protocol Due Diligence', 'Structured diligence and onboarding for new DeFi protocols', [
      ('01', 'Protocol Onboarding Framework', 'Standardised process for approving new DeFi protocol interactions', [
        ('01', 'DeFi protocol onboarding checklist', 'Comprehensive onboarding checklist covering code, governance, liquidity', 'd'),
        ('02', 'Protocol TVL trend and liquidity depth analysis', 'Historical TVL trend and liquidity depth assessment', 'd'),
        ('03', 'Token governance concentration risk assessment', 'Assessing governance token distribution and whale concentration', 'd'),
        ('04', 'DeFi protocol insurance coverage check', 'Verifying Nexus Mutual or similar coverage for protocol risk', 'd'),
        ('05', 'Historical incident and hack review', 'Reviewing protocol history of exploits and security incidents', 'd'),
        ('06', 'Economic model and tokenomics sustainability review', 'Assessing protocol economic model for long-term sustainability', 'd'),
      ]),
    ]),
  ]),
],

'security': [
  ('05', 'Data & Network Security', 'Data protection and network security controls', [
    ('01', 'Network Security', 'Controls protecting digital asset infrastructure networks', [
      ('01', 'Network Segmentation & Zero Trust', 'Zero trust architecture and network segmentation for custody', [
        ('01', 'Zero trust network architecture for custody systems', 'Zero trust segmentation isolating custody infrastructure', 'm'),
        ('02', 'Micro-segmentation of HSM and signing networks', 'Network micro-segmentation isolating HSM signing networks', 'm'),
        ('03', 'API gateway security for custody APIs', 'API gateway with rate limiting, WAF, and authentication for custody APIs', 'm'),
        ('04', 'DDoS protection for custody infrastructure', 'DDoS mitigation for externally accessible custody services', 'm'),
        ('05', 'Encrypted data-in-transit for all custody communications', 'TLS 1.3 and mTLS enforced for all custody data in transit', 'm'),
        ('06', 'Network traffic anomaly detection (NDR)', 'AI-driven network detection and response for custody networks', 'd'),
      ]),
    ]),
    ('02', 'Data Security', 'Protecting sensitive data in custody and compliance operations', [
      ('01', 'Data Classification & Protection', 'Controls protecting custody and client data', [
        ('01', 'Data classification policy for digital asset data', 'Classifying custody data by sensitivity (public/internal/confidential/secret)', 'm'),
        ('02', 'Encryption at rest for custody databases', 'AES-256 encryption at rest for all custody-related databases', 'm'),
        ('03', 'Key management for data encryption keys (KMIP)', 'Central KMIP-compliant key management for data encryption keys', 'm'),
        ('04', 'Data loss prevention (DLP) for custody operations', 'DLP controls preventing exfiltration of sensitive custody data', 'm'),
        ('05', 'Database activity monitoring for custody systems', 'Real-time monitoring and alerting on custody database access', 's'),
        ('06', 'GDPR/data privacy compliance for client data', 'GDPR and data privacy controls for digital asset client data', 'm'),
        ('07', 'Sensitive data masking in logs and analytics', 'Masking private keys, addresses, and PII in logs and analytics', 'm'),
      ]),
    ]),
  ]),
  ('06', 'Third-Party & Supply Chain Risk', 'Managing security risks from third-party vendors and supply chain', [
    ('01', 'Vendor Security Management', 'Security assessment and monitoring of third-party vendors', [
      ('01', 'Third-Party Risk Programme', 'Formal third-party security risk management for custody vendors', [
        ('01', 'Vendor security assessment (SOC 2, ISO 27001)', 'Reviewing SOC 2 and ISO 27001 reports for custody technology vendors', 'm'),
        ('02', 'MPC vendor technical due diligence', 'Deep technical review of MPC library vendors and their cryptographic implementations', 's'),
        ('03', 'Cloud provider shared responsibility model review', 'Reviewing cloud provider SRM for custody workloads', 'm'),
        ('04', 'Software dependency vulnerability scanning (SCA)', 'Software composition analysis on custody codebase dependencies', 's'),
        ('05', 'Vendor concentration risk assessment', 'Monitoring single-vendor concentration in custody infrastructure', 's'),
        ('06', 'Fourth-party supply chain risk assessment', 'Assessing sub-vendors used by critical custody technology providers', 'd'),
      ]),
    ]),
  ]),
],

'ai_agentic': [
  ('04', 'AI Analytics & Data Infrastructure', 'Data infrastructure and analytics capabilities powering AI in digital assets', [
    ('01', 'On-Chain Data Analytics', 'AI-powered analytics on blockchain and DeFi data', [
      ('01', 'On-Chain Intelligence Platform', 'Platform for AI-driven analysis of on-chain data', [
        ('01', 'On-chain entity attribution and labelling', 'AI-assisted labelling of on-chain addresses and entities', 'd'),
        ('02', 'Network graph analytics for crypto flows', 'Graph analytics visualising fund flow networks on-chain', 'd'),
        ('03', 'DeFi protocol health scoring via AI', 'AI health scoring of DeFi protocols using on-chain metrics', 'd'),
        ('04', 'Smart money wallet tracking', 'Identifying and tracking institutional and smart money wallet activity', 'd'),
        ('05', 'Token unlock and supply schedule analytics', 'Tracking upcoming token unlocks and their market impact signals', 'd'),
        ('06', 'On-chain sentiment and social signal integration', 'Incorporating social media and forum signals into on-chain analytics', 'd'),
      ]),
    ]),
    ('02', 'AI-Assisted Trading & Execution', 'AI tools supporting institutional trading and execution decisions', [
      ('01', 'AI Execution Analytics', 'AI-driven transaction cost analysis and execution optimisation', [
        ('01', 'TWAP/VWAP AI execution optimisation', 'AI-optimised TWAP and VWAP execution for large crypto orders', 'd'),
        ('02', 'Slippage prediction for institutional crypto orders', 'ML models predicting market impact and slippage for large orders', 'd'),
        ('03', 'Cross-venue routing AI for crypto execution', 'AI routing engine optimising execution across multiple crypto venues', 'd'),
        ('04', 'Pre-trade AI market impact assessment', 'Pre-trade model estimating market impact of proposed block trades', 'd'),
        ('05', 'Post-trade TCA for crypto execution quality', 'Transaction cost analysis evaluating crypto execution quality', 'd'),
      ]),
    ]),
    ('03', 'AI Data Governance', 'Governance of data used to train and operate AI models', [
      ('01', 'AI Data Management', 'Data quality, lineage, and governance for AI in digital assets', [
        ('01', 'Training data quality and lineage programme', 'Ensuring data quality and documenting lineage for AI training data', 'd'),
        ('02', 'Feature store for digital asset ML models', 'Centralised feature store serving on-chain features to ML models', 'd'),
        ('03', 'Model training data privacy review', 'Ensuring training data does not contain client PII or confidential data', 'd'),
        ('04', 'AI data access controls and audit log', 'Controls on who can access AI training data with audit logging', 'd'),
        ('05', 'Synthetic data generation for AML model training', 'Generating synthetic transaction data for AML model training', 'd'),
      ]),
    ]),
  ]),
],

'compliance_regulation': [
  ('04', 'Prudential & Capital Requirements', 'Capital requirements and prudential rules for digital asset exposures', [
    ('01', 'Basel III/IV Digital Asset Capital', 'Implementing Basel prudential standards for digital asset exposures', [
      ('01', 'Basel Crypto Prudential Implementation', 'Bank capital treatment of digital assets under Basel framework', [
        ('01', 'Group 1 cryptoasset capital calculation (tokenised assets)', 'RWA calculation for Group 1 tokenised assets under Basel III', 'd'),
        ('02', 'Group 2a cryptoasset capital calculation (stablecoins)', 'RWA calculation for Group 2a unbacked stablecoins', 'd'),
        ('03', 'Group 2b cryptoasset capital calculation (BTC/ETH)', '1250% RWA charge implementation for Group 2b crypto assets', 'd'),
        ('04', 'Basel crypto aggregate exposure limit (1% of T1)', 'Monitoring and enforcing Basel 1% Tier 1 capital exposure limit', 'd'),
        ('05', 'Crypto hedging recognition under Basel framework', 'Assessing hedge recognition for crypto positions under Basel', 'd'),
        ('06', 'Pillar 3 disclosure for digital asset exposures', 'Public disclosure of digital asset exposure and capital metrics', 'd'),
      ]),
    ]),
    ('02', 'Liquidity & Funding Risk', 'Liquidity risk management for digital asset businesses', [
      ('01', 'Digital Asset Liquidity Risk Management', 'LCR, NSFR, and liquidity risk for digital asset operations', [
        ('01', 'LCR treatment of digital asset holdings', 'Assessing HQLA eligibility and LCR treatment of crypto assets', 'd'),
        ('02', 'NSFR funding requirements for crypto lending', 'Net stable funding ratio analysis for digital asset lending activities', 'd'),
        ('03', 'Intraday liquidity monitoring for crypto settlements', 'Real-time monitoring of intraday liquidity for crypto settlement', 's'),
        ('04', 'Crypto liquidity stress testing scenarios', 'Stress test scenarios for digital asset liquidity (market crash, exchange failure)', 'd'),
        ('05', 'Contingency funding plan for digital asset operations', 'CFP covering digital asset-specific liquidity stress scenarios', 'd'),
      ]),
    ]),
  ]),
  ('05', 'Data Privacy & Operational Risk', 'Data privacy compliance and operational risk management', [
    ('01', 'Data Privacy in Digital Asset Operations', 'GDPR and privacy requirements for digital asset client data', [
      ('01', 'Data Privacy Programme', 'Privacy compliance for digital asset client and transaction data', [
        ('01', 'GDPR lawful basis for processing crypto client data', 'Establishing GDPR lawful basis for digital asset client data processing', 'm'),
        ('02', 'Privacy impact assessment for on-chain data use', 'PIA for use of public blockchain data in compliance monitoring', 'm'),
        ('03', 'Right to erasure and blockchain immutability conflict', 'Addressing GDPR right to erasure in context of blockchain immutability', 'd'),
        ('04', 'Cross-border data transfer compliance for crypto data', 'GDPR SCCs and adequacy decisions for international crypto data transfers', 'm'),
        ('05', 'Biometric and KYC data retention controls', 'Retention limits and security controls for KYC biometric data', 'm'),
      ]),
    ]),
    ('02', 'Operational Risk Management', 'Operational risk identification and control for digital assets', [
      ('01', 'Digital Asset Operational Risk Framework', 'RCSA and key risk indicators for digital asset operations', [
        ('01', 'Digital asset RCSA (risk control self-assessment)', 'Formal RCSA covering operational risks in custody and trading', 'm'),
        ('02', 'Key risk indicators for digital asset operations', 'KRIs monitoring wallet errors, failed transactions, key incidents', 'm'),
        ('03', 'Operational risk event collection for digital assets', 'Collecting and analysing operational loss events in DA operations', 'm'),
        ('04', 'Op risk scenario analysis for crypto (tail events)', 'Scenario analysis for extreme operational risk events in crypto', 'd'),
        ('05', 'Business continuity testing for compliance systems', 'BCP testing for KYC, TM, and regulatory reporting systems', 'm'),
        ('06', 'Third-party op risk for blockchain analytics providers', 'Operational risk assessment for blockchain analytics vendor dependency', 'd'),
      ]),
    ]),
  ]),
],

}  # end DOMAINS_EXTRA

DOMAINS_EXTRA2 = {

'custody': [
  ('04', 'Custody Client Services', 'Client-facing services and onboarding for institutional custody clients', [
    ('01', 'Client Onboarding', 'Onboarding processes for institutional custody clients', [
      ('01', 'Institutional Client Onboarding', 'End-to-end onboarding for institutional custody clients', [
        ('01', 'Institutional custody RFP response framework', 'Structured framework for responding to institutional custody RFPs', 's'),
        ('02', 'Custody account opening and legal documentation', 'Account opening documentation including custody agreement and SLA', 'm'),
        ('03', 'Sub-custody network management', 'Managing relationships with sub-custodians for multi-jurisdiction coverage', 's'),
        ('04', 'Omnibus vs segregated account election process', 'Client election process for omnibus or segregated custody structures', 'm'),
        ('05', 'Custody fee billing and invoice generation', 'Automated fee calculation and invoice generation for custody clients', 'm'),
        ('06', 'Client portal access provisioning', 'Providing clients access to custody portal for reporting and monitoring', 's'),
      ]),
    ]),
    ('02', 'Client Reporting', 'Regular reports delivered to institutional custody clients', [
      ('01', 'Custody Client Reporting Suite', 'Portfolio and regulatory reports for custody clients', [
        ('01', 'Daily NAV and asset statement report', 'Daily statement of custodied asset values and balances', 'm'),
        ('02', 'Monthly custody performance report', 'Monthly summary of custody activities, income, and corporate actions', 'm'),
        ('03', 'Transaction history export (CSV/PDF/API)', 'Client-accessible transaction history in multiple formats', 'm'),
        ('04', 'Tax reporting package for custody clients', 'Annual tax reporting data export for client tax compliance', 's'),
        ('05', 'Regulatory reporting support for clients (Basel III)', 'Supporting clients with Basel III reporting using custody data', 'd'),
        ('06', 'ESG and carbon footprint report for custodied assets', 'Reporting carbon footprint of PoW and PoS assets in custody', 'e'),
      ]),
    ]),
  ]),
],

'wallets': [
  ('05', 'Wallet Security Deep Controls', 'Advanced security controls for institutional wallet operations', [
    ('01', 'Wallet Access Controls', 'Authentication and authorisation for wallet access', [
      ('01', 'Strong Authentication for Wallets', 'Multi-factor authentication controls for wallet access', [
        ('01', 'Hardware token (FIDO2) for wallet operations', 'FIDO2/WebAuthn hardware keys required for wallet operations', 'm'),
        ('02', 'Biometric authentication for wallet mobile access', 'Biometric auth for institutional mobile wallet access', 'd'),
        ('03', 'Role-based access control for wallet functions', 'RBAC matrix governing wallet operations by staff role', 'm'),
        ('04', 'Wallet operation approval workflow engine', 'Configurable approval workflows for wallet transactions', 's'),
        ('05', 'IP allowlisting for wallet API access', 'Restricting wallet API access to approved IP ranges', 'm'),
        ('06', 'Time-based access controls for wallet ops', 'Restricting wallet operations to defined business hours', 's'),
        ('07', 'Anomaly detection on wallet admin access patterns', 'ML-based anomaly detection on wallet administrator behaviour', 'd'),
      ]),
    ]),
    ('02', 'Wallet Audit & Compliance', 'Audit trails and compliance records for wallet operations', [
      ('01', 'Wallet Audit Programme', 'Comprehensive audit and compliance for wallet operations', [
        ('01', 'Immutable wallet operation audit log', 'Immutable log of all wallet operations with non-repudiation', 'm'),
        ('02', 'Wallet audit log SIEM integration', 'Forwarding wallet audit logs to SIEM for security monitoring', 's'),
        ('03', 'Quarterly wallet access review', 'Quarterly review and certification of wallet access permissions', 'm'),
        ('04', 'Wallet transaction anomaly alerting', 'Automated alerts for unusual wallet transaction patterns', 's'),
        ('05', 'Wallet compliance report for regulators', 'Periodic compliance reports covering wallet activity for regulators', 'd'),
        ('06', 'SOC 2 Type II audit coverage for wallet platform', 'Including wallet platform in annual SOC 2 Type II audit scope', 's'),
      ]),
    ]),
  ]),
  ('06', 'Institutional Wallet Use Cases', 'Specific wallet configurations for institutional use cases', [
    ('01', 'Treasury Wallet Operations', 'Wallet configuration for corporate treasury and working capital', [
      ('01', 'Corporate Treasury Crypto Wallet', 'Wallet management for corporate treasury digital asset holdings', [
        ('01', 'Corporate BTC/ETH treasury wallet policy', 'Governance policy for corporate crypto treasury management', 's'),
        ('02', 'Stablecoin payment wallet for vendor settlement', 'Stablecoin wallet for B2B vendor and supplier payments', 'd'),
        ('03', 'Multi-currency stablecoin treasury management', 'Managing USDC, EURC, and other stablecoins in corporate treasury', 'd'),
        ('04', 'On-chain FX conversion for treasury', 'Converting between stablecoins on-chain for treasury FX needs', 'd'),
        ('05', 'Treasury crypto exposure hedging integration', 'Connecting treasury crypto holdings to hedging instruments', 'd'),
        ('06', 'Payroll in digital assets processing', 'Processing employee compensation in digital assets where permitted', 'd'),
      ]),
    ]),
    ('02', 'Institutional Trading Wallet', 'Wallet infrastructure supporting institutional trading desks', [
      ('01', 'Trading Desk Wallet Configuration', 'Wallets configured for trading desk operations', [
        ('01', 'Market maker hot wallet inventory management', 'Managing market-making inventory across hot wallet tiers', 's'),
        ('02', 'Pre-funded exchange wallet management', 'Managing exchange-pre-funded wallets for algorithmic trading', 's'),
        ('03', 'Real-time P&L tracking by wallet', 'Per-wallet P&L tracking for trading desk attribution', 's'),
        ('04', 'Overnight sweep of trading wallets to cold', 'Automated end-of-day sweep of trading wallet balances to cold storage', 's'),
        ('05', 'Multi-exchange wallet rebalancing automation', 'Automated rebalancing of exchange balances for optimal liquidity', 'd'),
      ]),
    ]),
  ]),
],

'stablecoins': [
  ('04', 'Stablecoin Payments & Infrastructure', 'Payment use cases and infrastructure for stablecoin adoption', [
    ('01', 'Cross-Border Payment Use Cases', 'Stablecoin-based cross-border payment corridors', [
      ('01', 'Institutional Cross-Border Stablecoin Flows', 'Enabling institutional cross-border payments via stablecoins', [
        ('01', 'Real-time stablecoin cross-border payment execution', 'Sub-minute cross-border stablecoin transfers for B2B payments', 'd'),
        ('02', 'SWIFT gpi vs stablecoin corridor comparison', 'Cost and speed benchmarking of stablecoin vs SWIFT gpi for corridors', 'd'),
        ('03', 'Correspondent banking stablecoin integration', 'Integrating stablecoin payments with correspondent banking network', 'd'),
        ('04', 'Stablecoin FX conversion at point of receipt', 'Converting received stablecoins to local fiat at destination', 'd'),
        ('05', 'Stablecoin payment compliance (AML/sanctions)', 'Screening stablecoin cross-border payments for AML and sanctions', 'm'),
        ('06', 'G20 cross-border payment roadmap alignment', 'Aligning stablecoin payment strategy with G20 cross-border roadmap', 'd'),
        ('07', 'Stablecoin remittance corridor development', 'Developing retail remittance corridors using stablecoins', 'd'),
      ]),
    ]),
    ('02', 'Institutional Stablecoin Settlement', 'Using stablecoins for institutional settlement flows', [
      ('01', 'Stablecoin Settlement Operations', 'Operational procedures for stablecoin-based settlement', [
        ('01', 'DVP settlement using stablecoins', 'Using stablecoins as payment leg in tokenised asset DvP settlement', 'd'),
        ('02', 'Intraday stablecoin liquidity management', 'Managing intraday stablecoin liquidity for settlement obligations', 'd'),
        ('03', 'Stablecoin nostro account management', 'Managing stablecoin balances in nostro accounts for payments', 'd'),
        ('04', 'End-of-day stablecoin position reconciliation', 'Reconciling stablecoin positions at close of business', 's'),
        ('05', 'Failed stablecoin transfer resolution', 'Procedures for identifying and resolving failed stablecoin payments', 's'),
      ]),
    ]),
    ('03', 'Stablecoin Risk Management', 'Risk management framework specific to stablecoin operations', [
      ('01', 'Stablecoin Risk Framework', 'Comprehensive risk management for stablecoin issuers and users', [
        ('01', 'Reserve run risk scenario modelling', 'Modelling risk of mass redemption events on reserve liquidity', 's'),
        ('02', 'Stablecoin peg break contingency plan', 'Contingency procedures for stablecoin de-pegging events', 's'),
        ('03', 'Counterparty concentration risk in reserves', 'Monitoring concentration of reserve assets at individual banks', 's'),
        ('04', 'Smart contract risk for stablecoin contracts', 'Ongoing security monitoring of stablecoin smart contracts', 's'),
        ('05', 'Regulatory action scenario planning', 'Planning for regulatory action scenarios (ban, restriction, audit)', 'd'),
        ('06', 'FX risk in multi-currency stablecoin reserves', 'Managing FX risk in reserves backing non-USD stablecoins', 'd'),
      ]),
    ]),
  ]),
],

'cbdc': [
  ('05', 'CBDC Risk & Compliance', 'Risk management and compliance for CBDC participation', [
    ('01', 'CBDC Operational Risk', 'Operational risk specific to CBDC programme participation', [
      ('01', 'CBDC Operational Controls', 'Controls for safe CBDC programme participation', [
        ('01', 'CBDC system availability SLA monitoring', 'Monitoring CBDC platform availability against SLA commitments', 'e'),
        ('02', 'CBDC transaction error handling and retry', 'Automated error handling and retry for failed CBDC transactions', 'e'),
        ('03', 'CBDC operational incident classification', 'Incident severity classification for CBDC platform events', 'e'),
        ('04', 'CBDC cyber resilience testing (DORA compliance)', 'CBDC-specific cyber resilience testing under DORA requirements', 'e'),
        ('05', 'Central bank reporting obligations for CBDC participation', 'Meeting central bank reporting requirements as a CBDC distributor', 'e'),
        ('06', 'CBDC settlement finality risk management', 'Managing operational risk from CBDC settlement finality rules', 'e'),
      ]),
    ]),
    ('02', 'CBDC Financial Risk', 'Financial risks arising from CBDC participation', [
      ('01', 'CBDC Financial Risk Assessment', 'Capital, liquidity, and market risks from CBDC programme', [
        ('01', 'Disintermediation risk assessment from retail CBDC', 'Modelling deposit outflow risk from retail CBDC adoption', 'e'),
        ('02', 'CBDC liquidity management and facility access', 'Accessing central bank liquidity facilities during CBDC stress', 'e'),
        ('03', 'Interest rate risk from CBDC remuneration policy', 'Managing interest rate risk from CBDC remuneration design', 'e'),
        ('04', 'CBDC credit risk (counterparty exposure)', 'Assessing credit risk exposure arising from CBDC participation', 'e'),
        ('05', 'CBDC market risk in reserve management', 'Market risk in assets held against CBDC distribution liabilities', 'e'),
      ]),
    ]),
    ('03', 'CBDC Client Experience', 'Commercial bank client experience for CBDC distribution', [
      ('01', 'CBDC Client Journey Design', 'User experience design for CBDC distribution to retail and corporate clients', [
        ('01', 'Retail CBDC UX research and design', 'User research and design for retail CBDC customer journeys', 'e'),
        ('02', 'Corporate CBDC treasury integration UX', 'UX for corporate treasury teams accessing CBDC payment features', 'e'),
        ('03', 'CBDC accessibility features (inclusivity)', 'Designing CBDC access for populations with limited digital access', 'e'),
        ('04', 'CBDC client education and awareness programme', 'Client education programme on CBDC use cases and safety', 'e'),
        ('05', 'CBDC support and dispute resolution procedures', 'Customer support and dispute resolution for CBDC transactions', 'e'),
        ('06', 'CBDC product bundling with banking services', 'Packaging CBDC access within existing bank product offerings', 'e'),
      ]),
    ]),
  ]),
],

'settlement': [
  ('05', 'Settlement Connectivity', 'Connectivity and integration with settlement infrastructure', [
    ('01', 'CSD & CCP Connectivity', 'Technical connectivity with CSDs and CCPs for digital assets', [
      ('01', 'CSD Integration', 'Connecting to central securities depositories for digital asset settlement', [
        ('01', 'DTCC settlement connectivity for tokenised securities', 'Connecting tokenised securities settlement to DTCC infrastructure', 'd'),
        ('02', 'Euroclear / Clearstream integration for DA settlement', 'Linking digital asset settlement to Euroclear/Clearstream', 'd'),
        ('03', 'SIX Digital Exchange (SDX) connectivity', 'Direct connectivity to SIX Digital Exchange for CHF-denominated tokens', 'd'),
        ('04', 'BondbloX settlement connectivity (tokenised bonds)', 'Integration with BondbloX Bond Exchange for fractional bond trading', 'd'),
        ('05', 'CSD API modernisation for DLT integration', 'Using CSD REST APIs for settlement instruction submission', 'd'),
        ('06', 'Central bank settlement account integration', 'Direct connection to central bank settlement accounts for final settlement', 'd'),
      ]),
    ]),
    ('02', 'Exchange & Venue Connectivity', 'Connectivity to crypto trading and settlement venues', [
      ('01', 'Exchange Connectivity', 'API connectivity to institutional crypto exchanges', [
        ('01', 'Prime brokerage connectivity for crypto trading', 'Connecting to prime brokerage platforms for institutional crypto access', 's'),
        ('02', 'Institutional exchange API connectivity (Coinbase, Kraken)', 'Institutional-grade API connectivity to regulated crypto exchanges', 's'),
        ('03', 'OTC desk electronic connectivity (RFQ/streaming)', 'Electronic connectivity to OTC desks for crypto price streaming', 's'),
        ('04', 'Dark pool and block trading venue connectivity', 'Connectivity to institutional crypto dark pool venues', 'd'),
        ('05', 'Smart order routing across crypto venues', 'Intelligent order routing across exchanges and OTC venues', 'd'),
        ('06', 'Crypto exchange credit risk monitoring', 'Real-time credit risk monitoring for exchange counterparty exposures', 's'),
      ]),
    ]),
    ('03', 'Treasury & Cash Management Integration', 'Integrating settlement with treasury and cash management', [
      ('01', 'Treasury Integration', 'Linking digital asset settlement to bank treasury systems', [
        ('01', 'Nostro account integration for crypto settlement', 'Integrating crypto settlement flows with nostro account management', 'd'),
        ('02', 'Intraday settlement cash flow forecasting', 'Forecasting intraday settlement cash requirements for digital assets', 'd'),
        ('03', 'Real-time debit and credit posting to GL', 'Real-time general ledger postings for digital asset settlement events', 'd'),
        ('04', 'Settlement cut-off time management for crypto', 'Managing crypto settlement cut-off times across time zones', 's'),
        ('05', 'Crypto settlement capital charge optimisation', 'Minimising capital charges on unsettled crypto exposures', 'd'),
      ]),
    ]),
  ]),
],

'tokenisation': [
  ('04', 'Tokenisation Market Infrastructure', 'Market infrastructure supporting the tokenised asset ecosystem', [
    ('01', 'Regulated Tokenisation Platforms', 'Regulated platforms for tokenised asset issuance and trading', [
      ('01', 'Regulated Venue Participation', 'Participating in regulated tokenised asset venues', [
        ('01', 'SIX Digital Exchange participation (Switzerland)', 'Participation in SDX for CHF tokenised asset issuance and trading', 'd'),
        ('02', 'HKEX digitalised securities platform', 'Engagement with HKEX tokenised securities platform', 'd'),
        ('03', 'LuxSE Digital Securities platform', 'Listing tokenised bonds on Luxembourg Stock Exchange digital platform', 'd'),
        ('04', 'Singapore MAS Project Guardian participation', 'Participation in MAS Project Guardian for institutional DeFi', 'd'),
        ('05', 'DTCC tokenised asset settlement integration', 'Connecting tokenised assets to DTCC for settlement processing', 'd'),
        ('06', 'Euronext tokenised security listing', 'Process for listing tokenised equity or debt on Euronext markets', 'd'),
      ]),
    ]),
    ('02', 'Tokenisation Legal & Tax Framework', 'Legal and tax treatment for tokenised asset structures', [
      ('01', 'Legal & Tax Infrastructure', 'Legal and tax frameworks supporting tokenised asset operations', [
        ('01', 'Digital asset legal ownership determination', 'Analysis of legal title and ownership for tokenised assets', 'd'),
        ('02', 'Conflict of laws analysis for tokenised assets', 'Cross-border conflict of laws analysis for token transfers', 'd'),
        ('03', 'UNIDROIT digital assets convention alignment', 'Aligning tokenised asset structures with UNIDROIT Digital Assets Convention', 'd'),
        ('04', 'Capital gains tax treatment of tokenised asset sales', 'Tax analysis of capital gains treatment for institutional token sales', 'd'),
        ('05', 'Stamp duty and transaction tax for token transfers', 'Analysis of stamp duty and transaction taxes on secondary token trades', 'd'),
        ('06', 'Accounting treatment for tokenised assets (IFRS/US GAAP)', 'IFRS and US GAAP accounting treatment for tokenised asset holdings', 'd'),
      ]),
    ]),
    ('03', 'Tokenisation Analytics', 'Analytics and reporting for tokenised asset programmes', [
      ('01', 'Tokenisation Market Intelligence', 'Market data and intelligence for the tokenised asset ecosystem', [
        ('01', 'Tokenised asset market size and growth tracking', 'Tracking total market size and growth of tokenised real world assets', 'd'),
        ('02', 'On-chain tokenised asset liquidity analytics', 'Analysing secondary market liquidity depth for tokenised assets', 'd'),
        ('03', 'Tokenised asset price performance benchmarking', 'Benchmarking tokenised asset price performance vs traditional equivalents', 'd'),
        ('04', 'Cross-platform tokenised asset inventory', 'Aggregating tokenised asset inventory across multiple platforms', 'd'),
        ('05', 'Institutional adoption tracker for tokenisation', 'Tracking institutional adoption rates across asset classes', 'd'),
      ]),
    ]),
  ]),
],

'defi_protocols': [
  ('05', 'DeFi Regulatory Compliance', 'Regulatory compliance for institutional DeFi activities', [
    ('01', 'DeFi Legal & Regulatory Framework', 'Legal analysis and regulatory compliance for DeFi participation', [
      ('01', 'DeFi Regulatory Engagement', 'Regulatory strategy and compliance for DeFi activities', [
        ('01', 'MiCA DeFi activity classification analysis', 'Classifying DeFi activities under MiCA regulatory categories', 'd'),
        ('02', 'SEC Howey test analysis for DeFi token exposure', 'Applying Howey test analysis to DeFi governance token holdings', 'd'),
        ('03', 'CFTC jurisdiction assessment for DeFi derivatives', 'Analysing CFTC jurisdiction over DeFi perpetuals and options', 'd'),
        ('04', 'AML obligations for DeFi interactions', 'Understanding and meeting AML obligations for VASP-DeFi interactions', 'd'),
        ('05', 'Sanctions screening for DeFi smart contract interactions', 'OFAC and EU sanctions screening before DeFi contract interaction', 'm'),
        ('06', 'FATF Travel Rule application to DeFi flows', 'Applying FATF Travel Rule to DeFi transfers above threshold', 'd'),
        ('07', 'DeFi activity regulatory reporting requirements', 'Assessing reporting obligations for institutional DeFi activities', 'd'),
      ]),
    ]),
    ('02', 'DeFi Operational Compliance', 'Operational compliance controls for DeFi interactions', [
      ('01', 'DeFi Compliance Operations', 'Day-to-day compliance operations for DeFi activities', [
        ('01', 'DeFi interaction pre-approval workflow', 'Compliance pre-approval process for new DeFi protocol interactions', 'd'),
        ('02', 'DeFi activity logging for compliance audit', 'Complete transaction log of all DeFi interactions for audit', 'd'),
        ('03', 'DeFi profit and loss regulatory reporting', 'Reporting P&L and income from DeFi activities to regulators', 'd'),
        ('04', 'DeFi KYC obligation for permissioned pools', 'Meeting KYC obligations when accessing permissioned DeFi pools', 'd'),
        ('05', 'DeFi legal entity disclosure requirements', 'Disclosing DeFi activities in financial statements and regulatory filings', 'd'),
      ]),
    ]),
  ]),
  ('06', 'DeFi Innovation Tracking', 'Monitoring and assessing emerging DeFi developments', [
    ('01', 'DeFi Protocol Pipeline', 'Identifying and assessing new DeFi protocol opportunities', [
      ('01', 'DeFi Innovation Monitoring', 'Ongoing monitoring of DeFi protocol developments', [
        ('01', 'Weekly DeFi protocol landscape review', 'Systematic weekly review of new DeFi protocols and protocol upgrades', 'd'),
        ('02', 'DeFi protocol volume and fee trend tracking', 'Tracking weekly volume and fee revenue across key DeFi protocols', 'd'),
        ('03', 'Institutional DeFi partnership development', 'Building strategic partnerships with compliant DeFi protocol teams', 'd'),
        ('04', 'DeFi protocol deprecation risk monitoring', 'Monitoring for signals of protocol deprecation or migration', 'd'),
        ('05', 'Layer 2 DeFi ecosystem development tracking', 'Monitoring DeFi ecosystem growth on Arbitrum, Optimism, Base, zkSync', 'd'),
      ]),
    ]),
  ]),
],

'security': [
  ('07', 'DORA & Regulatory Security Compliance', 'Digital Operational Resilience Act and regulatory security requirements', [
    ('01', 'DORA ICT Risk Management', 'Implementing DORA ICT risk management requirements', [
      ('01', 'DORA ICT Risk Framework', 'Core DORA ICT risk management framework for financial entities', [
        ('01', 'DORA ICT risk management policy and governance', 'ICT risk management policy meeting DORA Article 5 requirements', 'd'),
        ('02', 'DORA ICT asset register and classification', 'Comprehensive ICT asset register supporting DORA risk assessment', 'd'),
        ('03', 'DORA threat-led penetration testing (TLPT)', 'Threat-led penetration testing programme under DORA Article 26', 'd'),
        ('04', 'DORA major ICT incident classification and reporting', 'Classifying and reporting major ICT incidents per DORA RTS', 'd'),
        ('05', 'DORA third-party ICT provider register', 'Register of critical third-party ICT providers under DORA', 'd'),
        ('06', 'DORA digital operational resilience testing programme', 'Annual DORA resilience testing including scenario and BCP tests', 'd'),
        ('07', 'DORA information sharing participation', 'Participating in DORA cyber threat information sharing arrangements', 'd'),
      ]),
    ]),
    ('02', 'Cyber Regulatory Reporting', 'Cyber incident reporting to regulators', [
      ('01', 'Cyber Incident Regulatory Reporting', 'Regulatory notification for material cyber incidents', [
        ('01', 'FCA cyber incident reporting (72-hour rule)', 'FCA material cyber incident notification within 72 hours', 'm'),
        ('02', 'DORA initial and final cyber incident notification', 'DORA three-stage cyber incident notification process', 'd'),
        ('03', 'SEC cybersecurity incident disclosure (Form 8-K)', 'SEC cybersecurity incident disclosure under Reg S-K Item 1.05', 'd'),
        ('04', 'MAS cyber incident reporting (TRM Guidelines)', 'MAS Technology Risk Management cyber incident reporting', 's'),
        ('05', 'Cross-jurisdiction cyber incident notification management', 'Coordinating cyber incident notifications across multiple regulators', 'd'),
        ('06', 'Post-incident regulatory review preparation', 'Preparing for regulatory review following a significant cyber incident', 'd'),
      ]),
    ]),
  ]),
  ('08', 'Physical Security', 'Physical security controls for digital asset infrastructure', [
    ('01', 'Data Centre & Vault Physical Security', 'Physical security for data centres and key storage vaults', [
      ('01', 'Physical Security Controls', 'Controls protecting physical infrastructure for digital assets', [
        ('01', 'Tier IV data centre selection for custody systems', 'Selecting Tier IV data centres for custody infrastructure hosting', 'm'),
        ('02', 'Biometric access control for data centres', 'Biometric authentication required for custody data centre access', 'm'),
        ('03', 'CCTV monitoring of server rooms and vaults', '24/7 CCTV coverage of custody server rooms and key storage vaults', 'm'),
        ('04', 'Mantrap and anti-tailgating controls', 'Physical mantrap systems preventing unauthorised data centre entry', 'm'),
        ('05', 'Physical security audit programme', 'Annual independent audit of physical security controls for custody', 'm'),
        ('06', 'Device control for custody locations (USB, mobile)', 'Restricting personal devices and storage media in custody areas', 'm'),
      ]),
    ]),
  ]),
],

'ai_agentic': [
  ('05', 'Agentic System Safety', 'Safety controls for AI agents operating in financial contexts', [
    ('01', 'AI Agent Safety Framework', 'Safety and control framework for autonomous AI agents', [
      ('01', 'Agentic Safety Controls', 'Core safety controls for AI agents in digital asset operations', [
        ('01', 'Agent kill switch and emergency stop', 'Immediate halt capability for any AI agent in production', 'e'),
        ('02', 'Agent rate limiting and blast radius controls', 'Limiting frequency and scope of AI agent tool calls', 'e'),
        ('03', 'Agent output sanitisation and validation', 'Validating AI agent outputs before execution in production', 'e'),
        ('04', 'Prompt injection detection for agent inputs', 'Detecting and blocking prompt injection attempts in agent inputs', 'e'),
        ('05', 'Agent sandbox environment for pre-production testing', 'Isolated sandbox for testing AI agent behaviour before deployment', 'e'),
        ('06', 'Agent financial limit enforcement', 'Hard financial limits enforced on AI agent transaction authority', 'e'),
        ('07', 'Agent behaviour regression testing', 'Automated regression tests for AI agent behaviour on known scenarios', 'e'),
      ]),
    ]),
    ('02', 'AI Transparency & Explainability', 'Transparency and explainability of AI decisions in financial operations', [
      ('01', 'AI Explainability Controls', 'Controls ensuring AI decisions are explainable to regulators and clients', [
        ('01', 'AI decision explanation for compliance decisions', 'Generating human-readable explanations for AI compliance decisions', 'd'),
        ('02', 'Model card documentation for production AI', 'Publishing model cards for all AI models in production', 'd'),
        ('03', 'Counterfactual explanation generation', 'Generating counterfactual explanations for rejected or flagged decisions', 'd'),
        ('04', 'AI output uncertainty quantification', 'Quantifying and communicating confidence levels in AI outputs', 'd'),
        ('05', 'Regulator-accessible AI explanation interface', 'Interface enabling regulators to request explanations of AI decisions', 'd'),
        ('06', 'AI decision appeal and override process', 'Formal process for appealing and overriding AI-generated decisions', 'd'),
      ]),
    ]),
  ]),
  ('06', 'AI Infrastructure & MLOps', 'Infrastructure and MLOps platform for digital asset AI', [
    ('01', 'MLOps Platform', 'Machine learning operations infrastructure for production AI', [
      ('01', 'ML Infrastructure', 'Core MLOps infrastructure supporting digital asset AI models', [
        ('01', 'Model registry and versioning', 'Central registry tracking all ML model versions in production', 'd'),
        ('02', 'CI/CD pipeline for ML model deployment', 'Automated testing and deployment pipeline for ML model updates', 'd'),
        ('03', 'A/B testing framework for ML models', 'Statistical A/B testing framework for comparing ML model versions', 'd'),
        ('04', 'Model serving infrastructure for real-time scoring', 'Low-latency model serving infrastructure for real-time decisions', 'd'),
        ('05', 'Distributed training for large blockchain dataset models', 'Distributed ML training on large-scale on-chain transaction datasets', 'd'),
        ('06', 'GPU/accelerator resource management for AI', 'Managing GPU and AI accelerator resources for ML workloads', 'd'),
        ('07', 'ML experiment tracking (MLflow, Weights & Biases)', 'Tracking ML experiments for reproducibility and comparison', 'd'),
      ]),
    ]),
  ]),
],

'compliance_regulation': [
  ('06', 'Financial Crime Technology', 'Technology platforms supporting financial crime compliance', [
    ('01', 'Compliance Technology Platform', 'Core technology platform for financial crime compliance operations', [
      ('01', 'RegTech Platform Architecture', 'Architecture and tooling for compliance technology platform', [
        ('01', 'Case management system for AML investigations', 'Unified case management for AML alert investigation and disposition', 'm'),
        ('02', 'Workflow automation for KYC refresh', 'Automated workflow engine for triggering and tracking KYC refresh', 's'),
        ('03', 'Regulatory reporting automation platform', 'Automated generation and submission of regulatory reports', 's'),
        ('04', 'Compliance data lake architecture', 'Centralised compliance data lake for analytics and auditing', 'd'),
        ('05', 'Regulatory change management system', 'Tracking regulatory changes and mapping to compliance controls', 's'),
        ('06', 'Compliance API for real-time screening integration', 'REST API enabling real-time AML screening in transaction flows', 's'),
      ]),
    ]),
    ('02', 'Sanctions Compliance Programme', 'Comprehensive sanctions compliance controls', [
      ('01', 'Sanctions Screening Operations', 'Operational sanctions screening controls for digital asset businesses', [
        ('01', 'Dual-use goods and crypto mining sanction screening', 'Screening for sanctioned entities in crypto mining equipment supply', 'm'),
        ('02', 'OFAC Specially Designated Nationals (SDN) list screening', 'Automated SDN list screening for all client and transaction data', 'm'),
        ('03', 'EU consolidated sanctions list screening', 'EU consolidated sanctions list screening for European operations', 'm'),
        ('04', 'UN Security Council sanctions list screening', 'UN Security Council sanctions screening for global operations', 'm'),
        ('05', 'Jurisdiction-specific sanctions monitoring (UK, AU, CA)', 'OFSI, DFAT, and Global Affairs Canada sanctions list monitoring', 'm'),
        ('06', 'Sanctions hit false positive management', 'Structured process for reviewing and clearing sanctions false positives', 'm'),
        ('07', 'OFAC licence application for blocked asset management', 'Process for applying for OFAC licence to manage blocked assets', 's'),
      ]),
    ]),
  ]),
],

}  # end DOMAINS_EXTRA2

DOMAINS_EXTRA3 = {

'stablecoins': [
  ('05', 'Stablecoin Market & Ecosystem', 'Market development and ecosystem engagement for stablecoin issuers', [
    ('01', 'Ecosystem Development', 'Building developer and market participant ecosystems', [
      ('01', 'Stablecoin Ecosystem & Developer Relations', 'Programmes supporting stablecoin ecosystem growth', [
        ('01', 'Stablecoin developer grant programme', 'Funding developers building on stablecoin payment infrastructure', 'd'),
        ('02', 'Stablecoin merchant acceptance programme', 'Working with merchants to accept stablecoin payments', 'd'),
        ('03', 'Stablecoin API developer documentation', 'Comprehensive developer documentation for stablecoin integration', 'd'),
        ('04', 'Stablecoin test network (testnet) provision', 'Providing testnet for developers building stablecoin integrations', 'd'),
        ('05', 'Stablecoin exchange listing strategy', 'Securing listings on regulated exchanges for stablecoin liquidity', 'd'),
        ('06', 'Market maker programme for stablecoin liquidity', 'Engaging market makers to maintain stablecoin liquidity and peg', 'd'),
        ('07', 'Stablecoin DeFi protocol integration programme', 'Working with DeFi protocols to integrate stablecoin as base asset', 'd'),
        ('08', 'Industry standards participation (Centre, Pyth)', 'Participating in stablecoin industry standards bodies and consortia', 'd'),
      ]),
    ]),
    ('02', 'Stablecoin Product Management', 'Product strategy and lifecycle management for stablecoin offerings', [
      ('01', 'Product Lifecycle Management', 'Managing stablecoin product design, launch, and evolution', [
        ('01', 'Stablecoin product roadmap and versioning', 'Managing stablecoin product features and upgrade roadmap', 'd'),
        ('02', 'Multi-currency stablecoin product suite', 'Issuing stablecoins in USD, EUR, GBP, CHF, and other currencies', 'd'),
        ('03', 'Institutional vs retail stablecoin product differentiation', 'Designing separate institutional and retail stablecoin product tiers', 'd'),
        ('04', 'Stablecoin interest-bearing variant design', 'Designing yield-bearing variants of stablecoin products', 'd'),
        ('05', 'Stablecoin sunset and migration procedures', 'Procedures for safely deprecating and migrating stablecoin versions', 'd'),
        ('06', 'Stablecoin brand and trust building programme', 'Brand management and trust-building for stablecoin credibility', 'd'),
      ]),
    ]),
  ]),
],

'cbdc': [
  ('06', 'CBDC Business Strategy', 'Commercial strategy for bank participation in CBDC programmes', [
    ('01', 'CBDC Commercial Model', 'Business model design for CBDC distribution and services', [
      ('01', 'CBDC Revenue Model', 'Designing revenue models around CBDC distribution', [
        ('01', 'CBDC distribution fee model development', 'Designing fee structures for CBDC distribution services to end users', 'e'),
        ('02', 'Value-added CBDC services monetisation', 'Monetising programmable and data services layered on CBDC infrastructure', 'e'),
        ('03', 'CBDC cross-sell and bundling strategy', 'Bundling CBDC with FX, trade finance, and other bank products', 'e'),
        ('04', 'CBDC institutional B2B payment revenue', 'Generating revenue from institutional B2B CBDC payment services', 'e'),
        ('05', 'CBDC competitive positioning vs stablecoins', 'Positioning bank-distributed CBDC vs private stablecoin alternatives', 'e'),
        ('06', 'CBDC first-mover advantage strategy', 'Identifying and capturing first-mover advantages in CBDC distribution', 'e'),
        ('07', 'CBDC ecosystem partnership development', 'Building payment ecosystem partnerships around CBDC distribution', 'e'),
        ('08', 'CBDC impact on deposit franchise analysis', 'Modelling impact of CBDC on bank deposit funding and NII', 'e'),
      ]),
    ]),
    ('02', 'CBDC Readiness Assessment', 'Assessing organisational readiness for CBDC participation', [
      ('01', 'CBDC Readiness Diagnostic', 'Internal assessment of readiness for CBDC programme participation', [
        ('01', 'CBDC technology readiness assessment', 'Assessing internal technology stack readiness for CBDC integration', 'e'),
        ('02', 'CBDC operational readiness assessment', 'Evaluating operational processes and staffing for CBDC participation', 'e'),
        ('03', 'CBDC compliance readiness assessment', 'Reviewing compliance capability for CBDC regulatory obligations', 'e'),
        ('04', 'CBDC financial risk readiness assessment', 'Assessing capital and liquidity framework readiness for CBDC', 'e'),
        ('05', 'CBDC staff training and skills programme', 'Training programme building internal CBDC knowledge and skills', 'e'),
        ('06', 'CBDC board and senior management briefing', 'Governance briefings for board and senior management on CBDC strategy', 'e'),
      ]),
    ]),
  ]),
],

'settlement': [
  ('06', 'Derivatives Settlement', 'Settlement operations for digital asset derivative instruments', [
    ('01', 'Crypto Derivatives Settlement', 'Settlement processes for crypto futures, options, and swaps', [
      ('01', 'Crypto Derivative Settlement Operations', 'Operational settlement for crypto derivative instruments', [
        ('01', 'Physically settled Bitcoin futures delivery', 'Physical delivery settlement for Bitcoin futures at expiry', 's'),
        ('02', 'Cash-settled crypto futures settlement', 'Cash settlement of crypto futures contracts at expiry price', 's'),
        ('03', 'Crypto options exercise and assignment', 'Options exercise and assignment settlement for crypto options', 's'),
        ('04', 'Perpetual swap funding rate settlement', 'Periodic funding rate settlement for crypto perpetual swap positions', 's'),
        ('05', 'Crypto total return swap cash settlement', 'Cash flow settlement for crypto total return swap transactions', 'd'),
        ('06', 'DeFi options settlement (Lyra / Dopex)', 'Settlement of options exercised via DeFi protocol infrastructure', 'd'),
        ('07', 'Crypto structured product coupon settlement', 'Periodic coupon and principal settlement for crypto structured products', 'd'),
        ('08', 'Cross-asset delta settlement (crypto vs equities)', 'Net settlement across crypto and traditional equity derivative books', 'd'),
      ]),
    ]),
    ('02', 'Margin & Collateral Operations', 'Margin and collateral operations for derivative positions', [
      ('01', 'Margin & Collateral Lifecycle', 'End-to-end margin and collateral management for crypto derivatives', [
        ('01', 'Initial margin posting in crypto or stablecoin', 'Posting initial margin for derivatives in crypto or stablecoin form', 'd'),
        ('02', 'Intraday variation margin calls for crypto', 'Multiple daily VM calls for highly volatile crypto derivative books', 'd'),
        ('03', 'Cross-margining crypto with traditional assets', 'Portfolio cross-margining across crypto and traditional instruments', 'd'),
        ('04', 'Crypto collateral haircut framework', 'Applying and managing haircuts on crypto collateral received', 'd'),
        ('05', 'Collateral dispute resolution for crypto', 'Resolving collateral valuation disputes with counterparties', 'd'),
        ('06', 'Collateral optimisation across crypto and bonds', 'Optimising collateral composition across crypto and bond holdings', 'd'),
      ]),
    ]),
  ]),
],

'tokenisation': [
  ('05', 'Tokenisation Client Services', 'Client-facing services for issuers and investors in tokenised markets', [
    ('01', 'Issuer Platform Services', 'Services supporting tokenised asset issuers', [
      ('01', 'Issuer Origination & Structuring', 'Front-to-back support for tokenised asset issuers', [
        ('01', 'Tokenised bond structuring advisory', 'Advisory on optimal structure for tokenised bond programmes', 'd'),
        ('02', 'Green and sustainability token structuring', 'Structuring ESG-linked tokenised instruments (green bonds, SLBs)', 'd'),
        ('03', 'Tokenisation feasibility study for issuers', 'Producing feasibility studies for new tokenised asset programmes', 'd'),
        ('04', 'Tokenised asset target investor analysis', 'Identifying and profiling institutional investor appetite for tokens', 'd'),
        ('05', 'Tokenised asset marketing and roadshow support', 'Supporting issuer roadshows and investor marketing for token launches', 'd'),
        ('06', 'Smart contract parameter configuration for issuers', 'Configuring token contract parameters per issuer requirements', 'd'),
        ('07', 'Tokenised asset post-issuance support', 'Ongoing lifecycle support for issuers post-token launch', 'd'),
      ]),
    ]),
    ('02', 'Investor Platform Services', 'Services for institutional investors in tokenised assets', [
      ('01', 'Investor Access & Portfolio Management', 'Portfolio management tools for institutional tokenised asset investors', [
        ('01', 'Tokenised asset portfolio management dashboard', 'Real-time portfolio view of all tokenised asset holdings', 'd'),
        ('02', 'Multi-asset tokenised portfolio rebalancing', 'Automated rebalancing of tokenised asset portfolios per mandate', 'd'),
        ('03', 'Tokenised asset risk analytics', 'DV01, duration, and credit risk analytics for tokenised fixed income', 'd'),
        ('04', 'Tokenised fund subscription automation', 'Automated subscription and redemption execution for tokenised funds', 'd'),
        ('05', 'On-chain settlement confirmation to portfolio system', 'Real-time settlement confirmation feed to investor portfolio systems', 'd'),
        ('06', 'Tokenised asset performance attribution reporting', 'Detailed performance attribution for tokenised asset portfolios', 'd'),
      ]),
    ]),
  ]),
],

'defi_protocols': [
  ('07', 'DeFi Product Development', 'Developing institutional DeFi products and partnerships', [
    ('01', 'Institutional DeFi Product Suite', 'Product development for institutional DeFi offerings', [
      ('01', 'DeFi Product Innovation', 'Innovating and launching new institutional DeFi products', [
        ('01', 'Institutional DeFi fund product design', 'Designing fund products providing institutional DeFi exposure', 'd'),
        ('02', 'Crypto credit facility backed by DeFi positions', 'Providing credit against institutional DeFi collateral holdings', 'd'),
        ('03', 'DeFi index product for institutional exposure', 'Creating diversified DeFi protocol index products', 'd'),
        ('04', 'Structured DeFi product (principal protected note)', 'Principal-protected note providing DeFi yield upside', 'd'),
        ('05', 'DeFi insurance and protection product', 'Packaging smart contract insurance for institutional DeFi clients', 'd'),
        ('06', 'DeFi managed account with mandate', 'Discretionary DeFi managed account for institutional investors', 'd'),
        ('07', 'DeFi prime brokerage services', 'Prime brokerage service stack for institutional DeFi participants', 'd'),
        ('08', 'DeFi strategy back-test and simulation tools', 'Historical back-testing tools for evaluating DeFi yield strategies', 'd'),
      ]),
    ]),
  ]),
],

'ai_agentic': [
  ('07', 'AI Client Services', 'AI-powered tools and services for institutional digital asset clients', [
    ('01', 'AI-Powered Client Tools', 'Client-facing AI tools for digital asset portfolio management', [
      ('01', 'Institutional AI Client Platform', 'AI tools provided to institutional digital asset clients', [
        ('01', 'AI-powered portfolio risk dashboard for clients', 'Client-facing AI dashboard providing real-time portfolio risk insights', 'd'),
        ('02', 'Natural language digital asset query interface', 'LLM-powered interface for clients to query custody and portfolio data', 'd'),
        ('03', 'AI market intelligence briefing service', 'Daily AI-generated market intelligence for institutional digital asset clients', 'd'),
        ('04', 'AI-powered rebalancing recommendation engine', 'AI engine providing portfolio rebalancing recommendations', 'd'),
        ('05', 'Predictive analytics for digital asset price signals', 'ML price signal service for institutional trading clients', 'd'),
        ('06', 'AI-driven ESG scoring for digital asset protocols', 'Automated ESG scoring of blockchain protocols and DeFi projects', 'd'),
        ('07', 'Customised AI-generated research reports for clients', 'On-demand AI-generated research reports per client mandate', 'd'),
        ('08', 'AI trade idea generation for digital asset desks', 'AI-assisted trade idea generation for digital asset trading desks', 'd'),
      ]),
    ]),
  ]),
],

}  # end DOMAINS_EXTRA3

DOMAINS_EXTRA4 = {

'wallets': [
  ('07', 'Wallet Product & Client Experience', 'Client experience and product design for institutional wallets', [
    ('01', 'Wallet UX & Product', 'User experience and product features for institutional wallet clients', [
      ('01', 'Institutional Wallet Product Features', 'Features differentiating institutional wallet offerings', [
        ('01', 'Institutional wallet onboarding journey design', 'Designing frictionless onboarding for institutional wallet clients', 'd'),
        ('02', 'Wallet usage analytics and client insights', 'Analysing wallet usage patterns to improve client experience', 'd'),
        ('03', 'Self-service wallet configuration portal', 'Client portal for configuring wallet policies and access controls', 'd'),
        ('04', 'Wallet SLA monitoring and client reporting', 'Tracking and reporting wallet platform SLA metrics to clients', 's'),
        ('05', 'Wallet API playground and sandbox environment', 'Developer sandbox environment for testing wallet API integration', 'd'),
        ('06', 'Wallet integration certification programme', 'Certifying third-party integrators of institutional wallet APIs', 'd'),
        ('07', 'Wallet client success management programme', 'Dedicated client success management for institutional wallet clients', 's'),
        ('08', 'Wallet product competitive benchmarking', 'Benchmarking institutional wallet features vs market competitors', 'd'),
        ('09', 'Institutional wallet mobile app (iOS/Android)', 'Dedicated mobile app for institutional wallet management and approval', 'd'),
      ]),
    ]),
  ]),
],

'stablecoins': [
  ('06', 'Stablecoin Operations Excellence', 'Operational excellence programme for stablecoin issuers', [
    ('01', 'Stablecoin Operations Management', 'Day-to-day operational management of stablecoin issuance', [
      ('01', 'Stablecoin Operational Controls', 'Controls ensuring reliable stablecoin operations', [
        ('01', 'Stablecoin smart contract emergency pause', 'Emergency pause capability for stablecoin contracts in crisis', 'm'),
        ('02', 'Stablecoin issuance rate limiting', 'Controls limiting maximum daily stablecoin issuance velocity', 'd'),
        ('03', 'Stablecoin operational incident response plan', 'Incident response plan for stablecoin platform failures', 'm'),
        ('04', 'Reserve composition change governance process', 'Governance process for approving changes to reserve composition', 'm'),
        ('05', 'Stablecoin wallet blacklist and freeze capability', 'On-chain capability to freeze specific addresses for compliance', 'm'),
        ('06', 'Stablecoin contract upgrade governance', 'Time-locked, multi-sig governance for stablecoin contract upgrades', 'm'),
        ('07', 'Stablecoin operational runbook library', 'Library of documented operational runbooks for key processes', 's'),
        ('08', 'Stablecoin BCP and disaster recovery testing', 'Annual BCP testing for stablecoin issuance and redemption systems', 's'),
        ('09', 'Stablecoin team on-call rota and escalation', 'Defined on-call rota and escalation paths for stablecoin operations', 's'),
        ('10', 'Stablecoin operational KPI dashboard', 'Real-time KPI dashboard for stablecoin operations performance', 'd'),
      ]),
    ]),
  ]),
],

'cbdc': [
  ('07', 'CBDC Innovation & Research', 'Research and innovation activities supporting CBDC strategy', [
    ('01', 'CBDC Research Programme', 'Internal research activities supporting CBDC engagement strategy', [
      ('01', 'CBDC Technology Research', 'Technology research informing CBDC strategy and participation', [
        ('01', 'CBDC distributed ledger technology research', 'Internal research on DLT options for CBDC deployment', 'e'),
        ('02', 'CBDC programmability use case research', 'Identifying and assessing high-value programmable CBDC use cases', 'e'),
        ('03', 'CBDC privacy-enhancing technology research', 'Researching ZKP and MPC solutions for CBDC privacy', 'e'),
        ('04', 'CBDC interoperability protocol research (ILP, Quant Overledger)', 'Evaluating interoperability protocols for cross-CBDC connectivity', 'e'),
        ('05', 'CBDC quantum-resistance cryptography research', 'Assessing post-quantum cryptography requirements for CBDC', 'e'),
        ('06', 'CBDC user behaviour and adoption research', 'Research on customer adoption behaviour for retail CBDC', 'e'),
        ('07', 'CBDC macroeconomic impact modelling', 'Modelling macroeconomic effects of CBDC on bank deposits and credit', 'e'),
        ('08', 'CBDC academic and policy partnership programme', 'Building academic and policy research partnerships for CBDC', 'e'),
        ('09', 'CBDC competitive landscape monitoring', 'Monitoring competitor CBDC programme activities and readiness', 'e'),
        ('10', 'CBDC innovation lab and proof of concept environment', 'Internal innovation lab for rapid CBDC proof-of-concept testing', 'e'),
      ]),
    ]),
  ]),
],

'settlement': [
  ('07', 'Real-Time Settlement Innovation', 'Innovation in settlement speed and efficiency', [
    ('01', 'Instant Settlement Capabilities', 'Technology enabling instantaneous settlement finality', [
      ('01', 'T+0 and Instant Settlement Infrastructure', 'Infrastructure supporting T+0 and real-time settlement', [
        ('01', 'T+0 settlement readiness assessment', 'Assessing operational readiness for T+0 settlement timelines', 'd'),
        ('02', 'Real-time gross settlement for crypto (24/7)', '24/7/365 real-time gross settlement capability for digital assets', 'd'),
        ('03', 'Instant settlement client demand analysis', 'Analysing institutional client demand for instant settlement', 'd'),
        ('04', 'Pre-funding optimisation for T+0 settlement', 'Minimising pre-funding requirements for T+0 settlement', 'd'),
        ('05', 'Instant settlement SLA and commercial model', 'Designing SLA and fee model for instant settlement service', 'd'),
        ('06', 'T+0 settlement regulatory dialogue programme', 'Engaging regulators on T+0 settlement framework development', 'd'),
        ('07', 'Settlement acceleration pilot programme', 'Running pilots to test and demonstrate settlement acceleration benefits', 'd'),
        ('08', 'Atomic settlement vs sequential settlement comparison', 'Analysing operational differences between atomic and sequential settlement', 'd'),
        ('09', 'Block chain finality risk assessment by chain', 'Assessing probabilistic vs deterministic finality per blockchain', 'd'),
        ('10', 'Settlement innovation partnership with fintech', 'Building fintech partnerships to accelerate settlement innovation', 'd'),
      ]),
    ]),
  ]),
],

'tokenisation': [
  ('06', 'Tokenisation Standards Participation', 'Participating in industry standards bodies for tokenised assets', [
    ('01', 'Industry Standards Engagement', 'Active participation in tokenisation standard-setting bodies', [
      ('01', 'Tokenisation Standards Bodies', 'Engaging with key industry bodies setting tokenisation standards', [
        ('01', 'ICMA digital bond standards working group', 'Participating in ICMA digital bond market standards development', 'd'),
        ('02', 'SIFMA digital asset market structure group', 'Engaging with SIFMA digital asset market structure committee', 'd'),
        ('03', 'GFMA tokenisation policy paper contribution', 'Contributing to GFMA global tokenisation policy recommendations', 'd'),
        ('04', 'ISO TC68 digital asset standards participation', 'ISO TC68 standards committee participation for digital assets', 'd'),
        ('05', 'Swift digital asset connectivity programme', 'Participating in Swift digital asset settlement connectivity pilots', 'd'),
        ('06', 'World Economic Forum digital asset governance', 'Contributing to WEF digital asset governance and standards work', 'd'),
        ('07', 'Broadridge DLR network participation', 'Participating in Broadridge Distributed Ledger Repo network', 'd'),
        ('08', 'DTCC tokenisation working group', 'Engaging with DTCC tokenisation strategy and standards group', 'd'),
        ('09', 'Project Guardian (MAS) tokenisation contribution', 'Active contribution to MAS Project Guardian tokenisation pilots', 'd'),
        ('10', 'T-REX and STEX standards body participation', 'Participating in T-REX and STEX tokenisation protocol governance', 'd'),
      ]),
    ]),
  ]),
],

'defi_protocols': [
  ('08', 'DeFi Market Structure', 'Understanding and influencing DeFi market structure', [
    ('01', 'DeFi Market Intelligence', 'Intelligence and analysis of DeFi market structure', [
      ('01', 'DeFi Market Analysis', 'Ongoing analysis of DeFi market structure and dynamics', [
        ('01', 'DeFi TVL concentration and dominance analysis', 'Analysing TVL concentration across DeFi protocols and chains', 'd'),
        ('02', 'DeFi protocol revenue and fee benchmarking', 'Benchmarking protocol revenue vs fees paid by institutional users', 'd'),
        ('03', 'DeFi market microstructure research', 'Researching DeFi market microstructure including AMM price discovery', 'd'),
        ('04', 'MEV landscape analysis for institutional DeFi', 'Analysing MEV impact on institutional DeFi transaction costs', 'd'),
        ('05', 'Layer 2 DeFi cost and speed benchmarking', 'Benchmarking L2 DeFi platforms on cost, speed, and security', 'd'),
        ('06', 'DeFi protocol market share trend tracking', 'Monthly market share analysis across competing DeFi protocols', 'd'),
        ('07', 'DeFi institutional capital flow analysis', 'Tracking institutional capital inflows and outflows in DeFi', 'd'),
        ('08', 'DeFi vs CeFi spread and cost comparison', 'Comparing DeFi and CeFi execution costs for institutional trades', 'd'),
        ('09', 'DeFi protocol competitive moat assessment', 'Assessing competitive moat and switching costs of DeFi protocols', 'd'),
        ('10', 'DeFi regulatory arbitrage risk assessment', 'Monitoring DeFi regulatory arbitrage and its sustainability', 'd'),
      ]),
    ]),
  ]),
],

'security': [
  ('09', 'Security Governance & Culture', 'Security governance framework and security culture programme', [
    ('01', 'Security Governance', 'Governance structures for digital asset security programme', [
      ('01', 'Security Governance Framework', 'Board and management security governance for digital assets', [
        ('01', 'Board-level cybersecurity oversight for digital assets', 'Board-level visibility and oversight of cyber risk in DA operations', 'm'),
        ('02', 'CISO digital asset security roadmap', 'Strategic security roadmap specific to digital asset operations', 'm'),
        ('03', 'Security KRI dashboard for senior management', 'Key risk indicator dashboard for senior management security oversight', 'm'),
        ('04', 'Security risk appetite statement for digital assets', 'Formal risk appetite statement covering digital asset cyber risks', 'm'),
        ('05', 'Security budget allocation for digital asset programme', 'Dedicated security budget for digital asset security controls', 'm'),
        ('06', 'Security operating model (SOC, MSSP, in-house)', 'Defining security operating model for digital asset security monitoring', 'm'),
        ('07', 'Security metrics and OKR programme', 'Defining and tracking OKRs for digital asset security programme', 's'),
        ('08', 'Security culture and awareness programme', 'Security awareness training specific to digital asset risks', 'm'),
        ('09', 'Bug bounty programme management', 'Managing responsible disclosure and bug bounty programme', 's'),
        ('10', 'Security community engagement (BSides, DEF CON)', 'Engaging with security research community for intelligence and talent', 'd'),
      ]),
    ]),
  ]),
],

'ai_agentic': [
  ('08', 'AI Ethics & Responsible AI', 'Responsible AI framework for digital asset applications', [
    ('01', 'Responsible AI Programme', 'Ethics and responsible use framework for AI in digital assets', [
      ('01', 'Responsible AI Controls', 'Controls ensuring ethical and responsible AI deployment', [
        ('01', 'AI ethics policy for digital asset operations', 'Formal ethics policy governing AI use in digital asset contexts', 'd'),
        ('02', 'Fairness testing for AI credit and risk models', 'Regular fairness audits of AI models affecting client outcomes', 'd'),
        ('03', 'Algorithmic accountability framework', 'Framework assigning accountability for AI-generated decisions', 'd'),
        ('04', 'AI environmental impact assessment', 'Assessing carbon and energy footprint of AI compute in DA ops', 'd'),
        ('05', 'Human oversight requirements for high-stakes AI', 'Mandatory human review for AI decisions above risk threshold', 'd'),
        ('06', 'AI third-party ethics risk assessment', 'Assessing ethics risks in third-party AI tools used in DA operations', 'd'),
        ('07', 'AI whistleblower and concern reporting channel', 'Safe channel for reporting AI ethics concerns in DA operations', 'd'),
        ('08', 'Responsible AI regulatory engagement', 'Engaging regulators on responsible AI standards for digital assets', 'd'),
        ('09', 'AI use case ethics review board', 'Internal review board approving new AI use cases for ethical risks', 'd'),
        ('10', 'AI ethics training for digital asset staff', 'Training programme on responsible AI for DA business and tech staff', 'd'),
      ]),
    ]),
  ]),
],

'compliance_regulation': [
  ('07', 'Compliance Analytics & Intelligence', 'Analytics and intelligence capabilities supporting compliance operations', [
    ('01', 'Compliance Analytics Platform', 'Data analytics capabilities for compliance monitoring and reporting', [
      ('01', 'Compliance Data Analytics', 'Analytics tools supporting compliance programme effectiveness', [
        ('01', 'Compliance programme effectiveness dashboard', 'Dashboard measuring KPIs across all compliance programme areas', 'm'),
        ('02', 'AML alert volume and false positive rate analytics', 'Tracking TM alert volumes, disposition rates, and false positive trends', 'm'),
        ('03', 'SAR filing trend analysis', 'Analysing SAR filing trends to identify regulatory patterns', 'm'),
        ('04', 'KYC refresh completion rate monitoring', 'Tracking on-time completion of periodic KYC refresh across client base', 'm'),
        ('05', 'Regulatory examination findings tracker', 'Tracking regulatory examination findings and remediation progress', 'm'),
        ('06', 'Compliance cost per unit analysis', 'Measuring compliance cost per client, transaction, and product line', 'd'),
        ('07', 'Industry typology benchmarking (FATF/Egmont)', 'Benchmarking typology coverage against FATF and Egmont guidance', 'd'),
        ('08', 'Regulatory penalty and enforcement action tracker', 'Monitoring industry enforcement actions for lessons learned', 's'),
        ('09', 'Compliance staff capacity and workload analytics', 'Tracking compliance team capacity, caseloads, and SLA adherence', 's'),
        ('10', 'Compliance programme maturity model assessment', 'Periodic maturity model assessment across compliance programme pillars', 's'),
      ]),
    ]),
  ]),
],

}  # end DOMAINS_EXTRA4

DOMAINS_EXTRA5 = {

'stablecoins': [
  ('07', 'Stablecoin Stress Testing', 'Stress testing and resilience planning for stablecoin operations', [
    ('01', 'Stablecoin Resilience Programme', 'Comprehensive stress testing and resilience for stablecoin issuers', [
      ('01', 'Stablecoin Stress Scenarios', 'Stress scenarios and contingency plans for stablecoin resilience', [
        ('01', 'Mass redemption stress test (50% run scenario)', 'Modelling and testing 50% redemption run within 24 hours', 's'),
        ('02', 'Reserve bank failure contingency plan', 'Plan for managing reserves if primary reserve bank fails', 's'),
        ('03', 'Smart contract exploit response scenario', 'Full response scenario for stablecoin contract exploit', 'm'),
        ('04', 'Regulatory ban scenario contingency plan', 'Planning for regulatory restriction or ban on stablecoin operations', 'd'),
        ('05', 'Market liquidity crisis impact modelling', 'Modelling impact of market-wide liquidity crisis on reserves', 's'),
        ('06', 'Peg attack defence scenario', 'Modelling and defending against coordinated peg attack attempts', 'd'),
        ('07', 'Cross-chain bridge failure contingency', 'Contingency plan for major bridge failure affecting stablecoin supply', 'd'),
        ('08', 'Oracle failure contingency for reserve reporting', 'Backup procedures when reserve reporting oracle fails', 's'),
        ('09', 'Custodian bank operational failure scenario', 'Plan for reserve custodian bank operational outage', 's'),
        ('10', 'Redemption gate and suspension policy', 'Policy governing use of redemption gates under stress conditions', 's'),
        ('11', 'Stablecoin stress test board reporting', 'Board reporting on stablecoin stress test results and actions', 's'),
      ]),
    ]),
  ]),
],

'cbdc': [
  ('08', 'CBDC Accounting & Reporting', 'Accounting treatment and financial reporting for CBDC activities', [
    ('01', 'CBDC Financial Reporting', 'IFRS and regulatory financial reporting for CBDC activities', [
      ('01', 'CBDC Financial Accounting', 'Accounting policies and reporting for CBDC-related activities', [
        ('01', 'CBDC on-balance-sheet vs off-balance-sheet classification', 'Accounting classification of CBDC liabilities on bank balance sheet', 'e'),
        ('02', 'CBDC interest expense accounting treatment', 'Accounting for interest payments on remunerated CBDC holdings', 'e'),
        ('03', 'CBDC distribution fee income recognition', 'Revenue recognition policy for CBDC distribution service fees', 'e'),
        ('04', 'CBDC operational cost allocation', 'Cost allocation methodology for CBDC programme costs', 'e'),
        ('05', 'CBDC exposure disclosure in annual report', 'Disclosing CBDC exposures and activities in annual report', 'e'),
        ('06', 'CBDC capital adequacy impact assessment', 'Assessing capital adequacy impact of CBDC distribution activities', 'e'),
        ('07', 'CBDC deposit substitution accounting', 'Accounting for deposit-to-CBDC substitution in funding model', 'e'),
        ('08', 'CBDC NII impact modelling', 'Modelling net interest income impact of CBDC adoption scenarios', 'e'),
        ('09', 'CBDC tax treatment across jurisdictions', 'Cross-jurisdiction tax analysis for CBDC transactions and income', 'e'),
        ('10', 'CBDC management accounting and segment reporting', 'Segment reporting and management accounts for CBDC activities', 'e'),
        ('11', 'CBDC IFRS 9 classification (amortised cost vs FVTPL)', 'IFRS 9 classification of CBDC assets held by commercial banks', 'e'),
      ]),
    ]),
  ]),
],

'settlement': [
  ('08', 'Settlement Analytics', 'Analytics programme for settlement performance and optimisation', [
    ('01', 'Settlement Performance Analytics', 'Metrics and analytics for settlement operational performance', [
      ('01', 'Settlement Data Analytics', 'Data-driven analytics for settlement optimisation', [
        ('01', 'Settlement rate analytics by asset class', 'Tracking on-time settlement rates by asset class and counterparty', 'm'),
        ('02', 'Settlement velocity trend analysis', 'Analysing settlement speed trends across digital asset types', 'd'),
        ('03', 'Settlement cost attribution by business line', 'Allocating settlement costs to business lines and products', 's'),
        ('04', 'Settlement fail root cause heat map', 'Visualising settlement fail root causes by type and frequency', 's'),
        ('05', 'Settlement counterparty performance scorecard', 'Scoring counterparty settlement performance for relationship management', 's'),
        ('06', 'Settlement SLA breach trend and root cause', 'Analysing trends in settlement SLA breaches for process improvement', 's'),
        ('07', 'Cross-asset settlement efficiency benchmarking', 'Benchmarking settlement efficiency across digital and traditional assets', 'd'),
        ('08', 'Settlement liquidity efficiency ratio', 'Tracking liquidity efficiency in settlement processing operations', 'd'),
        ('09', 'End-to-end settlement cycle time analytics', 'Measuring total end-to-end cycle time from trade to final settlement', 's'),
        ('10', 'Settlement analytics regulatory reporting pack', 'Analytics pack supporting settlement-related regulatory reports', 'd'),
        ('11', 'Settlement operations productivity metrics', 'Tracking per-operator productivity and error rates in settlement ops', 's'),
      ]),
    ]),
  ]),
],

'tokenisation': [
  ('07', 'Tokenisation Business Development', 'Business development and client engagement for tokenisation', [
    ('01', 'Tokenisation Market Development', 'Building institutional markets and client pipelines for tokenisation', [
      ('01', 'Tokenisation Business Development Programme', 'Structured business development for tokenisation services', [
        ('01', 'Tokenisation client pipeline management', 'Managing a structured pipeline of tokenisation mandate opportunities', 'd'),
        ('02', 'Tokenisation thought leadership programme', 'Publishing research and hosting events on tokenisation topics', 'd'),
        ('03', 'Tokenisation proof of concept with anchor clients', 'Running proof of concept tokenisation mandates with anchor clients', 'd'),
        ('04', 'Tokenisation pricing model and fee schedule', 'Developing pricing model and fee schedule for tokenisation services', 'd'),
        ('05', 'Tokenisation RFP and pitch capability', 'Building structured RFP response and pitch capability for tokenisation', 'd'),
        ('06', 'Tokenisation strategic partnership programme', 'Building strategic partnerships with DLT platforms and legal firms', 'd'),
        ('07', 'Multi-asset class tokenisation roadmap', 'Roadmap for expanding tokenisation across new asset classes', 'd'),
        ('08', 'Tokenisation conference and industry presence strategy', 'Strategy for industry conference participation to build market position', 'd'),
        ('09', 'Tokenisation mandate tracking and pipeline reporting', 'Tracking tokenisation mandate pipeline for senior management', 'd'),
        ('10', 'Tokenisation revenue attribution and reporting', 'Attribution and reporting of revenue from tokenisation activities', 'd'),
        ('11', 'Cross-product tokenisation bundling strategy', 'Bundling tokenisation with custody, settlement, and lending products', 'd'),
      ]),
    ]),
  ]),
],

'defi_protocols': [
  ('09', 'DeFi Education & Capability Building', 'Building internal and client DeFi knowledge and capabilities', [
    ('01', 'DeFi Knowledge Programme', 'Internal knowledge building and client education for DeFi', [
      ('01', 'DeFi Capability Building', 'Structured programmes building DeFi expertise', [
        ('01', 'Internal DeFi training and certification programme', 'Structured DeFi training for front office and technology staff', 'd'),
        ('02', 'DeFi glossary and knowledge base for clients', 'Client-facing DeFi knowledge base and educational resources', 'd'),
        ('03', 'DeFi simulation and test environment', 'Internal simulation environment for staff DeFi training', 'd'),
        ('04', 'DeFi protocol demo days and technical briefings', 'Regular briefings from DeFi protocol teams for institutional staff', 'd'),
        ('05', 'DeFi client education webinar programme', 'Regular DeFi client education webinars covering key topics', 'd'),
        ('06', 'DeFi risk education for senior management', 'DeFi risk briefings for senior management and risk committees', 'd'),
        ('07', 'DeFi regulatory engagement training for legal teams', 'Training for legal teams on DeFi regulatory landscape', 'd'),
        ('08', 'DeFi research partnership with universities', 'Research partnerships with academic institutions on DeFi topics', 'd'),
        ('09', 'DeFi case study library of institutional transactions', 'Library of anonymised DeFi transaction case studies for training', 'd'),
        ('10', 'DeFi operational runbook for new staff', 'Operational runbook enabling new staff to safely execute DeFi activities', 'd'),
        ('11', 'DeFi community participation (ETHGlobal, hackathons)', 'Staff participation in DeFi community events and hackathons', 'd'),
      ]),
    ]),
  ]),
],

'security': [
  ('10', 'Security Innovation & Research', 'Security research and innovation for digital asset operations', [
    ('01', 'Security Research Programme', 'Internal security research for emerging digital asset threats', [
      ('01', 'Security Research & Innovation', 'Research activities addressing emerging digital asset security risks', [
        ('01', 'Quantum computing threat assessment for custody', 'Assessing quantum computing threat timeline for ECDSA-protected custody', 'd'),
        ('02', 'Post-quantum cryptography migration planning', 'Planning migration to NIST-approved post-quantum algorithms for custody', 'd'),
        ('03', 'AI-generated phishing threat assessment', 'Assessing threat from AI-generated spear phishing against custody staff', 'd'),
        ('04', 'Zero-day exploit monitoring for blockchain clients', 'Monitoring zero-day exploits affecting blockchain client software', 'm'),
        ('05', 'Blockchain protocol vulnerability research programme', 'Internal research on consensus and protocol-level vulnerabilities', 'd'),
        ('06', 'Deepfake threat assessment for voice authorisation', 'Assessing deepfake audio risk in voice-based authorisation systems', 'd'),
        ('07', 'DeFi flash loan attack modelling for held positions', 'Modelling flash loan attack vectors affecting institutional DeFi positions', 'd'),
        ('08', 'Hardware supply chain integrity programme', 'Ensuring integrity of hardware supply chain for custody devices', 'd'),
        ('09', 'Insider threat programme for digital asset ops', 'Behavioural analytics and controls targeting insider threat risks', 'm'),
        ('10', 'Security research publications and conference talks', 'Publishing security research and presenting at industry conferences', 'd'),
        ('11', 'External security research partnership programme', 'Partnering with external security research teams and labs', 'd'),
      ]),
    ]),
  ]),
],

'ai_agentic': [
  ('09', 'AI Partnerships & Ecosystem', 'AI technology partnerships supporting digital asset AI capabilities', [
    ('01', 'AI Technology Partnerships', 'Strategic AI technology partnerships for digital asset applications', [
      ('01', 'AI Vendor & Ecosystem Management', 'Managing AI vendor relationships and ecosystem participation', [
        ('01', 'LLM provider evaluation and selection framework', 'Structured framework for evaluating and selecting LLM providers', 'd'),
        ('02', 'AI model API vendor management programme', 'Managing SLAs and commercial terms with AI model API vendors', 'd'),
        ('03', 'AI ethics partnership with third-party auditors', 'Engaging third-party ethics auditors for AI model reviews', 'd'),
        ('04', 'Open source AI model contribution programme', 'Contributing to and maintaining open source AI models for DA', 'd'),
        ('05', 'Fintech AI partnership for compliance innovation', 'Strategic partnerships with AI-focused compliance fintech firms', 'd'),
        ('06', 'Academic AI research collaboration programme', 'Research collaborations with universities on AI for digital assets', 'd'),
        ('07', 'AI regulatory sandboxes (FCA, MAS) participation', 'Participating in regulatory AI sandboxes for digital asset applications', 'd'),
        ('08', 'AI consortium participation (FS AI, FINOS)', 'Participating in financial services AI industry consortia', 'd'),
        ('09', 'AI talent acquisition and retention programme', 'Attracting and retaining AI/ML talent for digital asset operations', 'd'),
        ('10', 'AI innovation lab with digital asset focus', 'Internal AI innovation lab piloting AI use cases for digital assets', 'd'),
        ('11', 'AI patent strategy for digital asset innovations', 'Strategic patenting of proprietary AI methods for digital assets', 'd'),
      ]),
    ]),
  ]),
],

'compliance_regulation': [
  ('08', 'Compliance Operations Excellence', 'Operational excellence programme for compliance functions', [
    ('01', 'Compliance Operating Model', 'Designing and optimising the compliance operating model', [
      ('01', 'Compliance Function Design', 'Structuring and optimising the compliance function for digital assets', [
        ('01', 'First, second, and third line model for digital assets', 'Implementing three-line-of-defence model for digital asset compliance', 'm'),
        ('02', 'Compliance technology investment roadmap', 'Multi-year technology investment plan for compliance tooling', 's'),
        ('03', 'Compliance headcount model and capacity planning', 'Modelling compliance headcount requirements as volumes scale', 's'),
        ('04', 'Compliance outsourcing and managed service strategy', 'Strategy for outsourcing specific compliance functions to managed services', 'd'),
        ('05', 'Compliance training and certification programme', 'Mandatory compliance training including digital asset-specific modules', 'm'),
        ('06', 'Compliance onboarding for new digital asset products', 'Compliance sign-off process for launching new digital asset products', 'm'),
        ('07', 'Ethics hotline and speak-up culture for compliance', 'Confidential reporting channel for compliance concerns', 'm'),
        ('08', 'Compliance performance management framework', 'KPIs and performance management for compliance team members', 's'),
        ('09', 'External compliance peer benchmarking', 'Benchmarking compliance programme against peer institutions', 'd'),
        ('10', 'Compliance function board reporting framework', 'Regular board reporting on compliance programme status and risks', 'm'),
        ('11', 'Compliance innovation and automation roadmap', 'Roadmap for automating and innovating compliance processes via RegTech', 'd'),
      ]),
    ]),
  ]),
],

}  # end DOMAINS_EXTRA5

DOMAINS_EXTRA6 = {

'defi_protocols': [
  ('10', 'DeFi Cross-Protocol Strategy', 'Strategic management of cross-protocol DeFi exposure', [
    ('01', 'Cross-Protocol Portfolio Management', 'Managing DeFi positions across multiple protocols strategically', [
      ('01', 'Cross-Protocol Optimisation', 'Optimising DeFi strategy across competing protocols', [
        ('01', 'Cross-protocol yield optimisation algorithm', 'Automated yield optimisation across multiple DeFi protocols', 'd'),
        ('02', 'Protocol migration strategy and execution', 'Systematic migration of positions between DeFi protocols', 'd'),
        ('03', 'DeFi portfolio correlation analysis', 'Analysing correlation between DeFi protocol exposures', 'd'),
        ('04', 'DeFi protocol sunset monitoring', 'Monitoring for protocol deprecation signals and exit strategies', 'd'),
        ('05', 'Multi-protocol governance voting strategy', 'Coordinated governance voting strategy across DeFi protocol holdings', 'd'),
        ('06', 'DeFi protocol insurance portfolio management', 'Managing insurance coverage portfolio across DeFi protocol positions', 'd'),
        ('07', 'DeFi token economic model due diligence', 'Assessing token economic sustainability of DeFi protocols held', 'd'),
        ('08', 'DeFi cross-chain liquidity optimisation', 'Optimising liquidity deployment across chains for maximum yield', 'd'),
      ]),
    ]),
  ]),
],

'security': [
  ('11', 'Custody Platform Security Testing', 'Continuous security testing programme for custody platform', [
    ('01', 'Continuous Security Validation', 'Ongoing validation of security controls for custody systems', [
      ('01', 'Continuous Security Testing', 'Automated and scheduled security testing of custody infrastructure', [
        ('01', 'Automated API security testing for custody APIs', 'Scheduled automated security testing of custody REST APIs', 'm'),
        ('02', 'Infrastructure-as-code security scanning', 'Security scanning of IaC templates for custody infrastructure', 's'),
        ('03', 'Container image vulnerability scanning', 'Continuous scanning of container images used in custody systems', 's'),
        ('04', 'Secrets management and rotation audit', 'Auditing secrets management and rotation compliance', 'm'),
        ('05', 'Security drift detection for custody systems', 'Detecting configuration drift from security baselines', 'm'),
        ('06', 'Continuous compliance monitoring (SOC 2, ISO 27001)', 'Automated compliance posture monitoring against SOC 2 and ISO 27001', 's'),
        ('07', 'Cloud security posture management (CSPM)', 'Cloud security posture management for custody cloud workloads', 's'),
      ]),
    ]),
  ]),
],

'ai_agentic': [
  ('10', 'AI Integration Architecture', 'Architecture for integrating AI into digital asset systems', [
    ('01', 'AI System Integration', 'Technical architecture for AI integration in DA operations', [
      ('01', 'AI Architecture Standards', 'Standards and patterns for AI system integration', [
        ('01', 'AI API gateway for digital asset systems', 'Central AI API gateway managing requests to AI services', 'd'),
        ('02', 'Event-driven AI processing for DA transactions', 'Event-driven architecture triggering AI processing on DA events', 'd'),
        ('03', 'AI output caching and latency optimisation', 'Caching AI outputs and optimising latency for real-time applications', 'd'),
        ('04', 'AI fallback and degraded mode operation', 'Graceful degradation when AI services are unavailable', 'd'),
        ('05', 'AI integration testing framework', 'Automated testing framework for AI-integrated digital asset systems', 'd'),
        ('06', 'Multi-model AI routing (cost vs quality)', 'Dynamic routing of requests across AI models balancing cost and quality', 'd'),
        ('07', 'AI system observability and tracing', 'Full observability stack for AI system calls in DA operations', 'd'),
        ('08', 'AI token usage budget management', 'Monitoring and controlling AI API token spend across teams', 'd'),
      ]),
    ]),
  ]),
],

}  # end DOMAINS_EXTRA6

# ---------------------------------------------------------------------------
# Markets and regulatory frameworks
# ---------------------------------------------------------------------------

MARKETS = [
  ('us', 'United States', 'Americas'),
  ('uk', 'United Kingdom', 'Europe'),
  ('eu', 'European Union', 'Europe'),
  ('ch', 'Switzerland', 'Europe'),
  ('sg', 'Singapore', 'Asia-Pacific'),
  ('hk', 'Hong Kong', 'Asia-Pacific'),
  ('uae', 'United Arab Emirates', 'Middle East'),
  ('jp', 'Japan', 'Asia-Pacific'),
  ('ca', 'Canada', 'Americas'),
  ('au', 'Australia', 'Asia-Pacific'),
]

REG_FRAMEWORKS = [
  ('mica', 'Markets in Crypto-Assets Regulation', 'MiCA', 'EU comprehensive crypto regulation', 'in_force', '2024-12-30', 'EBA/ESMA/EC', 'eu', 'eu'),
  ('mas_psa', 'Payment Services Act (Digital Payment Token Services)', 'MAS PSA', 'Singapore DPT service regulation', 'in_force', '2020-01-28', 'MAS', 'sg', 'sg'),
  ('hkma_vasp', 'VASP Licensing Regime', 'HKMA VASP', 'Hong Kong mandatory VASP licensing', 'in_force', '2023-06-01', 'SFC/HKMA', 'hk', 'hk'),
  ('finma_va', 'FINMA Virtual Assets Guidelines', 'FINMA VA', 'Swiss FINMA guidance on virtual assets', 'in_force', '2019-09-16', 'FINMA', 'ch', 'ch'),
  ('fca_mlr', 'Money Laundering Regulations (Cryptoasset Business)', 'FCA MLR', 'UK FCA cryptoasset AML registration', 'in_force', '2020-01-10', 'FCA', 'uk', 'uk'),
  ('fatf_travel', 'FATF Recommendation 16 (Travel Rule)', 'Travel Rule', 'FATF Travel Rule for VASP transfers', 'in_force', '2019-06-21', 'FATF', 'global', None),
  ('ofac', 'OFAC Sanctions Programme (Crypto)', 'OFAC', 'US Treasury OFAC sanctions for crypto', 'in_force', '2021-10-15', 'OFAC/FinCEN', 'us', 'us'),
  ('sec_crypto', 'SEC Digital Asset Regulatory Framework', 'SEC', 'US SEC regulation of digital asset securities', 'developing', '2023-01-01', 'SEC', 'us', 'us'),
  ('vara', 'Virtual Assets Regulatory Authority Framework', 'VARA', 'Dubai VARA comprehensive VA regulation', 'in_force', '2023-02-07', 'VARA', 'uae', 'uae'),
  ('dora', 'Digital Operational Resilience Act', 'DORA', 'EU digital operational resilience for financial sector', 'in_force', '2025-01-17', 'EC/ESAs', 'eu', 'eu'),
  ('basel_crypto', 'Basel III Cryptoasset Prudential Standard', 'Basel III Crypto', 'BCBS prudential standard for bank crypto exposures', 'in_force', '2025-01-01', 'BCBS', 'global', None),
  ('jfsa', 'JFSA Crypto Asset Exchange Service Regulation', 'JFSA CAES', 'Japan FSA registration for crypto asset exchange', 'in_force', '2020-05-01', 'JFSA', 'jp', 'jp'),
]

DOMAIN_REG_MAP = {
  'custody': ['mica', 'mas_psa', 'hkma_vasp', 'finma_va', 'fca_mlr', 'basel_crypto', 'dora'],
  'wallets': ['mica', 'fatf_travel', 'ofac', 'fca_mlr'],
  'stablecoins': ['mica', 'mas_psa', 'ofac', 'fatf_travel', 'fca_mlr'],
  'cbdc': ['mica', 'dora', 'basel_crypto'],
  'settlement': ['mica', 'dora', 'basel_crypto', 'finma_va'],
  'tokenisation': ['mica', 'sec_crypto', 'mas_psa', 'fca_mlr', 'finma_va'],
  'defi_protocols': ['mica', 'ofac', 'fatf_travel', 'sec_crypto'],
  'security': ['dora', 'mica', 'fca_mlr'],
  'ai_agentic': ['dora', 'mica'],
  'compliance_regulation': ['fatf_travel', 'ofac', 'mica', 'mas_psa', 'hkma_vasp', 'finma_va', 'fca_mlr', 'vara', 'jfsa', 'sec_crypto'],
}

DOMAIN_MARKET_MAP = {
  'custody': ['us', 'uk', 'eu', 'ch', 'sg', 'hk'],
  'wallets': ['us', 'uk', 'eu', 'sg', 'hk'],
  'stablecoins': ['us', 'uk', 'eu', 'sg'],
  'cbdc': ['uk', 'eu', 'sg', 'hk', 'jp'],
  'settlement': ['uk', 'eu', 'us', 'sg', 'hk', 'jp'],
  'tokenisation': ['uk', 'eu', 'us', 'sg', 'hk', 'ch'],
  'defi_protocols': ['us', 'eu', 'sg'],
  'security': ['us', 'uk', 'eu', 'sg'],
  'ai_agentic': ['us', 'uk', 'eu'],
  'compliance_regulation': ['us', 'uk', 'eu', 'ch', 'sg', 'hk', 'uae', 'jp', 'ca', 'au'],
}

# ---------------------------------------------------------------------------
# Seed
# ---------------------------------------------------------------------------

def seed(conn):
    c = conn.cursor()
    for tbl in ['capability_regulations', 'capability_markets', 'capability_tags',
                 'periodic_positions', 'capabilities_l3', 'capabilities_l2',
                 'capabilities_l1', 'capabilities_l0', 'regulatory_frameworks', 'markets']:
        c.execute(f'DELETE FROM {tbl}')

    for mid, name, region in MARKETS:
        c.execute('INSERT INTO markets (id, name, region) VALUES (?, ?, ?)', (mid, name, region))

    for row in REG_FRAMEWORKS:
        c.execute('''INSERT INTO regulatory_frameworks
                     (id, name, short_name, description, status, effective_date, regulator, jurisdiction, jurisdiction_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Merge extra data
    merged = {k: list(v) for k, v in DOMAINS.items()}
    for domain_id, extra_l0s in DOMAINS_EXTRA.items():
        merged.setdefault(domain_id, []).extend(extra_l0s)
    for domain_id, extra_l0s in DOMAINS_EXTRA2.items():
        merged.setdefault(domain_id, []).extend(extra_l0s)
    for domain_id, extra_l0s in DOMAINS_EXTRA3.items():
        merged.setdefault(domain_id, []).extend(extra_l0s)
    for domain_id, extra_l0s in DOMAINS_EXTRA4.items():
        merged.setdefault(domain_id, []).extend(extra_l0s)
    for domain_id, extra_l0s in DOMAINS_EXTRA5.items():
        merged.setdefault(domain_id, []).extend(extra_l0s)
    for domain_id, extra_l0s in DOMAINS_EXTRA6.items():
        merged.setdefault(domain_id, []).extend(extra_l0s)

    l3_ids_by_domain = {}

    for domain_id, l0s in merged.items():
        l3_ids_by_domain[domain_id] = []
        for l0_i, (l0_sfx, l0_name, l0_desc, l1s) in enumerate(l0s, 1):
            l0_id = f'{domain_id[:4]}-l0-{l0_sfx}'
            c.execute('INSERT INTO capabilities_l0 (id, domain_id, name, description, sort_order) VALUES (?,?,?,?,?)',
                      (l0_id, domain_id, l0_name, l0_desc, l0_i))

            for l1_i, (l1_sfx, l1_name, l1_desc, l2s) in enumerate(l1s, 1):
                l1_id = f'{domain_id[:4]}-l1-{l0_sfx}{l1_sfx}'
                c.execute('INSERT INTO capabilities_l1 (id, l0_id, domain_id, name, description, sort_order) VALUES (?,?,?,?,?,?)',
                          (l1_id, l0_id, domain_id, l1_name, l1_desc, l1_i))

                for l2_i, (l2_sfx, l2_name, l2_desc, l3s) in enumerate(l2s, 1):
                    l2_id = f'{domain_id[:4]}-l2-{l0_sfx}{l1_sfx}{l2_sfx}'
                    c.execute('INSERT INTO capabilities_l2 (id, l1_id, l0_id, domain_id, name, description, sort_order) VALUES (?,?,?,?,?,?,?)',
                              (l2_id, l1_id, l0_id, domain_id, l2_name, l2_desc, l2_i))

                    for l3_i, (l3_sfx, l3_name, l3_desc, mat_key) in enumerate(l3s, 1):
                        l3_id = f'{domain_id[:4]}-l3-{l0_sfx}{l1_sfx}{l2_sfx}{l3_sfx}'
                        maturity = M.get(mat_key, 'developing')
                        c.execute('''INSERT INTO capabilities_l3
                                     (id, l2_id, l1_id, l0_id, domain_id, name, description, maturity, sort_order)
                                     VALUES (?,?,?,?,?,?,?,?,?)''',
                                  (l3_id, l2_id, l1_id, l0_id, domain_id, l3_name, l3_desc, maturity, l3_i))
                        l3_ids_by_domain[domain_id].append(l3_id)

    for domain_id, l3_ids in l3_ids_by_domain.items():
        for l3_id in l3_ids:
            for mid in DOMAIN_MARKET_MAP.get(domain_id, []):
                c.execute('INSERT OR IGNORE INTO capability_markets VALUES (?,?)', (l3_id, mid))
            for fid in DOMAIN_REG_MAP.get(domain_id, []):
                c.execute('INSERT OR IGNORE INTO capability_regulations VALUES (?,?)', (l3_id, fid))

    conn.commit()


def report(conn):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM capabilities_l3')
    total = c.fetchone()[0]
    print(f'\nTotal L3 features: {total}')
    c.execute('''SELECT d.name, COUNT(l3.id) as cnt FROM domains d
                 LEFT JOIN capabilities_l0 l0 ON l0.domain_id=d.id
                 LEFT JOIN capabilities_l1 l1 ON l1.l0_id=l0.id
                 LEFT JOIN capabilities_l2 l2 ON l2.l1_id=l1.id
                 LEFT JOIN capabilities_l3 l3 ON l3.l2_id=l2.id
                 GROUP BY d.id ORDER BY d.sort_order''')
    for name, cnt in c.fetchall():
        print(f'  {name}: {cnt}')
    for tbl in ['markets', 'regulatory_frameworks', 'capability_markets', 'capability_regulations']:
        c.execute(f'SELECT COUNT(*) FROM {tbl}')
        print(f'{tbl}: {c.fetchone()[0]}')


if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    print('Seeding...')
    seed(conn)
    report(conn)
    conn.close()
    print('Done.')
