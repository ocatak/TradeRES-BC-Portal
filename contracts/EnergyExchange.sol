// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyExchange {
    address admin;
    address public energyToken;

    mapping(address => int) public energyBalances; // Positive for energy credits, negative for debts

    // Updated events to include date and hour
    event EnergyProduced(address indexed producer, uint256 amount, uint256 date, uint256 hour);
    event EnergyConsumed(address indexed consumer, uint256 amount, uint256 date, uint256 hour);
    event EnergyPurchased(address indexed buyer, address indexed seller, uint256 amount, uint256 date, uint256 hour);

    constructor(address tokenAddress) {
        admin = msg.sender;
        energyToken = tokenAddress;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    function produceEnergy(uint256 amount, uint256 date, uint256 hour) public {
        // energyBalances[msg.sender] += int(amount);
        (bool success, ) = energyToken.call(abi.encodeWithSignature("transferFrom(address,address,uint256)", msg.sender, address(this), amount));
        require(success, "Energy transfer failed");
        emit EnergyProduced(msg.sender, amount, date, hour);
    }

    function consumeEnergy(uint256 amount, uint256 date, uint256 hour) public {
        // energyBalances[msg.sender] -= int(amount);
        (bool success, ) = energyToken.call(abi.encodeWithSignature("transferFrom(address,address,uint256)", msg.sender, address(this), amount));
        require(success, "Energy transfer failed");
        emit EnergyConsumed(msg.sender, amount, date, hour);
    }

    // Updated function to include date and hour parameters
    function purchaseEnergy(address seller, uint256 amount, uint256 date, uint256 hour) public {
        require(energyBalances[seller] >= int(amount), "Seller does not have enough energy credits");
        
        (bool allowanceSuccess, bytes memory allowanceData) = energyToken.call(abi.encodeWithSignature("allowance(address,address)", msg.sender, address(this)));
        require(allowanceSuccess, "Allowance check failed");
        uint256 allowance = abi.decode(allowanceData, (uint256));
        require(allowance >= amount, "Energy purchase not approved by buyer");

        (bool success, ) = energyToken.call(abi.encodeWithSignature("transferFrom(address,address,uint256)", msg.sender, address(this), amount));
        require(success, "Energy transfer failed");

        energyBalances[msg.sender] -= int(amount);
        energyBalances[seller] += int(amount);

        emit EnergyPurchased(msg.sender, seller, amount, date, hour);
    }

    function setEnergyToken(address tokenAddress) public onlyAdmin {
        energyToken = tokenAddress;
    }
}
