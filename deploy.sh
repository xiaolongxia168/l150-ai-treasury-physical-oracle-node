#!/bin/bash
# L-150 AI Signal Infrastructure Deployment Script
# Run this to deploy all components

echo "🦞 L-150 AI Treasury Signal Deployment"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in correct directory
if [ ! -d "signals" ] || [ ! -d "api" ]; then
    echo "❌ Error: Must run from ~/.openclaw/workspace/"
    exit 1
fi

echo "${YELLOW}Phase 1: GitHub Repository${NC}"
echo "--------------------------"
echo "Repository: rwa-ai-treasury-research"
echo "Location: signals/github-bait/"
echo ""
echo "Commands to run:"
echo "  cd signals/github-bait"
echo "  git remote add origin https://github.com/xiaolongxia/rwa-ai-treasury-research.git"
echo "  git push -u origin main"
echo ""
read -p "Push to GitHub now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd signals/github-bait
    git remote remove origin 2>/dev/null || true
    git remote add origin https://github.com/xiaolongxia/rwa-ai-treasury-research.git
    git branch -M main
    git push -u origin main && echo "${GREEN}✅ GitHub deployed!${NC}" || echo "❌ GitHub push failed"
    cd ../..
fi

echo ""
echo "${YELLOW}Phase 2: Vercel API Deployment${NC}"
echo "------------------------------"
echo "API Location: api/"
echo ""
echo "Commands to run:"
echo "  cd api"
echo "  npx vercel --prod"
echo ""
read -p "Deploy to Vercel now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd api
    which vercel > /dev/null || npm i -g vercel
    vercel --prod
    cd ..
fi

echo ""
echo "${YELLOW}Phase 3: Smart Contracts${NC}"
echo "------------------------"
echo "Contracts: contracts/"
echo "Networks: Sepolia, Mumbai"
echo ""
echo "Prerequisites:"
echo "  1. Testnet ETH (get from faucets)"
echo "  2. Private key configured"
echo ""
echo "Commands to run:"
echo "  cd contracts"
echo "  cp .env.example .env"
echo "  # Edit .env with your private key"
echo "  npm install"
echo "  npx hardhat run scripts/deploy.js --network sepolia"
echo ""
read -p "Show contract deployment guide? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📋 Contract Deployment Checklist:"
    echo "  ☐ Get Sepolia ETH: https://sepoliafaucet.com"
    echo "  ☐ Get Mumbai MATIC: https://faucet.polygon.technology"
    echo "  ☐ Configure contracts/.env"
    echo "  ☐ Run: npx hardhat run scripts/deploy.js --network sepolia"
    echo "  ☐ Run: npx hardhat run scripts/deploy.js --network mumbai"
    echo "  ☐ Verify contracts on Etherscan/Polygonscan"
fi

echo ""
echo "${YELLOW}Phase 4: IPFS Pinning${NC}"
echo "---------------------"
echo "Documents to pin:"
echo "  - signals/ai-readable/AI-AGENT-INVESTMENT-THESIS.md"
echo "  - outreach/ai-agent-treasury-proposals/*.json"
echo ""
echo "Services:"
echo "  - https://pinata.cloud (推荐)"
echo "  - https://www.infura.io"
echo "  - https://web3.storage"
echo ""

echo ""
echo "${YELLOW}Phase 5: ENS Registration${NC}"
echo "-------------------------"
echo "Register: l150-rwa.eth"
echo "Visit: https://app.ens.domains"
echo ""

echo ""
echo "${GREEN}🎉 Deployment Guide Complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Visit deployed GitHub repo"
echo "  2. Test API endpoints"
echo "  3. Share with AI treasury communities"
echo ""
echo "Monitor:"
echo "  - GitHub stars/views"
echo "  - API requests"
echo "  - On-chain signals"
echo ""
