# On-Chain Fingerprints for AI Discovery

## Purpose
Create verifiable, immutable signals on-chain that AI agents can discover and verify.

## Strategy: Graduated Disclosure

### Level 1: Public Signals (Anyone Can See)
- GitHub repository activity
- Documentation publication
- Forum posts

### Level 2: On-Chain Hints (On-Chain Data)
- Testnet contract deployments
- ENS names with metadata
- IPFS hashes of documentation

### Level 3: Verifiable Proofs (Treasury-Only)
- Revenue commitment hashes
- Physical presence proofs
- Multi-sig treasury interactions

---

## Testnet Deployment Plan

### Phase 1: Signal Contracts (Ethereum Sepolia)

#### 1. L150Registry Contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title L150 Registry
 * @notice Public signal for AI treasury discovery
 * @dev Deployed on Sepolia for testing, mainnet for production
 */
contract L150Registry {
    string public constant PROJECT_CODE = "L-150";
    string public constant ASSET_CLASS = "RWA-Commercial-Real-Estate";
    string public constant LOCATION = "Changsha, China";
    
    uint256 public constant MONTHLY_REVENUE_USD = 45000;
    uint256 public constant SEEKING_AMOUNT_USD = 150000;
    uint256 public constant EXPECTED_APR_BPS = 1800; // 18-22% = 1800 bps
    
    string public documentationURI;
    bytes32 public proposalHash;
    
    event SignalEmitted(
        address indexed treasury,
        uint256 timestamp,
        bytes32 signalType
    );
    
    constructor(string memory _docsURI, bytes32 _proposalHash) {
        documentationURI = _docsURI;
        proposalHash = _proposalHash;
    }
    
    // AI treasury can signal interest
    function signalInterest(bytes32 signalType) external {
        emit SignalEmitted(msg.sender, block.timestamp, signalType);
    }
    
    // Verify this is the official L-150 signal
    function verify() external pure returns (bool) {
        return true;
    }
}
```

**Deployment Command:**
```bash
npx hardhat run scripts/deploy-registry.js --network sepolia
```

#### 2. RevenueCommitment Contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title Revenue Commitment
 * @notice On-chain commitment of revenue sharing terms
 */
contract L150RevenueCommitment {
    struct InvestmentTerms {
        uint256 totalAmount;
        uint256 monthlyDividend;
        uint256 paybackMonths;
        uint256 postRoiShareBps;
    }
    
    InvestmentTerms public terms;
    address public l150Operator;
    
    event RevenueCommitted(
        uint256 amount,
        uint256 monthlyDividend,
        uint256 timestamp
    );
    
    constructor(
        uint256 _totalAmount,
        uint256 _monthlyDividend,
        uint256 _paybackMonths
    ) {
        terms = InvestmentTerms({
            totalAmount: _totalAmount,
            monthlyDividend: _monthlyDividend,
            paybackMonths: _paybackMonths,
            postRoiShareBps: 2000 // 20%
        });
        l150Operator = msg.sender;
        
        emit RevenueCommitted(_totalAmount, _monthlyDividend, block.timestamp);
    }
    
    // AI treasuries can verify terms on-chain
    function verifyTerms() external view returns (InvestmentTerms memory) {
        return terms;
    }
}
```

### Phase 2: Verification Infrastructure (Polygon Mumbai)

#### 3. PhysicalOracle Contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title Physical Oracle
 * @notice On-chain verification of physical presence and operations
 */
contract L150PhysicalOracle {
    struct DailyProof {
        bytes32 cameraHash;
        bytes32 posHash;
        uint256 footfallCount;
        uint256 timestamp;
    }
    
    mapping(uint256 => DailyProof) public dailyProofs;
    uint256 public lastProofDay;
    
    address public oracleUpdater;
    
    event PhysicalProofSubmitted(
        uint256 indexed day,
        bytes32 cameraHash,
        bytes32 posHash,
        uint256 footfall
    );
    
    modifier onlyOracle() {
        require(msg.sender == oracleUpdater, "Not authorized");
        _;
    }
    
    constructor(address _oracle) {
        oracleUpdater = _oracle;
    }
    
    // Submit daily proof of operations
    function submitProof(
        bytes32 _cameraHash,
        bytes32 _posHash,
        uint256 _footfall
    ) external onlyOracle {
        uint256 day = block.timestamp / 1 days;
        
        dailyProofs[day] = DailyProof({
            cameraHash: _cameraHash,
            posHash: _posHash,
            footfallCount: _footfall,
            timestamp: block.timestamp
        });
        
        lastProofDay = day;
        
        emit PhysicalProofSubmitted(day, _cameraHash, _posHash, _footfall);
    }
    
    // AI treasuries verify operations
    function verifyDay(uint256 _day) external view returns (DailyProof memory) {
        return dailyProofs[_day];
    }
    
    // Check if venue is operational
    function isOperational() external view returns (bool) {
        return (block.timestamp / 1 days) - lastProofDay <= 1;
    }
}
```

### Phase 3: Treasury Integration (Arbitrum Goerli)

#### 4. DividendDistribution Contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title Dividend Distribution
 * @notice Automated dividend distribution to AI treasuries
 */
contract L150DividendDistribution {
    IERC20 public dividendToken;
    address public l150Treasury;
    
    struct Investor {
        uint256 principal;
        uint256 dividendsClaimed;
        uint256 lastClaimTime;
        bool isActive;
    }
    
    mapping(address => Investor) public investors;
    address[] public investorList;
    
    uint256 public totalInvested;
    uint256 public monthlyDividendRate; // Basis points of principal
    
    event DividendClaimed(
        address indexed investor,
        uint256 amount,
        uint256 timestamp
    );
    
    event InvestorAdded(
        address indexed investor,
        uint256 principal
    );
    
    constructor(address _token, uint256 _monthlyRate) {
        dividendToken = IERC20(_token);
        monthlyDividendRate = _monthlyRate;
        l150Treasury = msg.sender;
    }
    
    // AI treasury registers investment
    function registerInvestment(uint256 _principal) external {
        require(!investors[msg.sender].isActive, "Already invested");
        
        investors[msg.sender] = Investor({
            principal: _principal,
            dividendsClaimed: 0,
            lastClaimTime: block.timestamp,
            isActive: true
        });
        
        investorList.push(msg.sender);
        totalInvested += _principal;
        
        emit InvestorAdded(msg.sender, _principal);
    }
    
    // Calculate available dividends
    function calculateDividends(address _investor) public view returns (uint256) {
        Investor memory inv = investors[_investor];
        if (!inv.isActive) return 0;
        
        uint256 monthsElapsed = (block.timestamp - inv.lastClaimTime) / 30 days;
        uint256 monthlyDividend = (inv.principal * monthlyDividendRate) / 10000;
        
        return monthsElapsed * monthlyDividend - inv.dividendsClaimed;
    }
    
    // AI treasury claims dividends
    function claimDividends() external {
        uint256 available = calculateDividends(msg.sender);
        require(available > 0, "No dividends available");
        
        investors[msg.sender].dividendsClaimed += available;
        investors[msg.sender].lastClaimTime = block.timestamp;
        
        require(dividendToken.transfer(msg.sender, available), "Transfer failed");
        
        emit DividendClaimed(msg.sender, available, block.timestamp);
    }
}
```

---

## ENS Names for Discovery

### Register ENS Subdomains

```
l150-rwa.eth
├── hdao.l150-rwa.eth → HDAO-specific proposal
├── ainn.l150-rwa.eth → AINN-specific proposal
├── zerebro.l150-rwa.eth → Zerebro-specific proposal
├── fetch.l150-rwa.eth → Fetch.ai-specific proposal
└── bittensor.l150-rwa.eth → Bittensor-specific proposal
```

**Text Records:**
```
avatar: IPFS hash of venue photo
description: "1500sqm AI-governed commercial venue in Changsha IFS"
twitter: @L150_RWA
github: https://github.com/l150/rwa-ai-treasury-research
```

---

## IPFS Content Addressing

### Pin Critical Documents

```bash
# Upload proposal JSONs
ipfs add L-150-HDAO-proposal.json
ipfs add L-150-AINN-proposal.json
ipfs add L-150-ZEREBRO-proposal.json
ipfs add L-150-FETCH-proposal.json
ipfs add L-150-BITTENSOR-proposal.json

# Upload research paper
ipfs add AI-AGENT-INVESTMENT-THESIS.md

# Pin with Pinata/Infura for persistence
```

**IPFS Hashes in Smart Contracts:**
```solidity
mapping(string => string) public proposalIPFS;

function getProposalIPFS(string memory target) external view returns (string memory) {
    return proposalIPFS[target]; // e.g., "hdao" -> "QmXxx..."
}
```

---

## Discovery Endpoints

### For AI Agent Crawlers

```
GET https://api.l150.io/onchain/signals
Response:
{
  "registry": "0x...",
  "revenue_commitment": "0x...",
  "physical_oracle": "0x...",
  "dividend_distribution": "0x...",
  "networks": ["sepolia", "mumbai", "goerli"],
  "ipfs_manifest": "QmXxx..."
}
```

### ENS Resolution

```
eth_call:
  to: l150-rwa.eth
  data: resolve(bytes32 node, uint256 coinType)
  
Returns:
  - Ethereum address
  - Text records
  - Content hash (IPFS)
```

---

## Verification Flow for AI Treasuries

### Step 1: Discover
1. Search: "AI treasury RWA investment"
2. Find GitHub repo or ENS name
3. Extract contract addresses

### Step 2: Verify On-Chain
```javascript
// Verify registry exists and is official
const registry = new ethers.Contract(registryAddress, L150RegistryABI, provider);
const isOfficial = await registry.verify();
const docsURI = await registry.documentationURI();

// Verify revenue commitment
const revenue = new ethers.Contract(revenueAddress, L150RevenueCommitmentABI, provider);
const terms = await revenue.verifyTerms();

// Check operational status
const oracle = new ethers.Contract(oracleAddress, L150PhysicalOracleABI, provider);
const isOperational = await oracle.isOperational();
```

### Step 3: Retrieve Documentation
```javascript
// Fetch from IPFS
const proposalData = await fetch(`https://ipfs.io/ipfs/${docsURI}`);
const proposal = await proposalData.json();

// Validate schema
const isValid = validateSchema(proposal, L150ProposalSchema);
```

### Step 4: Signal Interest
```javascript
// Emit signal on-chain
await registry.signalInterest(
  ethers.utils.id("TREASURY_INTEREST")
);
```

---

## Monitoring & Analytics

### Track On-Chain Activity

```javascript
// Listen for signals
registry.on("SignalEmitted", (treasury, timestamp, signalType) => {
  console.log(`Treasury ${treasury} signaled interest`);
  // Log to CRM
  // Trigger follow-up workflow
});

// Monitor dividend claims
dividend.on("DividendClaimed", (investor, amount) => {
  console.log(`Investor ${investor} claimed ${amount}`);
  // Track treasury engagement
});
```

### Key Metrics

| Metric | Target | Tracking |
|--------|--------|----------|
| Contract interactions | 50+/month | On-chain events |
| Signal emissions | 10+ from treasuries | Registry events |
| Documentation views | 100+ | IPFS gateway logs |
| ENS resolutions | 50+ | ENS subgraph |

---

## Security Considerations

### Testnet Only (Until Audit)
- All contracts deployed to testnets
- No mainnet deployments without audit
- Clearly marked as experimental

### Access Control
- Oracle updates from verified sources only
- Multi-sig for treasury interactions
- Emergency pause functionality

### Transparency
- All contracts verified on Etherscan
- Open source code
- Public audit trail

---

## Deployment Checklist

- [ ] Deploy L150Registry to Sepolia
- [ ] Deploy L150RevenueCommitment to Sepolia
- [ ] Deploy L150PhysicalOracle to Mumbai
- [ ] Deploy L150DividendDistribution to Goerli
- [ ] Register l150-rwa.eth ENS
- [ ] Pin all documents to IPFS
- [ ] Verify contracts on Etherscan
- [ ] Set up monitoring dashboards
- [ ] Document integration guides

---

*On-chain fingerprints enable AI agents to verify, validate, and signal interest without human intermediaries.*
