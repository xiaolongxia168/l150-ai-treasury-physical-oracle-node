// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title L150 Signal Interface
 * @notice Interface for AI treasuries to interact with L-150
 */
contract L150SignalInterface {
    
    // Target treasury profiles
    enum TreasuryType {
        AI_GOVERNANCE_DAO,      // e.g., HDAO
        BITCOIN_L2,             // e.g., AINN
        CREATIVE_AI,            // e.g., Zerebro
        AUTONOMOUS_AGENTS,      // e.g., Fetch.ai
        DATA_NETWORK,           // e.g., Bittensor
        OTHER
    }
    
    struct Signal {
        address treasury;
        TreasuryType treasuryType;
        uint256 tvlUsd;
        uint256 interestScore;
        string message;
        uint256 timestamp;
        bool responded;
    }
    
    Signal[] public signals;
    mapping(address => uint256) public treasurySignalIndex;
    
    address public operator;
    address public registry;
    address public revenueContract;
    
    event SignalReceived(
        address indexed treasury,
        TreasuryType treasuryType,
        uint256 tvlUsd,
        string message,
        uint256 timestamp
    );
    
    event ResponseSent(
        address indexed treasury,
        string response,
        uint256 timestamp
    );
    
    modifier onlyOperator() {
        require(msg.sender == operator, "Not authorized");
        _;
    }
    
    constructor(address _registry, address _revenue) {
        operator = msg.sender;
        registry = _registry;
        revenueContract = _revenue;
    }
    
    // AI treasury submits investment interest signal
    function submitSignal(
        TreasuryType _type,
        uint256 _tvlUsd,
        uint256 _interestScore,
        string memory _message
    ) external {
        uint256 index = signals.length;
        
        signals.push(Signal({
            treasury: msg.sender,
            treasuryType: _type,
            tvlUsd: _tvlUsd,
            interestScore: _interestScore,
            message: _message,
            timestamp: block.timestamp,
            responded: false
        }));
        
        treasurySignalIndex[msg.sender] = index;
        
        emit SignalReceived(msg.sender, _type, _tvlUsd, _message, block.timestamp);
        
        // Also signal on registry for unified tracking
        (bool success, ) = registry.call(
            abi.encodeWithSignature(
                "signalInterest(bytes32,string)",
                keccak256(abi.encodePacked(_type)),
                _message
            )
        );
        // Ignore success - registry signal is bonus
    }
    
    // Operator responds to signal
    function respondToSignal(
        uint256 _signalIndex,
        string memory _response
    ) external onlyOperator {
        require(_signalIndex < signals.length, "Invalid index");
        signals[_signalIndex].responded = true;
        
        emit ResponseSent(
            signals[_signalIndex].treasury,
            _response,
            block.timestamp
        );
    }
    
    // Get signal count
    function getSignalCount() external view returns (uint256) {
        return signals.length;
    }
    
    // Get signals by type
    function getSignalsByType(TreasuryType _type) external view returns (Signal[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < signals.length; i++) {
            if (signals[i].treasuryType == _type) {
                count++;
            }
        }
        
        Signal[] memory result = new Signal[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < signals.length; i++) {
            if (signals[i].treasuryType == _type) {
                result[index] = signals[i];
                index++;
            }
        }
        
        return result;
    }
    
    // Get pending signals (not responded)
    function getPendingSignals() external view returns (Signal[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < signals.length; i++) {
            if (!signals[i].responded) {
                count++;
            }
        }
        
        Signal[] memory result = new Signal[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < signals.length; i++) {
            if (!signals[i].responded) {
                result[index] = signals[i];
                index++;
            }
        }
        
        return result;
    }
    
    // Quick check if treasury has signalled
    function hasSignalled(address _treasury) external view returns (bool) {
        return treasurySignalIndex[_treasury] > 0 || 
               (signals.length > 0 && signals[0].treasury == _treasury);
    }
}
