#!/bin/bash
# Emergency deployment without interactive login
# This creates deployable packages for manual upload

echo "🚀 L-150 Emergency Deployment Packager"
echo "======================================"
echo ""

# Create deployment packages
mkdir -p ~/.openclaw/workspace/deployment-packages

echo "📦 Packaging GitHub Repository..."
cd ~/.openclaw/workspace/signals/github-bait
tar czf ~/.openclaw/workspace/deployment-packages/github-repo.tar.gz .
echo "✅ github-repo.tar.gz created"

echo ""
echo "📦 Packaging API Server..."
cd ~/.openclaw/workspace/api
tar czf ~/.openclaw/workspace/deployment-packages/api-server.tar.gz .
echo "✅ api-server.tar.gz created"

echo ""
echo "📦 Packaging Smart Contracts..."
cd ~/.openclaw/workspace/contracts
tar czf ~/.openclaw/workspace/deployment-packages/smart-contracts.tar.gz .
echo "✅ smart-contracts.tar.gz created"

echo ""
echo "📦 Packaging All Proposals..."
cd ~/.openclaw/workspace/outreach/ai-agent-treasury-proposals
tar czf ~/.openclaw/workspace/deployment-packages/proposals.tar.gz .
echo "✅ proposals.tar.gz created"

echo ""
echo "📝 Creating deployment instructions..."
cat > ~/.openclaw/workspace/deployment-packages/README.txt << 'EOF'
L-150 AI Treasury Signal Deployment Packages
============================================

Package Contents:
1. github-repo.tar.gz - GitHub repository for SEO bait
2. api-server.tar.gz - Express API server for Vercel
3. smart-contracts.tar.gz - Solidity contracts for Hardhat
4. proposals.tar.gz - Machine-readable JSON proposals

Quick Deployment:

1. GitHub:
   - Create repo: github.com/new
   - Name: rwa-ai-treasury-research
   - Extract github-repo.tar.gz
   - Push to repo

2. Vercel:
   - Visit: vercel.com/new
   - Import GitHub repo
   - Framework: Other
   - Deploy

3. Contracts:
   - Get testnet ETH from faucets
   - Configure .env with private key
   - Run: npx hardhat run scripts/deploy.js --network sepolia

Faucets:
- Sepolia: https://sepoliafaucet.com
- Mumbai: https://faucet.polygon.technology

Status Check:
- GitHub: github.com/[username]/rwa-ai-treasury-research
- API: https://[project].vercel.app/api/v1/project
EOF
echo "✅ README.txt created"

echo ""
echo "📂 All packages ready in:"
echo "   ~/.openclaw/workspace/deployment-packages/"
echo ""
echo "🎯 Next: Upload these packages to deploy"
ls -lh ~/.openclaw/workspace/deployment-packages/
