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
