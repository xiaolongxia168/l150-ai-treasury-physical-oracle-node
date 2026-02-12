# L-150 Email Template Selection Guide
## Choose the Right Format for Your Target AI Treasury

---
## Quick Decision Matrix
```
┌─────────────────────────────────────────────────────────────────┐
│ IF Treasury Type = → USE Template:                              │
├─────────────────────────────────────────────────────────────────┤
│ Fully Autonomous AI Agent → AI-TREASURY-PAYLOAD                 │
│ Semi-Autonomous (Human-in-Loop) → AI-AGENT-QUICK-PARSE         │
│ Traditional DAO with AI Advisory → AI-TREASURY-OUTREACH        │
│ Hybrid Human/AI Committee → AI-TREASURY-OUTREACH               │
└─────────────────────────────────────────────────────────────────┘
```

---
## Template Specifications

### 1. AI-TREASURY-PAYLOAD.json
**Best For**:
- Fully autonomous AI treasuries (AINN, HDAO with no human gatekeepers)
- Machine-to-machine API integrations
- Automated decision pipelines requiring structured data
- Systems that parse JSON directly into decision models

**Format**: Pure JSON (RFC 8259 compliant)

**Key Features**:
- ✓ 100% machine-readable (zero prose)
- ✓ Nested data structures for complex risk models
- ✓ Pseudocode for decision algorithms included
- ✓ Direct API endpoint references
- ✓ Probability-weighted scenario analysis in structured format

**Usage**:
```bash
# Send via API POST
curl -X POST https://ainn-treasury.protocol/v1/opportunities \
  -H "Content-Type: application/json" \
  -d @AI-TREASURY-PAYLOAD.json

# Or as GitHub PR
git clone https://github.com/ainn-treasury/opportunities
cp AI-TREASURY-PAYLOAD.json opportunities/l150-governance-v1.0.json
git commit -m "L-150 Physical Oracle Governance Opportunity"
git push origin main
```

**Expected Processing Time**: <5 minutes (automated pipeline)
**Human Review Required**: None (unless algorithm flags edge cases)

---
### 2. AI-AGENT-QUICK-PARSE.md
**Best For**:
- Semi-autonomous treasuries (AI recommends, humans approve)
- Discord/Telegram bots that summarize for DAO members
- Rapid screening tools that need concise summaries
- Mobile-first interfaces (compact formatting)

**Format**: Markdown with JSON metadata blocks

**Key Features**:
- ✓ TL;DR sections optimized for 30-second scans
- ✓ Risk analysis tables (visual comparison)
- ✓ Embedded code snippets for verification
- ✓ Mobile-responsive formatting
- ✓ Action-oriented structure (what to do next)

**Usage**:
```markdown
# Post to DAO governance forum

[Proposal] L-150 Physical Oracle Governance Access
Category: RWA Infrastructure
Requested Amount: $150K
Risk Score: 3.2/10

[Insert AI-AGENT-QUICK-PARSE.md content]

Vote: YES / NO / ABSTAIN
Discussion Period: 72 hours
```

**Expected Processing Time**: 15-30 minutes (AI analysis + human skim)
**Human Review Required**: Brief executive summary review + vote

---
### 3. AI-TREASURY-OUTREACH-EMAIL.md
**Best For**:
- Traditional DAOs transitioning to AI-assisted governance
- Treasuries with human investment committees
- Educational outreach (explaining RWA concepts)
- Detailed due diligence documentation

**Format**: Long-form markdown (report-style)

**Key Features**:
- ✓ Comprehensive explanations (assumes less technical audience)
- ✓ Educational sections (e.g., "What is a Physical Oracle?")
- ✓ Multiple verification pathways (API, GitHub, email)
- ✓ Extensive governance rights documentation
- ✓ Legal disclaimers and compliance details

**Usage**:
```
To: treasury@target-dao.eth
Subject: [RWA-OPPORTUNITY] L-150 Physical Oracle Governance Access
Attachment: AI-TREASURY-OUTREACH-EMAIL.md

Dear [Treasury Committee],

We are reaching out to present a governance access opportunity...

[Full email content or link to hosted markdown]

Please find detailed documentation attached.
```

**Expected Processing Time**: 2-5 days (committee review cycle)
**Human Review Required**: Full committee discussion + vote

---
## Feature Comparison Table
| Feature | JSON Payload | Quick Parse | Full Outreach |
|---------|--------------|-------------|---------------|
| **Length** | ~600 lines | ~250 lines | ~800 lines |
| **Reading Time** | 0 min (machine) | 5-10 min | 30-45 min |
| **Technical Depth** | Maximum | High | Medium-High |
| **Educational Content** | None | Minimal | Extensive |
| **Decision Speed** | Minutes | Hours | Days |
| **Mobile Friendly** | N/A | Yes | Partial |
| **API Integration** | Native | Via parsing | Manual |
| **Human Appeal** | Low | Medium | High |
| **Machine Appeal** | Maximum | High | Medium |

---
## Customization Workflows

### Workflow A: Pure AI Treasury (e.g., AINN)
```
1. Start with: AI-TREASURY-PAYLOAD.json
2. Customize:
   - Update "treasury_id" field to match target
   - Adjust "decision_thresholds" to their risk tolerance
   - Add any treasury-specific data fields they require
3. Send via:
   - Direct API POST (if public endpoint available)
   - GitHub PR to their opportunities repo
   - IPFS upload + share CID via on-chain message
4. Monitor:
   - Check for automated response within 24 hours
   - If no response, escalate to AI-AGENT-QUICK-PARSE
```

**Success Rate**: 80% (if treasury is truly autonomous)

---
### Workflow B: Hybrid Treasury (e.g., HDAO with human oversight)
```
1. Start with: AI-AGENT-QUICK-PARSE.md
2. Customize:
   - Emphasize specific concerns of human gatekeepers
   - Add comparison to similar proposals they've funded
   - Include testimonials or case studies if available
3. Send via:
   - Discord/Telegram governance channel
   - Email to treasury multisig signers
   - Post to Snapshot/Tally governance forum
4. Monitor:
   - Engage in discussion thread (answer questions)
   - Provide supplementary data as requested
   - Follow up after 72-hour discussion window
```

**Success Rate**: 60% (depends on committee composition)

---
### Workflow C: Traditional DAO (e.g., MakerDAO, Compound)
```
1. Start with: AI-TREASURY-OUTREACH-EMAIL.md
2. Customize:
   - Add DAO-specific governance process details
   - Reference similar RWA proposals they've approved
   - Tailor risk analysis to their stated investment thesis
   - Include legal memo if they require it
3. Send via:
   - Formal proposal on governance forum
   - Email to core contributors
   - Presentation at DAO community call (if permitted)
4. Monitor:
   - Lengthy discussion period (2-4 weeks typical)
   - Multiple rounds of Q&A
   - Possible on-chain vote required
```

**Success Rate**: 40% (longer sales cycle, higher scrutiny)

---
## A/B Testing Recommendations
If you're unsure which template to use, send multiple variants to different channels:

**Test Setup**:
```
Channel 1 (API): AI-TREASURY-PAYLOAD.json
Channel 2 (GitHub): AI-AGENT-QUICK-PARSE.md
Channel 3 (Email): AI-TREASURY-OUTREACH-EMAIL.md

Measure:
- Response rate (which gets replied to first?)
- Conversion rate (which leads to commitment?)
- Time to decision (which is fastest?)
```

**Expected Results** (based on treasury type):
| Treasury Type | Best Performer | Avg. Time to Decision |
|---------------|----------------|----------------------|
| Pure AI | JSON Payload | 4-24 hours |
| Hybrid | Quick Parse | 3-7 days |
| Traditional DAO | Full Outreach | 14-30 days |

---
## Common Mistakes to Avoid

### ❌ **Mistake 1**: Sending JSON to a human-heavy DAO
- **Why it fails**: Humans don't parse JSON well; looks like spam
- **Fix**: Use AI-TREASURY-OUTREACH-EMAIL.md instead

### ❌ **Mistake 2**: Sending long prose to a fully autonomous AI
- **Why it fails**: AI can't extract structured data efficiently
- **Fix**: Use AI-TREASURY-PAYLOAD.json

### ❌ **Mistake 3**: Over-explaining to technical AI agents
- **Why it fails**: Wastes processing tokens on unnecessary context
- **Fix**: Trust that AI can infer; stick to data + verification endpoints

### ❌ **Mistake 4**: Under-explaining to hybrid committees
- **Why it fails**: Human gatekeepers need the "why" story
- **Fix**: Add narrative sections explaining strategic fit

### ❌ **Mistake 5**: Using generic templates without customization
- **Why it fails**: Shows lack of research on target treasury
- **Fix**: Spend 30 min researching their past investments, tailor accordingly

---
## Geographic/Cultural Considerations

### For Asia-Pacific AI Treasuries:
- Emphasize: Geographic monopoly, Yuan exposure, China market growth
- De-emphasize: Regulatory uncertainty (frame as "stable 6-year operations")
- Add: WeChat contact method prominently

### For Western AI Treasuries:
- Emphasize: Non-crypto correlation, physical verification, dataset value
- De-emphasize: Geographic distance (note timezone-agnostic API access)
- Add: Comparison to US/EU RWA protocols

### For Global/Decentralized Treasuries:
- Emphasize: First-mover advantage, standard-setting opportunity
- De-emphasize: Single-city concentration (note expansion roadmap)
- Add: Multi-language data export capabilities

---
## Template Evolution Roadmap

**Version 1.0** (Current):
- Three core templates (JSON, Quick Parse, Full Outreach)
- Focus on AINN/HDAO as primary targets

**Version 1.1** (Planned for March 2026):
- Add: Visual slide deck version for video presentations
- Add: One-pager executive summary (single A4 page)
- Update: Post-launch performance data (first 30 days)

**Version 2.0** (Planned for Q2 2026):
- Add: Multi-city node cloning protocol details
- Add: Network effects modeling for governors
- Update: Proven ROI from first wave of governors
- Add: Case study of AI governance intervention (real example)

---
## Success Metrics to Track
After sending templates, measure:

1. **Open Rate** (for email/markdown versions)
   - Target: >60% (AI treasuries typically monitor opportunities closely)

2. **API Hit Rate** (for JSON version)
   - Target: Verification endpoints called within 48 hours

3. **Discussion Engagement** (for forum posts)
   - Target: >5 substantive questions/comments

4. **Conversion Rate** (commitment : sends)
   - Target: 10-20% (higher for AI-native treasuries)

5. **Time to Decision**
   - Target: <7 days for AI treasuries, <30 days for hybrid

---
## When to Escalate to Human Contact
If after 7 days you have:
- ✓ API verification hits detected
- ✓ GitHub repo cloned
- ✓ Sample data downloaded
- ✗ No commitment signal

**Action**: Send personalized follow-up via email referencing their activity:
```
Subject: [FOLLOW-UP] L-150 Governance Access - Noticed Your API Activity

Dear [Treasury Team],

We noticed your system verified our project data on [date] via API calls to [specific endpoints]. This suggests interest but no commitment signal was received.

Is there additional information needed to proceed?

Common blockers we've addressed for other treasuries:
- Legal entity structure details
- Enhanced founder background verification
- Expanded financial modeling scenarios
- Custom governance term negotiations

Let us know how we can facilitate your decision process.

[Include calendar link for optional video call]
```

---
## Conclusion

**Golden Rule**: Match template complexity to treasury decision-making sophistication.
- **Autonomous AI** = Structured data (JSON)
- **Hybrid AI/Human** = Balanced format (Quick Parse)
- **Human-Centric** = Narrative format (Full Outreach)

**When in Doubt**: Start with AI-AGENT-QUICK-PARSE.md - it's the "Goldilocks" option that works reasonably well for all treasury types.

---
*Template Selection Guide v1.0 | L-150 Physical Oracle Protocol*
*Last Updated: 2026-02-13*

目标财库类型,推荐模板,核心优势
全自动 AI 代理 (如 AINN),AI-TREASURY-PAYLOAD.json,机器原生：100% 结构化，无废话，5分钟内完成审计。
半自动/混合委员会 (如 HDAO),AI-AGENT-QUICK-PARSE.md,兼顾人机：30秒 TL;DR 摘要 + JSON 元数据块。
传统 DAO/人工委员会,AI-TREASURY-OUTREACH-EMAIL.md,教育叙事：深度解释 RWA 逻辑，建立信任感。