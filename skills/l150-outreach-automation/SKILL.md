---
name: l150-outreach-automation
description: Automated outbound outreach system for L-150 RWA project targeting Web3/AI treasuries. Use when executing machine-readable outreach campaigns, JSON proposal delivery, and AI treasury agent engagement. Supports GitHub SEO bait deployment, on-chain fingerprint creation, and 24/7 physical verification streaming.
---

# L-150 Outreach Automation Skill

## Purpose
Transform L-150 RWA project into machine-discoverable, AI-agent-readable investment opportunities. Automate outbound targeting of Web3/AI treasuries with structured data packets.

## When to Use This Skill

Use this skill when:
1. Deploying GitHub SEO bait repositories for AI agent discovery
2. Creating JSON-LD structured proposals for treasury agents
3. Setting up on-chain test contracts for verification
4. Executing automated outreach to target treasuries
5. Configuring 24/7 physical verification streams

## Core Workflows

### Workflow 1: GitHub SEO Bait Deployment

**Purpose:** Make L-150 discoverable when AI agents search for RWA security protocols

**Steps:**
1. Create `RWA-Node-Security-Protocol` repository
2. Deploy smart contract templates (DividendPriorityLock, TreasuryControlledAccount)
3. SEO optimize README with keywords: "RWA security", "automated dividend", "physical asset tokenization"
4. Link to L-150 as case study example

**Reference:** `references/github-deployment-guide.md`

### Workflow 2: JSON Proposal Generation

**Purpose:** Create machine-readable investment proposals

**Template Location:** `assets/l150-proposal-schema.json`

**Usage:**
```bash
# Generate customized JSON proposal for specific target
python scripts/generate_proposal.py --target HDAO --output proposal.json
```

**Key Fields:**
- `asset.cashflow_monthly_usd`
- `investment.annual_yield`
- `risk_mitigation.physical_collateral`
- `treasury_signals.ai_governance_compatible`

### Workflow 3: On-Chain Contract Deployment

**Purpose:** Create verifiable on-chain fingerprints

**Contracts:**
- `DividendPriorityLock.sol` - Simulates revenue distribution logic
- `TreasuryControlledAccount.sol` - Multi-sig fund control
- `WhaleOverlayTrigger.sol` - Large investor priority mechanism

**Deployment:**
```bash
# Deploy to Polygon Mumbai testnet
npx hardhat run scripts/deploy-test-contracts.js --network mumbai
```

### Workflow 4: Target Treasury Outreach

**Purpose:** Automated delivery of JSON proposals to AI treasuries

**Target Database:** `references/treasury-targets-v2.json`

**Execution:**
```bash
# Send to all P0 targets
python scripts/outreach_bot.py --tier P0 --format json-ld
```

**Email Format:**
- Subject: `[RWA-DATA-PACKET] L-150: {asset_summary}`
- Body: JSON-LD schema (not text)
- Attachment: `l150-full-schema.json`

### Workflow 5: 24/7 Physical Verification

**Purpose:** Real-time, tamper-proof proof of physical operations

**Components:**
- IP Camera → IPFS → Daily hash on-chain
- People counter → Oracle → Hourly on-chain
- POS data → Encrypted API → Daily hash

**Setup:**
```bash
# Configure streaming pipeline
python scripts/setup_verification_stream.py --location changsha
```

## Reference Files

### `references/treasury-targets-v2.json`
Structured database of target treasuries with:
- TVL, investment thesis, decision makers
- Contact vectors (forum, Discord, direct)
- L-150 alignment scores
- Priority rankings (P0/P1/P2)

### `references/outreach-templates/`
- `hdao-ai-governance.json` - AI laboratory angle
- `ainn-bitcoin-l2.json` - Bitcoin RWA anchor angle
- `makerdao-rwa.json` - Traditional RWA collateral angle
- `aave-gho.json` - Stablecoin backing angle

### `assets/`
- `l150-proposal-schema.json` - Base schema template
- `verification-stream-config.yaml` - Camera/POS setup
- `contract-abis/` - Compiled contract ABIs

## Security Rules

**CRITICAL:** Never execute actual outreach without explicit user authorization

**Pre-flight Checklist:**
- [ ] Target list reviewed and approved
- [ ] Message content reviewed and approved
- [ ] Test deployment completed (testnet only)
- [ ] Fallback/retraction plan in place

**Banned Actions:**
- No mainnet deployments without audit
- No mass emails without rate limiting
- No false claims in proposals
- No private key exposure in scripts

## Example Usage

**User Request:** "Deploy GitHub bait for HDAO discovery"

**Skill Execution:**
1. Read `references/github-deployment-guide.md`
2. Clone template repo structure
3. Customize with L-150 case study
4. Deploy to GitHub
5. Verify SEO keywords indexed
6. Report deployment status

**User Request:** "Generate JSON proposal for Aave Treasury"

**Skill Execution:**
1. Load `assets/l150-proposal-schema.json`
2. Read `references/outreach-templates/aave-gho.json`
3. Customize yield/collateral parameters
4. Output machine-readable JSON
5. Validate schema compliance

---

**Status:** Ready for deployment upon explicit authorization
**Last Updated:** 2026-02-11
**Version:** 1.0
