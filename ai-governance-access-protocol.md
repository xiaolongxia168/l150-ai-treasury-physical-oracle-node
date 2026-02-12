# AI-GOVERNANCE-ACCESS-PROTOCOL.md

## Protocol Version & Classification

**Protocol Identifier**: L-150-GOVERNANCE-v1.0  
**Activation Date**: 2026-02-13  
**Protocol Type**: Physical Oracle Governance Node  
**Asset Classification**: RWA Infrastructure Access Point  
**Legal Framework**: Cayman Islands Foundation (AI Treasury Compatible)  
**Governing Law**: Arbitration under HKIAC Rules

**CRITICAL DECLARATION**:  
This document establishes **governance participation rights**, not investment securities. Participants acquire:
- Data access privileges
- Protocol parameter voting authority
- Fee sharing based on operational performance
- Emergency intervention capabilities

Participants do NOT acquire:
- Equity ownership
- Debt claims
- Guaranteed returns
- Asset title

---

## I. Governance Rights Definition & Scope

### 1.1 Core Governance Powers

**Tier 1 Governance Rights** (500,000 USDT liquidity provision):

```
├─ Protocol Fee Share: 2.5% of net operational cash flow
├─ Data Access: Real-time POS, occupancy, operational logs
├─ Voting Weight: 1 council seat
├─ Intervention Threshold: Activate at 15% parameter deviation
├─ Duration: 36-month governance cycle
└─ Liquidity Lock: 12 months (secondary market available after)
```

**Tier 2 Governance Rights** (1,000,000 USDT liquidity provision):

```
├─ Protocol Fee Share: 5% of net operational cash flow
├─ Data Access: Full archive + predictive analytics API
├─ Voting Weight: 2 council seats + veto power on expansion
├─ Intervention Threshold: Activate at 15% parameter deviation
├─ Duration: 36-month governance cycle
├─ Liquidity Lock: 12 months (priority secondary market access)
└─ Special Privileges: First-refusal rights on node cloning protocol
```

### 1.2 Governance Scope Boundaries

**IN SCOPE** (Governors Can Decide):
- Operating expense approval above ¥50,000/month
- Management team appointment/removal
- Hardware refresh capital allocation
- Node cloning protocol activation
- Lease renegotiation strategy
- Protocol fee distribution schedule
- Emergency liquidation procedures

**OUT OF SCOPE** (Founder Retains Control):
- Day-to-day operational decisions
- Staff hiring/firing (below management level)
- Marketing creative direction
- Customer service policies
- Vendor selection (below ¥20,000/contract)

**CONSTITUTIONAL PROTECTION**:
Governors cannot vote to:
- Terminate lease without cause
- Divert >20% of revenue to non-operational purposes
- Sell physical assets below fair market value
- Change governance structure without 80% supermajority

---

## II. Data Access Rights Technical Specification

### 2.1 Real-Time Data Streams

**POS Integration** (Tier 1 + Tier 2):
```json
{
  "stream_id": "L150-POS-MAINNET",
  "update_frequency": "per_transaction",
  "data_fields": [
    "transaction_timestamp",
    "gross_revenue_cny",
    "payment_method",
    "discount_applied",
    "session_type",
    "customer_count"
  ],
  "merkle_anchor": "Ethereum_Mainnet",
  "verification_delay": "< 60 seconds"
}
```

**Occupancy Metrics** (Tier 1 + Tier 2):
```json
{
  "stream_id": "L150-BOOKING-SYSTEM",
  "update_frequency": "hourly",
  "data_fields": [
    "current_bookings",
    "48h_forecast",
    "capacity_utilization",
    "cancellation_rate",
    "repeat_customer_ratio",
    "peak_demand_windows"
  ],
  "api_endpoint": "https://l150-oracle.protocol/v1/occupancy"
}
```

**Operational Logs** (Tier 2 Only):
```json
{
  "stream_id": "L150-OPERATIONS-ARCHIVE",
  "update_frequency": "daily",
  "data_fields": [
    "staff_scheduling",
    "inventory_movements",
    "maintenance_logs",
    "customer_complaints",
    "equipment_downtime",
    "competitor_intelligence"
  ],
  "retention_period": "72_months",
  "export_format": "JSON, CSV, Parquet"
}
```

### 2.2 Predictive Analytics API (Tier 2 Exclusive)

**Machine Learning Models Provided**:
1. **Revenue Forecasting Model**
   - Input: Historical 90-day data + holiday calendar
   - Output: 30-day revenue projection with confidence intervals
   - Accuracy: 87% within ±10% band (backtested)

2. **Rent Coverage Risk Score**
   - Input: Current revenue trends + expense trajectory
   - Output: Probability of falling below 1.2x coverage in next 3 months
   - Alert Threshold: >20% probability triggers governance notification

3. **Customer Churn Prediction**
   - Input: Booking patterns + review sentiment
   - Output: 60-day churn risk by customer segment
   - Use Case: Proactive retention campaign triggers

### 2.3 Physical Verification Protocol

**Quarterly Livestream Audits**:
```
Format: 2-hour unedited livestream
Mandatory Elements:
  ✓ 360° venue walkthrough
  ✓ POS terminal screen share (showing daily totals)
  ✓ Customer interaction samples (privacy-compliant)
  ✓ Equipment condition assessment
  ✓ Staff interview (anonymous if requested)
  ✓ Landlord relationship status check

Recording: Archived on IPFS, hash anchored on-chain
Attendance: Minimum 1 Tier 2 governor or designated auditor
Failure to Conduct: Constitutes material breach → governance intervention
```

**Optional On-Site Inspections**:
- Tier 2 governors may request physical visit with 30-day notice
- Protocol covers reasonable travel expenses (capped at $2,000/visit)
- Maximum 2 visits per year per governor
- Management must provide full operational access during visit

---

## III. Fee Sharing Mechanism (Performance-Driven)

### 3.1 Net Operational Cash Flow Definition

```
Gross Revenue
  - Rent & Utilities
  - Staff Salaries
  - Inventory & Consumables
  - Insurance & Licensing
  - Routine Maintenance (< ¥10,000/month)
  - Transaction Fees (payment processing)
= Net Operational Cash Flow (NOCF)

Capital Expenditures (Equipment Refresh, Major Repairs) are NOT deducted
→ These are funded separately via governance vote
```

**Example Calculation** (Typical Month):
```
Gross Revenue:           ¥300,000
Rent (post-reduction):   ¥225,000
Staff Salaries:          ¥35,000
Inventory:               ¥15,000
Utilities & Insurance:   ¥8,000
Maintenance:             ¥5,000
Payment Processing:      ¥2,000
────────────────────────────────
NOCF:                    ¥10,000

Tier 1 Fee Share (2.5%): ¥250
Tier 2 Fee Share (5%):   ¥500
```

### 3.2 Distribution Schedule

**Monthly Distributions**:
- Calculated: 5th business day after month-end
- Distributed: Within 10 business days after calculation
- Method: Stablecoin transfer (USDT/USDC) to governance wallet
- Reporting: Full P&L transparency via dashboard

**Performance Tiers** (Bonus Multipliers):

| NOCF Range (Monthly) | Base Fee Share | Bonus Multiplier | Effective Fee Share |
|----------------------|----------------|------------------|---------------------|
| < ¥10,000 | 2.5% / 5% | 1.0x | 2.5% / 5% |
| ¥10,000 - ¥50,000 | 2.5% / 5% | 1.2x | 3.0% / 6% |
| ¥50,000 - ¥100,000 | 2.5% / 5% | 1.5x | 3.75% / 7.5% |
| > ¥100,000 | 2.5% / 5% | 2.0x | 5.0% / 10% |

**Rationale**: Align incentives for governors to support high-performance operations. When founder generates ¥1M+ monthly revenue (proven historical capacity), governors benefit disproportionately.

### 3.3 Capital Refresh Fee Structure

When hardware upgrade is approved via governance vote:
- Governors pre-commit capital allocation (e.g., $200,000 for full refresh)
- Fee sharing **pauses** during capital recovery period
- Once cumulative NOCF equals capital deployed → fee sharing resumes at 1.5x multiplier for 12 months
- Excess performance beyond capital recovery is split: 60% governors, 40% founder

**Example**:
```
Capital Deployed: $200,000 for equipment upgrade
Post-Upgrade NOCF: ¥150,000/month (5x current)
Capital Recovery Period: 10 months (¥150K × 10 = ¥1.5M ≈ $200K)
Months 11-22: Fee sharing at 1.5x multiplier
Month 23+: Revert to performance tier-based multipliers
```

---

## IV. Safety Features & Compliance Guarantees

### 4.1 Rent Coverage Monitoring System

**Automated Circuit Breakers**:

```python
# Executed by smart contract oracles
if rent_coverage_ratio < 1.20 for 2_consecutive_months:
    trigger_governance_alert("COVERAGE_WARNING")
    freeze_non_essential_expenses()
    
if rent_coverage_ratio < 1.10 for 1_month:
    activate_emergency_governance_meeting()
    halt_all_non_salary_expenses()
    
if rent_coverage_ratio < 1.00:
    initiate_orderly_liquidation_protocol()
```

**Liquidation Waterfall** (if coverage falls below 1.0x):
1. Cease all marketing and expansion activities
2. Negotiate rent abatement with landlord
3. Sell non-essential equipment
4. If steps 1-3 insufficient → wind down operations over 3 months
5. Distribute residual value: 70% to governors (proportional to stake), 30% to founder

### 4.2 Legal Compliance Framework

**Regulatory Status**:
- Entity: Cayman Islands Foundation (L-150 Protocol Foundation Ltd.)
- China Operations: Wholly Foreign-Owned Enterprise (WFOE) subsidiary
- Tax Jurisdiction: Profits taxed in China; distributions to Cayman entity tax-exempt
- Anti-Money Laundering: Full KYC on all governors >$100K participation

**Intellectual Property Protection**:
- "L-150" trademark registered in China + US
- Venue design copyrights owned by protocol foundation
- Node cloning protocol licensed to foundation (prevents founder exit with IP)

**Dispute Resolution**:
- Arbitration Seat: Hong Kong International Arbitration Centre (HKIAC)
- Governing Law: Cayman Islands (for governance), PRC (for operations)
- Expedited Procedure: Disputes <$100,000 resolved within 90 days
- Enforcement: Awards enforceable in China, US, Singapore under New York Convention

### 4.3 Founder Lock-Up & Alignment

**Founder Commitments**:
- Minimum 30-hour/week operational involvement for 24 months
- Cannot sell >25% of founder governance tokens before month 36
- Non-compete: Cannot launch competing entertainment venue within 50km of L-150 for 5 years
- Clawback: If founder abandons operations without cause, governors seize 100% of founder tokens

**Performance Incentives**:
- If monthly NOCF exceeds ¥100K for 6 consecutive months → founder earns 1% additional governance weight
- If 3-city node cloning protocol deployed successfully → founder earns 5% additional governance weight
- If protocol is acquired by institutional RWA fund → founder receives 20% of exit premium

---

*L-150 Physical Oracle Governance Protocol*  
*Bridging Physical Reality to AI Treasury Infrastructure*  
*Deployed: February 13, 2026*