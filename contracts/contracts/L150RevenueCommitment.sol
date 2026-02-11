// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title L150 Revenue Commitment
 * @notice On-chain commitment of revenue sharing terms
 */
contract L150RevenueCommitment {
    struct InvestmentTerms {
        uint256 totalAmount;
        uint256 monthlyDividend;
        uint256 paybackMonths;
        uint256 postRoiShareBps;
        uint256 tranche1Amount;
        uint256 tranche2Amount;
    }
    
    InvestmentTerms public terms;
    address public operator;
    
    mapping(address => bool) public verifiedTreasuries;
    address[] public treasuryList;
    
    event RevenueCommitted(
        uint256 amount,
        uint256 monthlyDividend,
        uint256 timestamp
    );
    
    event TreasuryVerified(
        address indexed treasury,
        uint256 timestamp
    );
    
    modifier onlyOperator() {
        require(msg.sender == operator, "Not authorized");
        _;
    }
    
    constructor(
        uint256 _totalAmount,
        uint256 _monthlyDividend,
        uint256 _paybackMonths
    ) {
        terms = InvestmentTerms({
            totalAmount: _totalAmount,
            monthlyDividend: _monthlyDividend,
            paybackMonths: _paybackMonths,
            postRoiShareBps: 2000, // 20%
            tranche1Amount: 100000,
            tranche2Amount: 50000
        });
        operator = msg.sender;
        
        emit RevenueCommitted(_totalAmount, _monthlyDividend, block.timestamp);
    }
    
    // AI treasuries verify terms on-chain
    function verifyTerms() external view returns (InvestmentTerms memory) {
        return terms;
    }
    
    // Quick calculation for potential investors
    function calculateReturns(uint256 _months) external view returns (
        uint256 totalDividends,
        uint256 principalReturned,
        uint256 postRoiShare
    ) {
        uint256 monthlyDividend = terms.monthlyDividend;
        totalDividends = monthlyDividend * _months;
        
        if (_months >= terms.paybackMonths) {
            principalReturned = terms.totalAmount;
            uint256 monthsPostRoi = _months - terms.paybackMonths;
            // Simplified: assumes constant monthly revenue for post-ROI share
            postRoiShare = (terms.totalAmount * terms.postRoiShareBps * monthsPostRoi) / (10000 * 12);
        }
        
        return (totalDividends, principalReturned, postRoiShare);
    }
    
    // Verify a treasury (operator only)
    function verifyTreasury(address _treasury) external onlyOperator {
        if (!verifiedTreasuries[_treasury]) {
            verifiedTreasuries[_treasury] = true;
            treasuryList.push(_treasury);
            emit TreasuryVerified(_treasury, block.timestamp);
        }
    }
    
    // Check if treasury is verified
    function isVerified(address _treasury) external view returns (bool) {
        return verifiedTreasuries[_treasury];
    }
    
    // Get all verified treasuries
    function getVerifiedTreasuries() external view returns (address[] memory) {
        return treasuryList;
    }
    
    // Calculate APR for display
    function getAPR() external pure returns (uint256) {
        return 40; // 40% APR
    }
    
    // Get payback period in months
    function getPaybackMonths() external view returns (uint256) {
        return terms.paybackMonths;
    }
}
