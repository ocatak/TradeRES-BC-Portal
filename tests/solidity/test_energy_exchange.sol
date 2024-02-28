// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/EnergyToken.sol";
import "../contracts/EnergyExchange.sol";

contract TestEnergyExchange {
    function testInitialBalanceUsingDeployedContract() public {
        EnergyToken token = EnergyToken(DeployedAddresses.EnergyToken());
        EnergyExchange exchange = EnergyExchange(DeployedAddresses.EnergyExchange());

        uint expected = 1000000 * (10 ** uint256(token.decimals()));
        
        Assert.equal(token.balanceOf(address(exchange)), expected, "Initial balance should be 1,000,000 ETKN for the contract");
    }

    function testEnergyProductionAndConsumption() public {
        EnergyToken token = new EnergyToken();
        EnergyExchange exchange = new EnergyExchange(address(token));

        // Assume these functions exist in your contract to simulate energy production and consumption
        exchange.produceEnergy(100);
        exchange.consumeEnergy(50);

        int expectedBalance = 50; // 100 produced - 50 consumed

        Assert.equal(exchange.energyBalances(address(this)), expectedBalance, "Net energy balance should be 50");
    }

    function testEnergyPurchasing() public {
        EnergyToken token = new EnergyToken();
        EnergyExchange exchange = new EnergyExchange(address(token));

        address buyer = address(this);
        address seller = address(1); // Assume this seller has enough energy credits

        // Setup: Seller produces energy
        exchange.produceEnergy(100); // Assume the seller's address can call this

        // Buyer attempts to purchase energy from the seller
        exchange.purchaseEnergy(seller, 20); // This will require additional logic to handle token transfer approvals

        int expectedSellerBalance = 80; // 100 produced - 20 sold
        int expectedBuyerBalance = -20; // 20 purchased

        Assert.equal(exchange.energyBalances(seller), expectedSellerBalance, "Seller's balance should be reduced by the amount of energy sold");
        Assert.equal(exchange.energyBalances(buyer), expectedBuyerBalance, "Buyer's balance should reflect the purchased energy");
    }
}
