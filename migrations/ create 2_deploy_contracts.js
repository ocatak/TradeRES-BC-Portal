const EnergyToken = artifacts.require("EnergyToken");
const EnergyExchange = artifacts.require("EnergyExchange");

module.exports = async function(deployer) {
  // Deploy EnergyToken contract first
  await deployer.deploy(EnergyToken);
  const tokenInstance = await EnergyToken.deployed();

  // Deploy EnergyExchange contract with the address of the deployed EnergyToken
  await deployer.deploy(EnergyExchange, tokenInstance.address);
};
