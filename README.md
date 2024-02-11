```
███████╗████████╗██╗  ██╗███████╗██████╗  ██████╗██╗     ██╗
██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗██╔════╝██║     ██║
█████╗     ██║   ███████║█████╗  ██████╔╝██║     ██║     ██║
██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗██║     ██║     ██║
███████╗   ██║   ██║  ██║███████╗██║  ██║╚██████╗███████╗██║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝
      Coded by @hambosto - https://github.com/hambosto
EtherCLI - Ethereum Virtual Machine Wallet CLI   
A command-line tool for managing your Ethereum wallets, transactions, and more.
Take control of your digital assets with ease.
```

The Ethereum Wallet CLI is a command-line interface for managing Ethereum wallets. It allows users to perform various actions, including creating, restoring, and importing wallets, checking balances, sending transactions, and more.

## Features

- **Wallet Action:** Check balances, send funds, receive wallet addresses, add contracts, create wallets, restore wallets, import wallets, export private keys, decrypt wallets, and erase wallet configurations.

- **Logger Setup:** Configured with the `rich` library for colored and formatted output. Different log levels and traceback features for robust error handling.

- **Rich Console Output:** Enhanced console output using the `rich` library, including banners and formatted tables for displaying wallet balances.

- **And More:**

## Getting Started

### Prerequisites

First of all, clone this project:
```bash
git clone https://github.com/hambosto/EtherCLI.git && cd EtherCLI
```

Make sure you have Python installed. You can install the required packages using:

```bash
pip install -r requirements.txt
```

### Provider Configuration
Before using the Ethereum Wallet CLI, you need to set up the initial configuration in the `wallet/provider.py` file. This file contains essential parameters for interacting with the blockchain node. Open the provider.py file and adjust the following attributes according to your preferences:


```python
DEFAULT_NODE_URL     = "https://rpc.ankr.com/eth" 
DEFAULT_SYMBOL       = "ETH"
DEFAULT_EXPLORER_URL = "https://etherscan.io"
DEFAULT_NODE_NAME    = "Ethereum Main Network"
DEFAULT_GAS_LIMIT    = 21000
DEFAULT_CURRENCY     = "USD"

CRYPTOCOMPARE_API_KEY = "PUT YOUR API KEY HERE"
```


## Usage

### Wallet Setup

Before setting up the wallet, you can explore available commands and options using the following command:

- **Command Help:**
```bash
python script.py --help
```
This will display a list of available commands and their descriptions.
```plaintext
Usage: ether.py [-h] {create,restore,import} ...

Ethereum Virtual Machine Wallet CLI

Options:
  -h, --help            show this help message and exit

Subcommands:
  Wallet Setup Commands

  {create,restore,import}
                        Available Actions
    create              Create a new wallet
    restore             Restore your wallet from a mnemonic phrase
    import              Import a wallet from a private key
```


If the wallet configuration file doesn't exist, use the following commands to set up a wallet:

- **Create a New Wallet:**
```bash
python script.py create --passphrase <your_passphrase> --password <your_password>
```
This command creates a new Ethereum wallet. You'll be prompted to provide a passphrase and password for additional security.

- **Restore Wallet from Mnemonic:**
```bash
python script.py restore --mnemonic word1 word2 ... --passphrase <your_passphrase> --password <your_password>

```
If you have a mnemonic (recovery phrase) for an existing wallet, use this command to restore it. Replace word1, word2, etc., with your actual mnemonic words.

- **Import Wallet from Private Key:**
```bash
python script.py import --private-key 0xabcdef... --password <your_password>
```
Import an existing wallet using its private key. Replace 0xabcdef... with your actual private key.

Ensure you replace <your_passphrase> and <your_password> with your chosen passphrase and password, respectively.

## Wallet Actions
If the wallet configuration file exists, you can perform various wallet actions:

- Check Wallet Balance:
To check the balance of your Ethereum wallet, use the following command:
```bash
python script.py balance
```
- Send Funds:
To send funds from your wallet to another address, use the following command:
```bash
python script.py send --symbol ETH --amount 1.0 --address 0x12345 --password <your_password>

```
Replace <your_password> with your wallet password. This command sends 1.0 ETH to the specified address (0x12345). Adjust the amount and address accordingly.


- Receive Wallet Address:
To receive your Ethereum wallet address, use the following command:
```bash
python script.py receive
```
This command provides your wallet address for receiving funds.

- Add Contract:
If you want to add a custom contract to your wallet, use the following command:

```bash
python script.py add-contract --token-address 0x6789...
```
Replace 0x6789... with the actual token address you want to add.

- Create Wallet:
If you need to create a new Ethereum wallet, use the following command:
```bash
python script.py create --passphrase <your_passphrase> --password <your_password>
```
This command creates a new wallet, and you'll be prompted to provide a passphrase and password for security.

- Restore Wallet:
To restore a wallet using a mnemonic (recovery phrase), use the following command:
```bash
python script.py restore --mnemonic word1 word2 ... --passphrase <your_passphrase> --password <your_password>
```
Replace word1, word2, etc., with your actual mnemonic words.

- Import Wallet:
To import an existing wallet using its private key, use the following command:
```bash
python script.py import --private-key 0xabcdef... --password <your_password>
```
Replace 0xabcdef... with your actual private key.


- Export Wallet Private Key:
To export the private key of your wallet, use the following command:
```bash
python script.py export --password <your_password>
```
Replace <your_password> with your wallet password.

- Decrypt Wallet:
To decrypt your wallet and view its details, use the following command:
```bash
python script.py decrypt --password <your_password>
```
Replace <your_password> with your wallet password.

- Erase Wallet 
To erase the wallet configuration and start fresh, use the following command:Configuration:
```bash
python script.py erase
```
This command resets the wallet configuration and prompts you to set it up again.

## Additional Notes

- The script utilizes a configuration file, and sensitive information like private keys should be safeguarded with passwords.

- A CryptoCompare API key is used to fetch currency prices.

**Disclaimer:** Handle private keys, passphrases, and passwords securely. Avoid sharing sensitive information.

**Contributions:** Contributions, issues, and suggestions are welcome. Feel free to open an issue or submit a pull request for improvements or bug fixes.

