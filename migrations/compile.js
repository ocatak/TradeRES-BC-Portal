const fs = require("fs"); //.promises;
const solc = require("solc");
const path = require('path');

function findImports(_path) {
    if (_path.startsWith('@openzeppelin')) {
        const openZeppelinPath = path.join(__dirname, '../node_modules', _path);
        return { contents: fs.readFileSync(openZeppelinPath, 'utf8') };
    } else {
        // Handle other paths, possibly with more conditions
        return { error: 'File not found' };
    }
}

async function main() {
  // Load the contract source code
  const sourceCode = await fs.promises.readFile("contracts/EnergyExchange.sol");
  // Compile the source code and retrieve the ABI and Bytecode
  const { abi, bytecode } = compile(sourceCode.toString(), "EnergyExchange");
  // Store the ABI and Bytecode into a JSON file
  const artifact = JSON.stringify({ abi, bytecode }, null, 2);
  await fs.promises.writeFile("build/EnergyExchange.json", artifact);

  // Load the contract source code
  const sourceCode2 = await fs.promises.readFile("contracts/EnergyToken.sol");
  // Compile the source code and retrieve the ABI and Bytecode
  const { abi: abi2, bytecode: bytecode2 } = compile(sourceCode2.toString(), "EnergyToken");
  // Store the ABI and Bytecode into a JSON file
  const artifact2 = JSON.stringify({ abi: abi2, bytecode: bytecode2 }, null, 2);
  await fs.promises.writeFile("build/EnergyToken.json", artifact2);
}

function compile(sourceCode, contractName) {
  // Create the Solidity Compiler Standard Input and Output JSON
  const input = {
    language: "Solidity",
    sources: { [contractName]: { content: sourceCode } },
    settings: { outputSelection: { "*": { "*": ["abi", "evm.bytecode"] } } },
  };
  // Parse the compiler output to retrieve the ABI and Bytecode
  const output = JSON.parse(solc.compile(JSON.stringify(input), { import: findImports }));
  // Check for and log errors
  if (output.errors) {
    output.errors.forEach(error => {
      console.error(error.formattedMessage);
    });
  }
  const artifact = output.contracts[contractName][contractName];
  return {
    abi: artifact.abi,
    bytecode: artifact.evm.bytecode.object,
  };
}

// node migrations/compile.js
main();
