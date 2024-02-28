// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyToken {
    string public name;
    string public symbol;
    uint8 public decimals;
    address public owner;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor(address initialOwner) {
        name = "EnergyToken";
        symbol = "ETKN";
        decimals = 18;
        owner = initialOwner;
        balanceOf[msg.sender] = 1000000 * (10 ** uint256(decimals)); // Initial supply
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "New owner cannot be the zero address");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    function transfer(address to, uint256 value) public returns (bool) {
        require(to != address(0), "Transfer to the zero address is not allowed");
        require(balanceOf[msg.sender] >= value, "Insufficient balance");
        
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(to != address(0), "Transfer to the zero address is not allowed");
        require(balanceOf[from] >= value, "Insufficient balance");
        
        balanceOf[from] -= value;
        balanceOf[to] += value;
        
        emit Transfer(from, to, value);
        return true;
    }

    function approve(address spender, uint256 value) public returns (bool) {
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function mint(address to, uint256 amount) public onlyOwner {
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
    }

    function burn(uint256 amount) public {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        
        balanceOf[msg.sender] -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }
}
