---
name: web3-rwa-outreach
description: Web3/AI treasury outreach and RWA tokenization proposal generation. Use when crafting investment proposals for DAO treasuries, AI labs, and Web3 funds seeking real-world asset exposure. Supports target research, pitch deck structuring, and cold outreach optimization for physical asset tokenization deals.
---

# Web3 RWA Outreach Skill

## Purpose
Transform physical asset deals (real estate, cash-flowing businesses) into investment proposals targeting Web3/AI treasuries and DAOs.

## Core Workflow

### 1. Asset Analysis
Required inputs:
- Asset location & size
- Monthly revenue (verified)
- Founder capital committed
- Financing need
- Unique moat/scarcity factor

### 2. Target Mapping
Match asset profile to treasury types:
- **AI-Agent DAOs** (HDAO, etc.) → Need physical validation for governance experiments
- **Creative AI Treasuries** (Zerebro) → Need physical manifestation of AI art
- **Infrastructure Foundations** (Fetch.ai) → Need real-world deployment cases
- **Decentralized AI Networks** (Bittensor) → Need ground-truth datasets
- **Bitcoin L2 Treasuries** (AINN) → Need RWA yield on BTC infrastructure

### 3. Proposal Architecture
Every proposal must include:
1. **Hook** — Why this matters to THEM specifically
2. **Asset Lock** — Hard numbers, location, revenue
3. **Security Protocol** — Fund controls, escrow, priority rights
4. **Skin in Game** — Founder's personal capital commitment
5. **Vision** — What this unlocks for both parties
6. **CTA** — Clear next step

### 4. Voice Guidelines
- Confident but not arrogant
- Specific (names, numbers, locations)
- Security-first (acknowledge treasury risk aversion)
- Asymmetric opportunity framing
- No hype words without backing data

## Reference Files

### Target Database
See `references/treasury-targets.md` for active Web3/AI treasury profiles including:
- AUM/TVL estimates
- Investment thesis alignment
- Contact protocols
- Response time history

### Proposal Templates
See `references/proposal-templates.md` for sector-specific templates:
- AI-Agent DAO pitch
- Creative AI treasury pitch
- Infrastructure foundation pitch
- Decentralized AI network pitch
- Bitcoin L2 RWA pitch

## Example Usage

**User:** "I have a cash-flowing venue in [City]. Need to pitch [Specific DAO]."

**Process:**
1. Load target profile from `references/treasury-targets.md`
2. Select matching template from `references/proposal-templates.md`
3. Customize with user's asset specifics
4. Output ready-to-send proposal
5. Archive in `outreach/` folder with timestamp

## Security Rules
- NEVER send proposals without explicit user authorization
- Archive all drafts locally before any external action
- Flag any target requesting unusual pre-payments or sensitive keys
- Maintain target confidentiality (no public sharing of target lists)
