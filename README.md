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

Ethereum Wallet CLI is a powerful command-line interface for managing Ethereum wallets. It provides a range of features for interacting with the Ethereum blockchain, including wallet creation, restoration, and management, as well as transaction handling and balance checking.

## Features

- **Wallet Management:** Create, restore, and import wallets
- **Balance Checking:** View wallet balances in ETH and USD
- **Transactions:** Send funds to other Ethereum addresses
- **Contract Interaction:** Add and interact with custom ERC20 tokens
- **Security:** Encrypted wallet storage with password protection
- **Private Key Management:** Export and decrypt private keys
- **Rich Console Output:** Enhanced CLI experience with colored and formatted output

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed
- Git installed (for cloning the repository)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/hambosto/EtherCLI.git
   cd EtherCLI
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Before using the Ethereum Wallet CLI, configure the provider settings in `wallet/provider.py`:

```python
DEFAULT_NODE_URL     = "https://rpc.ankr.com/eth" 
DEFAULT_SYMBOL       = "ETH"
DEFAULT_EXPLORER_URL = "https://etherscan.io"
DEFAULT_NODE_NAME    = "Ethereum Main Network"
DEFAULT_GAS_LIMIT    = 21000
DEFAULT_CURRENCY     = "USD"

CRYPTOCOMPARE_API_KEY = "YOUR_API_KEY_HERE"
```

Replace `YOUR_API_KEY_HERE` with your actual CryptoCompare API key.

## Usage

### Wallet Setup

To see available commands and options:

```
python eth.py --help
```

#### Create a New Wallet

```
python eth.py create --passphrase <your_passphrase> --password <your_password>
```

#### Restore a Wallet from Mnemonic

```
python eth.py restore --mnemonic word1 word2 ... --passphrase <your_passphrase> --password <your_password>
```

#### Import a Wallet from Private Key

```
python eth.py import --private-key 0xabcdef... --password <your_password>
```

### Wallet Actions

#### Check Balance

```
python eth.py balance
```

#### Send Funds

```
python eth.py send --symbol ETH --amount 1.0 --address 0x12345... --password <your_password>
```

#### Get Wallet Address

```
python eth.py receive
```

#### Add Custom Token Contract

```
python eth.py add-contract --token-address 0x6789...
```

#### Export Private Key

```
python eth.py export --password <your_password>
```

#### Decrypt Wallet

```
python eth.py decrypt --password <your_password>
```

#### Erase Wallet Configuration

```
python eth.py erase
```

## Security

- Always keep your passphrases, passwords, and private keys secure.
- Never share sensitive information.
- Use strong, unique passwords for each wallet.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Disclaimer

This tool is for educational and developmental purposes only. Use at your own risk. The authors are not responsible for any loss of funds or other damages that may occur through the use of this software.


## Star History

<a href="https://star-history.com/#hambosto/EtherCLI&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=hambosto/EtherCLI&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=hambosto/EtherCLI&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=hambosto/EtherCLI&type=Date" />
  </picture>
</a>

