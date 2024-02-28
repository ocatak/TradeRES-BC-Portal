// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/EnergyToken.sol";

contract TestEnergyToken {
    EnergyToken token = EnergyToken(DeployedAddresses.EnergyToken());

    // Test the token's initial supply
    function testInitialSupply() public {
        uint expectedInitialSupply = 1000000 * (10 ** uint256(token.decimals()));
        Assert.equal(token.totalSupply(), expectedInitialSupply, "Initial supply should be 1,000,000 tokens");
    }

    // Test the mint function
    function testMintingTokens() public {
        address to = address(this);
        uint256 amount = 100 * (10 ** uint256(token.decimals()));
        uint256 previousBalance = token.balanceOf(to);

        // Call the mint function, which is available to the contract owner
        token.mint(to, amount);

        uint256 newBalance = token.balanceOf(to);
        Assert.equal(newBalance, previousBalance + amount, "Minting should increase the balance by the minted amount");
    }

    // Test the burn function
    function testBurningTokens() public {
        uint256 amountToBurn = 50 * (10 ** uint256(token.decimals()));
        uint256 previousBalance = token.balanceOf(address(this));

        // Ensure there's enough balance to burn
        if (previousBalance < amountToBurn) {
            token.mint(address(this), amountToBurn);
        }

        // Call the burn function
        token.burn(amountToBurn);

        uint256 newBalance = token.balanceOf(address(this));
        Assert.equal(newBalance, previousBalance - amountToBurn, "Burning should decrease the balance by the burned amount");
    }
}
