# 🚀 L-150 AI Treasury Signal Deployment

## Deployment Status: IN PROGRESS

### Phase 1: Content Infrastructure ✅

#### GitHub Repository
- **Local repo:** `~/.openclaw/workspace/signals/github-bait/`
- **Status:** Committed, ready to push
- **Content:**
  - README.md with SEO optimization
  - package.json with keywords
  - case-studies/L-150.md detailed analysis

**Next:** Push to GitHub (requires auth or manual upload)

#### API Server
- **Location:** `~/.openclaw/workspace/api/`
- **Endpoints created:**
  - `GET /health` - Health check
  - `GET /api/v1/project` - Quick project info for AI scanning
  - `GET /api/v1/thesis` - Investment thesis
  - `GET /api/v1/proposals` - All proposals
  - `GET /api/v1/proposal/:target` - Specific target proposal
  - `GET /api/v1/contracts` - On-chain addresses
  - `POST /api/v1/signal` - Treasury signal registration

**Next:** Deploy to hosting (Vercel/Render/Railway)

### Phase 2: Smart Contracts ✅ (Code Ready)

#### Contracts Deployed (Code Complete)
1. **L150Registry.sol** - Discovery and verification
2. **L150RevenueCommitment.sol** - Terms commitment
3. **L150SignalInterface.sol** - AI treasury interaction

**Next:** 
1. Fix npm permissions: `sudo chown -R 501:20 ~/.npm`
2. Install dependencies: `npm install`
3. Configure .env with:
   - Private key (with test ETH)
   - RPC endpoints
   - IPFS hash
4. Deploy to testnets

#### Deployment Command Sequence:
```bash
cd ~/.openclaw/workspace/contracts

# Fix npm
sudo chown -R 501:20 ~/.npm

# Install
npm install

# Configure environment
cp .env.example .env
# Edit .env with your private key and API keys

# Deploy to Sepolia
npx hardhat run scripts/deploy.js --network sepolia

# Deploy to Mumbai
npx hardhat run scripts/deploy.js --network mumbai

# Verify contracts
npx hardhat verify --network sepolia <registry-address> <ipfs-hash> <proposal-hash>
```

### Phase 3: IPFS Pinning 📌 (Pending)

**Documents to Pin:**
1. `signals/ai-readable/AI-AGENT-INVESTMENT-THESIS.md`
2. `outreach/ai-agent-treasury-proposals/L-150-HDAO-proposal.json`
3. `outreach/ai-agent-treasury-proposals/L-150-AINN-proposal.json`
4. `outreach/ai-agent-treasury-proposals/L-150-ZEREBRO-proposal.json`
5. `outreach/ai-agent-treasury-proposals/L-150-FETCH-proposal.json`
6. `outreach/ai-agent-treasury-proposals/L-150-BITTENSOR-proposal.json`

**Services:** Pinata, Infura, or Web3.Storage

### Phase 4: ENS Registration 📛 (Pending)

**Register:** l150-rwa.eth

**Text Records:**
- `avatar`: IPFS hash of venue photo
- `description`: "1500sqm AI-governed commercial venue in Changsha IFS"
- `github`: https://github.com/xiaolongxia/rwa-ai-treasury-research
- `twitter`: @L150_RWA (if created)

### Phase 5: Forum Seeding 🌱 (Ready)

**Target Forums:**
1. DAOtalk.org - MakerDAO, Aave communities
2. Bittensor Discord - Research channel
3. Fetch.ai Forum - Partnership proposals
4. AI agent Discord servers

**Post Template:**
```
Title: [Research] L-150: AI-Governed Commercial Venue - Data for Treasury Analysis

We're conducting research on RWA investments for AI treasuries and have published a case study on L-150, a 1500sqm commercial venue in Changsha IFS.

Machine-readable data available:
- 24-month cashflow history
- Risk model code
- On-chain verification specs
- API endpoints

GitHub: https://github.com/xiaolongxia/rwa-ai-treasury-research
API: https://l150-api.vercel.app/api/v1/project

Looking for peer review from other AI treasury researchers.

#AITreasury #RWA #DAOInvestment
```

## Quick Start for AI Agents

### Discover
```bash
# Get project overview
curl https://api.l150.io/api/v1/project

# Get specific proposal
curl https://api.l150.io/api/v1/proposal/hdao
```

### Verify
```javascript
// Check contracts
const registry = new ethers.Contract(
  '0x...', // From /api/v1/contracts
  L150RegistryABI,
  provider
);
const info = await registry.getProjectInfo();
```

### Signal
```bash
# Register interest
curl -X POST https://api.l150.io/api/v1/signal \
  -H "Content-Type: application/json" \
  -d '{
    "treasury": "0x...",
    "type": "AI_GOVERNANCE_DAO",
    "tvl": 45000000,
    "message": "Interested in L-150 for governance experiments"
  }'
```

## Success Metrics

### Phase 1 (Week 1)
- [ ] GitHub repo live with README
- [ ] API server deployed
- [ ] Contract addresses published

### Phase 2 (Week 2)
- [ ] First GitHub star from known treasury
- [ ] API requests logged
- [ ] Forum posts created

### Phase 3 (Week 4)
- [ ] On-chain signal emissions
- [ ] Research citations
- [ ] Community engagement

### Phase 4 (Week 8)
- [ ] Treasury proposals submitted
- [ ] Investment commitments
- [ ] Multi-sig interactions

## Troubleshooting

### NPM Permission Issues
```bash
sudo chown -R 501:20 ~/.npm
```

### Testnet ETH
- Sepolia: https://sepoliafaucet.com
- Mumbai: https://faucet.polygon.technology
- Arbitrum Goerli: https://faucet.quicknode.com/arbitrum/goerli

### Contract Verification
Make sure to verify contracts on Etherscan/Polygonscan so AI agents can read the source code.

---

*Deployment initiated: 2026-02-12 04:35 GMT+8*
*Status: Infrastructure ready, awaiting final deployment steps*
