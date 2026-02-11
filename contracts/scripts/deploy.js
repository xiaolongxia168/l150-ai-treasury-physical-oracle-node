const hre = require('hardhat');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('🚀 Deploying L-150 AI Treasury Signal Contracts...\n');

  const [deployer] = await hre.ethers.getSigners();
  console.log('Deploying with account:', deployer.address);
  console.log(
    'Account balance:',
    (await deployer.provider.getBalance(deployer.address)).toString()
  );

  // IPFS hash for documentation (placeholder - will be updated)
  const docsIPFS = process.env.DOCS_IPFS || 'QmPlaceholder123456789';
  const proposalHash = hre.ethers.keccak256(
    hre.ethers.toUtf8Bytes('L-150-Proposal-v6.0')
  );

  console.log('\n📋 Deployment Parameters:');
  console.log('Docs IPFS:', docsIPFS);
  console.log('Proposal Hash:', proposalHash);

  // Deploy L150Registry
  console.log('\n📝 Deploying L150Registry...');
  const L150Registry = await hre.ethers.getContractFactory('L150Registry');
  const registry = await L150Registry.deploy(docsIPFS, proposalHash);
  await registry.waitForDeployment();
  console.log('✅ L150Registry deployed to:', await registry.getAddress());

  // Deploy L150RevenueCommitment
  console.log('\n💰 Deploying L150RevenueCommitment...');
  const L150RevenueCommitment = await hre.ethers.getContractFactory(
    'L150RevenueCommitment'
  );
  const revenue = await L150RevenueCommitment.deploy(
    150000, // $150K
    5000, // $5K monthly dividend
    30 // 30 months payback
  );
  await revenue.waitForDeployment();
  console.log(
    '✅ L150RevenueCommitment deployed to:',
    await revenue.getAddress()
  );

  // Deploy L150SignalInterface
  console.log('\n📡 Deploying L150SignalInterface...');
  const L150SignalInterface = await hre.ethers.getContractFactory(
    'L150SignalInterface'
  );
  const signalInterface = await L150SignalInterface.deploy(
    await registry.getAddress(),
    await revenue.getAddress()
  );
  await signalInterface.waitForDeployment();
  console.log(
    '✅ L150SignalInterface deployed to:',
    await signalInterface.getAddress()
  );

  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    chainId: hre.network.config.chainId,
    timestamp: new Date().toISOString(),
    deployer: deployer.address,
    contracts: {
      L150Registry: await registry.getAddress(),
      L150RevenueCommitment: await revenue.getAddress(),
      L150SignalInterface: await signalInterface.getAddress(),
    },
    ipfs: {
      documentation: docsIPFS,
    },
    proposalHash: proposalHash,
  };

  const deploymentsDir = path.join(__dirname, '..', 'deployments');
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir, { recursive: true });
  }

  fs.writeFileSync(
    path.join(deploymentsDir, `${hre.network.name}-deployment.json`),
    JSON.stringify(deploymentInfo, null, 2)
  );

  console.log('\n📦 Deployment Info Saved!');
  console.log(JSON.stringify(deploymentInfo, null, 2));

  // Verification instructions
  console.log('\n🔍 Verification Commands:');
  console.log(
    `npx hardhat verify --network ${hre.network.name} ${await registry.getAddress()} "${docsIPFS}" "${proposalHash}"`
  );
  console.log(
    `npx hardhat verify --network ${hre.network.name} ${await revenue.getAddress()} 150000 5000 30`
  );
  console.log(
    `npx hardhat verify --network ${hre.network.name} ${await signalInterface.getAddress()} ${await registry.getAddress()} ${await revenue.getAddress()}`
  );

  console.log('\n✨ Deployment Complete!');
  console.log(
    '\n🎯 AI Treasuries can now discover and interact with L-150 on-chain!'
  );
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
